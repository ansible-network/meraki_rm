"""Colocated tests for APIAdaptivePolicy_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import adaptive_policy as adaptive_policy_api
from ...user_models import adaptive_policy as adaptive_policy_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = adaptive_policy_api.APIAdaptivePolicy_v1(
            enabledNetworks=['item1', 'item2'],
            lastEntryRule='lastEntryRule_val',
        )
        user = api.to_ansible(_ctx())

        assert user.enabled_networks == api.enabledNetworks
        assert user.last_entry_rule == api.lastEntryRule


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = adaptive_policy_user.UserAdaptivePolicy(
            enabled_networks=['item1', 'item2'],
            last_entry_rule='last_entry_rule_val',
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.enabled_networks == original.enabled_networks
        assert roundtripped.last_entry_rule == original.last_entry_rule


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = adaptive_policy_api.APIAdaptivePolicy_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = adaptive_policy_api.APIAdaptivePolicy_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

