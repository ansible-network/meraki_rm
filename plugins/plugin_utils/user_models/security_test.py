"""Colocated tests for UserSecurity — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import security


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserSecurity can be constructed with all fields."""

    def test_defaults(self):
        obj = security.UserSecurity()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserSecurity -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = security.UserSecurity(
            mode='mode_val',
            ids_rulesets='ids_rulesets_val',
            protected_networks={'enabled': True},
            allowed_files=[{'key': 'value'}],
            allowed_urls=[{'key': 'value'}],
        )
        api = user.to_api(_ctx())

        assert api.mode == user.mode
        assert api.idsRulesets == user.ids_rulesets
        assert api.protectedNetworks == user.protected_networks
        assert api.allowedFiles == user.allowed_files
        assert api.allowedUrls == user.allowed_urls

    def test_none_fields_omitted(self):
        user = security.UserSecurity(mode='mode_val')
        api = user.to_api(_ctx())
        assert api.mode == user.mode
        assert getattr(api, 'idsRulesets', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = security.UserSecurity(network_id='network_id_val', mode='mode_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

