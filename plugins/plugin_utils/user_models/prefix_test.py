"""Colocated tests for UserPrefix — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import prefix


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserPrefix can be constructed with all fields."""

    def test_defaults(self):
        obj = prefix.UserPrefix()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserPrefix -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = prefix.UserPrefix(
            static_delegated_prefix_id='static_delegated_prefix_id_val',
            prefix='prefix_val',
            description='description_val',
            origin={'enabled': True},
        )
        api = user.to_api(_ctx())

        assert api.staticDelegatedPrefixId == user.static_delegated_prefix_id
        assert api.prefix == user.prefix
        assert api.description == user.description
        assert api.origin == user.origin

    def test_none_fields_omitted(self):
        user = prefix.UserPrefix(static_delegated_prefix_id='static_delegated_prefix_id_val')
        api = user.to_api(_ctx())
        assert api.staticDelegatedPrefixId == user.static_delegated_prefix_id
        assert getattr(api, 'prefix', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = prefix.UserPrefix(network_id='network_id_val', static_delegated_prefix_id='static_delegated_prefix_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

