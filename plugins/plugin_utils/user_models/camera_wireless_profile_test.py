"""Colocated tests for UserCameraWirelessProfile — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import camera_wireless_profile


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserCameraWirelessProfile can be constructed with all fields."""

    def test_defaults(self):
        obj = camera_wireless_profile.UserCameraWirelessProfile()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserCameraWirelessProfile -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = camera_wireless_profile.UserCameraWirelessProfile(
            wireless_profile_id='wireless_profile_id_val',
            name='name_val',
            identity={'enabled': True},
            ssid={'enabled': True},
        )
        api = user.to_api(_ctx())

        assert api.id == user.wireless_profile_id
        assert api.name == user.name
        assert api.identity == user.identity
        assert api.ssid == user.ssid

    def test_none_fields_omitted(self):
        user = camera_wireless_profile.UserCameraWirelessProfile(wireless_profile_id='wireless_profile_id_val')
        api = user.to_api(_ctx())
        assert api.id == user.wireless_profile_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = camera_wireless_profile.UserCameraWirelessProfile(network_id='network_id_val', wireless_profile_id='wireless_profile_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

