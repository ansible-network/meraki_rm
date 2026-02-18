"""Colocated tests for UserAirMarshal — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import air_marshal


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserAirMarshal can be constructed with all fields."""

    def test_defaults(self):
        obj = air_marshal.UserAirMarshal()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserAirMarshal -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = air_marshal.UserAirMarshal(
            rule_id='rule_id_val',
            type='type_val',
            match={'enabled': True},
            default_policy='default_policy_val',
            ssid='ssid_val',
            bssids=[{'key': 'value'}],
            channels=24,
            first_seen=24,
            last_seen=24,
            created_at='created_at_val',
            updated_at='updated_at_val',
        )
        api = user.to_api(_ctx())

        assert api.ruleId == user.rule_id
        assert api.type == user.type
        assert api.match == user.match
        assert api.defaultPolicy == user.default_policy
        assert api.ssid == user.ssid
        assert api.bssids == user.bssids
        assert api.channels == user.channels
        assert api.firstSeen == user.first_seen
        assert api.lastSeen == user.last_seen
        assert api.createdAt == user.created_at
        assert api.updatedAt == user.updated_at

    def test_none_fields_omitted(self):
        user = air_marshal.UserAirMarshal(rule_id='rule_id_val')
        api = user.to_api(_ctx())
        assert api.ruleId == user.rule_id
        assert getattr(api, 'type', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = air_marshal.UserAirMarshal(network_id='network_id_val', rule_id='rule_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

