"""User model for Meraki appliance traffic shaping."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserTrafficShaping(BaseTransformMixin):
    """User-facing traffic shaping model with snake_case fields."""

    MODULE_NAME = 'traffic_shaping'
    SUPPORTS_DELETE = False

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    default_rules_enabled: Optional[bool] = field(default=None, metadata={"description": "Whether default traffic shaping rules are enabled."})
    default_uplink: Optional[str] = field(default=None, metadata={"description": "The default uplink (e.g., wan1, wan2)."})
    rules: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "Array of traffic shaping rules."})
    bandwidth_limits: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Uplink bandwidth limits by interface."})
    global_bandwidth_limits: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Global per-client bandwidth limit."})
    failover_and_failback: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "WAN failover and failback settings."})
    load_balancing_enabled: Optional[bool] = field(default=None, metadata={"description": "Whether load balancing is enabled."})
    active_active_auto_vpn_enabled: Optional[bool] = field(default=None, metadata={"description": "Whether active-active AutoVPN is enabled."})
    vpn_traffic_uplink_preferences: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "Uplink preference rules for VPN traffic."})
    wan_traffic_uplink_preferences: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "Uplink preference rules for WAN traffic."})

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
