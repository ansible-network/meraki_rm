#!/usr/bin/env python3
"""Sync field descriptions from module DOCUMENTATION into User Model dataclasses.

Reads each module's DOCUMENTATION YAML string, extracts per-field descriptions
from options.config.suboptions, and rewrites the corresponding User Model file
to use dataclasses.field(metadata={"description": "..."}).

Idempotent: safe to re-run after editing DOCUMENTATION strings.

Usage:
    python tools/generate_model_descriptions.py
"""

import ast
import re
import textwrap
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MODULES_DIR = ROOT / "plugins" / "modules"
ACTION_DIR = ROOT / "plugins" / "action"
USER_MODELS_DIR = ROOT / "plugins" / "plugin_utils" / "user_models"

SKIP_MODULES = {"meraki_facts"}


def extract_documentation(module_path: Path) -> dict:
    """Extract DOCUMENTATION YAML from a module file."""
    source = module_path.read_text()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "DOCUMENTATION":
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        return yaml.safe_load(node.value.value)
    return {}


def get_field_descriptions(doc: dict) -> dict[str, str]:
    """Extract field_name -> description from DOCUMENTATION suboptions."""
    config_opt = doc.get("options", {}).get("config", {})
    suboptions = config_opt.get("suboptions", {})
    descriptions = {}
    for field_name, spec in suboptions.items():
        desc = spec.get("description", "")
        if isinstance(desc, list):
            desc = " ".join(d.strip() for d in desc)
        desc = desc.strip()
        if desc:
            descriptions[field_name] = desc
    return descriptions


def get_user_model_path(action_path: Path) -> Path | None:
    """Read USER_MODEL from an action plugin to find the user model file."""
    source = action_path.read_text()
    match = re.search(r"USER_MODEL\s*=\s*['\"]([^'\"]+)['\"]", source)
    if not match:
        return None
    dotted = match.group(1)
    parts = dotted.split(".")
    file_part = parts[-2]
    return USER_MODELS_DIR / f"{file_part}.py"


def rewrite_model_file(model_path: Path, descriptions: dict[str, str]) -> bool:
    """Rewrite a User Model file to add field descriptions as metadata.

    Transforms:
        field_name: Optional[str] = None
    Into:
        field_name: Optional[str] = field(default=None, metadata={"description": "..."})
    """
    content = model_path.read_text()
    original = content

    if not descriptions:
        return False

    needs_field_import = False

    for field_name, desc in descriptions.items():
        desc_escaped = desc.replace("\\", "\\\\").replace('"', '\\"')

        old_pattern = re.compile(
            rf"^(\s+){re.escape(field_name)}:\s*(Optional\[.*?\])\s*=\s*None\s*$",
            re.MULTILINE,
        )

        already_has = re.compile(
            rf"^(\s+){re.escape(field_name)}:\s*(Optional\[.*?\])\s*=\s*field\(",
            re.MULTILINE,
        )

        if already_has.search(content):
            old_meta_pattern = re.compile(
                rf'^(\s+){re.escape(field_name)}:\s*(Optional\[.*?\])\s*=\s*field\(default=None,\s*metadata=\{{"description":\s*"[^"]*"\}}\)\s*$',
                re.MULTILINE,
            )
            match = old_meta_pattern.search(content)
            if match:
                indent = match.group(1)
                type_hint = match.group(2)
                new_line = f'{indent}{field_name}: {type_hint} = field(default=None, metadata={{"description": "{desc_escaped}"}})'
                content = content[: match.start()] + new_line + content[match.end() :]
                needs_field_import = True
            continue

        match = old_pattern.search(content)
        if match:
            indent = match.group(1)
            type_hint = match.group(2)
            new_line = f'{indent}{field_name}: {type_hint} = field(default=None, metadata={{"description": "{desc_escaped}"}})'
            content = content[: match.start()] + new_line + content[match.end() :]
            needs_field_import = True

    if needs_field_import and "from dataclasses import dataclass, field" not in content:
        content = content.replace(
            "from dataclasses import dataclass",
            "from dataclasses import dataclass, field",
        )

    if content != original:
        model_path.write_text(content)
        return True
    return False


def build_module_to_action_map() -> dict[str, Path]:
    """Map module name (e.g., 'meraki_appliance_vlans') -> action plugin path."""
    result = {}
    for action_path in sorted(ACTION_DIR.glob("meraki_*.py")):
        module_name = action_path.stem
        result[module_name] = action_path
    return result


def main():
    action_map = build_module_to_action_map()
    modified = 0
    skipped = 0
    errors = 0

    for module_path in sorted(MODULES_DIR.glob("meraki_*.py")):
        module_name = module_path.stem
        if module_name in SKIP_MODULES:
            continue

        action_path = action_map.get(module_name)
        if not action_path:
            print(f"  SKIP {module_name}: no action plugin")
            skipped += 1
            continue

        model_path = get_user_model_path(action_path)
        if not model_path or not model_path.exists():
            print(f"  SKIP {module_name}: no user model file")
            skipped += 1
            continue

        doc = extract_documentation(module_path)
        descriptions = get_field_descriptions(doc)
        if not descriptions:
            print(f"  SKIP {module_name}: no suboption descriptions")
            skipped += 1
            continue

        try:
            if rewrite_model_file(model_path, descriptions):
                count = len(descriptions)
                print(f"  OK   {model_path.name}: {count} descriptions synced")
                modified += 1
            else:
                print(f"  NOOP {model_path.name}: already up to date")
                skipped += 1
        except Exception as e:
            print(f"  ERR  {model_path.name}: {e}")
            errors += 1

    print(f"\nDone: {modified} modified, {skipped} skipped, {errors} errors")


if __name__ == "__main__":
    main()
