"""Colocated tests for APIApplianceRfProfile_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import appliance_rf_profile as appliance_rf_profile_api
from ...user_models import appliance_rf_profile as appliance_rf_profile_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = appliance_rf_profile_api.APIApplianceRfProfile_v1(
            id='id_val',
            name='name_val',
            twoFourGhzSettings={'enabled': True},
            fiveGhzSettings={'enabled': True},
            perSsidSettings={'enabled': True},
            assigned=[{'key': 'value'}],
        )
        user = api.to_ansible(_ctx())

        assert user.rf_profile_id == api.id
        assert user.name == api.name
        assert user.two_four_ghz_settings == api.twoFourGhzSettings
        assert user.five_ghz_settings == api.fiveGhzSettings
        assert user.per_ssid_settings == api.perSsidSettings
        assert user.assigned == api.assigned


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = appliance_rf_profile_user.UserApplianceRfProfile(
            rf_profile_id='rf_profile_id_val',
            name='name_val',
            two_four_ghz_settings={'enabled': True},
            five_ghz_settings={'enabled': True},
            per_ssid_settings={'enabled': True},
            assigned=[{'key': 'value'}],
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.rf_profile_id == original.rf_profile_id
        assert roundtripped.name == original.name
        assert roundtripped.two_four_ghz_settings == original.two_four_ghz_settings
        assert roundtripped.five_ghz_settings == original.five_ghz_settings
        assert roundtripped.per_ssid_settings == original.per_ssid_settings
        assert roundtripped.assigned == original.assigned


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = appliance_rf_profile_api.APIApplianceRfProfile_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = appliance_rf_profile_api.APIApplianceRfProfile_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

