"""Full-flow spec validation tests.

Reads Molecule vars.yml fixtures and runs them through the entire
transform pipeline, then validates at every stage — all in pure Python,
no mock server needed.

Four validation stages per module:

  0. Argspec  – vars.yml validated through Ansible's ArgumentSpecValidator
               (types, choices, required_if, mutually_exclusive, etc.)

  1. Outbound – vars.yml -> UserModel -> APIModel -> validate() constraints
               -> request body -> jsonschema.validate() against spec schema

  2. Inbound  – simulated spec-compliant response -> _safe_construct()
               -> .to_ansible() -> compare against original expected_config

  3. Output argspec – the to_ansible() result fed back through the argspec,
               ensuring returned data also conforms (types, choices, etc.)
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, fields as dc_fields, is_dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import jsonschema
import pytest
import yaml
from ansible.module_utils.common.arg_spec import ArgumentSpecValidator

from .conftest import (
    ACTION_DIR,
    MOLECULE_DIR,
    REPO_ROOT,
    SCOPE_DUMMY_VALUES,
    SPEC_PATH,
    discover_action_plugins,
    load_classes,
    parse_action_plugin,
)

# ---------------------------------------------------------------------------
# Spec + schema helpers
# ---------------------------------------------------------------------------

_tools_dir = str(REPO_ROOT / "tools")
if _tools_dir not in sys.path:
    sys.path.insert(0, _tools_dir)

from mock_server.response_generator import merge_with_schema_defaults
from mock_server.spec_loader import SpecLoader

MODULES_DIR = REPO_ROOT / "plugins" / "modules"

_SPEC: Optional[SpecLoader] = None


def _get_spec() -> SpecLoader:
    global _SPEC
    if _SPEC is None:
        _SPEC = SpecLoader(str(SPEC_PATH))
    return _SPEC


def _load_module_argspec(dir_name: str) -> Optional[dict]:
    """Parse a module's DOCUMENTATION string into an ArgumentSpecValidator-ready dict."""
    module_file = MODULES_DIR / f"meraki_{dir_name}.py"
    if not module_file.exists():
        return None

    text = module_file.read_text()
    m = re.search(
        r"DOCUMENTATION\s*=\s*r?'''(.+?)'''",
        text,
        re.DOTALL,
    )
    if not m:
        m = re.search(
            r'DOCUMENTATION\s*=\s*r?"""(.+?)"""',
            text,
            re.DOTALL,
        )
    if not m:
        return None

    try:
        doc = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None

    return doc.get("options")


def _safe_construct(cls: type, data: dict) -> Any:
    """Construct a dataclass filtering out unknown keys (mirrors PlatformManager)."""
    if is_dataclass(cls):
        valid = {f.name for f in dc_fields(cls)}
        data = {k: v for k, v in data.items() if k in valid}
    return cls(**data)


def _build_request_body(api_data_dict: dict, user_data_dict: dict, endpoint_op) -> dict:
    """Build the HTTP request body — mirrors _execute_operations logic."""
    request_data = {}
    for field_name in endpoint_op.fields:
        if field_name in api_data_dict and api_data_dict[field_name] is not None:
            request_data[field_name] = api_data_dict[field_name]
        elif field_name in user_data_dict and user_data_dict[field_name] is not None:
            request_data[field_name] = user_data_dict[field_name]
    return request_data


# ---------------------------------------------------------------------------
# Discovery: vars.yml -> action plugin -> classes + endpoint ops
# ---------------------------------------------------------------------------

def _discover_fixtures(state: str = "merged") -> List[Dict[str, Any]]:
    """Find all {state}/vars.yml files and pair with their action plugin metadata."""
    fixtures = []

    for vars_path in sorted(MOLECULE_DIR.glob(f"*/{state}/vars.yml")):
        dir_name = vars_path.parent.parent.name
        plugin_file = ACTION_DIR / f"meraki_{dir_name}.py"

        if not plugin_file.exists():
            continue

        attrs = parse_action_plugin(plugin_file)
        if not attrs:
            continue

        with open(vars_path) as f:
            vars_data = yaml.safe_load(f)

        expected_config = vars_data.get("expected_config")
        if not expected_config or not isinstance(expected_config, dict):
            continue

        fixtures.append({
            "state": state,
            "dir_name": dir_name,
            "module_name": attrs["MODULE_NAME"],
            "attrs": attrs,
            "expected_config": expected_config,
        })

    return fixtures


