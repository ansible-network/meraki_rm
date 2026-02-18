"""Colocated tests for APIDeviceManagementInterface_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import device_management_interface as device_management_interface_api
from ...user_models import device_management_interface as device_management_interface_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = device_management_interface_api.APIDeviceManagementInterface_v1(
            wan1={'enabled': True},
            wan2={'enabled': True},
            ddnsHostnames={'enabled': True},
        )
        user = api.to_ansible(_ctx())

        assert user.wan1 == api.wan1
        assert user.wan2 == api.wan2
        assert user.ddns_hostnames == api.ddnsHostnames


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = device_management_interface_user.UserDeviceManagementInterface(
            wan1={'enabled': True},
            wan2={'enabled': True},
            ddns_hostnames={'enabled': True},
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.wan1 == original.wan1
        assert roundtripped.wan2 == original.wan2
        assert roundtripped.ddns_hostnames == original.ddns_hostnames


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = device_management_interface_api.APIDeviceManagementInterface_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = device_management_interface_api.APIDeviceManagementInterface_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

