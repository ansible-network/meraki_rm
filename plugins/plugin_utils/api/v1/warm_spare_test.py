"""Colocated tests for APIWarmSpare_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import warm_spare as warm_spare_api
from ...user_models import warm_spare as warm_spare_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = warm_spare_api.APIWarmSpare_v1(
            enabled=True,
            spareSerial='spareSerial_val',
            uplinkMode='uplinkMode_val',
            virtualIp1='virtualIp1_val',
            virtualIp2='virtualIp2_val',
            wan1={'enabled': True},
            wan2={'enabled': True},
            primarySerial='primarySerial_val',
        )
        user = api.to_ansible(_ctx())

        assert user.enabled == api.enabled
        assert user.spare_serial == api.spareSerial
        assert user.uplink_mode == api.uplinkMode
        assert user.virtual_ip1 == api.virtualIp1
        assert user.virtual_ip2 == api.virtualIp2
        assert user.wan1 == api.wan1
        assert user.wan2 == api.wan2
        assert user.primary_serial == api.primarySerial


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = warm_spare_user.UserWarmSpare(
            enabled=True,
            spare_serial='spare_serial_val',
            uplink_mode='uplink_mode_val',
            virtual_ip1='virtual_ip1_val',
            virtual_ip2='virtual_ip2_val',
            wan1={'enabled': True},
            wan2={'enabled': True},
            primary_serial='primary_serial_val',
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.enabled == original.enabled
        assert roundtripped.spare_serial == original.spare_serial
        assert roundtripped.uplink_mode == original.uplink_mode
        assert roundtripped.virtual_ip1 == original.virtual_ip1
        assert roundtripped.virtual_ip2 == original.virtual_ip2
        assert roundtripped.wan1 == original.wan1
        assert roundtripped.wan2 == original.wan2
        assert roundtripped.primary_serial == original.primary_serial


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = warm_spare_api.APIWarmSpare_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = warm_spare_api.APIWarmSpare_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