_FIXTURES = _discover_fixtures("merged") + _discover_fixtures("gathered")
_FIX_IDS = [f["dir_name"] + "/" + f["state"] for f in _FIXTURES]


@pytest.fixture(params=_FIXTURES, ids=_FIX_IDS)
def fixture(request):
    fix = request.param
    attrs = fix["attrs"]
    user_cls, api_cls, ops = load_classes(attrs)
    return attrs, user_cls, api_cls, ops, fix["expected_config"], fix["dir_name"]


# ===================================================================
# 0. Argspec: vars.yml validated through Ansible's ArgumentSpecValidator
# ===================================================================

class TestArgspecValidation:
    """expected_config must pass Ansible's own argument spec validation."""

    def test_argspec(self, fixture):
        attrs, user_cls, api_cls, ops, expected_config, dir_name = fixture
        options = _load_module_argspec(dir_name)
        if options is None:
            pytest.skip(f"{attrs['MODULE_NAME']}: no DOCUMENTATION options found")

        scope = attrs["SCOPE_PARAM"]
        scope_val = SCOPE_DUMMY_VALUES.get(scope, "DUMMY")

        module_params = {
            scope: scope_val,
            "state": "merged",
            "config": [expected_config],
        }

        validator = ArgumentSpecValidator(options)
        result = validator.validate(module_params)

        if result.error_messages:
            pytest.fail(
                f"{attrs['MODULE_NAME']}: Ansible argspec validation failed:\n"
                + "\n".join(f"  - {e}" for e in result.error_messages)
            )



# ===================================================================
# 1. Outbound: request body matches spec + API model constraints
# ===================================================================

class TestRequestMatchesSpec:
    """Transformed request body must validate against the OpenAPI spec."""

    @staticmethod
    def _find_write_op(ops: dict):
        for name in ("update", "create"):
            if name in ops:
                return ops[name]
        for op in ops.values():
            if op.required_for in ("update", "create"):
                return op
        return None

    def test_request_body_valid(self, fixture):
        attrs, user_cls, api_cls, ops, expected_config, dir_name = fixture
        spec = _get_spec()

        write_op = self._find_write_op(ops)
        if write_op is None:
            pytest.skip(f"{attrs['MODULE_NAME']}: no write endpoint operation")

        if not write_op.fields:
            pytest.skip(f"{attrs['MODULE_NAME']}: write op has no fields")

        request_schema = spec.get_request_schema(
            write_op.path, write_op.method.lower(),
        )
        if request_schema is None:
            pytest.skip(
                f"{attrs['MODULE_NAME']}: no request schema in spec for "
                f"{write_op.method} {write_op.path}"
            )

        scope = attrs["SCOPE_PARAM"]
        scope_val = SCOPE_DUMMY_VALUES.get(scope, "DUMMY")
        ctx = {"manager": None, "cache": {}}

        user_data = user_cls(**{scope: scope_val, **expected_config})
        api_data = user_data.to_api(ctx)

        try:
            api_data.validate()
        except ValueError as exc:
            pytest.fail(
                f"{attrs['MODULE_NAME']}: API model constraint violation: {exc}"
            )

        api_data_dict = asdict(api_data) if is_dataclass(api_data) else api_data
        user_data_dict = asdict(user_data) if is_dataclass(user_data) else user_data

        request_body = _build_request_body(api_data_dict, user_data_dict, write_op)

        try:
            jsonschema.validate(instance=request_body, schema=request_schema)
        except jsonschema.ValidationError as exc:
            pytest.fail(
                f"{attrs['MODULE_NAME']}: request body fails spec validation "
                f"for {write_op.method} {write_op.path}\n"
                f"Body: {json.dumps(request_body, indent=2, default=str)}\n"
                f"Error: {exc.message}\n"
                f"Path: {list(exc.absolute_path)}"
            )


# ===================================================================
# 2. Inbound: spec response -> _safe_construct -> to_ansible roundtrip
# ===================================================================

