#!/usr/bin/env python3
"""Restructure flat Molecule scenarios into nested module/state/ directories.

Reads examples/{module}/{state}.yml files, splits each into:
  - vars.yml     (expected_config data — shared between converge and verify)
  - converge.yml (vars_files + module call — documentation source)
  - verify.yml   (vars_files + gather + path_contained_in assertions)
  - prepare.yml  (seed data for replaced/overridden/deleted/gathered)
  - cleanup.yml  (remove test data)
  - molecule.yml (minimal, inherits config.yml)

Usage:
    python tools/restructure_molecule.py [--dry-run]
"""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = ROOT / "examples"
MOLECULE_DIR = ROOT / "extensions" / "molecule"

STATES_NEEDING_PREPARE = {"replaced", "overridden", "deleted"}
STATES_NEEDING_CLEANUP = {"merged", "replaced", "overridden"}
STATES_WITH_PATH_CHECK = {"merged", "replaced", "overridden"}


def parse_example(filepath: Path) -> dict:
    """Parse an example YAML task file, extracting module info and expected config."""
    with open(filepath) as f:
        raw = f.read()

    tasks = yaml.safe_load(raw)
    if not isinstance(tasks, list):
        return {}

    module_fqcn = None
    scope_param = None
    scope_value = None
    register_var = None
    expected_config = None
    module_call_tasks = []

    for task in tasks:
        if not isinstance(task, dict):
            continue

        is_module_call = False
        for key in task:
            if key.startswith("cisco.meraki_rm.meraki_"):
                is_module_call = True
                module_fqcn = key
                params = task[key] if isinstance(task[key], dict) else {}
                for p in ("network_id", "serial", "organization_id"):
                    if p in params:
                        scope_param = p
                        scope_value = params[p]
                        break
                register_var = task.get("register")
                break

        if is_module_call:
            module_call_tasks.append(task)
        elif "ansible.builtin.set_fact" in task:
            sf = task.get("ansible.builtin.set_fact")
            if isinstance(sf, dict) and "expected_config" in sf:
                expected_config = sf["expected_config"]

    return {
        "module_fqcn": module_fqcn,
        "scope_param": scope_param,
        "scope_value": scope_value,
        "register_var": register_var,
        "expected_config": expected_config,
        "module_call_tasks": module_call_tasks,
        "raw": raw,
    }


def get_merged_config(module_dir: Path) -> dict | None:
    """Extract the expected_config from a module's merged.yml for use in prepare."""
    merged_file = module_dir / "merged.yml"
    if not merged_file.exists():
        return None
    info = parse_example(merged_file)
    return info.get("expected_config")


def yaml_dump(data) -> str:
    return yaml.dump(data, default_flow_style=False, sort_keys=False, width=120)


def write_molecule_yml(scenario_dir: Path) -> None:
    content = "---\n# Inherits shared config from ../../config.yml\n"
    (scenario_dir / "molecule.yml").write_text(content)


def write_vars_yml(scenario_dir: Path, expected_config) -> None:
    """Write vars.yml with expected_config data."""
    content = "---\n" + yaml_dump({"expected_config": expected_config})
    (scenario_dir / "vars.yml").write_text(content)


def write_converge(scenario_dir: Path, module_name: str, state: str,
                   module_call_tasks: list, has_vars: bool) -> None:
    """Write converge.yml with vars_files (if vars.yml exists) and module call tasks."""
    play = {
        "name": f"Converge — {module_name} ({state})",
        "hosts": "localhost",
        "gather_facts": False,
    }
    if has_vars:
        play["vars_files"] = ["vars.yml"]
    play["tasks"] = module_call_tasks

    content = "---\n" + yaml_dump([play])
    (scenario_dir / "converge.yml").write_text(content)


