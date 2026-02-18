"""Colocated tests for UserSsid — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import ssid


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserSsid can be constructed with all fields."""

    def test_defaults(self):
        obj = ssid.UserSsid()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserSsid -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = ssid.UserSsid(
            number=24,
            name='name_val',
            enabled=True,
            auth_mode='auth_mode_val',
            encryption_mode='encryption_mode_val',
            psk='psk_val',
            wpa_encryption_mode='wpa_encryption_mode_val',
            ip_assignment_mode='ip_assignment_mode_val',
            use_vlan_tagging=True,
            default_vlan_id=24,
            vlan_id=24,
            splash_page='splash_page_val',
            band_selection='band_selection_val',
            min_bitrate=1.5,
            per_client_bandwidth_limit_up=24,
            per_client_bandwidth_limit_down=24,
            per_ssid_bandwidth_limit_up=24,
            per_ssid_bandwidth_limit_down=24,
            visible=True,
            available_on_all_aps=True,
            availability_tags=['item1', 'item2'],
        )
        api = user.to_api(_ctx())

        assert api.number == user.number
        assert api.name == user.name
        assert api.enabled == user.enabled
        assert api.authMode == user.auth_mode
        assert api.encryptionMode == user.encryption_mode
        assert api.psk == user.psk
        assert api.wpaEncryptionMode == user.wpa_encryption_mode
        assert api.ipAssignmentMode == user.ip_assignment_mode
        assert api.useVlanTagging == user.use_vlan_tagging
        assert api.defaultVlanId == user.default_vlan_id
        assert api.vlanId == user.vlan_id
        assert api.splashPage == user.splash_page
        assert api.bandSelection == user.band_selection
        assert api.minBitrate == user.min_bitrate
        assert api.perClientBandwidthLimitUp == user.per_client_bandwidth_limit_up
        assert api.perClientBandwidthLimitDown == user.per_client_bandwidth_limit_down
        assert api.perSsidBandwidthLimitUp == user.per_ssid_bandwidth_limit_up
        assert api.perSsidBandwidthLimitDown == user.per_ssid_bandwidth_limit_down
        assert api.visible == user.visible
        assert api.availableOnAllAps == user.available_on_all_aps
        assert api.availabilityTags == user.availability_tags

    def test_none_fields_omitted(self):
        user = ssid.UserSsid(number=24)
        api = user.to_api(_ctx())
        assert api.number == user.number
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = ssid.UserSsid(network_id='network_id_val', number=24)
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

