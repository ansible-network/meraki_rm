"""Shared discovery helpers for unit tests.

Provides functions to parse action plugin metadata and load the
corresponding User Model, API Model, and endpoint operations — without
importing from Ansible-scanned plugin directories.
"""

from __future__ import annotations

import importlib
import re
from dataclasses import fields as dc_fields
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
ACTION_DIR = REPO_ROOT / "plugins" / "action"
MOLECULE_DIR = REPO_ROOT / "extensions" / "molecule"
SPEC_PATH = REPO_ROOT / "spec3.json"

# ---------------------------------------------------------------------------
# Regex patterns for extracting class attributes from action plugin source
# ---------------------------------------------------------------------------

_ATTR_RE = {
    attr: re.compile(rf"{attr}\s*=\s*['\"](.+?)['\"]")
    for attr in ("MODULE_NAME", "SCOPE_PARAM", "USER_MODEL", "CANONICAL_KEY")
}
_BOOL_RE = re.compile(r"SUPPORTS_DELETE\s*=\s*(True|False)")
_STATES_RE = re.compile(
    r"VALID_STATES\s*=\s*frozenset\(\{(.+?)\}\)", re.DOTALL,
)

_ALL_STATES = frozenset({"merged", "replaced", "overridden", "deleted", "gathered"})

_DEFAULTS: Dict[str, Any] = {
    "SCOPE_PARAM": "network_id",
    "CANONICAL_KEY": None,
    "SUPPORTS_DELETE": True,
    "VALID_STATES": _ALL_STATES,
}

SCOPE_DUMMY_VALUES = {
    "network_id": "N_123456789012345678",
    "organization_id": "123456",
    "serial": "Q2XX-XXXX-XXXX",
}


def parse_action_plugin(path: Path) -> Optional[Dict[str, Any]]:
    """Extract class-level attributes from one action plugin file."""
    text = path.read_text()
    attrs: Dict[str, Any] = {}

    for attr, pattern in _ATTR_RE.items():
        m = pattern.search(text)
        if m:
            attrs[attr] = m.group(1)

    m = _BOOL_RE.search(text)
    if m:
        attrs["SUPPORTS_DELETE"] = m.group(1) == "True"

    m = _STATES_RE.search(text)
    if m:
        raw = m.group(1)
        attrs["VALID_STATES"] = frozenset(
            s.strip().strip("'\"") for s in raw.split(",") if s.strip()
        )

    for k, v in _DEFAULTS.items():
        attrs.setdefault(k, v)

    if "MODULE_NAME" not in attrs or "USER_MODEL" not in attrs:
        return None

    attrs["_file"] = path.name
    return attrs


def load_classes(
    attrs: Dict[str, Any],
) -> Tuple[type, type, Dict]:
    """Import user model -> derive API class -> get endpoint ops."""
    dotted = attrs["USER_MODEL"]
    stripped = dotted.replace("plugins.", "", 1)
    module_path, class_name = stripped.rsplit(".", 1)

    mod = importlib.import_module(module_path)
    user_cls = getattr(mod, class_name)
    api_cls = user_cls._get_api_class()

    ops = {}
    if hasattr(api_cls, "get_endpoint_operations"):
        ops = api_cls.get_endpoint_operations()

    return user_cls, api_cls, ops


def discover_action_plugins() -> List[Dict[str, Any]]:
    """Find and parse all resource action plugins (excluding meraki_facts)."""
    plugins: List[Dict[str, Any]] = []
    for p in sorted(ACTION_DIR.glob("meraki_*.py")):
        if p.name == "meraki_facts.py":
            continue
        parsed = parse_action_plugin(p)
        if parsed:
            plugins.append(parsed)
    return plugins
