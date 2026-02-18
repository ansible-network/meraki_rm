"""Colocated tests for UserApplianceSsid — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import appliance_ssid


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserApplianceSsid can be constructed with all fields."""

    def test_defaults(self):
        obj = appliance_ssid.UserApplianceSsid()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserApplianceSsid -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = appliance_ssid.UserApplianceSsid(
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
        api = user.to_api(_ctx())

        assert api.number == user.number
        assert api.name == user.name
        assert api.enabled == user.enabled
        assert api.authMode == user.auth_mode
        assert api.encryptionMode == user.encryption_mode
        assert api.psk == user.psk
        assert api.defaultVlanId == user.default_vlan_id
        assert api.visible == user.visible
        assert api.wpaEncryptionMode == user.wpa_encryption_mode
        assert api.radiusServers == user.radius_servers

    def test_none_fields_omitted(self):
        user = appliance_ssid.UserApplianceSsid(number=24)
        api = user.to_api(_ctx())
        assert api.number == user.number
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = appliance_ssid.UserApplianceSsid(network_id='network_id_val', number=24)
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

