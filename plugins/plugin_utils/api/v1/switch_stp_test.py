"""Colocated tests for APISwitchStp_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import switch_stp as switch_stp_api
from ...user_models import switch_stp as switch_stp_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = switch_stp_api.APISwitchStp_v1(
            rstpEnabled=True,
            stpBridgePriority=[{'key': 'value'}],
        )
        user = api.to_ansible(_ctx())

        assert user.rstp_enabled == api.rstpEnabled
        assert user.stp_bridge_priority == api.stpBridgePriority


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = switch_stp_user.UserSwitchStp(
            rstp_enabled=True,
            stp_bridge_priority=[{'key': 'value'}],
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.rstp_enabled == original.rstp_enabled
        assert roundtripped.stp_bridge_priority == original.stp_bridge_priority


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = switch_stp_api.APISwitchStp_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = switch_stp_api.APISwitchStp_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