def write_verify(scenario_dir: Path, module_name: str, state: str,
                 module_fqcn: str, scope_param: str, scope_value: str,
                 has_vars: bool, extra_assertions: list | None = None) -> None:
    """Write verify.yml with gather + path_contained_in assertions."""
    gather_task = {
        "name": "Gather current configuration",
        module_fqcn: {
            scope_param: scope_value,
            "state": "gathered",
        },
        "register": "gathered",
    }

    tasks = [gather_task]

    if state == "deleted":
        tasks.append({
            "name": "Assert no resources remain after delete",
            "ansible.builtin.assert": {
                "that": [
                    "gathered.gathered is defined",
                    "gathered.gathered | length == 0",
                ],
                "fail_msg": "Expected empty config after delete, got {{ gathered.gathered }}",
            },
        })
    elif state in STATES_WITH_PATH_CHECK and has_vars:
        tasks.append({
            "name": f"Assert configuration exists after {state}",
            "ansible.builtin.assert": {
                "that": [
                    "gathered.gathered is defined",
                    "gathered.gathered | length > 0",
                ],
                "fail_msg": f"Expected at least one resource after {state}",
            },
        })
        tasks.append({
            "name": "Compare expected paths to gathered state (subset check)",
            "ansible.builtin.set_fact": {
                "path_check": "{{ expected_paths | cisco.meraki_rm.path_contained_in(result_paths) }}",
            },
            "vars": {
                "expected_paths": "{{ expected_config | ansible.utils.to_paths }}",
                "result_paths": "{{ gathered.gathered[0] | ansible.utils.to_paths }}",
            },
        })
        tasks.append({
            "name": "Assert all expected fields are present and match",
            "ansible.builtin.assert": {
                "that": "path_check.contained | bool",
                "success_msg": "{{ success_msg }}",
                "fail_msg": "{{ fail_msg }}",
            },
            "vars": {
                "success_msg": "All expected fields match. Extras: {{ path_check.extras }}",
                "fail_msg": "Missing or mismatch: {{ path_check.missing }}. Extras: {{ path_check.extras }}",
            },
        })
    else:
        tasks.append({
            "name": f"Assert gathered configuration is not empty",
            "ansible.builtin.assert": {
                "that": [
                    "gathered.gathered is defined",
                    "gathered.gathered | length > 0",
                ],
                "fail_msg": "Gathered config is empty — expected at least one resource",
            },
        })

    if extra_assertions:
        tasks.extend(extra_assertions)

    play = {
        "name": f"Verify — {module_name} ({state})",
        "hosts": "localhost",
        "gather_facts": False,
    }
    if has_vars and state in STATES_WITH_PATH_CHECK:
        play["vars_files"] = ["vars.yml"]
    play["tasks"] = tasks

    content = "---\n" + yaml_dump([play])
    (scenario_dir / "verify.yml").write_text(content)


def write_prepare(scenario_dir: Path, module_name: str, state: str,
                  module_fqcn: str, scope_param: str, scope_value: str,
                  seed_config: dict | list) -> None:
    """Write prepare.yml that seeds prerequisite data via merged."""
    if isinstance(seed_config, dict):
        config_list = [seed_config]
    else:
        config_list = seed_config

    module_task = {
        "name": f"Seed resource via merged (prerequisite for {state})",
        module_fqcn: {
            scope_param: scope_value,
            "state": "merged",
            "config": config_list,
        },
    }

    play = {
        "name": f"Prepare — {module_name} ({state})",
        "hosts": "localhost",
        "gather_facts": False,
        "tasks": [module_task],
    }
    content = "---\n" + yaml_dump([play])
    (scenario_dir / "prepare.yml").write_text(content)


def write_cleanup(scenario_dir: Path, module_name: str, state: str,
                  module_fqcn: str | None = None, scope_param: str | None = None,
                  scope_value: str | None = None,
                  delete_config: dict | list | None = None) -> None:
    """Write cleanup.yml — deletes resources or no-op for deleted state."""
    if state == "deleted":
        play = {
            "name": f"Cleanup — {module_name} ({state})",
            "hosts": "localhost",
            "gather_facts": False,
            "tasks": [{
                "name": "No-op — resource already deleted by converge",
                "ansible.builtin.debug": {"msg": "Nothing to clean up"},
            }],
        }
    elif module_fqcn and scope_param and delete_config is not None:
        if isinstance(delete_config, dict):
            config_list = [delete_config]
        else:
            config_list = delete_config
        play = {
            "name": f"Cleanup — {module_name} ({state})",
            "hosts": "localhost",
            "gather_facts": False,
            "tasks": [{
                "name": "Remove test resources",
                module_fqcn: {
                    scope_param: scope_value,
                    "state": "deleted",
                    "config": config_list,
                },
                "ignore_errors": True,
            }],
        }
    else:
        play = {
            "name": f"Cleanup — {module_name} ({state})",
            "hosts": "localhost",
            "gather_facts": False,
            "tasks": [{
                "name": "No cleanup configured for singleton resource",
                "ansible.builtin.debug": {"msg": f"{module_name} does not support delete"},
            }],
        }

    content = "---\n" + yaml_dump([play])
    (scenario_dir / "cleanup.yml").write_text(content)


def get_delete_config(module_example_dir: Path) -> dict | None:
    """Extract the config from a module's deleted.yml for cleanup purposes."""
    deleted_file = module_example_dir / "deleted.yml"
    if not deleted_file.exists():
        return None
    info = parse_example(deleted_file)
    return info.get("expected_config")


