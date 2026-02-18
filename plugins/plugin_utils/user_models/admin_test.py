"""Colocated tests for UserAdmin — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import admin


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserAdmin can be constructed with all fields."""

    def test_defaults(self):
        obj = admin.UserAdmin()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserAdmin -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = admin.UserAdmin(
            admin_id='admin_id_val',
            name='name_val',
            email='email_val',
            org_access='org_access_val',
            tags=[{'key': 'value'}],
            networks=[{'key': 'value'}],
            authentication_method='authentication_method_val',
            account_status='account_status_val',
            two_factor_auth_enabled=True,
            has_api_key=True,
            last_active='last_active_val',
        )
        api = user.to_api(_ctx())

        assert api.id == user.admin_id
        assert api.name == user.name
        assert api.email == user.email
        assert api.orgAccess == user.org_access
        assert api.tags == user.tags
        assert api.networks == user.networks
        assert api.authenticationMethod == user.authentication_method
        assert api.accountStatus == user.account_status
        assert api.twoFactorAuthEnabled == user.two_factor_auth_enabled
        assert api.hasApiKey == user.has_api_key
        assert api.lastActive == user.last_active

    def test_none_fields_omitted(self):
        user = admin.UserAdmin(admin_id='admin_id_val')
        api = user.to_api(_ctx())
        assert api.id == user.admin_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = admin.UserAdmin(organization_id='organization_id_val', admin_id='admin_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'organization_id' not in api_field_names or getattr(api, 'organization_id', None) is None

