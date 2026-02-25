"""MCP server for the Meraki RM SDK.

Dynamically generates tools by introspecting User Model dataclasses.
Supports three modes:

  --mode=task  (default): Returns Ansible task YAML snippets. No auth needed.
  --mode=live:            Executes operations against the Meraki API.
                          Requires MERAKI_API_KEY env var.
  --mock:                 Starts the mock server automatically, then runs
                          in live mode against it.  No real API key needed.

Uses the low-level mcp.server.Server API for full control over tool
schemas (generated at runtime from dataclass introspection).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
from typing import Any, Dict

import yaml
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from .introspect import build_tool_definitions


def _build_ansible_task(tool_name: str, args: Dict[str, Any], metadata: Dict[str, Any]) -> str:
    """Generate an Ansible task YAML snippet from tool call arguments."""
    fqcn = f"cisco.meraki_rm.{tool_name}"

    module_args: Dict[str, Any] = {}

    scope_param = metadata["scope_param"]
    if scope_param in args:
        module_args[scope_param] = args[scope_param]

    if "state" in args:
        module_args["state"] = args["state"]

    if "config" in args:
        module_args["config"] = args["config"]

    state = args.get("state", "merged")
    task = {
        "name": f"{tool_name.replace('_', ' ').title()} — {state}",
        fqcn: module_args,
    }

    if state != "gathered":
        task["register"] = f"{tool_name}_result"

    return yaml.dump([task], default_flow_style=False, sort_keys=False)


def _execute_live(tool_name: str, args: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Execute an operation against the Meraki Dashboard API.

    Args:
        tool_name: MCP tool name (e.g. ``meraki_vlan``).
        args: Tool call arguments from the MCP client.
        metadata: Internal metadata dict for this tool.

    Returns:
        Dict with ``state`` and ``results`` keys.
    """
    api_key = os.environ.get("MERAKI_API_KEY")
    dashboard_url = os.environ.get("MERAKI_DASHBOARD_URL", "https://api.meraki.com/api/v1")

    from dataclasses import asdict

    from ..manager.platform_manager import PlatformService

    service = PlatformService(dashboard_url, api_key)

    user_cls = metadata["user_model_class"]
    scope_param = metadata["scope_param"]
    module_name = metadata["module_name"]

    scope_value = args.get(scope_param)
    state = args.get("state", "merged")
    config = args.get("config", [{}])

    state_to_op = {
        "merged": "update",
        "replaced": "replace",
        "overridden": "override",
        "deleted": "delete",
        "gathered": "find",
    }
    operation = state_to_op.get(state, "update")

    results = []
    for item in config:
        user_data = user_cls(**{scope_param: scope_value}, **item)
        result = service.execute(operation, module_name, asdict(user_data))
        results.append(result)

    return {"state": state, "results": results}


def _describe_tools(tool_defs: list[Dict[str, Any]], arguments: Dict[str, Any]) -> str:
    """Build a self-documentation response for the describe_tools meta-tool.

    Args:
        tool_defs: All tool definitions from introspection.
        arguments: Caller-supplied arguments (optional ``name`` filter).

    Returns:
        JSON string with tool catalogue or single-tool detail.
    """
    name_filter = arguments.get("name")

    if name_filter:
        matches = [t for t in tool_defs if t["name"] == name_filter]
        if not matches:
            return json.dumps({"error": f"Unknown tool: {name_filter}"}, indent=2)
        td = matches[0]
        meta = td["_metadata"]
        return json.dumps({
            "name": td["name"],
            "description": td["description"],
            "scope_param": meta["scope_param"],
            "canonical_key": meta["canonical_key"],
            "system_key": meta["system_key"],
            "supports_delete": meta["supports_delete"],
            "valid_states": meta["valid_states"],
            "inputSchema": td["inputSchema"],
        }, indent=2, default=str)

    catalogue = []
    for td in sorted(tool_defs, key=lambda t: t["name"]):
        meta = td["_metadata"]
        catalogue.append({
            "name": td["name"],
            "scope": meta["scope_param"],
            "canonical_key": meta["canonical_key"],
            "states": meta["valid_states"],
        })
    return json.dumps({"tool_count": len(catalogue), "tools": catalogue}, indent=2)


def create_server(mode: str = "task") -> Server:
    """Create and configure the MCP server with dynamically generated tools.

    Args:
        mode: Server mode — ``"task"`` for Ansible YAML generation or
            ``"live"`` for direct API execution.

    Returns:
        Configured ``mcp.server.Server`` instance.
    """
    server = Server("meraki-rm")

    tool_defs = build_tool_definitions()
    tool_index: Dict[str, Dict[str, Any]] = {t["name"]: t for t in tool_defs}

    _DESCRIBE_SCHEMA: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Tool name to describe. Omit for a full catalogue.",
            },
        },
    }

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """Return all dynamically generated resource tools plus the meta-tool."""
        tools = []
        for td in tool_defs:
            desc = td["description"]
            if mode == "task":
                desc += " Returns an Ansible task YAML snippet."
            else:
                desc += " Executes the operation against the Meraki API."

            tools.append(Tool(
                name=td["name"],
                description=desc,
                inputSchema=td["inputSchema"],
            ))

        tools.append(Tool(
            name="describe_tools",
            description=(
                "Self-documentation meta-tool. Returns a catalogue of all "
                "available tools, or detailed info for a specific tool by name."
            ),
            inputSchema=_DESCRIBE_SCHEMA,
        ))

        return tools

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """Dispatch a tool call to the appropriate handler."""
        if name == "describe_tools":
            text = _describe_tools(tool_defs, arguments)
            return [TextContent(type="text", text=text)]

        td = tool_index.get(name)
        if td is None:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}. Available: {sorted(tool_index.keys())}",
            )]

        metadata = td["_metadata"]

        if mode == "task":
            text = _build_ansible_task(name, arguments, metadata)
        else:
            result = _execute_live(name, arguments, metadata)
            text = json.dumps(result, indent=2, default=str)

        return [TextContent(type="text", text=text)]

    return server


async def _run_server(mode: str) -> None:
    """Run the MCP server over stdio."""
    server = create_server(mode=mode)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main() -> None:
    """CLI entry point for the MCP server."""
    parser = argparse.ArgumentParser(
        description="Meraki RM MCP Server — dynamic tool generation from User Model introspection",
    )
    parser.add_argument(
        "--mode",
        choices=["task", "live"],
        default="task",
        help="Server mode: 'task' generates Ansible YAML (default), 'live' executes API calls",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help=(
            "Auto-start the mock server and run in live mode against it. "
            "Implies --mode=live. No MERAKI_API_KEY needed."
        ),
    )
    args = parser.parse_args()

    from ..mock import MOCK_URL, start_mock_server, stop_mock_server

    mock_proc: subprocess.Popen | None = None

    if args.mock:
        args.mode = "live"
        os.environ["MERAKI_API_KEY"] = "mock-api-key"
        os.environ["MERAKI_DASHBOARD_URL"] = MOCK_URL
        mock_proc = start_mock_server()
    elif args.mode == "live":
        api_key = os.environ.get("MERAKI_API_KEY")
        if not api_key:
            print(
                "ERROR: --mode=live requires MERAKI_API_KEY environment variable",
                file=sys.stderr,
            )
            sys.exit(1)

    try:
        asyncio.run(_run_server(args.mode))
    finally:
        if mock_proc is not None:
            stop_mock_server(mock_proc)


if __name__ == "__main__":
    main()
