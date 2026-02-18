"""Colocated tests for UserSwitchAcl — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import switch_acl


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserSwitchAcl can be constructed with all fields."""

    def test_defaults(self):
        obj = switch_acl.UserSwitchAcl()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserSwitchAcl -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = switch_acl.UserSwitchAcl(
            rules=[{'key': 'value'}],
        )
        api = user.to_api(_ctx())

        assert api.rules == user.rules

    def test_none_fields_omitted(self):
        user = switch_acl.UserSwitchAcl(rules=[{'key': 'value'}])
        api = user.to_api(_ctx())
        assert api.rules == user.rules


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = switch_acl.UserSwitchAcl(network_id='network_id_val', rules=[{'key': 'value'}])
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

