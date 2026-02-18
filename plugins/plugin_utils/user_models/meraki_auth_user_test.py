"""Colocated tests for UserMerakiAuthUser — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import meraki_auth_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserMerakiAuthUser can be constructed with all fields."""

    def test_defaults(self):
        obj = meraki_auth_user.UserMerakiAuthUser()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserMerakiAuthUser -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = meraki_auth_user.UserMerakiAuthUser(
            meraki_auth_user_id='meraki_auth_user_id_val',
            name='name_val',
            email='email_val',
            password='password_val',
            account_type='account_type_val',
            authorizations=[{'key': 'value'}],
            is_admin=True,
            email_password_to_user=True,
        )
        api = user.to_api(_ctx())

        assert api.id == user.meraki_auth_user_id
        assert api.name == user.name
        assert api.email == user.email
        assert api.password == user.password
        assert api.accountType == user.account_type
        assert api.authorizations == user.authorizations
        assert api.isAdmin == user.is_admin
        assert api.emailPasswordToUser == user.email_password_to_user

    def test_none_fields_omitted(self):
        user = meraki_auth_user.UserMerakiAuthUser(meraki_auth_user_id='meraki_auth_user_id_val')
        api = user.to_api(_ctx())
        assert api.id == user.meraki_auth_user_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = meraki_auth_user.UserMerakiAuthUser(network_id='network_id_val', meraki_auth_user_id='meraki_auth_user_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

