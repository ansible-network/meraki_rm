"""Colocated tests for APIApplianceSsid_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import appliance_ssid as appliance_ssid_api
from ...user_models import appliance_ssid as appliance_ssid_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = appliance_ssid_api.APIApplianceSsid_v1(
            number=24,
            name='name_val',
            enabled=True,
            authMode='authMode_val',
            encryptionMode='encryptionMode_val',
            psk='psk_val',
            defaultVlanId=24,
            visible=True,
            wpaEncryptionMode='wpaEncryptionMode_val',
            radiusServers=[{'key': 'value'}],
        )
        user = api.to_ansible(_ctx())

        assert user.number == api.number
        assert user.name == api.name
        assert user.enabled == api.enabled
        assert user.auth_mode == api.authMode
        assert user.encryption_mode == api.encryptionMode
        assert user.psk == api.psk
        assert user.default_vlan_id == api.defaultVlanId
        assert user.visible == api.visible
        assert user.wpa_encryption_mode == api.wpaEncryptionMode
        assert user.radius_servers == api.radiusServers


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = appliance_ssid_user.UserApplianceSsid(
            number=24,
            name='name_val',
            enabled=True,
            auth_mode='auth_mode_val',
            encryption_mode='encryption_mode_val',
            psk='psk_val',
            default_vlan_id=24,
            visible=True,
            wpa_encryption_mode='wpa_encryption_mode_val',
            radius_servers=[{'key': 'value'}],
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.number == original.number
        assert roundtripped.name == original.name
        assert roundtripped.enabled == original.enabled
        assert roundtripped.auth_mode == original.auth_mode
        assert roundtripped.encryption_mode == original.encryption_mode
        assert roundtripped.psk == original.psk
        assert roundtripped.default_vlan_id == original.default_vlan_id
        assert roundtripped.visible == original.visible
        assert roundtripped.wpa_encryption_mode == original.wpa_encryption_mode
        assert roundtripped.radius_servers == original.radius_servers


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = appliance_ssid_api.APIApplianceSsid_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = appliance_ssid_api.APIApplianceSsid_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