class TestResponseRoundtrip:
    """A spec-shaped response must survive _safe_construct -> to_ansible,
    preserve every field from the original expected_config, and the
    resulting user-facing dataclass must pass the module's argspec."""

    @staticmethod
    def _find_write_op(ops: dict):
        for name in ("update", "create"):
            if name in ops:
                return ops[name]
        for op in ops.values():
            if op.required_for in ("update", "create"):
                return op
        return None

    def test_response_roundtrip(self, fixture):
        attrs, user_cls, api_cls, ops, expected_config, dir_name = fixture
        spec = _get_spec()

        write_op = self._find_write_op(ops)
        if write_op is None:
            pytest.skip(f"{attrs['MODULE_NAME']}: no write endpoint operation")

        scope = attrs["SCOPE_PARAM"]
        scope_val = SCOPE_DUMMY_VALUES.get(scope, "DUMMY")
        ctx = {"manager": None, "cache": {}}

        user_data = user_cls(**{scope: scope_val, **expected_config})
        api_data = user_data.to_api(ctx)
        api_data_dict = asdict(api_data) if is_dataclass(api_data) else api_data
        user_data_dict = asdict(user_data) if is_dataclass(user_data) else user_data

        request_body = _build_request_body(api_data_dict, user_data_dict, write_op)

        stored_resource = {
            k: v for k, v in api_data_dict.items() if v is not None
        }
        stored_resource.update(request_body)

        resp_schema = spec.get_response_schema(
            write_op.path, write_op.method.lower(),
        )
        if resp_schema is not None:
            simulated_response = merge_with_schema_defaults(
                stored_resource, resp_schema,
            )
        else:
            simulated_response = dict(stored_resource)

        api_inst = _safe_construct(api_cls, simulated_response)
        user_result = api_inst.to_ansible(ctx)
        result_dict = asdict(user_result) if is_dataclass(user_result) else user_result

        result_clean = {k: v for k, v in result_dict.items() if v is not None}

        missing = {}
        for key, expected_val in expected_config.items():
            actual_val = result_clean.get(key)
            if actual_val != expected_val:
                missing[key] = {"expected": expected_val, "got": actual_val}

        assert not missing, (
            f"{attrs['MODULE_NAME']}: response roundtrip lost fields: {missing}"
        )

    def test_output_passes_argspec(self, fixture):
        """The to_ansible() output must also pass the module's argspec."""
        attrs, user_cls, api_cls, ops, expected_config, dir_name = fixture
        spec = _get_spec()

        write_op = self._find_write_op(ops)
        if write_op is None:
            pytest.skip(f"{attrs['MODULE_NAME']}: no write endpoint operation")

        options = _load_module_argspec(dir_name)
        if options is None:
            pytest.skip(f"{attrs['MODULE_NAME']}: no DOCUMENTATION options found")

        scope = attrs["SCOPE_PARAM"]
        scope_val = SCOPE_DUMMY_VALUES.get(scope, "DUMMY")
        ctx = {"manager": None, "cache": {}}

        user_data = user_cls(**{scope: scope_val, **expected_config})
        api_data = user_data.to_api(ctx)
        api_data_dict = asdict(api_data) if is_dataclass(api_data) else api_data
        user_data_dict = asdict(user_data) if is_dataclass(user_data) else user_data
        request_body = _build_request_body(api_data_dict, user_data_dict, write_op)

        stored_resource = {
            k: v for k, v in api_data_dict.items() if v is not None
        }
        stored_resource.update(request_body)

        resp_schema = spec.get_response_schema(
            write_op.path, write_op.method.lower(),
        )
        if resp_schema is not None:
            simulated_response = merge_with_schema_defaults(
                stored_resource, resp_schema,
            )
        else:
            simulated_response = dict(stored_resource)

        api_inst = _safe_construct(api_cls, simulated_response)
        user_result = api_inst.to_ansible(ctx)
        result_dict = asdict(user_result) if is_dataclass(user_result) else user_result
        result_clean = {k: v for k, v in result_dict.items() if v is not None}

        # Feed the output back through the argspec as if it were module input
        module_params = {
            scope: scope_val,
            "state": "merged",
            "config": [result_clean],
        }

        validator = ArgumentSpecValidator(options)
        result = validator.validate(module_params)

        if result.error_messages:
            pytest.fail(
                f"{attrs['MODULE_NAME']}: output fails argspec validation:\n"
                + "\n".join(f"  - {e}" for e in result.error_messages)
            )
