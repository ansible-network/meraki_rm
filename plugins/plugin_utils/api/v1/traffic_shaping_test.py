"""Colocated tests for APITrafficShaping_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import traffic_shaping as traffic_shaping_api
from ...user_models import traffic_shaping as traffic_shaping_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = traffic_shaping_api.APITrafficShaping_v1(
            defaultRulesEnabled=True,
            defaultUplink='defaultUplink_val',
            rules=[{'key': 'value'}],
            bandwidthLimits={'enabled': True},
            globalBandwidthLimits={'enabled': True},
            failoverAndFailback={'enabled': True},
            loadBalancingEnabled=True,
            activeActiveAutoVpnEnabled=True,
            vpnTrafficUplinkPreferences=[{'key': 'value'}],
            wanTrafficUplinkPreferences=[{'key': 'value'}],
        )
        user = api.to_ansible(_ctx())

        assert user.default_rules_enabled == api.defaultRulesEnabled
        assert user.default_uplink == api.defaultUplink
        assert user.rules == api.rules
        assert user.bandwidth_limits == api.bandwidthLimits
        assert user.global_bandwidth_limits == api.globalBandwidthLimits
        assert user.failover_and_failback == api.failoverAndFailback
        assert user.load_balancing_enabled == api.loadBalancingEnabled
        assert user.active_active_auto_vpn_enabled == api.activeActiveAutoVpnEnabled
        assert user.vpn_traffic_uplink_preferences == api.vpnTrafficUplinkPreferences
        assert user.wan_traffic_uplink_preferences == api.wanTrafficUplinkPreferences


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = traffic_shaping_user.UserTrafficShaping(
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
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.default_rules_enabled == original.default_rules_enabled
        assert roundtripped.default_uplink == original.default_uplink
        assert roundtripped.rules == original.rules
        assert roundtripped.bandwidth_limits == original.bandwidth_limits
        assert roundtripped.global_bandwidth_limits == original.global_bandwidth_limits
        assert roundtripped.failover_and_failback == original.failover_and_failback
        assert roundtripped.load_balancing_enabled == original.load_balancing_enabled
        assert roundtripped.active_active_auto_vpn_enabled == original.active_active_auto_vpn_enabled
        assert roundtripped.vpn_traffic_uplink_preferences == original.vpn_traffic_uplink_preferences
        assert roundtripped.wan_traffic_uplink_preferences == original.wan_traffic_uplink_preferences


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = traffic_shaping_api.APITrafficShaping_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = traffic_shaping_api.APITrafficShaping_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

