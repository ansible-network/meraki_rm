"""Colocated tests for UserWebhook — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import webhook


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserWebhook can be constructed with all fields."""

    def test_defaults(self):
        obj = webhook.UserWebhook()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserWebhook -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = webhook.UserWebhook(
            http_server_id='http_server_id_val',
            name='name_val',
            url='url_val',
            shared_secret='shared_secret_val',
            payload_template={'enabled': True},
        )
        api = user.to_api(_ctx())

        assert api.id == user.http_server_id
        assert api.name == user.name
        assert api.url == user.url
        assert api.sharedSecret == user.shared_secret
        assert api.payloadTemplate == user.payload_template

    def test_none_fields_omitted(self):
        user = webhook.UserWebhook(http_server_id='http_server_id_val')
        api = user.to_api(_ctx())
        assert api.id == user.http_server_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = webhook.UserWebhook(network_id='network_id_val', http_server_id='http_server_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

