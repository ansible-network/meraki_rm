#!/usr/bin/env python3
"""Generate check-mode Molecule scenarios for all resource modules.

Creates a ``check/`` scenario directory alongside existing ``merged/``,
``gathered/``, etc. under ``extensions/molecule/{module}/check/``.

Each check scenario validates two contracts:
  1. Check mode returns a correct prediction (changed, before/after, diff).
  2. Check mode makes NO actual changes to the device/mock state.

Collection resources start from an empty state; singleton resources seed a
baseline via ``gathered/vars.yml`` before running check mode with the
``merged/vars.yml`` config.

Usage:
    python tools/generate_check_scenarios.py [--dry-run] [--module NAME ...]
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MOLECULE_DIR = ROOT / "extensions" / "molecule"
ACTION_DIR = ROOT / "plugins" / "action"

SKIP_MODULES = {"default", "facts", "wireless_air_marshal_rules"}

_SCOPE_PREFIXES = {
    "network_id": "N",
    "organization_id": "org",
    "serial": "Q2XX",
}


def make_scope_id(scope_param: str, module_name: str, state: str = "check") -> str:
    """Generate a deterministic, collision-free scope value for a scenario."""
    prefix = _SCOPE_PREFIXES.get(scope_param, "N")
    sep = "-" if scope_param == "serial" else "_"
    return f"{prefix}{sep}{module_name}{sep}{state}"


def yaml_dump(data: object) -> str:
    return yaml.dump(data, default_flow_style=False, sort_keys=False, width=120)


def parse_action_plugin(module_name: str) -> dict:
    """Extract CANONICAL_KEY, SYSTEM_KEY, SCOPE_PARAM, SUPPORTS_DELETE from an
    action plugin using AST parsing (no imports required)."""
    fqcn_suffix = f"meraki_{module_name}"
    action_file = ACTION_DIR / f"{fqcn_suffix}.py"
    if not action_file.exists():
        return {}

    source = action_file.read_text()
    tree = ast.parse(source, filename=str(action_file))

    attrs: dict[str, object] = {
        "CANONICAL_KEY": None,
        "SYSTEM_KEY": None,
        "SCOPE_PARAM": "network_id",
        "SUPPORTS_DELETE": True,
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "ActionModule":
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name) and target.id in attrs:
                            val = item.value
                            if isinstance(val, ast.Constant):
                                attrs[target.id] = val.value
                            elif isinstance(val, ast.NameConstant):
                                attrs[target.id] = val.value
            break

    return attrs


def _molecule_yml() -> str:
    return (
        "---\n"
        "scenario:\n"
        "  test_sequence:\n"
        "    - prepare\n"
        "    - converge\n"
        "    - verify\n"
        "    - cleanup\n"
    )


def _converge_yml(module_name: str, scope_param: str, scope_value: str) -> str:
    fqcn = f"cisco.meraki_rm.meraki_{module_name}"
    play = [
        {
            "name": f"Converge \u2014 {module_name} (check)",
            "hosts": "localhost",
            "gather_facts": False,
            "vars_files": ["vars.yml"],
            "tasks": [
                {
                    "name": "Run module in check mode (predict change, do not apply)",
                    fqcn: {
                        scope_param: scope_value,
                        "state": "merged",
                        "config": ["{{ expected_config }}"],
                    },
                    "check_mode": True,
                    "diff": True,
                    "register": "check_result",
                },
                {
                    "name": "Assert check mode predicted a change",
                    "ansible.builtin.assert": {
                        "that": [
                            "check_result.changed == true",
                            "check_result.before is defined",
                            "check_result.after is defined",
                        ],
                        "fail_msg": "Check mode did not predict a change",
                    },
                },
                {
                    "name": "Assert diff output is present",
                    "ansible.builtin.assert": {
                        "that": [
                            "check_result.diff is defined",
                            "check_result.diff.before is defined",
                            "check_result.diff.after is defined",
                        ],
                        "fail_msg": "Diff mode output missing from check result",
                    },
                },
            ],
        }
    ]
    return "---\n" + yaml_dump(play)


def _verify_collection_yml(module_name: str, scope_param: str, scope_value: str) -> str:
    """Verify for collection resources: assert no resources were created."""
    fqcn = f"cisco.meraki_rm.meraki_{module_name}"
    play = [
        {
            "name": f"Verify \u2014 {module_name} (check)",
            "hosts": "localhost",
            "gather_facts": False,
            "tasks": [
                {
                    "name": "Gather actual state (should be unchanged)",
                    fqcn: {
                        scope_param: scope_value,
                        "state": "gathered",
                    },
                    "register": "actual",
                },
                {
                    "name": "Assert no resources were created (check mode is dry-run)",
                    "ansible.builtin.assert": {
                        "that": [
                            "actual.gathered | default([]) | length == 0",
                        ],
                        "fail_msg": "Check mode leaked changes \u2014 resources found after check-only run",
                    },
                },
            ],
        }
    ]
    return "---\n" + yaml_dump(play)


def _verify_singleton_yml(
    module_name: str, scope_param: str, scope_value: str,
) -> str:
    """Verify for singleton resources: assert state matches the prepare baseline."""
    fqcn = f"cisco.meraki_rm.meraki_{module_name}"
    play = [
        {
            "name": f"Verify \u2014 {module_name} (check)",
            "hosts": "localhost",
            "gather_facts": False,
            "vars_files": ["vars.yml"],
            "tasks": [
                {
                    "name": "Gather actual state (should match prepare baseline)",
                    fqcn: {
                        scope_param: scope_value,
                        "state": "gathered",
                    },
                    "register": "actual",
                },
                {
                    "name": "Assert gathered state is not empty",
                    "ansible.builtin.assert": {
                        "that": [
                            "actual.gathered is defined",
                            "actual.gathered | length > 0",
                        ],
                        "fail_msg": "Gathered config is empty after check mode",
                    },
                },
                {
                    "name": "Compare prepare baseline to gathered state (subset check)",
                    "ansible.builtin.set_fact": {
                        "path_check": "{{ expected_paths | cisco.meraki_rm.path_contained_in(result_paths) }}",
                    },
                    "vars": {
                        "expected_paths": "{{ prepare_config | ansible.utils.to_paths }}",
                        "result_paths": "{{ actual.gathered[0] | ansible.utils.to_paths }}",
                    },
                },
                {
                    "name": "Assert check mode did not alter the baseline",
                    "ansible.builtin.assert": {
                        "that": "path_check.contained | bool",
                        "success_msg": "Baseline intact. Extras: {{ path_check.extras }}",
                        "fail_msg": "Baseline changed! Missing: {{ path_check.missing }}. Extras: {{ path_check.extras }}",
                    },
                },
            ],
        }
    ]
    return "---\n" + yaml_dump(play)


def _prepare_singleton_yml(
    module_name: str, scope_param: str, scope_value: str,
) -> str:
    """Prepare for singleton: seed baseline from gathered/vars.yml config."""
    fqcn = f"cisco.meraki_rm.meraki_{module_name}"
    play = [
        {
            "name": f"Prepare \u2014 {module_name} (check)",
            "hosts": "localhost",
            "gather_facts": False,
            "vars_files": ["vars.yml"],
            "tasks": [
                {
                    "name": "Seed singleton baseline via merged",
                    fqcn: {
                        scope_param: scope_value,
                        "state": "merged",
                        "config": ["{{ prepare_config }}"],
                    },
                },
            ],
        }
    ]
    return "---\n" + yaml_dump(play)


def _prepare_collection_noop_yml(module_name: str) -> str:
    """Prepare for collection: no-op (start from empty state)."""
    play = [
        {
            "name": f"Prepare \u2014 {module_name} (check)",
            "hosts": "localhost",
            "gather_facts": False,
            "tasks": [
                {
                    "name": "No-op \u2014 collection starts from empty state",
                    "ansible.builtin.debug": {
                        "msg": "Empty baseline for check mode test",
                    },
                },
            ],
        }
    ]
    return "---\n" + yaml_dump(play)


def _cleanup_collection_yml(module_name: str, scope_param: str, scope_value: str) -> str:
    """Cleanup for collection: gather + delete any leaked resources."""
    fqcn = f"cisco.meraki_rm.meraki_{module_name}"
    play = [
        {
            "name": f"Cleanup \u2014 {module_name} (check)",
            "hosts": "localhost",
            "gather_facts": False,
            "tasks": [
                {
                    "name": f"Gather remaining {module_name} resources",
                    fqcn: {
                        scope_param: scope_value,
                        "state": "gathered",
                    },
                    "register": "current",
                },
                {
                    "name": "Remove all test resources",
                    fqcn: {
                        scope_param: scope_value,
                        "state": "deleted",
                        "config": "{{ current.gathered }}",
                    },
                    "when": "current.gathered | default([]) | length > 0",
                    "ignore_errors": True,
                },
            ],
        }
    ]
    return "---\n" + yaml_dump(play)


def _cleanup_singleton_yml(module_name: str) -> str:
    """Cleanup for singleton: no-op."""
    play = [
        {
            "name": f"Cleanup \u2014 {module_name} (check)",
            "hosts": "localhost",
            "gather_facts": False,
            "tasks": [
                {
                    "name": "No cleanup needed for singleton resource",
                    "ansible.builtin.debug": {
                        "msg": f"{module_name} does not support delete",
                    },
                },
            ],
        }
    ]
    return "---\n" + yaml_dump(play)


def _build_vars(
    merged_vars: dict,
    gathered_vars: dict | None,
    is_singleton: bool,
) -> dict:
    """Build the vars.yml content for the check scenario.

    For collections:  expected_config = merged config (the desired change).
    For singletons:   prepare_config  = gathered config (baseline to seed),
                      expected_config = merged config (the desired change).
    """
    result = {"expected_config": merged_vars["expected_config"]}

    if is_singleton and gathered_vars:
        result["prepare_config"] = gathered_vars["expected_config"]

    pk = merged_vars.get("server_assigned_pk")
    if pk:
        result["server_assigned_pk"] = pk

    return result


def generate_check_scenario(module_name: str, dry_run: bool = False) -> list[str]:
    """Generate the check/ scenario directory for one module."""
    module_dir = MOLECULE_DIR / module_name
    merged_dir = module_dir / "merged"

    if not merged_dir.exists():
        return [f"SKIP {module_name}: no merged/ scenario"]

    merged_vars_file = merged_dir / "vars.yml"
    if not merged_vars_file.exists():
        return [f"SKIP {module_name}: no merged/vars.yml"]

    merged_vars = yaml.safe_load(merged_vars_file.read_text())
    if not merged_vars or "expected_config" not in merged_vars:
        return [f"SKIP {module_name}: no expected_config in merged/vars.yml"]

    attrs = parse_action_plugin(module_name)
    if not attrs:
        return [f"SKIP {module_name}: could not parse action plugin"]

    is_singleton = attrs["CANONICAL_KEY"] is None and attrs["SYSTEM_KEY"] is None
    scope_param = attrs["SCOPE_PARAM"]
    scope_value = make_scope_id(scope_param, module_name, "check")

    gathered_vars = None
    if is_singleton:
        gathered_vars_file = module_dir / "gathered" / "vars.yml"
        if gathered_vars_file.exists():
            gathered_vars = yaml.safe_load(gathered_vars_file.read_text())

    check_dir = module_dir / "check"
    actions = [f"CREATE {check_dir}"]

    if dry_run:
        return actions

    check_dir.mkdir(parents=True, exist_ok=True)

    (check_dir / "molecule.yml").write_text(_molecule_yml())

    vars_data = _build_vars(merged_vars, gathered_vars, is_singleton)
    (check_dir / "vars.yml").write_text("---\n" + yaml_dump(vars_data))

    (check_dir / "converge.yml").write_text(
        _converge_yml(module_name, scope_param, scope_value)
    )

    if is_singleton:
        (check_dir / "prepare.yml").write_text(
            _prepare_singleton_yml(module_name, scope_param, scope_value)
        )
        (check_dir / "verify.yml").write_text(
            _verify_singleton_yml(module_name, scope_param, scope_value)
        )
        (check_dir / "cleanup.yml").write_text(
            _cleanup_singleton_yml(module_name)
        )
    else:
        (check_dir / "prepare.yml").write_text(
            _prepare_collection_noop_yml(module_name)
        )
        (check_dir / "verify.yml").write_text(
            _verify_collection_yml(module_name, scope_param, scope_value)
        )
        (check_dir / "cleanup.yml").write_text(
            _cleanup_collection_yml(module_name, scope_param, scope_value)
        )

    return actions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done without making changes")
    parser.add_argument("--module", action="append", dest="modules",
                        metavar="NAME",
                        help="Generate for specific module(s) only (repeatable)")
    args = parser.parse_args()

    if args.modules:
        module_names = args.modules
    else:
        module_names = sorted(
            d.name for d in MOLECULE_DIR.iterdir()
            if d.is_dir() and d.name not in SKIP_MODULES
            and (d / "merged").is_dir()
        )

    prefix = "DRY RUN \u2014 " if args.dry_run else ""
    print(f"{prefix}Generating check-mode Molecule scenarios...\n")
    print(f"Modules to process: {len(module_names)}\n")

    created = 0
    skipped = 0
    for name in module_names:
        actions = generate_check_scenario(name, dry_run=args.dry_run)
        for a in actions:
            print(f"  {a}")
            if a.startswith("CREATE"):
                created += 1
            elif a.startswith("SKIP"):
                skipped += 1

    verb = "Would create" if args.dry_run else "Created"
    print(f"\n{verb} {created} check scenarios, skipped {skipped}.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
