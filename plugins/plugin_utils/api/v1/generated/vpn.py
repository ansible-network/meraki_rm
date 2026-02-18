"""Generated API dataclass for Meraki appliance vpn.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/appliance/vpn/bgp
    /networks/{networkId}/appliance/vpn/siteToSiteVpn
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Vpn:
    """Meraki appliance vpn API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # The number of the Autonomous System to which the appliance belongs
    asNumber: Optional[int] = None
    # Whether BGP is enabled on the appliance
    enabled: Optional[bool] = None
    # The list of VPN hubs, in order of preference.
    hubs: Optional[List[Dict[str, Any]]] = None
    # The iBGP hold time in seconds
    ibgpHoldTimer: Optional[int] = None
    # The site-to-site VPN mode.
    mode: Optional[str] = None
    # List of eBGP neighbor configurations
    neighbors: Optional[List[Dict[str, Any]]] = None
    # Configuration of subnet features
    subnet: Optional[Dict[str, Any]] = None
    # The list of subnets and their VPN presence.
    subnets: Optional[List[Dict[str, Any]]] = None
