"""Colocated tests for UserTrafficShaping — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import traffic_shaping


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserTrafficShaping can be constructed with all fields."""

    def test_defaults(self):
        obj = traffic_shaping.UserTrafficShaping()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserTrafficShaping -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = traffic_shaping.UserTrafficShaping(
            default_rules_enabled=True,
            default_uplink='default_uplink_val',
            rules=[{'key': 'value'}],
            bandwidth_limits={'enabled': True},
            global_bandwidth_limits={'enabled': True},
            failover_and_failback={'enabled': True},
            load_balancing_enabled=True,
            active_active_auto_vpn_enabled=True,
            vpn_traffic_uplink_preferences=[{'key': 'value'}],
            wan_traffic_uplink_preferences=[{'key': 'value'}],
        )
        api = user.to_api(_ctx())

        assert api.defaultRulesEnabled == user.default_rules_enabled
        assert api.defaultUplink == user.default_uplink
        assert api.rules == user.rules
        assert api.bandwidthLimits == user.bandwidth_limits
        assert api.globalBandwidthLimits == user.global_bandwidth_limits
        assert api.failoverAndFailback == user.failover_and_failback
        assert api.loadBalancingEnabled == user.load_balancing_enabled
        assert api.activeActiveAutoVpnEnabled == user.active_active_auto_vpn_enabled
        assert api.vpnTrafficUplinkPreferences == user.vpn_traffic_uplink_preferences
        assert api.wanTrafficUplinkPreferences == user.wan_traffic_uplink_preferences

    def test_none_fields_omitted(self):
        user = traffic_shaping.UserTrafficShaping(default_rules_enabled=True)
        api = user.to_api(_ctx())
        assert api.defaultRulesEnabled == user.default_rules_enabled
        assert getattr(api, 'defaultUplink', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = traffic_shaping.UserTrafficShaping(network_id='network_id_val', default_rules_enabled=True)
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