def process_module(module_name: str, dry_run: bool = False) -> list[str]:
    """Process a single module — generate nested scenarios for all available states."""
    module_example_dir = EXAMPLES_DIR / module_name
    if not module_example_dir.is_dir():
        return [f"SKIP {module_name}: no examples directory"]

    state_files = sorted(module_example_dir.glob("*.yml"))
    states = [f.stem for f in state_files]
    if not states:
        return [f"SKIP {module_name}: no state files found"]

    merged_info = parse_example(module_example_dir / "merged.yml") if (module_example_dir / "merged.yml").exists() else {}
    module_fqcn = merged_info.get("module_fqcn")
    scope_param = merged_info.get("scope_param")
    scope_value = merged_info.get("scope_value")

    if not module_fqcn:
        gathered_info = parse_example(module_example_dir / "gathered.yml") if (module_example_dir / "gathered.yml").exists() else {}
        module_fqcn = gathered_info.get("module_fqcn")
        scope_param = gathered_info.get("scope_param")
        scope_value = gathered_info.get("scope_value")

    if not module_fqcn:
        return [f"SKIP {module_name}: could not determine module FQCN"]

    merged_config = get_merged_config(module_example_dir)
    delete_config = get_delete_config(module_example_dir)
    has_delete = "deleted" in states

    actions = []
    for state in states:
        state_file = module_example_dir / f"{state}.yml"
        info = parse_example(state_file)
        if not info:
            actions.append(f"SKIP {module_name}/{state}: could not parse")
            continue

        scenario_dir = MOLECULE_DIR / module_name / state
        actions.append(f"CREATE {scenario_dir}")

        if dry_run:
            continue

        scenario_dir.mkdir(parents=True, exist_ok=True)

        write_molecule_yml(scenario_dir)

        expected_config = info.get("expected_config")
        has_vars = expected_config is not None

        if has_vars:
            write_vars_yml(scenario_dir, expected_config)

        module_call_tasks = info.get("module_call_tasks", [])
        write_converge(scenario_dir, module_name, state, module_call_tasks, has_vars)

        if state in STATES_NEEDING_PREPARE and merged_config:
            if state == "overridden" and merged_config:
                extra_seed = dict(merged_config)
                pk = next((k for k in extra_seed if k.endswith("_id") or k == "id"), None)
                if pk and isinstance(extra_seed.get(pk), str):
                    extra_seed[pk] = "999"
                    extra_seed["name"] = "Extra-To-Delete"
                    seed_config = [merged_config, extra_seed]
                else:
                    seed_config = merged_config
            else:
                seed_config = merged_config
            write_prepare(scenario_dir, module_name, state, module_fqcn,
                          scope_param, scope_value, seed_config)

        if state == "gathered" and merged_config:
            write_prepare(scenario_dir, module_name, state, module_fqcn,
                          scope_param, scope_value, merged_config)

        extra_assert = None
        if state == "overridden":
            extra_assert = [{
                "name": "Assert only desired resources remain",
                "ansible.builtin.assert": {
                    "that": ["gathered.gathered | length == 1"],
                    "fail_msg": "Overridden should leave exactly one resource, got {{ gathered.gathered | length }}",
                },
            }]

        write_verify(
            scenario_dir, module_name, state,
            module_fqcn, scope_param, scope_value,
            has_vars=has_vars,
            extra_assertions=extra_assert,
        )

        if state in STATES_NEEDING_CLEANUP:
            if has_delete and delete_config:
                write_cleanup(scenario_dir, module_name, state,
                              module_fqcn, scope_param, scope_value, delete_config)
            elif has_delete and merged_config:
                write_cleanup(scenario_dir, module_name, state,
                              module_fqcn, scope_param, scope_value, merged_config)
            else:
                write_cleanup(scenario_dir, module_name, state)
        elif state == "deleted":
            write_cleanup(scenario_dir, module_name, state)
        elif state == "gathered":
            if has_delete and delete_config:
                write_cleanup(scenario_dir, module_name, state,
                              module_fqcn, scope_param, scope_value, delete_config)
            else:
                write_cleanup(scenario_dir, module_name, state)

    return actions


def remove_old_flat_scenarios(dry_run: bool = False) -> list[str]:
    """Remove old flat molecule scenarios (keep default/ and config files)."""
    keep = {"default", "config.yml", "inventory.yml", "__pycache__"}
    actions = []

    for item in sorted(MOLECULE_DIR.iterdir()):
        if item.name in keep or not item.is_dir():
            continue
        has_molecule_yml = (item / "molecule.yml").exists()
        has_nested_states = any(
            (item / s).is_dir() for s in ("merged", "replaced", "deleted", "gathered", "overridden")
        )
        if has_nested_states:
            continue
        if has_molecule_yml:
            actions.append(f"DELETE {item}")
            if not dry_run:
                shutil.rmtree(item)

    return actions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done without making changes")
    args = parser.parse_args()

    print(f"{'DRY RUN — ' if args.dry_run else ''}Restructuring Molecule scenarios...\n")

    module_dirs = sorted(d.name for d in EXAMPLES_DIR.iterdir() if d.is_dir())
    print(f"Found {len(module_dirs)} modules with examples\n")

    total_scenarios = 0
    for module_name in module_dirs:
        actions = process_module(module_name, dry_run=args.dry_run)
        for a in actions:
            if a.startswith("CREATE"):
                total_scenarios += 1
            print(f"  {a}")

    print(f"\n{'Would create' if args.dry_run else 'Created'} {total_scenarios} nested scenarios\n")

    print("Removing old flat scenarios...")
    remove_actions = remove_old_flat_scenarios(dry_run=args.dry_run)
    for a in remove_actions:
        print(f"  {a}")

    if not remove_actions:
        print("  (no flat scenarios to remove — may need manual cleanup)")

    print("\nDone.")


if __name__ == "__main__":
    main()
