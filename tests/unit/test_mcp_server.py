"""Tests for the MCP server: schema conversion, introspection, and end-to-end.

Validates three layers of the MCP server stack:

1. ``schema.py`` — dataclass-to-JSON-Schema conversion
2. ``introspect.py`` — User Model discovery and tool definition generation
3. ``server.py`` — full MCP protocol round-trip via ``mcp.ClientSession``

Tests import directly from ``plugins.plugin_utils.mcp.*`` and do not
require network access or the Ansible runtime.
"""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import pytest
import yaml

from plugins.plugin_utils.mcp.schema import dataclass_to_json_schema
from plugins.plugin_utils.mcp.introspect import build_tool_definitions
from plugins.plugin_utils.mcp.server import _build_ansible_task


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def tool_defs() -> list[dict[str, Any]]:
    """Build tool definitions once for the entire module.

    Returns:
        List of tool definition dicts from ``build_tool_definitions()``.
    """
    return build_tool_definitions()


@pytest.fixture(scope="module")
def tool_index(tool_defs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Index tool definitions by name for fast lookup.

    Args:
        tool_defs: List of tool definition dicts.

    Returns:
        Dict mapping tool name to tool definition.
    """
    return {t["name"]: t for t in tool_defs}


# ---------------------------------------------------------------------------
# schema.py — dataclass_to_json_schema
# ---------------------------------------------------------------------------

def test_schema_basic_types() -> None:
    """Verify JSON Schema mapping for str, int, float, and bool."""
    @dataclass
    class Sample:
        s: Optional[str] = None
        i: Optional[int] = None
        f: Optional[float] = None
        b: Optional[bool] = None

    schema = dataclass_to_json_schema(Sample)

    assert schema["type"] == "object"
    assert schema["properties"]["s"] == {"type": "string"}
    assert schema["properties"]["i"] == {"type": "integer"}
    assert schema["properties"]["f"] == {"type": "number"}
    assert schema["properties"]["b"] == {"type": "boolean"}


def test_schema_list_and_dict_types() -> None:
    """Verify JSON Schema mapping for List and Dict type annotations."""
    @dataclass
    class Sample:
        tags: Optional[List[str]] = None
        items: Optional[List[Dict[str, Any]]] = None
        metadata: Optional[Dict[str, Any]] = None

    schema = dataclass_to_json_schema(Sample)

    assert schema["properties"]["tags"] == {
        "type": "array", "items": {"type": "string"},
    }
    assert schema["properties"]["items"] == {
        "type": "array", "items": {"type": "object"},
    }
    assert schema["properties"]["metadata"] == {"type": "object"}


def test_schema_descriptions_from_field_metadata() -> None:
    """Verify descriptions are extracted from field metadata dicts."""
    @dataclass
    class Sample:
        name: Optional[str] = field(
            default=None, metadata={"description": "The name."},
        )
        count: Optional[int] = field(
            default=None, metadata={"description": "Item count."},
        )

    schema = dataclass_to_json_schema(Sample)

    assert schema["properties"]["name"]["description"] == "The name."
    assert schema["properties"]["count"]["description"] == "Item count."


def test_schema_no_description_when_absent() -> None:
    """Verify no description key when field has no metadata."""
    @dataclass
    class Sample:
        plain: Optional[str] = None

    schema = dataclass_to_json_schema(Sample)

    assert "description" not in schema["properties"]["plain"]


def test_schema_exclude_fields() -> None:
    """Verify exclude_fields omits specified fields from the schema."""
    @dataclass
    class Sample:
        network_id: Optional[str] = None
        name: Optional[str] = None

    schema = dataclass_to_json_schema(Sample, exclude_fields={"network_id"})

    assert "network_id" not in schema["properties"]
    assert "name" in schema["properties"]


def test_schema_private_fields_excluded() -> None:
    """Verify fields starting with underscore are omitted."""
    @dataclass
    class Sample:
        name: Optional[str] = None
        _internal: Optional[str] = None

    schema = dataclass_to_json_schema(Sample)

    assert "name" in schema["properties"]
    assert "_internal" not in schema["properties"]


def test_schema_not_a_dataclass_raises() -> None:
    """Verify TypeError is raised for non-dataclass types."""
    class NotDC:
        pass

    with pytest.raises(TypeError, match="is not a dataclass"):
        dataclass_to_json_schema(NotDC)


# ---------------------------------------------------------------------------
# introspect.py — build_tool_definitions
# ---------------------------------------------------------------------------

def test_discovers_48_tools(tool_defs: list[dict[str, Any]]) -> None:
    """Verify all 48 resource modules are discovered as tools."""
    assert len(tool_defs) == 48


def test_all_tools_have_required_keys(tool_defs: list[dict[str, Any]]) -> None:
    """Verify every tool dict has name, description, inputSchema, and _metadata."""
    for t in tool_defs:
        assert "name" in t, f"Missing 'name' in {t}"
        assert "description" in t, f"Missing 'description' in {t}"
        assert "inputSchema" in t, f"Missing 'inputSchema' in {t}"
        assert "_metadata" in t, f"Missing '_metadata' in {t}"


def test_tool_names_start_with_meraki(tool_defs: list[dict[str, Any]]) -> None:
    """Verify every tool name is prefixed with 'meraki_'."""
    for t in tool_defs:
        assert t["name"].startswith("meraki_"), t["name"]


def test_vlan_tool_schema_shape(tool_index: dict[str, dict[str, Any]]) -> None:
    """Verify the meraki_vlan tool has the correct schema structure.

    Checks scope requirement, config field presence, and a representative
    field description.
    """
    vlan = tool_index["meraki_vlan"]

    assert "Canonical key: vlan_id" in vlan["description"]

    schema = vlan["inputSchema"]
    assert schema["required"] == ["network_id"]
    assert "state" in schema["properties"]
    assert "config" in schema["properties"]

    config_props = schema["properties"]["config"]["items"]["properties"]
    assert "vlan_id" in config_props
    assert config_props["vlan_id"]["description"] == (
        "VLAN ID (1-4094). Required for merged and deleted."
    )


def test_admin_tool_org_scope(tool_index: dict[str, dict[str, Any]]) -> None:
    """Verify meraki_admin uses organization_id scope and Category B keys."""
    admin = tool_index["meraki_admin"]

    assert admin["_metadata"]["scope_param"] == "organization_id"
    assert admin["inputSchema"]["required"] == ["organization_id"]
    assert admin["_metadata"]["canonical_key"] == "email"
    assert admin["_metadata"]["system_key"] == "admin_id"


def test_air_marshal_restricted_states(
    tool_index: dict[str, dict[str, Any]],
) -> None:
    """Verify meraki_air_marshal exposes only its restricted state set."""
    am = tool_index["meraki_air_marshal"]
    states = set(am["_metadata"]["valid_states"])

    assert states == {"merged", "replaced", "deleted"}


def test_singleton_supports_delete_false(
    tool_index: dict[str, dict[str, Any]],
) -> None:
    """Verify singleton resources report SUPPORTS_DELETE=False."""
    fw = tool_index["meraki_firewall"]

    assert fw["_metadata"]["supports_delete"] is False


def test_config_schema_excludes_scope_field(
    tool_index: dict[str, dict[str, Any]],
) -> None:
    """Verify config items schema omits the scope parameter field."""
    admin = tool_index["meraki_admin"]
    config_props = (
        admin["inputSchema"]["properties"]["config"]["items"]["properties"]
    )

    assert "organization_id" not in config_props


def test_device_tool_serial_scope(
    tool_index: dict[str, dict[str, Any]],
) -> None:
    """Verify meraki_device uses serial as its scope parameter."""
    device = tool_index["meraki_device"]

    assert device["_metadata"]["scope_param"] == "serial"
    assert device["inputSchema"]["required"] == ["serial"]


# ---------------------------------------------------------------------------
# server.py — _build_ansible_task
# ---------------------------------------------------------------------------

def test_merged_produces_valid_yaml() -> None:
    """Verify merged state generates parseable Ansible task YAML."""
    text = _build_ansible_task(
        "meraki_vlan",
        {"network_id": "N_123", "state": "merged", "config": [{"vlan_id": "100"}]},
        {"scope_param": "network_id"},
    )
    tasks = yaml.safe_load(text)

    assert isinstance(tasks, list)
    assert len(tasks) == 1
    task = tasks[0]
    assert "cisco.meraki_rm.meraki_vlan" in task
    assert task["cisco.meraki_rm.meraki_vlan"]["network_id"] == "N_123"
    assert task["cisco.meraki_rm.meraki_vlan"]["state"] == "merged"
    assert task["register"] == "meraki_vlan_result"


def test_gathered_has_no_register() -> None:
    """Verify gathered state omits the register key."""
    text = _build_ansible_task(
        "meraki_admin",
        {"organization_id": "ORG_1", "state": "gathered"},
        {"scope_param": "organization_id"},
    )
    tasks = yaml.safe_load(text)

    assert "register" not in tasks[0]


def test_fqcn_format() -> None:
    """Verify the task uses the full cisco.meraki_rm FQCN."""
    text = _build_ansible_task(
        "meraki_wireless_rf_profile",
        {"network_id": "N_1", "state": "merged"},
        {"scope_param": "network_id"},
    )
    tasks = yaml.safe_load(text)

    assert "cisco.meraki_rm.meraki_wireless_rf_profile" in tasks[0]


# ---------------------------------------------------------------------------
# End-to-end MCP server via ClientSession
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def mcp_session():
    """Start an MCP server subprocess and yield a connected ClientSession.

    The fixture runs setup and teardown within a single asyncio task to
    satisfy anyio's requirement that cancel scopes are entered and exited
    in the same task.

    Yields:
        Tuple of ``(asyncio.AbstractEventLoop, mcp.ClientSession)``.
    """
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    loop = asyncio.new_event_loop()
    ready: asyncio.Future[None] = loop.create_future()
    done: asyncio.Future[None] = loop.create_future()
    holder: dict[str, Any] = {}

    async def lifecycle() -> None:
        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "meraki_rm_sdk.mcp.server", "--mode=task"],
        )
        async with stdio_client(params) as transport:
            read_stream, write_stream = transport
            async with ClientSession(read_stream, write_stream) as session_obj:
                await session_obj.initialize()
                holder["session"] = session_obj
                ready.set_result(None)
                await done

    task = loop.create_task(lifecycle())
    loop.run_until_complete(ready)

    yield loop, holder["session"]

    done.set_result(None)
    loop.run_until_complete(task)
    loop.close()


def test_e2e_list_tools_returns_49(
    mcp_session: tuple[asyncio.AbstractEventLoop, Any],
) -> None:
    """Verify the server exposes 49 tools (48 resources + describe_tools)."""
    loop, session = mcp_session
    result = loop.run_until_complete(session.list_tools())

    assert len(result.tools) == 49
    tool_names = {t.name for t in result.tools}
    assert "describe_tools" in tool_names


def test_e2e_tools_have_schemas(
    mcp_session: tuple[asyncio.AbstractEventLoop, Any],
) -> None:
    """Verify every listed tool has a non-empty inputSchema."""
    loop, session = mcp_session
    result = loop.run_until_complete(session.list_tools())

    for t in result.tools:
        assert t.inputSchema is not None
        assert "properties" in t.inputSchema


def test_e2e_call_tool_returns_valid_yaml(
    mcp_session: tuple[asyncio.AbstractEventLoop, Any],
) -> None:
    """Verify calling a tool returns parseable Ansible task YAML."""
    loop, session = mcp_session
    result = loop.run_until_complete(
        session.call_tool(
            "meraki_vlan",
            arguments={
                "network_id": "N_123",
                "state": "merged",
                "config": [{"vlan_id": "100", "name": "Test"}],
            },
        )
    )
    text = result.content[0].text
    tasks = yaml.safe_load(text)

    assert isinstance(tasks, list)
    assert "cisco.meraki_rm.meraki_vlan" in tasks[0]


def test_e2e_call_unknown_tool(
    mcp_session: tuple[asyncio.AbstractEventLoop, Any],
) -> None:
    """Verify calling a nonexistent tool returns an error message."""
    loop, session = mcp_session
    result = loop.run_until_complete(
        session.call_tool("nonexistent_tool", arguments={})
    )
    text = result.content[0].text

    assert "Unknown tool" in text


def test_e2e_tool_descriptions_include_mode_suffix(
    mcp_session: tuple[asyncio.AbstractEventLoop, Any],
) -> None:
    """Verify task-mode resource tool descriptions mention Ansible task YAML."""
    loop, session = mcp_session
    result = loop.run_until_complete(session.list_tools())

    resource_tools = [t for t in result.tools if t.name != "describe_tools"]
    for t in resource_tools:
        assert "Ansible task YAML" in t.description


def test_e2e_describe_tools_catalogue(
    mcp_session: tuple[asyncio.AbstractEventLoop, Any],
) -> None:
    """Verify describe_tools returns a catalogue when called with no name."""
    loop, session = mcp_session
    result = loop.run_until_complete(
        session.call_tool("describe_tools", arguments={})
    )
    data = json.loads(result.content[0].text)

    assert data["tool_count"] == 48
    assert isinstance(data["tools"], list)
    assert all("name" in t for t in data["tools"])


def test_e2e_describe_tools_single(
    mcp_session: tuple[asyncio.AbstractEventLoop, Any],
) -> None:
    """Verify describe_tools returns detail for a specific tool."""
    loop, session = mcp_session
    result = loop.run_until_complete(
        session.call_tool("describe_tools", arguments={"name": "meraki_vlan"})
    )
    data = json.loads(result.content[0].text)

    assert data["name"] == "meraki_vlan"
    assert data["canonical_key"] == "vlan_id"
    assert "inputSchema" in data


def test_e2e_describe_tools_unknown_name(
    mcp_session: tuple[asyncio.AbstractEventLoop, Any],
) -> None:
    """Verify describe_tools returns error for nonexistent tool name."""
    loop, session = mcp_session
    result = loop.run_until_complete(
        session.call_tool("describe_tools", arguments={"name": "nope"})
    )
    data = json.loads(result.content[0].text)

    assert "error" in data


# ---------------------------------------------------------------------------
# CLI: --mode=live without MERAKI_API_KEY
# ---------------------------------------------------------------------------

def test_live_mode_without_key_exits() -> None:
    """Verify --mode=live exits with code 1 when MERAKI_API_KEY is unset."""
    env = {k: v for k, v in os.environ.items() if k != "MERAKI_API_KEY"}
    result = subprocess.run(
        [sys.executable, "-m", "meraki_rm_sdk.mcp.server", "--mode=live"],
        capture_output=True,
        text=True,
        timeout=10,
        env=env,
    )

    assert result.returncode == 1
    assert "MERAKI_API_KEY" in result.stderr
