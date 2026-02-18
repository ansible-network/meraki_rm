"""Colocated tests for APISwitchStack_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import switch_stack as switch_stack_api
from ...user_models import switch_stack as switch_stack_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = switch_stack_api.APISwitchStack_v1(
            id='id_val',
            name='name_val',
            serials=['item1', 'item2'],
            members=[{'key': 'value'}],
            isMonitorOnly=True,
            virtualMac='virtualMac_val',
        )
        user = api.to_ansible(_ctx())

        assert user.switch_stack_id == api.id
        assert user.name == api.name
        assert user.serials == api.serials
        assert user.members == api.members
        assert user.is_monitor_only == api.isMonitorOnly
        assert user.virtual_mac == api.virtualMac


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = switch_stack_user.UserSwitchStack(
            switch_stack_id='switch_stack_id_val',
            name='name_val',
            serials=['item1', 'item2'],
            members=[{'key': 'value'}],
            is_monitor_only=True,
            virtual_mac='virtual_mac_val',
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.switch_stack_id == original.switch_stack_id
        assert roundtripped.name == original.name
        assert roundtripped.serials == original.serials
        assert roundtripped.members == original.members
        assert roundtripped.is_monitor_only == original.is_monitor_only
        assert roundtripped.virtual_mac == original.virtual_mac


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = switch_stack_api.APISwitchStack_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = switch_stack_api.APISwitchStack_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

