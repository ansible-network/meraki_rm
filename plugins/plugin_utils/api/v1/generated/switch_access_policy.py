"""Generated API dataclass for Meraki switch switch_access_policy.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/switch/accessPolicies
    /networks/{networkId}/switch/accessPolicies/{accessPolicyNumber}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional


@dataclass
class SwitchAccessPolicy:
    """Meraki switch switch_access_policy API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    _FIELD_CONSTRAINTS: ClassVar[dict] = {
        'accessPolicyType': {'enum': ['802.1x', 'Hybrid authentication', 'MAC authentication bypass']},
        'hostMode': {'enum': ['Multi-Auth', 'Multi-Domain', 'Multi-Host', 'Single-Host']},
    }

    # Access policy number is used to identify the access policy within the net...
    accessPolicyNumber: Optional[str] = None
    # Access Type of the policy. Automatically 'Hybrid authentication' when hos...
    accessPolicyType: Optional[str] = None
    # Counts associated with the access policy
    counts: Optional[Dict[str, Any]] = None
    # 802.1x Settings
    dot1x: Optional[Dict[str, Any]] = None
    # This is a readonly flag, indicating whether the access policy was under h...
    enforceRadiusMonitoring: Optional[bool] = None
    # Group policy Number for guest group policy (Requires MS 18 or higher)
    guestGroupPolicyId: Optional[str] = None
    # If enabled, Meraki devices will periodically send access-request messages...
    guestPortBouncing: Optional[bool] = None
    # Security Group Tag ID for guest group policy (Requires MS 18 or higher)
    guestSgtId: Optional[int] = None
    # ID for the guest VLAN allow unauthorized devices access to limited networ...
    guestVlanId: Optional[int] = None
    # Choose the Host Mode for the access policy.
    hostMode: Optional[str] = None
    # Enabling this option will make switches execute 802.1X and MAC-bypass aut...
    increaseAccessSpeed: Optional[bool] = None
    # Name of the access policy
    name: Optional[str] = None
    # Object for RADIUS Settings
    radius: Optional[Dict[str, Any]] = None
    # Enable to send start, interim-update and stop messages to a configured RA...
    radiusAccountingEnabled: Optional[bool] = None
    # List of RADIUS accounting servers to require connecting devices to authen...
    radiusAccountingServers: Optional[List[Dict[str, Any]]] = None
    # Change of authentication for RADIUS re-authentication and disconnection
    radiusCoaSupportEnabled: Optional[bool] = None
    # Acceptable values are `""` for None, or `"11"` for Group Policies ACL
    radiusGroupAttribute: Optional[str] = None
    # List of RADIUS servers to require connecting devices to authenticate agai...
    radiusServers: Optional[List[Dict[str, Any]]] = None
    # If enabled, Meraki devices will periodically send access-request messages...
    radiusTestingEnabled: Optional[bool] = None
    # Enable to restrict access for clients to a response_objectific set of IP ...
    urlRedirectWalledGardenEnabled: Optional[bool] = None
    # IP address ranges, in CIDR notation, to restrict access for clients to a ...
    urlRedirectWalledGardenRanges: Optional[List[str]] = None
    # CDP/LLDP capable voice clients will be able to use this VLAN. Automatical...
    voiceVlanClients: Optional[bool] = None
