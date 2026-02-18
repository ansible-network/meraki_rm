"""Generated API dataclass for Meraki appliance traffic_shaping.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/appliance/trafficShaping
    /networks/{networkId}/appliance/trafficShaping/customPerformanceClasses
    /networks/{networkId}/appliance/trafficShaping/customPerformanceClasses/{customPerformanceClassId}
    /networks/{networkId}/appliance/trafficShaping/rules
    /networks/{networkId}/appliance/trafficShaping/uplinkBandwidth
    /networks/{networkId}/appliance/trafficShaping/uplinkSelection
    /networks/{networkId}/appliance/trafficShaping/vpnExclusions
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TrafficShaping:
    """Meraki appliance traffic_shaping API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # ID of the network whose VPN exclusion rules are returned.
    networkId: Optional[str] = None
    # Name of the network whose VPN exclusion rules are returned.
    networkName: Optional[str] = None
    # Whether active-active AutoVPN is enabled
    activeActiveAutoVpnEnabled: Optional[bool] = None
    # A hash uplink keys and their configured settings for the Appliance
    bandwidthLimits: Optional[Dict[str, Any]] = None
    # Custom VPN exclusion rules. Pass an empty array to clear existing rules.
    custom: Optional[List[Dict[str, Any]]] = None
    # ID of the custom performance class
    customPerformanceClassId: Optional[str] = None
    # Whether default traffic shaping rules are enabled (true) or disabled (fal...
    defaultRulesEnabled: Optional[bool] = None
    # The default uplink. Must be a WAN interface 'wanX'
    defaultUplink: Optional[str] = None
    # WAN failover and failback
    failoverAndFailback: Optional[Dict[str, Any]] = None
    # Global per-client bandwidth limit
    globalBandwidthLimits: Optional[Dict[str, Any]] = None
    # Whether load balancing is enabled
    loadBalancingEnabled: Optional[bool] = None
    # Major Application based VPN exclusion rules. Pass an empty array to clear...
    majorApplications: Optional[List[Dict[str, Any]]] = None
    # Maximum jitter in milliseconds
    maxJitter: Optional[int] = None
    # Maximum latency in milliseconds
    maxLatency: Optional[int] = None
    # Maximum percentage of packet loss
    maxLossPercentage: Optional[int] = None
    # Name of the custom performance class
    name: Optional[str] = None
    # An array of traffic shaping rules. Rules are applied in the order that   ...
    rules: Optional[List[Dict[str, Any]]] = None
    # Uplink preference rules for VPN traffic
    vpnTrafficUplinkPreferences: Optional[List[Dict[str, Any]]] = None
    # Uplink preference rules for WAN traffic
    wanTrafficUplinkPreferences: Optional[List[Dict[str, Any]]] = None
