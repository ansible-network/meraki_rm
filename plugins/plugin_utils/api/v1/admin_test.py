"""Colocated tests for APIAdmin_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import admin as admin_api
from ...user_models import admin as admin_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = admin_api.APIAdmin_v1(
            id='id_val',
            name='name_val',
            email='email_val',
            orgAccess='orgAccess_val',
            tags=[{'key': 'value'}],
            networks=[{'key': 'value'}],
            authenticationMethod='authenticationMethod_val',
            accountStatus='accountStatus_val',
            twoFactorAuthEnabled=True,
            hasApiKey=True,
            lastActive='lastActive_val',
        )
        user = api.to_ansible(_ctx())

        assert user.admin_id == api.id
        assert user.name == api.name
        assert user.email == api.email
        assert user.org_access == api.orgAccess
        assert user.tags == api.tags
        assert user.networks == api.networks
        assert user.authentication_method == api.authenticationMethod
        assert user.account_status == api.accountStatus
        assert user.two_factor_auth_enabled == api.twoFactorAuthEnabled
        assert user.has_api_key == api.hasApiKey
        assert user.last_active == api.lastActive


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = admin_user.UserAdmin(
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
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.admin_id == original.admin_id
        assert roundtripped.name == original.name
        assert roundtripped.email == original.email
        assert roundtripped.org_access == original.org_access
        assert roundtripped.tags == original.tags
        assert roundtripped.networks == original.networks
        assert roundtripped.authentication_method == original.authentication_method
        assert roundtripped.account_status == original.account_status
        assert roundtripped.two_factor_auth_enabled == original.two_factor_auth_enabled
        assert roundtripped.has_api_key == original.has_api_key
        assert roundtripped.last_active == original.last_active


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = admin_api.APIAdmin_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = admin_api.APIAdmin_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

