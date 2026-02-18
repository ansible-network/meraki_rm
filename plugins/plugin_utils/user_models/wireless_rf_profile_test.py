"""Colocated tests for UserWirelessRfProfile — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import wireless_rf_profile


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserWirelessRfProfile can be constructed with all fields."""

    def test_defaults(self):
        obj = wireless_rf_profile.UserWirelessRfProfile()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserWirelessRfProfile -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = wireless_rf_profile.UserWirelessRfProfile(
            rf_profile_id='rf_profile_id_val',
            name='name_val',
            band_selection_type='band_selection_type_val',
            client_balancing_enabled=True,
            two_four_ghz_settings={'enabled': True},
            five_ghz_settings={'enabled': True},
            six_ghz_settings={'enabled': True},
            transmission={'enabled': True},
            is_indoor_default=True,
            is_outdoor_default=True,
            ap_band_settings={'enabled': True},
            per_ssid_settings={'enabled': True},
            min_bitrate_type='min_bitrate_type_val',
        )
        api = user.to_api(_ctx())

        assert api.id == user.rf_profile_id
        assert api.name == user.name
        assert api.bandSelectionType == user.band_selection_type
        assert api.clientBalancingEnabled == user.client_balancing_enabled
        assert api.twoFourGhzSettings == user.two_four_ghz_settings
        assert api.fiveGhzSettings == user.five_ghz_settings
        assert api.sixGhzSettings == user.six_ghz_settings
        assert api.transmission == user.transmission
        assert api.isIndoorDefault == user.is_indoor_default
        assert api.isOutdoorDefault == user.is_outdoor_default
        assert api.apBandSettings == user.ap_band_settings
        assert api.perSsidSettings == user.per_ssid_settings
        assert api.minBitrateType == user.min_bitrate_type

    def test_none_fields_omitted(self):
        user = wireless_rf_profile.UserWirelessRfProfile(rf_profile_id='rf_profile_id_val')
        api = user.to_api(_ctx())
        assert api.id == user.rf_profile_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = wireless_rf_profile.UserWirelessRfProfile(network_id='network_id_val', rf_profile_id='rf_profile_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

