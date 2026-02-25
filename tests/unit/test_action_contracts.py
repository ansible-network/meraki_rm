"""Contract tests for action plugin ↔ endpoint operation wiring.

These catch the class of bugs that transform-layer unit tests miss:
the glue between the action plugin state machine and the endpoint
operations that actually execute HTTP calls.

No mock server, no Ansible runtime — pure Python import + assert.

Validated contracts per module:

  1. State routing     – every supported state resolves to endpoint ops
  2. Field mapping     – _field_mapping keys/values match real dataclass fields
  3. Endpoint fields   – operation field lists reference real API class fields
  4. Identity fields   – SCOPE_PARAM and CANONICAL_KEY exist on the user model
  5. Data roundtrip    – User → API → User preserves all mapped fields
"""

from __future__ import annotations

from dataclasses import fields as dc_fields

import pytest

from .conftest import discover_action_plugins, load_classes

# ---------------------------------------------------------------------------
# Fixture: parametrised over every resource action plugin
# ---------------------------------------------------------------------------

_PLUGINS = discover_action_plugins()
_IDS = [p["MODULE_NAME"] for p in _PLUGINS]


@pytest.fixture(params=_PLUGINS, ids=_IDS)
def plugin(request):
    attrs = request.param
    user_cls, api_cls, ops = load_classes(attrs)
    return attrs, user_cls, api_cls, ops


# ===================================================================
# 1. State → operation routing
# ===================================================================

class TestStateRouting:
    """Every supported state must resolve to at least one endpoint operation.

    The action plugin state machine maps states to operation names:
        merged    → 'update'  (via _update_resource, required_for='update')
        replaced  → 'replace' (via _update_resource, required_for='update')
        overridden→ 'override'(via _update_resource, required_for='update')
        deleted   → 'delete'  (via _delete_resource, required_for='delete')
        gathered  → 'find'    (via _find_resource,   required_for='find')

    PlatformManager.execute() routes update/replace/override through
    _update_resource(), which always filters by required_for='update'.
    """

    @staticmethod
    def _ops_for(ops, required_for):
        return {
            n: o for n, o in ops.items()
            if o.required_for is None or o.required_for == required_for
        }

    def test_gathered_has_find_ops(self, plugin):
        attrs, _, _, ops = plugin
        if "gathered" not in attrs["VALID_STATES"]:
            pytest.skip("gathered not in VALID_STATES")
        found = self._ops_for(ops, "find")
        assert found, (
            f"{attrs['MODULE_NAME']}: 'gathered' state needs endpoint ops "
            f"with required_for='find'. Have: "
            f"{[(n, o.required_for) for n, o in ops.items()]}"
        )

    def test_merged_has_update_ops(self, plugin):
        attrs, _, _, ops = plugin
        if "merged" not in attrs["VALID_STATES"]:
            pytest.skip("merged not in VALID_STATES")
        found = self._ops_for(ops, "update")
        # Create-only resources (no PUT) may have merged for create path only
        if not found and attrs.get("CANONICAL_KEY"):
            found = self._ops_for(ops, "create")
        assert found, (
            f"{attrs['MODULE_NAME']}: 'merged' state needs endpoint ops "
            f"with required_for='update' (or 'create' if keyed). Have: "
            f"{[(n, o.required_for) for n, o in ops.items()]}"
        )

    def test_replaced_has_update_ops(self, plugin):
        attrs, _, _, ops = plugin
        if "replaced" not in attrs["VALID_STATES"]:
            pytest.skip("replaced not in VALID_STATES")
        found = self._ops_for(ops, "update")
        assert found, (
            f"{attrs['MODULE_NAME']}: 'replaced' routes through "
            f"_update_resource → required_for='update', but no ops match."
        )

    def test_deleted_has_delete_ops(self, plugin):
        attrs, _, _, ops = plugin
        if "deleted" not in attrs["VALID_STATES"]:
            pytest.skip("deleted not in VALID_STATES")
        if not attrs.get("SUPPORTS_DELETE", True):
            pytest.skip("SUPPORTS_DELETE=False")
        found = self._ops_for(ops, "delete")
        assert found, (
            f"{attrs['MODULE_NAME']}: 'deleted' state needs endpoint ops "
            f"with required_for='delete'. Have: "
            f"{[(n, o.required_for) for n, o in ops.items()]}"
        )

    def test_create_available_when_primary_key_set(self, plugin):
        """Keyed resources can create new items — needs a create endpoint."""
        attrs, _, _, ops = plugin
        if "merged" not in attrs["VALID_STATES"]:
            pytest.skip("merged not in VALID_STATES")
        if not attrs.get("CANONICAL_KEY"):
            pytest.skip("No CANONICAL_KEY — singleton resource")
        found = self._ops_for(ops, "create")
        assert found, (
            f"{attrs['MODULE_NAME']}: CANONICAL_KEY='{attrs['CANONICAL_KEY']}' "
            f"implies merged can create new items, but no endpoint op with "
            f"required_for='create' found."
        )


