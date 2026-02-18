"""Colocated tests for UserBrandingPolicy — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import branding_policy


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserBrandingPolicy can be constructed with all fields."""

    def test_defaults(self):
        obj = branding_policy.UserBrandingPolicy()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserBrandingPolicy -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = branding_policy.UserBrandingPolicy(
            branding_policy_id='branding_policy_id_val',
            name='name_val',
            enabled=True,
            admin_settings={'enabled': True},
            help_settings={'enabled': True},
            custom_logo={'enabled': True},
        )
        api = user.to_api(_ctx())

        assert api.id == user.branding_policy_id
        assert api.name == user.name
        assert api.enabled == user.enabled
        assert api.adminSettings == user.admin_settings
        assert api.helpSettings == user.help_settings
        assert api.customLogo == user.custom_logo

    def test_none_fields_omitted(self):
        user = branding_policy.UserBrandingPolicy(branding_policy_id='branding_policy_id_val')
        api = user.to_api(_ctx())
        assert api.id == user.branding_policy_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = branding_policy.UserBrandingPolicy(organization_id='organization_id_val', branding_policy_id='branding_policy_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'organization_id' not in api_field_names or getattr(api, 'organization_id', None) is None

