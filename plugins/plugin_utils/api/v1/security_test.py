"""Colocated tests for APISecurity_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import security as security_api
from ...user_models import security as security_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = security_api.APISecurity_v1(
            mode='mode_val',
            idsRulesets='idsRulesets_val',
            protectedNetworks={'enabled': True},
            allowedFiles=[{'key': 'value'}],
            allowedUrls=[{'key': 'value'}],
        )
        user = api.to_ansible(_ctx())

        assert user.mode == api.mode
        assert user.ids_rulesets == api.idsRulesets
        assert user.protected_networks == api.protectedNetworks
        assert user.allowed_files == api.allowedFiles
        assert user.allowed_urls == api.allowedUrls


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = security_user.UserSecurity(
            mode='mode_val',
            ids_rulesets='ids_rulesets_val',
            protected_networks={'enabled': True},
            allowed_files=[{'key': 'value'}],
            allowed_urls=[{'key': 'value'}],
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.mode == original.mode
        assert roundtripped.ids_rulesets == original.ids_rulesets
        assert roundtripped.protected_networks == original.protected_networks
        assert roundtripped.allowed_files == original.allowed_files
        assert roundtripped.allowed_urls == original.allowed_urls


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = security_api.APISecurity_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = security_api.APISecurity_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

