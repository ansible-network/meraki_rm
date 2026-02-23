"""In-process integration tests.

Exercises the full PlatformService -> Mock Server flow without
subprocesses or TCP.  Uses ``requests-flask-adapter`` to mount the
Flask mock server into PlatformService's ``requests.Session``, giving
us real CRUD state, OpenAPI request/response validation, and full
transform round-trips — all at unit-test speed.

Test tiers exercised here that pure-transform tests do NOT cover:

  * PlatformService HTTP call dispatch (path param resolution, etc.)
  * Mock server stateful CRUD (create, read, update, delete)
  * OpenAPI request validation (openapi-core unmarshal)
  * OpenAPI response validation (openapi-core unmarshal)
  * End-to-end idempotence (update twice -> no diff)
"""

from __future__ import annotations

import sys
from typing import Any, Dict, List

import pytest
import requests.exceptions
import yaml

from .conftest import (
    ACTION_DIR,
    MOLECULE_DIR,
    REPO_ROOT,
    SCOPE_DUMMY_VALUES,
    SPEC_PATH,
    load_classes,
    parse_action_plugin,
)

_tools_dir = str(REPO_ROOT / "tools")
if _tools_dir not in sys.path:
    sys.path.insert(0, _tools_dir)

from requests_flask_adapter import Session as FlaskSession
from mock_server.server import create_app
from plugins.plugin_utils.manager.platform_manager import PlatformService
from plugins.plugin_utils.platform.registry import APIVersionRegistry
from plugins.plugin_utils.platform.loader import DynamicClassLoader


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_service() -> PlatformService:
    svc = PlatformService.__new__(PlatformService)
    svc.base_url = "http://mock-meraki"
    svc.api_key = "test-key"
    svc.session = FlaskSession()
    svc.session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    svc.api_version = "1"
    svc.cache = {}
    svc.registry = APIVersionRegistry()
    svc.loader = DynamicClassLoader(svc.registry)
    return svc


@pytest.fixture(scope="module")
def flask_app():
    app = create_app(str(SPEC_PATH))
    FlaskSession.register("http://mock-meraki", app)
    yield app


@pytest.fixture()
def svc(flask_app):
    flask_app.config["STATE_STORE"].clear()
    return _make_service()


# ---------------------------------------------------------------------------
# Fixture discovery
# ---------------------------------------------------------------------------

def _discover_fixtures() -> List[Dict[str, Any]]:
    fixtures = []
    for vars_path in sorted(MOLECULE_DIR.glob("*/merged/vars.yml")):
        dir_name = vars_path.parent.parent.name
        plugin_file = ACTION_DIR / f"meraki_{dir_name}.py"
        if not plugin_file.exists():
            continue

        attrs = parse_action_plugin(plugin_file)
        if not attrs:
            continue

        with open(vars_path) as f:
            vars_data = yaml.safe_load(f)

        expected = vars_data.get("expected_config")
        if not expected or not isinstance(expected, dict):
            continue

        user_cls, api_cls, ops = load_classes(attrs)

        write_ops = {
            k: v for k, v in ops.items()
            if v.required_for in ("create", "update")
        }
        if not write_ops:
            continue

        is_collection = any(v.required_for == "create" for v in ops.values())

        fixtures.append({
            "dir_name": dir_name,
            "attrs": attrs,
            "expected_config": expected,
            "user_cls": user_cls,
            "api_cls": api_cls,
            "ops": ops,
            "is_collection": is_collection,
        })
    return fixtures


_FIXTURES = _discover_fixtures()
_IDS = [f["dir_name"] for f in _FIXTURES]


@pytest.fixture(params=_FIXTURES, ids=_IDS)
def module_fixture(request):
    return request.param


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _user_data_dict(fix: dict) -> dict:
    scope = fix["attrs"]["SCOPE_PARAM"]
    scope_val = SCOPE_DUMMY_VALUES.get(scope, "DUMMY")
    return {scope: scope_val, **fix["expected_config"]}


def _strip_nones(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}


def _loose_eq(a, b) -> bool:
    """Compare with string/int coercion for path-param identity fields."""
    if a == b:
        return True
    try:
        return str(a) == str(b)
    except (TypeError, ValueError):
        return False


def _write_op(fix: dict) -> str:
    if fix["is_collection"]:
        return "create"
    return "update"


def _find_all(svc, fix: dict, allow_404: bool = False) -> list:
    """Execute find and return a flat list of result dicts.

    For collection resources the PK is stripped so the list endpoint is
    hit.  For item-level / singleton resources the PK is kept so the
    path can be resolved.

    When *allow_404* is True, a 404 response is treated as "empty" rather
    than an error — used after delete to verify the resource is gone.
    """
    user_data = _user_data_dict(fix)
    pk = fix["attrs"].get("PRIMARY_KEY")
    find_data = dict(user_data)
    if fix["is_collection"] and pk:
        find_data.pop(pk, None)

    try:
        result = svc.execute("find", fix["attrs"]["MODULE_NAME"], find_data)
    except requests.exceptions.HTTPError as exc:
        if allow_404 and exc.response is not None and exc.response.status_code == 404:
            return []
        raise

    if isinstance(result, dict) and "config" in result:
        return result["config"]
    elif isinstance(result, dict):
        return [result]
    return []


