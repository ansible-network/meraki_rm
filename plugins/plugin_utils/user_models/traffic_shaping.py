"""User model for Meraki appliance traffic shaping."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserTrafficShaping(BaseTransformMixin):
    """User-facing traffic shaping model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    default_rules_enabled: Optional[bool] = None
    default_uplink: Optional[str] = None
    rules: Optional[List[Dict[str, Any]]] = None
    bandwidth_limits: Optional[Dict[str, Any]] = None
    global_bandwidth_limits: Optional[Dict[str, Any]] = None
    failover_and_failback: Optional[Dict[str, Any]] = None
    load_balancing_enabled: Optional[bool] = None
    active_active_auto_vpn_enabled: Optional[bool] = None
    vpn_traffic_uplink_preferences: Optional[List[Dict[str, Any]]] = None
    wan_traffic_uplink_preferences: Optional[List[Dict[str, Any]]] = None

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
        from ..api.v1.traffic_shaping import APITrafficShaping_v1
        return APITrafficShaping_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
