#!/usr/bin/env python3
"""Generate MCP server reference documentation from User Model introspection.

Produces ``docs/12-mcp-server.md`` by introspecting all User Model dataclasses
and the MCP server configuration.  The output includes a tool catalogue with
input schemas, metadata, and usage examples.

Idempotent: safe to re-run whenever User Models or server code change.

Usage::

    python tools/generate_mcp_docs.py
"""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from plugins.plugin_utils.mcp.introspect import build_tool_definitions


def _format_schema_table(schema: Dict[str, Any]) -> str:
    """Convert a JSON Schema properties dict into a Markdown table.

    Args:
        schema: JSON Schema ``object`` with ``properties`` and optional
            ``required`` keys.

    Returns:
        Markdown table string with columns: Field, Type, Required, Description.
    """
    props = schema.get("properties", {})
    required = set(schema.get("required", []))

    lines: list[str] = [
        "| Field | Type | Required | Description |",
        "|-------|------|----------|-------------|",
    ]

    for name, spec in sorted(props.items()):
        ftype = spec.get("type", "string")
        if ftype == "array":
            items = spec.get("items", {})
            inner = items.get("type", "object")
            ftype = f"array[{inner}]"

        req = "yes" if name in required else ""
        desc = spec.get("description", "")
        lines.append(f"| `{name}` | {ftype} | {req} | {desc} |")

    return "\n".join(lines)


def _tool_section(td: Dict[str, Any]) -> str:
    """Render a single tool definition as a Markdown section.

    Args:
        td: Tool definition dict from ``build_tool_definitions()``.

    Returns:
        Markdown string for this tool.
    """
    meta = td["_metadata"]
    name = td["name"]
    desc = td["description"]

    parts: list[str] = [f"### `{name}`", "", desc, ""]

    parts.append("**Metadata**")
    parts.append("")
    parts.append(f"- **Scope**: `{meta['scope_param']}`")
    parts.append(
        f"- **Canonical key**: `{meta['canonical_key'] or '(none — Category C)'}`"
    )
    parts.append(
        f"- **System key**: `{meta['system_key'] or '(same as canonical)'}`"
    )
    parts.append(f"- **Supports delete**: {meta['supports_delete']}")
    parts.append(f"- **Valid states**: {', '.join(meta['valid_states'])}")
    parts.append("")

    parts.append("**Top-level input schema**")
    parts.append("")
    parts.append(_format_schema_table(td["inputSchema"]))
    parts.append("")

    config_schema = td["inputSchema"]["properties"].get("config", {}).get(
        "items", {}
    )
    config_props = config_schema.get("properties", {})
    if config_props:
        parts.append("**Config item fields**")
        parts.append("")
        parts.append(_format_schema_table(config_schema))
        parts.append("")

    return "\n".join(parts)


def _category_for(td: Dict[str, Any]) -> str:
    """Return the identity category label for a tool definition.

    Args:
        td: Tool definition dict.

    Returns:
        One of 'A', 'B', or 'C'.
    """
    meta = td["_metadata"]
    if meta["canonical_key"] is None:
        return "C"
    if meta["system_key"] is not None:
        return "B"
    return "A"


def generate_doc(tool_defs: List[Dict[str, Any]]) -> str:
    """Generate the full Markdown document from tool definitions.

    Args:
        tool_defs: List of tool definition dicts.

    Returns:
        Complete Markdown document string.
    """
    parts: list[str] = []

    parts.append("# MCP Server Reference")
    parts.append("")
    parts.append(
        "Auto-generated from User Model introspection.  "
        "Do not edit manually — regenerate with "
        "`python tools/generate_mcp_docs.py`."
    )
    parts.append("")
    parts.append("---")
    parts.append("")

    parts.append("## Overview")
    parts.append("")
    parts.append(
        f"The Meraki RM MCP server exposes **{len(tool_defs)} tools**, "
        "one per resource module.  Tools are generated at startup by "
        "introspecting User Model dataclasses."
    )
    parts.append("")
    parts.append("### Running the Server")
    parts.append("")
    parts.append("```bash")
    parts.append("# Task mode (default) — returns Ansible YAML snippets")
    parts.append("meraki-mcp-server --mode=task")
    parts.append("")
    parts.append("# Live mode — executes against the Meraki Dashboard API")
    parts.append("export MERAKI_API_KEY=your_key_here")
    parts.append("meraki-mcp-server --mode=live")
    parts.append("```")
    parts.append("")
    parts.append("### Installation")
    parts.append("")
    parts.append("```bash")
    parts.append("pip install 'plugins/plugin_utils/[mcp]'")
    parts.append("```")
    parts.append("")
    parts.append("---")
    parts.append("")

    parts.append("## Tool Summary")
    parts.append("")
    parts.append("| Tool | Scope | Canonical Key | Category | States |")
    parts.append("|------|-------|---------------|----------|--------|")

    for td in sorted(tool_defs, key=lambda t: t["name"]):
        meta = td["_metadata"]
        cat = _category_for(td)
        ck = f"`{meta['canonical_key']}`" if meta["canonical_key"] else "—"
        states = ", ".join(meta["valid_states"])
        parts.append(
            f"| `{td['name']}` | `{meta['scope_param']}` | {ck} | {cat} | {states} |"
        )

    parts.append("")
    parts.append("---")
    parts.append("")

    parts.append("## Tool Reference")
    parts.append("")

    for td in sorted(tool_defs, key=lambda t: t["name"]):
        parts.append(_tool_section(td))
        parts.append("---")
        parts.append("")

    parts.append("---")
    parts.append("")
    parts.append(
        "*Generated by `tools/generate_mcp_docs.py` from User Model introspection.*"
    )

    return "\n".join(parts)


def main() -> None:
    """Entry point: build tool definitions and write the doc file."""
    tool_defs = build_tool_definitions()
    doc = generate_doc(tool_defs)

    output_path = ROOT / "docs" / "12-mcp-server.md"
    output_path.write_text(doc)
    print(f"Generated {output_path} ({len(tool_defs)} tools)")


if __name__ == "__main__":
    main()
