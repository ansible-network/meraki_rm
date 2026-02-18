"""Colocated tests for APIVpn_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import vpn as vpn_api
from ...user_models import vpn as vpn_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = vpn_api.APIVpn_v1(
            mode='mode_val',
            hubs=[{'key': 'value'}],
            subnets=[{'key': 'value'}],
            subnet={'enabled': True},
            enabled=True,
            asNumber=24,
            ibgpHoldTimer=24,
            neighbors=[{'key': 'value'}],
        )
        user = api.to_ansible(_ctx())

        assert user.mode == api.mode
        assert user.hubs == api.hubs
        assert user.subnets == api.subnets
        assert user.subnet == api.subnet
        assert user.enabled == api.enabled
        assert user.as_number == api.asNumber
        assert user.ibgp_hold_timer == api.ibgpHoldTimer
        assert user.neighbors == api.neighbors


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = vpn_user.UserVpn(
            mode='mode_val',
            hubs=[{'key': 'value'}],
            subnets=[{'key': 'value'}],
            subnet={'enabled': True},
            enabled=True,
            as_number=24,
            ibgp_hold_timer=24,
            neighbors=[{'key': 'value'}],
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.mode == original.mode
        assert roundtripped.hubs == original.hubs
        assert roundtripped.subnets == original.subnets
        assert roundtripped.subnet == original.subnet
        assert roundtripped.enabled == original.enabled
        assert roundtripped.as_number == original.as_number
        assert roundtripped.ibgp_hold_timer == original.ibgp_hold_timer
        assert roundtripped.neighbors == original.neighbors


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = vpn_api.APIVpn_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = vpn_api.APIVpn_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

