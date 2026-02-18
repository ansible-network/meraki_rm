"""Colocated tests for APIMerakiAuthUser_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import meraki_auth_user as meraki_auth_user_api
from ...user_models import meraki_auth_user as meraki_auth_user_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = meraki_auth_user_api.APIMerakiAuthUser_v1(
            id='id_val',
            name='name_val',
            email='email_val',
            password='password_val',
            accountType='accountType_val',
            authorizations=[{'key': 'value'}],
            isAdmin=True,
            emailPasswordToUser=True,
        )
        user = api.to_ansible(_ctx())

        assert user.meraki_auth_user_id == api.id
        assert user.name == api.name
        assert user.email == api.email
        assert user.password == api.password
        assert user.account_type == api.accountType
        assert user.authorizations == api.authorizations
        assert user.is_admin == api.isAdmin
        assert user.email_password_to_user == api.emailPasswordToUser


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = meraki_auth_user_user.UserMerakiAuthUser(
            meraki_auth_user_id='meraki_auth_user_id_val',
            name='name_val',
            email='email_val',
            password='password_val',
            account_type='account_type_val',
            authorizations=[{'key': 'value'}],
            is_admin=True,
            email_password_to_user=True,
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.meraki_auth_user_id == original.meraki_auth_user_id
        assert roundtripped.name == original.name
        assert roundtripped.email == original.email
        assert roundtripped.password == original.password
        assert roundtripped.account_type == original.account_type
        assert roundtripped.authorizations == original.authorizations
        assert roundtripped.is_admin == original.is_admin
        assert roundtripped.email_password_to_user == original.email_password_to_user


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = meraki_auth_user_api.APIMerakiAuthUser_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = meraki_auth_user_api.APIMerakiAuthUser_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

