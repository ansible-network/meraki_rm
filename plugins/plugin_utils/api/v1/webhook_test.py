"""Colocated tests for APIWebhook_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import webhook as webhook_api
from ...user_models import webhook as webhook_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = webhook_api.APIWebhook_v1(
            id='id_val',
            name='name_val',
            url='url_val',
            sharedSecret='sharedSecret_val',
            payloadTemplate={'enabled': True},
        )
        user = api.to_ansible(_ctx())

        assert user.http_server_id == api.id
        assert user.name == api.name
        assert user.url == api.url
        assert user.shared_secret == api.sharedSecret
        assert user.payload_template == api.payloadTemplate


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = webhook_user.UserWebhook(
            http_server_id='http_server_id_val',
            name='name_val',
            url='url_val',
            shared_secret='shared_secret_val',
            payload_template={'enabled': True},
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.http_server_id == original.http_server_id
        assert roundtripped.name == original.name
        assert roundtripped.url == original.url
        assert roundtripped.shared_secret == original.shared_secret
        assert roundtripped.payload_template == original.payload_template


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = webhook_api.APIWebhook_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = webhook_api.APIWebhook_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

