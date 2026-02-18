"""Colocated tests for APIPrefix_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import prefix as prefix_api
from ...user_models import prefix as prefix_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = prefix_api.APIPrefix_v1(
            staticDelegatedPrefixId='staticDelegatedPrefixId_val',
            prefix='prefix_val',
            description='description_val',
            origin={'enabled': True},
        )
        user = api.to_ansible(_ctx())

        assert user.static_delegated_prefix_id == api.staticDelegatedPrefixId
        assert user.prefix == api.prefix
        assert user.description == api.description
        assert user.origin == api.origin


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = prefix_user.UserPrefix(
            static_delegated_prefix_id='static_delegated_prefix_id_val',
            prefix='prefix_val',
            description='description_val',
            origin={'enabled': True},
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.static_delegated_prefix_id == original.static_delegated_prefix_id
        assert roundtripped.prefix == original.prefix
        assert roundtripped.description == original.description
        assert roundtripped.origin == original.origin


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = prefix_api.APIPrefix_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = prefix_api.APIPrefix_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

