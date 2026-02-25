"""Discover User Model dataclasses and generate MCP tool definitions.

Scans the ``user_models/`` package for dataclass subclasses of
``BaseTransformMixin``, reads their class-level metadata and field
schemas, and produces ready-to-serve MCP tool definitions.
"""

from __future__ import annotations

import dataclasses
import importlib
import pkgutil
from pathlib import Path
from typing import Any, Dict, List

from .schema import dataclass_to_json_schema


def _detect_prefix() -> str:
    """Derive the import prefix for sibling packages.

    Works under all install modes:
      - Collection: ansible_collections.cisco.meraki_rm.plugins.plugin_utils
      - Dev:        plugins.plugin_utils
      - SDK pip:    meraki_rm_sdk
    """
    parts = __name__.split(".")
    # __name__ = <prefix>.mcp.introspect → strip last two
    return ".".join(parts[:-2])


def _find_user_model_modules() -> List[str]:
    """Discover user model modules by scanning the user_models directory."""
    prefix = _detect_prefix()
    models_pkg = f"{prefix}.user_models"

    try:
        pkg = importlib.import_module(models_pkg)
    except ImportError:
        return []

    pkg_path = getattr(pkg, "__path__", None)
    if not pkg_path:
        return []

    modules = []
    for importer, name, is_pkg in pkgutil.iter_modules(pkg_path):
        if name.startswith("_") or name.endswith("_test"):
            continue
        modules.append(f"{models_pkg}.{name}")

    return sorted(modules)


def _load_user_model_class(module_name: str):
    """Import a module and find the User* dataclass."""
    mod = importlib.import_module(module_name)

    for attr_name in dir(mod):
        if not attr_name.startswith("User"):
            continue
        cls = getattr(mod, attr_name)
        if dataclasses.is_dataclass(cls) and hasattr(cls, "MODULE_NAME"):
            return cls

    return None


def _module_name_to_ansible_fqcn(module_name: str) -> str:
    """Derive the Ansible FQCN module name from the User Model's MODULE_NAME.

    Maps internal names like 'vlan' to 'cisco.meraki_rm.meraki_appliance_vlans'.
    Falls back to the user model module leaf name.
    """
    leaf = module_name.rsplit(".", 1)[-1]
    return leaf


def _build_tool_description(cls) -> str:
    """Build a human-readable tool description from model metadata."""
    doc = cls.__doc__ or ""
    first_line = doc.strip().split("\n")[0] if doc.strip() else ""

    parts = [f"Manage Meraki {cls.MODULE_NAME.replace('_', ' ')} resources."]

    if cls.CANONICAL_KEY:
        parts.append(f"Canonical key: {cls.CANONICAL_KEY}")
    if cls.SYSTEM_KEY:
        parts.append(f"System key: {cls.SYSTEM_KEY}")

    scope = cls.SCOPE_PARAM or "network_id"
    parts.append(f"Scope: {scope}")

    return " ".join(parts)


def build_tool_definitions() -> List[Dict[str, Any]]:
    """Discover all User Models and generate MCP tool definitions.

    Returns a list of dicts, each with:
      - name: tool name (module name)
      - description: human-readable description
      - inputSchema: JSON Schema for tool input
      - _metadata: internal metadata dict (scope_param, canonical_key, etc.)
    """
    tools = []

    for module_path in _find_user_model_modules():
        cls = _load_user_model_class(module_path)
        if cls is None or cls.MODULE_NAME is None:
            continue

        scope_param = cls.SCOPE_PARAM or "network_id"
        valid_states = sorted(cls.VALID_STATES) if cls.VALID_STATES else [
            "merged", "replaced", "overridden", "deleted", "gathered"
        ]

        config_schema = dataclass_to_json_schema(
            cls, exclude_fields={scope_param}
        )

        input_schema: Dict[str, Any] = {
            "type": "object",
            "properties": {
                "state": {
                    "type": "string",
                    "enum": valid_states,
                    "default": "merged",
                    "description": "Resource module state.",
                },
                scope_param: {
                    "type": "string",
                    "description": f"Target {scope_param.replace('_', ' ')}.",
                },
                "config": {
                    "type": "array",
                    "items": config_schema,
                    "description": "List of resource configurations.",
                },
            },
            "required": [scope_param],
        }

        tool_name = f"meraki_{cls.MODULE_NAME}"

        tools.append({
            "name": tool_name,
            "description": _build_tool_description(cls),
            "inputSchema": input_schema,
            "_metadata": {
                "module_name": cls.MODULE_NAME,
                "scope_param": scope_param,
                "canonical_key": cls.CANONICAL_KEY,
                "system_key": cls.SYSTEM_KEY,
                "supports_delete": cls.SUPPORTS_DELETE,
                "valid_states": valid_states,
                "user_model_class": cls,
            },
        })

    return tools
