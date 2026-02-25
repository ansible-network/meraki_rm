#!/usr/bin/env python3
"""Generate CLI reference documentation from User Model introspection.

Produces ``docs/13-cli.md`` by introspecting all User Model dataclasses
and the CLI configuration.  The output includes a command catalogue with
argument schemas, metadata, and usage examples.

Idempotent: safe to re-run whenever User Models or CLI code change.

Usage::

    python tools/generate_cli_docs.py
"""

from __future__ import annotations

import dataclasses
import sys
import typing
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from plugins.plugin_utils.mcp.introspect import build_tool_definitions
from plugins.plugin_utils.mcp.schema import _unwrap_optional


def _type_label(tp: type) -> str:
    """Return a human-readable type label for a field type.

    Args:
        tp: The Python type hint.

    Returns:
        Human-readable string like ``string``, ``integer``, ``JSON``, etc.
    """
    inner, _ = _unwrap_optional(tp)
    origin = getattr(inner, "__origin__", None)

    if inner is str:
        return "string"
    if inner is int:
        return "integer"
    if inner is float:
        return "number"
    if inner is bool:
        return "boolean"
    if origin in (list, typing.List):
        args = getattr(inner, "__args__", ())
        if args and args[0] is str:
            return "string[]"
        return "JSON"
    if origin in (dict, typing.Dict) or inner is dict:
        return "JSON"
    return "string"


def _flag_name(field_name: str) -> str:
    """Convert a snake_case field name to --kebab-case.

    Args:
        field_name: Python field name.

    Returns:
        CLI flag string.
    """
    return f"--{field_name.replace('_', '-')}"


def _command_section(td: Dict[str, Any]) -> str:
    """Render a single CLI command as a Markdown section.

    Args:
        td: Tool definition dict from ``build_tool_definitions()``.

    Returns:
        Markdown string for this command.
    """
    meta = td["_metadata"]
    module_name: str = meta["module_name"]
    cmd_name = module_name.replace("_", "-")
    scope_param: str = meta["scope_param"]
    valid_states: list[str] = meta["valid_states"]
    user_cls = meta["user_model_class"]
    hints = typing.get_type_hints(user_cls)

    parts: list[str] = [f"### `meraki-cli {cmd_name}`", ""]
    parts.append(td["description"])
    parts.append("")

    parts.append("**Usage**")
    parts.append("")
    parts.append("```bash")
    scope_flag = _flag_name(scope_param)
    parts.append(
        f"meraki-cli {cmd_name} <state> {scope_flag} <value> [options]"
    )
    parts.append("```")
    parts.append("")

    parts.append(f"**States**: {', '.join(f'`{s}`' for s in valid_states)}")
    parts.append("")

    ck = meta["canonical_key"]
    sk = meta["system_key"]
    if ck:
        parts.append(f"**Canonical key**: `{ck}`")
    if sk:
        parts.append(f"**System key**: `{sk}`")
    parts.append("")

    parts.append("**Arguments**")
    parts.append("")
    parts.append("| Flag | Type | Description |")
    parts.append("|------|------|-------------|")

    parts.append(
        f"| `{scope_flag}` (required) | string | "
        f"Target {scope_param.replace('_', ' ')} |"
    )

    for f in dataclasses.fields(user_cls):
        if f.name.startswith("_") or f.name == scope_param:
            continue
        tp = hints.get(f.name, str)
        label = _type_label(tp)
        desc = (f.metadata.get("description") if f.metadata else None) or ""
        flag = _flag_name(f.name)

        if label == "JSON":
            desc = f"{desc} (accepts JSON string or @file.json)"
        if label == "boolean":
            flag = f"{flag} / --no-{f.name.replace('_', '-')}"

        parts.append(f"| `{flag}` | {label} | {desc} |")

    parts.append("")
    return "\n".join(parts)


