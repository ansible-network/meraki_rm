"""Colocated tests for APIBrandingPolicy_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import branding_policy as branding_policy_api
from ...user_models import branding_policy as branding_policy_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = branding_policy_api.APIBrandingPolicy_v1(
            id='id_val',
            name='name_val',
            enabled=True,
            adminSettings={'enabled': True},
            helpSettings={'enabled': True},
            customLogo={'enabled': True},
        )
        user = api.to_ansible(_ctx())

        assert user.branding_policy_id == api.id
        assert user.name == api.name
        assert user.enabled == api.enabled
        assert user.admin_settings == api.adminSettings
        assert user.help_settings == api.helpSettings
        assert user.custom_logo == api.customLogo


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = branding_policy_user.UserBrandingPolicy(
            branding_policy_id='branding_policy_id_val',
            name='name_val',
            enabled=True,
            admin_settings={'enabled': True},
            help_settings={'enabled': True},
            custom_logo={'enabled': True},
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.branding_policy_id == original.branding_policy_id
        assert roundtripped.name == original.name
        assert roundtripped.enabled == original.enabled
        assert roundtripped.admin_settings == original.admin_settings
        assert roundtripped.help_settings == original.help_settings
        assert roundtripped.custom_logo == original.custom_logo


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = branding_policy_api.APIBrandingPolicy_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = branding_policy_api.APIBrandingPolicy_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

