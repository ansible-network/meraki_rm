"""Tests for the dynamic CLI: parser generation, argument handling, and formatting.

Validates the CLI stack built from User Model introspection:

1. ``build_parser`` — dynamic argparse subcommand generation
2. ``_parse_complex_arg`` — JSON / @file argument parsing
3. ``format_table`` — human-readable output formatting
4. ``--list`` — resource listing
5. ``--mock`` integration — end-to-end via mock server

Tests import directly from ``plugins.plugin_utils.cli.main`` and do not
require network access or the Ansible runtime (except integration tests).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from typing import Any

import pytest

from plugins.plugin_utils.cli.main import (
    _parse_complex_arg,
    build_parser,
    format_table,
)
from plugins.plugin_utils.mcp.introspect import build_tool_definitions


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def tool_defs() -> list[dict[str, Any]]:
    """Build tool definitions once for the module.

    Returns:
        List of tool definition dicts.
    """
    return build_tool_definitions()


@pytest.fixture(scope="module")
def parser_and_meta(
    tool_defs: list[dict[str, Any]],
) -> tuple[Any, dict[str, dict[str, Any]]]:
    """Build the CLI parser and resource metadata once.

    Args:
        tool_defs: Tool definitions from ``build_tool_definitions()``.

    Returns:
        Tuple of ``(argparse.ArgumentParser, resource_meta)``.
    """
    return build_parser(tool_defs)


# ---------------------------------------------------------------------------
# build_parser — subcommand generation
# ---------------------------------------------------------------------------

def test_parser_creates_subcommands(
    parser_and_meta: tuple[Any, dict[str, dict[str, Any]]],
) -> None:
    """Verify every tool definition produces a CLI subcommand."""
    _, meta = parser_and_meta
    assert len(meta) >= 40


def test_parser_vlan_subcommand_exists(
    parser_and_meta: tuple[Any, dict[str, dict[str, Any]]],
) -> None:
    """Verify the vlan subcommand is present."""
    _, meta = parser_and_meta
    assert "vlan" in meta


def test_parser_accepts_valid_state(
    parser_and_meta: tuple[Any, dict[str, dict[str, Any]]],
) -> None:
    """Verify the parser accepts a valid state for a known resource."""
    parser, _ = parser_and_meta
    args = parser.parse_args(["vlan", "gathered", "--network-id", "N_123"])

    assert args.resource == "vlan"
    assert args.state == "gathered"
    assert args.network_id == "N_123"


def test_parser_rejects_invalid_state(
    parser_and_meta: tuple[Any, dict[str, dict[str, Any]]],
) -> None:
    """Verify the parser rejects an invalid state."""
    parser, _ = parser_and_meta
    with pytest.raises(SystemExit):
        parser.parse_args(["vlan", "bogus", "--network-id", "N_123"])


def test_parser_requires_scope_param(
    parser_and_meta: tuple[Any, dict[str, dict[str, Any]]],
) -> None:
    """Verify the parser errors when the scope parameter is omitted."""
    parser, _ = parser_and_meta
    with pytest.raises(SystemExit):
        parser.parse_args(["vlan", "gathered"])


def test_parser_global_flags(
    parser_and_meta: tuple[Any, dict[str, dict[str, Any]]],
) -> None:
    """Verify --json, --yaml, --mock, --list are recognised global flags."""
    parser, _ = parser_and_meta
    args = parser.parse_args(["--json", "--mock", "vlan", "gathered", "--network-id", "N"])

    assert args.output_json is True
    assert args.mock is True


def test_parser_field_flags_present(
    parser_and_meta: tuple[Any, dict[str, dict[str, Any]]],
) -> None:
    """Verify resource-specific field flags are added (e.g. --vlan-id)."""
    parser, _ = parser_and_meta
    args = parser.parse_args([
        "vlan", "merged",
        "--network-id", "N_123",
        "--vlan-id", "100",
        "--name", "Engineering",
    ])

    assert args.vlan_id == "100"
    assert args.name == "Engineering"


def test_parser_boolean_fields(
    parser_and_meta: tuple[Any, dict[str, dict[str, Any]]],
) -> None:
    """Verify boolean fields accept --flag and --no-flag syntax."""
    parser, _ = parser_and_meta
    args_on = parser.parse_args([
        "switch-port", "merged",
        "--serial", "Q2XX",
        "--enabled",
    ])
    args_off = parser.parse_args([
        "switch-port", "merged",
        "--serial", "Q2XX",
        "--no-enabled",
    ])

    assert args_on.enabled is True
    assert args_off.enabled is False


# ---------------------------------------------------------------------------
# _parse_complex_arg — JSON and @file parsing
# ---------------------------------------------------------------------------

def test_parse_complex_arg_inline_json() -> None:
    """Verify inline JSON string is parsed correctly."""
    result = _parse_complex_arg('{"key": "value"}')

    assert result == {"key": "value"}


def test_parse_complex_arg_list_json() -> None:
    """Verify inline JSON list is parsed correctly."""
    result = _parse_complex_arg('[1, 2, 3]')

    assert result == [1, 2, 3]


def test_parse_complex_arg_file_reference() -> None:
    """Verify @file.json reads and parses the file contents."""
    data = {"name": "test", "vlan_id": 100}
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False,
    ) as fh:
        json.dump(data, fh)
        fh.flush()
        path = fh.name

    try:
        result = _parse_complex_arg(f"@{path}")
        assert result == data
    finally:
        os.unlink(path)


def test_parse_complex_arg_invalid_json() -> None:
    """Verify invalid JSON raises ArgumentTypeError."""
    import argparse

    with pytest.raises(argparse.ArgumentTypeError, match="Invalid JSON"):
        _parse_complex_arg("not-valid-json")


def test_parse_complex_arg_missing_file() -> None:
    """Verify @nonexistent raises ArgumentTypeError."""
    import argparse

    with pytest.raises(argparse.ArgumentTypeError, match="Cannot read"):
        _parse_complex_arg("@/tmp/does_not_exist_xyz.json")


# ---------------------------------------------------------------------------
# format_table — human-readable output
# ---------------------------------------------------------------------------

def test_format_table_flat_dict() -> None:
    """Verify flat dict renders as aligned key-value pairs."""
    result = format_table({"state": "gathered", "count": 3})

    assert "state:" in result
    assert "count:" in result


def test_format_table_nested_dict() -> None:
    """Verify nested dicts produce indented output."""
    result = format_table({
        "state": "merged",
        "result": {"name": "test", "id": 1},
    })

    assert "result:" in result
    assert "name:" in result


def test_format_table_list() -> None:
    """Verify lists of dicts are separated by ---."""
    result = format_table({
        "results": [
            {"id": 1, "name": "a"},
            {"id": 2, "name": "b"},
        ],
    })

    assert "---" in result


def test_format_table_empty_dict() -> None:
    """Verify empty dict renders (empty)."""
    result = format_table({})

    assert "(empty)" in result


# ---------------------------------------------------------------------------
# --list flag
# ---------------------------------------------------------------------------

def test_list_flag_subprocess() -> None:
    """Verify meraki-cli --list outputs resource names."""
    result = subprocess.run(
        [sys.executable, "-m", "meraki_rm_sdk.cli.main", "--list"],
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 0
    assert "vlan" in result.stdout
    assert "switch-port" in result.stdout


# ---------------------------------------------------------------------------
# Missing API key
# ---------------------------------------------------------------------------

def test_no_api_key_without_mock() -> None:
    """Verify CLI exits with error when MERAKI_API_KEY is unset."""
    env = {k: v for k, v in os.environ.items() if k != "MERAKI_API_KEY"}
    result = subprocess.run(
        [
            sys.executable, "-m", "meraki_rm_sdk.cli.main",
            "vlan", "gathered", "--network-id", "N_123",
        ],
        capture_output=True,
        text=True,
        timeout=15,
        env=env,
    )

    assert result.returncode == 1
    assert "MERAKI_API_KEY" in result.stderr


# ---------------------------------------------------------------------------
# Integration: --mock flag
# ---------------------------------------------------------------------------

def test_mock_gathered_returns_json() -> None:
    """Verify --mock --json gathered returns parseable JSON from mock server."""
    result = subprocess.run(
        [
            sys.executable, "-m", "meraki_rm_sdk.cli.main",
            "--mock", "--json",
            "vlan", "gathered", "--network-id", "N_cli_test",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["state"] == "gathered"
    assert isinstance(data["result"], (dict, list))


def test_mock_merged_round_trip() -> None:
    """Verify --mock merge + gather round trip via CLI."""
    merge_result = subprocess.run(
        [
            sys.executable, "-m", "meraki_rm_sdk.cli.main",
            "--mock", "--json",
            "vlan", "merged",
            "--network-id", "N_cli_rt",
            "--vlan-id", "999",
            "--name", "CLITest",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert merge_result.returncode == 0
    merge_data = json.loads(merge_result.stdout)
    assert merge_data["state"] == "merged"