def generate_doc(tool_defs: List[Dict[str, Any]]) -> str:
    """Generate the full CLI reference Markdown document.

    Args:
        tool_defs: List of tool definition dicts.

    Returns:
        Complete Markdown document string.
    """
    parts: list[str] = []

    parts.append("# CLI Reference")
    parts.append("")
    parts.append(
        "Auto-generated from User Model introspection.  "
        "Do not edit manually — regenerate with "
        "`python tools/generate_cli_docs.py`."
    )
    parts.append("")
    parts.append("---")
    parts.append("")

    parts.append("## Overview")
    parts.append("")
    parts.append(
        f"The `meraki-cli` tool provides **{len(tool_defs)} commands**, "
        "one per resource module.  Commands are generated dynamically by "
        "introspecting User Model dataclasses."
    )
    parts.append("")
    parts.append("### Installation")
    parts.append("")
    parts.append("```bash")
    parts.append("pip install 'plugins/plugin_utils/[cli]'")
    parts.append("```")
    parts.append("")
    parts.append("### Quick Start")
    parts.append("")
    parts.append("```bash")
    parts.append("# List all available resource commands")
    parts.append("meraki-cli --list")
    parts.append("")
    parts.append("# Gather VLANs from a network")
    parts.append("export MERAKI_API_KEY=your_key_here")
    parts.append(
        'meraki-cli vlan gathered --network-id "L_123456789012345678"'
    )
    parts.append("")
    parts.append("# Create/update a VLAN")
    parts.append(
        "meraki-cli vlan merged --network-id L_123 "
        "--vlan-id 100 --name Engineering"
    )
    parts.append("")
    parts.append("# Use mock server for testing")
    parts.append("meraki-cli --mock vlan gathered --network-id N_test")
    parts.append("")
    parts.append("# Output as JSON")
    parts.append(
        "meraki-cli --json admin gathered --organization-id ORG_1"
    )
    parts.append("")
    parts.append("# Output as YAML")
    parts.append(
        "meraki-cli --yaml webhook gathered --network-id N_123"
    )
    parts.append("```")
    parts.append("")
    parts.append("### Global Flags")
    parts.append("")
    parts.append("| Flag | Description |")
    parts.append("|------|-------------|")
    parts.append("| `--mock` | Auto-start mock server and execute against it |")
    parts.append("| `--json` | Output results as JSON |")
    parts.append("| `--yaml` | Output results as YAML |")
    parts.append("| `--list` | List available resource commands and exit |")
    parts.append("")
    parts.append("### Complex Arguments")
    parts.append("")
    parts.append(
        "Fields with complex types (Dict, List[Dict]) accept either "
        "inline JSON strings or file references:"
    )
    parts.append("")
    parts.append("```bash")
    parts.append("# Inline JSON")
    parts.append(
        "meraki-cli group-policy merged --network-id N_123 "
        '--bandwidth-limits \'{"limitUp": 1000, "limitDown": 2000}\''
    )
    parts.append("")
    parts.append("# File reference")
    parts.append(
        "meraki-cli group-policy merged --network-id N_123 "
        "--bandwidth-limits @limits.json"
    )
    parts.append("```")
    parts.append("")
    parts.append("---")
    parts.append("")

    parts.append("## Command Summary")
    parts.append("")
    parts.append("| Command | Scope | States |")
    parts.append("|---------|-------|--------|")

    for td in sorted(tool_defs, key=lambda t: t["name"]):
        meta = td["_metadata"]
        cmd = meta["module_name"].replace("_", "-")
        states = ", ".join(meta["valid_states"])
        parts.append(
            f"| `{cmd}` | `{meta['scope_param']}` | {states} |"
        )

    parts.append("")
    parts.append("---")
    parts.append("")

    parts.append("## Command Reference")
    parts.append("")

    for td in sorted(tool_defs, key=lambda t: t["name"]):
        parts.append(_command_section(td))
        parts.append("---")
        parts.append("")

    parts.append("---")
    parts.append("")
    parts.append(
        "*Generated by `tools/generate_cli_docs.py` from "
        "User Model introspection.*"
    )

    return "\n".join(parts)


def main() -> None:
    """Entry point: build tool definitions and write the doc file."""
    tool_defs = build_tool_definitions()
    doc = generate_doc(tool_defs)

    output_path = ROOT / "docs" / "13-cli.md"
    output_path.write_text(doc)
    print(f"Generated {output_path} ({len(tool_defs)} commands)")


if __name__ == "__main__":
    main()
