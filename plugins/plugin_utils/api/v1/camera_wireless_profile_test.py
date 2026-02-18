"""Colocated tests for APICameraWirelessProfile_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import camera_wireless_profile as camera_wireless_profile_api
from ...user_models import camera_wireless_profile as camera_wireless_profile_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = camera_wireless_profile_api.APICameraWirelessProfile_v1(
            id='id_val',
            name='name_val',
            identity={'enabled': True},
            ssid={'enabled': True},
        )
        user = api.to_ansible(_ctx())

        assert user.wireless_profile_id == api.id
        assert user.name == api.name
        assert user.identity == api.identity
        assert user.ssid == api.ssid


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = camera_wireless_profile_user.UserCameraWirelessProfile(
            wireless_profile_id='wireless_profile_id_val',
            name='name_val',
            identity={'enabled': True},
            ssid={'enabled': True},
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.wireless_profile_id == original.wireless_profile_id
        assert roundtripped.name == original.name
        assert roundtripped.identity == original.identity
        assert roundtripped.ssid == original.ssid


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = camera_wireless_profile_api.APICameraWirelessProfile_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = camera_wireless_profile_api.APICameraWirelessProfile_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

