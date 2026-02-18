"""Colocated tests for APIFirmwareUpgrade_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import firmware_upgrade as firmware_upgrade_api
from ...user_models import firmware_upgrade as firmware_upgrade_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = firmware_upgrade_api.APIFirmwareUpgrade_v1(
            upgradeWindow={'enabled': True},
            timezone='timezone_val',
            products={'enabled': True},
        )
        user = api.to_ansible(_ctx())

        assert user.upgrade_window == api.upgradeWindow
        assert user.timezone == api.timezone
        assert user.products == api.products


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = firmware_upgrade_user.UserFirmwareUpgrade(
            upgrade_window={'enabled': True},
            timezone='timezone_val',
            products={'enabled': True},
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.upgrade_window == original.upgrade_window
        assert roundtripped.timezone == original.timezone
        assert roundtripped.products == original.products


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = firmware_upgrade_api.APIFirmwareUpgrade_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = firmware_upgrade_api.APIFirmwareUpgrade_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

