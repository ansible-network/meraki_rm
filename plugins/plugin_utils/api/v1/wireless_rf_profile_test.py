"""Colocated tests for APIWirelessRfProfile_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import wireless_rf_profile as wireless_rf_profile_api
from ...user_models import wireless_rf_profile as wireless_rf_profile_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = wireless_rf_profile_api.APIWirelessRfProfile_v1(
            id='id_val',
            name='name_val',
            bandSelectionType='bandSelectionType_val',
            clientBalancingEnabled=True,
            twoFourGhzSettings={'enabled': True},
            fiveGhzSettings={'enabled': True},
            sixGhzSettings={'enabled': True},
            transmission={'enabled': True},
            isIndoorDefault=True,
            isOutdoorDefault=True,
            apBandSettings={'enabled': True},
            perSsidSettings={'enabled': True},
            minBitrateType='minBitrateType_val',
        )
        user = api.to_ansible(_ctx())

        assert user.rf_profile_id == api.id
        assert user.name == api.name
        assert user.band_selection_type == api.bandSelectionType
        assert user.client_balancing_enabled == api.clientBalancingEnabled
        assert user.two_four_ghz_settings == api.twoFourGhzSettings
        assert user.five_ghz_settings == api.fiveGhzSettings
        assert user.six_ghz_settings == api.sixGhzSettings
        assert user.transmission == api.transmission
        assert user.is_indoor_default == api.isIndoorDefault
        assert user.is_outdoor_default == api.isOutdoorDefault
        assert user.ap_band_settings == api.apBandSettings
        assert user.per_ssid_settings == api.perSsidSettings
        assert user.min_bitrate_type == api.minBitrateType


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = wireless_rf_profile_user.UserWirelessRfProfile(
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
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.rf_profile_id == original.rf_profile_id
        assert roundtripped.name == original.name
        assert roundtripped.band_selection_type == original.band_selection_type
        assert roundtripped.client_balancing_enabled == original.client_balancing_enabled
        assert roundtripped.two_four_ghz_settings == original.two_four_ghz_settings
        assert roundtripped.five_ghz_settings == original.five_ghz_settings
        assert roundtripped.six_ghz_settings == original.six_ghz_settings
        assert roundtripped.transmission == original.transmission
        assert roundtripped.is_indoor_default == original.is_indoor_default
        assert roundtripped.is_outdoor_default == original.is_outdoor_default
        assert roundtripped.ap_band_settings == original.ap_band_settings
        assert roundtripped.per_ssid_settings == original.per_ssid_settings
        assert roundtripped.min_bitrate_type == original.min_bitrate_type


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = wireless_rf_profile_api.APIWirelessRfProfile_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = wireless_rf_profile_api.APIWirelessRfProfile_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

