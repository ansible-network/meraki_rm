"""Dynamic CLI for managing Meraki Dashboard resources.

Generates argparse subcommands by introspecting User Model dataclasses.
Each resource becomes a subcommand with typed flags derived from its fields.

Usage::

    meraki-cli vlan merged --network-id N_123 --vlan-id 100 --name Eng
    meraki-cli switch-port gathered --serial Q2XX-XXXX-XXXX
    meraki-cli --mock vlan gathered --network-id N_test
    meraki-cli --json admin gathered --organization-id ORG_1
    meraki-cli --list
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import subprocess
import sys
import typing
from typing import Any, Dict, List, Optional

import yaml

from ..mcp.introspect import build_tool_definitions
from ..mcp.schema import _unwrap_optional


def _parse_complex_arg(value: str) -> Any:
    """Parse a complex CLI argument as JSON or a ``@file.json`` reference.

    Args:
        value: A raw JSON string, or a path prefixed with ``@`` pointing to
            a JSON file on disk.

    Returns:
        Parsed Python object (dict, list, etc.).

    Raises:
        argparse.ArgumentTypeError: If the JSON is invalid or the file
            cannot be read.
    """
    if value.startswith("@"):
        path = value[1:]
        try:
            with open(path) as fh:
                return json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            raise argparse.ArgumentTypeError(
                f"Cannot read JSON from {path}: {exc}"
            ) from exc
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid JSON: {exc}"
        ) from exc


def _flag_name(field_name: str) -> str:
    """Convert a snake_case field name to a --kebab-case CLI flag.

    Args:
        field_name: Python field name (e.g. ``vlan_id``).

    Returns:
        CLI flag string (e.g. ``--vlan-id``).
    """
    return f"--{field_name.replace('_', '-')}"


def _add_field_flags(
    parser: argparse.ArgumentParser,
    user_cls: type,
    exclude: set[str],
) -> list[str]:
    """Add argparse flags for every public dataclass field.

    Args:
        parser: The argparse subparser to add flags to.
        user_cls: The User Model dataclass class.
        exclude: Field names to skip (e.g. scope param, privates).

    Returns:
        List of field names that require complex-arg post-processing.
    """
    hints = typing.get_type_hints(user_cls)
    complex_fields: list[str] = []

    for f in dataclasses.fields(user_cls):
        if f.name.startswith("_") or f.name in exclude:
            continue

        tp = hints.get(f.name, str)
        inner, _ = _unwrap_optional(tp)
        desc = (f.metadata.get("description") if f.metadata else None) or ""
        flag = _flag_name(f.name)

        origin = getattr(inner, "__origin__", None)

        if inner is bool:
            parser.add_argument(
                flag,
                action=argparse.BooleanOptionalAction,
                default=None,
                help=desc,
            )
        elif inner is int:
            parser.add_argument(flag, type=int, default=None, help=desc)
        elif inner is float:
            parser.add_argument(flag, type=float, default=None, help=desc)
        elif inner is str:
            parser.add_argument(flag, type=str, default=None, help=desc)
        elif origin in (list, typing.List):
            args = getattr(inner, "__args__", ())
            if args and args[0] is str:
                parser.add_argument(flag, nargs="+", default=None, help=desc)
            else:
                parser.add_argument(
                    flag, type=str, default=None,
                    help=f"{desc} (JSON string or @file.json)",
                )
                complex_fields.append(f.name)
        elif origin in (dict, typing.Dict) or inner is dict:
            parser.add_argument(
                flag, type=str, default=None,
                help=f"{desc} (JSON string or @file.json)",
            )
            complex_fields.append(f.name)
        else:
            parser.add_argument(flag, type=str, default=None, help=desc)

    return complex_fields


def build_parser(
    tool_defs: list[dict[str, Any]],
) -> tuple[argparse.ArgumentParser, dict[str, dict[str, Any]]]:
    """Build the top-level parser with a subcommand per resource.

    Args:
        tool_defs: Tool definitions from ``build_tool_definitions()``.

    Returns:
        Tuple of ``(parser, resource_meta)`` where ``resource_meta`` maps
        subcommand name to its tool definition dict augmented with
        ``_complex_fields``.
    """
    parser = argparse.ArgumentParser(
        prog="meraki-cli",
        description="Manage Meraki Dashboard resources from the command line",
    )
    parser.add_argument(
        "--mock", action="store_true",
        help="Auto-start the mock server and execute against it",
    )
    parser.add_argument(
        "--json", action="store_true", dest="output_json",
        help="Output results as JSON",
    )
    parser.add_argument(
        "--yaml", action="store_true", dest="output_yaml",
        help="Output results as YAML",
    )
    parser.add_argument(
        "--list", action="store_true", dest="list_resources",
        help="List available resources and exit",
    )

    subparsers = parser.add_subparsers(dest="resource")
    resource_meta: dict[str, dict[str, Any]] = {}

    for td in sorted(tool_defs, key=lambda t: t["name"]):
        meta = td["_metadata"]
        module_name: str = meta["module_name"]
        cmd_name = module_name.replace("_", "-")
        scope_param: str = meta["scope_param"]
        valid_states: list[str] = meta["valid_states"]
        user_cls = meta["user_model_class"]

        sub = subparsers.add_parser(
            cmd_name,
            help=td["description"],
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        sub.add_argument(
            "state",
            choices=valid_states,
            help="Resource module state",
        )

        scope_flag = _flag_name(scope_param)
        sub.add_argument(
            scope_flag, required=True,
            help=f"Target {scope_param.replace('_', ' ')}",
        )

        complex_fields = _add_field_flags(
            sub, user_cls, exclude={scope_param},
        )

        resource_meta[cmd_name] = {
            **td,
            "_complex_fields": complex_fields,
        }

    return parser, resource_meta


def _execute(
    module_name: str,
    state: str,
    scope_param: str,
    scope_value: str,
    config: dict[str, Any],
    user_cls: type,
) -> dict[str, Any]:
    """Execute a resource operation via PlatformService.

    Args:
        module_name: Internal module name (e.g. ``vlan``).
        state: Resource state (``merged``, ``gathered``, etc.).
        scope_param: Scope parameter name (e.g. ``network_id``).
        scope_value: Scope parameter value.
        config: Config dict for a single resource item.
        user_cls: User Model dataclass class.

    Returns:
        Dict with ``state`` and ``result`` keys.
    """
    from dataclasses import asdict

    from ..manager.platform_manager import PlatformService

    api_key = os.environ.get("MERAKI_API_KEY", "")
    dashboard_url = os.environ.get(
        "MERAKI_DASHBOARD_URL", "https://api.meraki.com/api/v1",
    )

    service = PlatformService(dashboard_url, api_key)

    state_to_op = {
        "merged": "update",
        "replaced": "replace",
        "overridden": "override",
        "deleted": "delete",
        "gathered": "find",
    }
    operation = state_to_op.get(state, "update")

    user_data = user_cls(**{scope_param: scope_value}, **config)
    result = service.execute(operation, module_name, asdict(user_data))

    return {"state": state, "result": result}


def format_table(data: dict[str, Any]) -> str:
    """Format a result dict as aligned key-value pairs.

    Args:
        data: Result dict (may contain nested dicts/lists).

    Returns:
        Human-readable multi-line string.
    """
    lines: list[str] = []

    def _render(obj: Any, indent: int = 0) -> None:
        prefix = "  " * indent
        if isinstance(obj, dict):
            if not obj:
                lines.append(f"{prefix}(empty)")
                return
            max_key = max(len(str(k)) for k in obj)
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    lines.append(f"{prefix}{str(k) + ':':<{max_key + 1}}")
                    _render(v, indent + 1)
                else:
                    lines.append(f"{prefix}{str(k) + ':':<{max_key + 1}}  {v}")
        elif isinstance(obj, list):
            if not obj:
                lines.append(f"{prefix}(empty list)")
                return
            for i, item in enumerate(obj):
                if i > 0:
                    lines.append(f"{prefix}---")
                _render(item, indent)
        else:
            lines.append(f"{prefix}{obj}")

    _render(data)
    return "\n".join(lines)


def main() -> None:
    """CLI entry point."""
    tool_defs = build_tool_definitions()

    parser, resource_meta = build_parser(tool_defs)

    args = parser.parse_args()

    if args.list_resources:
        for td in sorted(tool_defs, key=lambda t: t["name"]):
            meta = td["_metadata"]
            name = meta["module_name"].replace("_", "-")
            print(f"  {name:<35} {td['description']}")
        return

    if not args.resource:
        parser.print_help()
        return

    mock_proc: subprocess.Popen | None = None
    if args.mock:
        from ..mock import MOCK_URL, start_mock_server

        os.environ["MERAKI_API_KEY"] = "mock-api-key"
        os.environ["MERAKI_DASHBOARD_URL"] = MOCK_URL
        mock_proc = start_mock_server()

    if not args.mock and not os.environ.get("MERAKI_API_KEY"):
        print(
            "ERROR: MERAKI_API_KEY environment variable required "
            "(or use --mock for testing)",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        cmd_name = args.resource
        td = resource_meta[cmd_name]
        meta = td["_metadata"]
        complex_fields: list[str] = td["_complex_fields"]

        scope_param: str = meta["scope_param"]
        scope_value = getattr(args, scope_param.replace("-", "_"))

        config: dict[str, Any] = {}
        user_cls = meta["user_model_class"]
        for f in dataclasses.fields(user_cls):
            if f.name.startswith("_") or f.name == scope_param:
                continue
            attr_name = f.name
            val = getattr(args, attr_name, None)
            if val is None:
                continue
            if attr_name in complex_fields and isinstance(val, str):
                val = _parse_complex_arg(val)
            config[attr_name] = val

        result = _execute(
            meta["module_name"],
            args.state,
            scope_param,
            scope_value,
            config,
            user_cls,
        )

        if args.output_json:
            print(json.dumps(result, indent=2, default=str))
        elif args.output_yaml:
            print(yaml.dump(result, default_flow_style=False, sort_keys=False))
        else:
            print(format_table(result))

    finally:
        if mock_proc is not None:
            from ..mock import stop_mock_server

            stop_mock_server(mock_proc)


if __name__ == "__main__":
    main()