# ===================================================================
# 2. Identity / scope fields
# ===================================================================

class TestIdentityFields:
    """SCOPE_PARAM and CANONICAL_KEY must exist on the user model."""

    def test_scope_param_on_user_model(self, plugin):
        attrs, user_cls, _, _ = plugin
        user_fields = {f.name for f in dc_fields(user_cls)}
        assert attrs["SCOPE_PARAM"] in user_fields, (
            f"{attrs['MODULE_NAME']}: SCOPE_PARAM='{attrs['SCOPE_PARAM']}' "
            f"not in {user_cls.__name__} fields: {sorted(user_fields)}"
        )

    def test_primary_key_on_user_model(self, plugin):
        attrs, user_cls, _, _ = plugin
        pk = attrs.get("CANONICAL_KEY")
        if not pk:
            pytest.skip("No CANONICAL_KEY set")
        user_fields = {f.name for f in dc_fields(user_cls)}
        assert pk in user_fields, (
            f"{attrs['MODULE_NAME']}: CANONICAL_KEY='{pk}' not in "
            f"{user_cls.__name__} fields: {sorted(user_fields)}"
        )


# ===================================================================
# 3. Field mapping validity
# ===================================================================

class TestFieldMapping:
    """_field_mapping on both user and API classes must reference real fields."""

    def test_mapping_sources_exist_on_user_model(self, plugin):
        attrs, user_cls, _, _ = plugin
        mapping = getattr(user_cls, "_field_mapping", None) or {}
        user_fields = {f.name for f in dc_fields(user_cls)}
        missing = [k for k in mapping if k not in user_fields]
        assert not missing, (
            f"{attrs['MODULE_NAME']}: _field_mapping keys missing from "
            f"{user_cls.__name__}: {missing}"
        )

    def test_mapping_targets_exist_on_api_class(self, plugin):
        attrs, _, api_cls, _ = plugin
        mapping = getattr(api_cls, "_field_mapping", None) or {}
        api_fields = {f.name for f in dc_fields(api_cls)}
        missing = []
        for user_field, spec in mapping.items():
            target = spec if isinstance(spec, str) else spec.get("api_field", user_field)
            root = target.split(".")[0]
            if root not in api_fields:
                missing.append((user_field, target))
        assert not missing, (
            f"{attrs['MODULE_NAME']}: _field_mapping targets missing from "
            f"{api_cls.__name__}: {missing}. "
            f"API fields: {sorted(api_fields)}"
        )


# ===================================================================
# 4. Endpoint operation field lists
# ===================================================================

class TestEndpointFields:
    """Field names in endpoint operations must exist on the API dataclass."""

    def test_operation_fields_on_api_class(self, plugin):
        attrs, _, api_cls, ops = plugin
        api_fields = {f.name for f in dc_fields(api_cls)}
        bad = []
        for op_name, op in ops.items():
            for field_name in op.fields or []:
                root = field_name.split(".")[0]
                if root not in api_fields:
                    bad.append((op_name, field_name))
        assert not bad, (
            f"{attrs['MODULE_NAME']}: endpoint op fields not on "
            f"{api_cls.__name__}: {bad}. "
            f"API fields: {sorted(api_fields)}"
        )


# ===================================================================
# 5. Data roundtrip fidelity
# ===================================================================

class TestRoundtrip:
    """User → API → User must preserve every mapped field's value."""

    @staticmethod
    def _test_value(field_obj):
        """Generate a non-None value appropriate to the field's type hint."""
        ts = str(field_obj.type)
        if "bool" in ts:
            return True
        if "int" in ts:
            return 42
        if "float" in ts:
            return 3.14
        if "List" in ts:
            return ["sentinel"]
        if "Dict" in ts:
            return {"key": "sentinel"}
        return f"{field_obj.name}_val"

    def test_roundtrip(self, plugin):
        attrs, user_cls, _, _ = plugin
        mapping = getattr(user_cls, "_field_mapping", None) or {}
        field_lookup = {f.name: f for f in dc_fields(user_cls)}

        kwargs = {}
        for user_field in mapping:
            f = field_lookup.get(user_field)
            if f:
                kwargs[user_field] = self._test_value(f)

        ctx = {"manager": None, "cache": {}}
        original = user_cls(**kwargs)
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        for user_field in mapping:
            orig = getattr(original, user_field, None)
            got = getattr(roundtripped, user_field, None)
            assert got == orig, (
                f"{attrs['MODULE_NAME']}: roundtrip lost '{user_field}': "
                f"sent {orig!r}, got {got!r}"
            )
