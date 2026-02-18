"""Colocated tests for APIPort_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import port as port_api
from ...user_models import port as port_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = port_api.APIPort_v1(
            number=24,
            enabled=True,
            type='type_val',
            vlan=24,
            allowedVlans='allowedVlans_val',
            accessPolicy='accessPolicy_val',
            dropUntaggedTraffic=True,
        )
        user = api.to_ansible(_ctx())

        assert user.port_id == api.number
        assert user.enabled == api.enabled
        assert user.type == api.type
        assert user.vlan == api.vlan
        assert user.allowed_vlans == api.allowedVlans
        assert user.access_policy == api.accessPolicy
        assert user.drop_untagged_traffic == api.dropUntaggedTraffic


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = port_user.UserPort(
            port_id='port_id_val',
            enabled=True,
            type='type_val',
            vlan=24,
            allowed_vlans='allowed_vlans_val',
            access_policy='access_policy_val',
            drop_untagged_traffic=True,
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.port_id == original.port_id
        assert roundtripped.enabled == original.enabled
        assert roundtripped.type == original.type
        assert roundtripped.vlan == original.vlan
        assert roundtripped.allowed_vlans == original.allowed_vlans
        assert roundtripped.access_policy == original.access_policy
        assert roundtripped.drop_untagged_traffic == original.drop_untagged_traffic


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = port_api.APIPort_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = port_api.APIPort_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

