"""Colocated tests for UserApplianceRfProfile — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import appliance_rf_profile


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserApplianceRfProfile can be constructed with all fields."""

    def test_defaults(self):
        obj = appliance_rf_profile.UserApplianceRfProfile()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserApplianceRfProfile -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = appliance_rf_profile.UserApplianceRfProfile(
            rf_profile_id='rf_profile_id_val',
            name='name_val',
            two_four_ghz_settings={'enabled': True},
            five_ghz_settings={'enabled': True},
            per_ssid_settings={'enabled': True},
            assigned=[{'key': 'value'}],
        )
        api = user.to_api(_ctx())

        assert api.id == user.rf_profile_id
        assert api.name == user.name
        assert api.twoFourGhzSettings == user.two_four_ghz_settings
        assert api.fiveGhzSettings == user.five_ghz_settings
        assert api.perSsidSettings == user.per_ssid_settings
        assert api.assigned == user.assigned

    def test_none_fields_omitted(self):
        user = appliance_rf_profile.UserApplianceRfProfile(rf_profile_id='rf_profile_id_val')
        api = user.to_api(_ctx())
        assert api.id == user.rf_profile_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = appliance_rf_profile.UserApplianceRfProfile(network_id='network_id_val', rf_profile_id='rf_profile_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

