"""Versioned API model and transform mixin for Meraki appliance traffic shaping (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.traffic_shaping import TrafficShaping as GeneratedTrafficShaping

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
}

# Mutable fields for update (singleton - no create/delete)
_UPDATE_FIELDS = [
    'defaultRulesEnabled', 'defaultUplink', 'rules', 'bandwidthLimits',
    'globalBandwidthLimits', 'failoverAndFailback', 'loadBalancingEnabled',
    'activeActiveAutoVpnEnabled', 'vpnTrafficUplinkPreferences',
    'wanTrafficUplinkPreferences',
]


class TrafficShapingTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki appliance traffic shaping (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find': EndpointOperation(
                path='/networks/{networkId}/appliance/trafficShaping',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/appliance/trafficShaping',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APITrafficShaping_v1(GeneratedTrafficShaping, TrafficShapingTransformMixin_v1):
    """Versioned API model for Meraki appliance traffic shaping (v1)."""

    _field_mapping = {
        'default_rules_enabled': 'defaultRulesEnabled',
        'default_uplink': 'defaultUplink',
        'rules': 'rules',
        'bandwidth_limits': 'bandwidthLimits',
        'global_bandwidth_limits': 'globalBandwidthLimits',
        'failover_and_failback': 'failoverAndFailback',
        'load_balancing_enabled': 'loadBalancingEnabled',
        'active_active_auto_vpn_enabled': 'activeActiveAutoVpnEnabled',
        'vpn_traffic_uplink_preferences': 'vpnTrafficUplinkPreferences',
        'wan_traffic_uplink_preferences': 'wanTrafficUplinkPreferences',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.traffic_shaping import UserTrafficShaping
        return UserTrafficShaping
