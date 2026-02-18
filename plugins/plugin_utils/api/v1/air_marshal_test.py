"""Colocated tests for APIAirMarshal_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import air_marshal as air_marshal_api
from ...user_models import air_marshal as air_marshal_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = air_marshal_api.APIAirMarshal_v1(
            ruleId='ruleId_val',
            type='type_val',
            match={'enabled': True},
            defaultPolicy='defaultPolicy_val',
            ssid='ssid_val',
            bssids=[{'key': 'value'}],
            channels=24,
            firstSeen=24,
            lastSeen=24,
            createdAt='createdAt_val',
            updatedAt='updatedAt_val',
        )
        user = api.to_ansible(_ctx())

        assert user.rule_id == api.ruleId
        assert user.type == api.type
        assert user.match == api.match
        assert user.default_policy == api.defaultPolicy
        assert user.ssid == api.ssid
        assert user.bssids == api.bssids
        assert user.channels == api.channels
        assert user.first_seen == api.firstSeen
        assert user.last_seen == api.lastSeen
        assert user.created_at == api.createdAt
        assert user.updated_at == api.updatedAt


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = air_marshal_user.UserAirMarshal(
            rule_id='rule_id_val',
            type='type_val',
            match={'enabled': True},
            default_policy='default_policy_val',
            ssid='ssid_val',
            bssids=[{'key': 'value'}],
            channels=24,
            first_seen=24,
            last_seen=24,
            created_at='created_at_val',
            updated_at='updated_at_val',
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.rule_id == original.rule_id
        assert roundtripped.type == original.type
        assert roundtripped.match == original.match
        assert roundtripped.default_policy == original.default_policy
        assert roundtripped.ssid == original.ssid
        assert roundtripped.bssids == original.bssids
        assert roundtripped.channels == original.channels
        assert roundtripped.first_seen == original.first_seen
        assert roundtripped.last_seen == original.last_seen
        assert roundtripped.created_at == original.created_at
        assert roundtripped.updated_at == original.updated_at


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = air_marshal_api.APIAirMarshal_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = air_marshal_api.APIAirMarshal_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