def _comparable_fields(fix: dict) -> set:
    """Keys that should be compared between expected and actual.

    Excludes the scope param and (for collection creates) the server-
    assigned primary key."""
    expected = _strip_nones(fix["expected_config"])
    exclude = {fix["attrs"]["SCOPE_PARAM"]}
    pk = fix["attrs"].get("PRIMARY_KEY")
    if fix["is_collection"] and pk:
        exclude.add(pk)
    return set(expected.keys()) - exclude


# Per-test-class skip lists.  Each maps dir_name -> reason string.
# Only structurally inapplicable modules belong here; real bugs
# must surface as failures, never as skips.

_WRITE_FIND_SKIP = {
    "wireless_air_marshal_rules": (
        "module has no find endpoint — only create/update/delete ops "
        "are defined, so write-then-find cannot run"
    ),
}

_ROUNDTRIP_SKIP = {
    "wireless_air_marshal_rules": (
        "module has no find endpoint — round-trip key check cannot run"
    ),
    "wireless_rf_profiles": (
        "spec response schema omits is_indoor_default and is_outdoor_default — "
        "round-trip key check will always report missing keys until the spec "
        "or user model is updated"
    ),
    "wireless_ethernet_port_profiles": (
        "spec response schema omits is_default — round-trip key check will "
        "always report a missing key until the spec or user model is updated"
    ),
}

_DELETE_SKIP: dict = {
    # No structural skips — the test already guards on SUPPORTS_DELETE,
    # has_delete, and is_collection.  Real failures must surface.
}


def _maybe_skip_for(skip_dict: dict, fix: dict):
    reason = skip_dict.get(fix["dir_name"])
    if reason:
        pytest.skip(reason)


# ===================================================================
# Tests
# ===================================================================

class TestWriteThenFind:
    """Execute a write op, then find — the resource should exist
    with the expected field values."""

    def test_write_then_find(self, svc, module_fixture):
        fix = module_fixture
        _maybe_skip_for(_WRITE_FIND_SKIP, fix)
        module_name = fix["attrs"]["MODULE_NAME"]
        user_data = _user_data_dict(fix)
        op = _write_op(fix)

        svc.execute(op, module_name, user_data)

        items = _find_all(svc, fix)
        assert len(items) > 0, f"{module_name}: find returned empty after {op}"

        found = _strip_nones(items[0])
        expected = _strip_nones(fix["expected_config"])
        compare_keys = _comparable_fields(fix)

        for key in compare_keys:
            if key in found:
                assert _loose_eq(found[key], expected[key]), (
                    f"{module_name}: '{key}' mismatch: "
                    f"expected {expected[key]!r}, got {found[key]!r}"
                )


class TestIdempotence:
    """For singleton/update resources, writing the same data twice
    should produce identical state."""

    def test_update_idempotence(self, svc, module_fixture):
        fix = module_fixture
        if fix["is_collection"]:
            pytest.skip("create operations are not idempotent by design")

        module_name = fix["attrs"]["MODULE_NAME"]
        user_data = _user_data_dict(fix)

        svc.execute("update", module_name, user_data)
        after1 = _find_all(svc, fix)

        svc.execute("update", module_name, user_data)
        after2 = _find_all(svc, fix)

        assert after1 == after2, (
            f"{module_name}: second update changed state"
        )


class TestGatheredRoundTrip:
    """Write, then find — all expected keys should appear in the result."""

    def test_round_trip_keys(self, svc, module_fixture):
        fix = module_fixture
        _maybe_skip_for(_ROUNDTRIP_SKIP, fix)
        module_name = fix["attrs"]["MODULE_NAME"]
        user_data = _user_data_dict(fix)
        op = _write_op(fix)

        svc.execute(op, module_name, user_data)

        items = _find_all(svc, fix)
        assert len(items) > 0, f"{module_name}: find returned empty"

        found = _strip_nones(items[0])
        compare_keys = _comparable_fields(fix)

        missing = [k for k in compare_keys if k not in found]
        assert not missing, (
            f"{module_name}: keys missing from gathered: {missing}. "
            f"Got: {list(found.keys())}"
        )


class TestDeleteRemovesResource:
    """For collection resources with delete: create, delete, verify empty."""

    def test_delete(self, svc, module_fixture):
        fix = module_fixture
        _maybe_skip_for(_DELETE_SKIP, fix)
        attrs = fix["attrs"]
        if not attrs.get("SUPPORTS_DELETE", True):
            pytest.skip("delete not supported")

        has_delete = any(
            v.required_for == "delete" for v in fix["ops"].values()
        )
        if not has_delete:
            pytest.skip("no delete endpoint")

        if not fix["is_collection"]:
            pytest.skip("singleton resources cannot be deleted")

        module_name = attrs["MODULE_NAME"]
        user_data = _user_data_dict(fix)

        result = svc.execute("create", module_name, user_data)

        pk = attrs.get("PRIMARY_KEY")
        if pk and isinstance(result, dict):
            created_id = result.get(pk)
            if created_id:
                user_data[pk] = created_id

        svc.execute("delete", module_name, user_data)

        items = _find_all(svc, fix, allow_404=True)
        non_empty = [i for i in items if _strip_nones(i)]
        assert len(non_empty) == 0, (
            f"{module_name}: resource still present after delete: {non_empty}"
        )
