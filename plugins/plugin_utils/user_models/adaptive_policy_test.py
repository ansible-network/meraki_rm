"""Colocated tests for UserAdaptivePolicy — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import adaptive_policy


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserAdaptivePolicy can be constructed with all fields."""

    def test_defaults(self):
        obj = adaptive_policy.UserAdaptivePolicy()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserAdaptivePolicy -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = adaptive_policy.UserAdaptivePolicy(
            enabled_networks=['item1', 'item2'],
            last_entry_rule='last_entry_rule_val',
        )
        api = user.to_api(_ctx())

        assert api.enabledNetworks == user.enabled_networks
        assert api.lastEntryRule == user.last_entry_rule

    def test_none_fields_omitted(self):
        user = adaptive_policy.UserAdaptivePolicy(enabled_networks=['item1', 'item2'])
        api = user.to_api(_ctx())
        assert api.enabledNetworks == user.enabled_networks
        assert getattr(api, 'lastEntryRule', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = adaptive_policy.UserAdaptivePolicy(organization_id='organization_id_val', enabled_networks=['item1', 'item2'])
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'organization_id' not in api_field_names or getattr(api, 'organization_id', None) is None

