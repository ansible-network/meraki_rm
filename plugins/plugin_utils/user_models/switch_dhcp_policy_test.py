"""Colocated tests for UserSwitchDhcpPolicy — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import switch_dhcp_policy


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserSwitchDhcpPolicy can be constructed with all fields."""

    def test_defaults(self):
        obj = switch_dhcp_policy.UserSwitchDhcpPolicy()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserSwitchDhcpPolicy -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = switch_dhcp_policy.UserSwitchDhcpPolicy(
            default_policy='default_policy_val',
            allowed_servers=['item1', 'item2'],
            blocked_servers=['item1', 'item2'],
            always_allowed_servers=['item1', 'item2'],
            arp_inspection={'enabled': True},
            alerts={'enabled': True},
        )
        api = user.to_api(_ctx())

        assert api.defaultPolicy == user.default_policy
        assert api.allowedServers == user.allowed_servers
        assert api.blockedServers == user.blocked_servers
        assert api.alwaysAllowedServers == user.always_allowed_servers
        assert api.arpInspection == user.arp_inspection
        assert api.alerts == user.alerts

    def test_none_fields_omitted(self):
        user = switch_dhcp_policy.UserSwitchDhcpPolicy(default_policy='default_policy_val')
        api = user.to_api(_ctx())
        assert api.defaultPolicy == user.default_policy
        assert getattr(api, 'allowedServers', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = switch_dhcp_policy.UserSwitchDhcpPolicy(network_id='network_id_val', default_policy='default_policy_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

