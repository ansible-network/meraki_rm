"""Generated API dataclass for Meraki organization org_vpn.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /organizations/{organizationId}/appliance/vpn/siteToSite/ipsec/peers/slas
    /organizations/{organizationId}/appliance/vpn/stats
    /organizations/{organizationId}/appliance/vpn/statuses
    /organizations/{organizationId}/appliance/vpn/thirdPartyVPNPeers
    /organizations/{organizationId}/appliance/vpn/vpnFirewallRules
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class OrgVpn:
    """Meraki organization org_vpn API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # Serial number of the device
    deviceSerial: Optional[str] = None
    # Device Status
    deviceStatus: Optional[str] = None
    # List of Exported Subnets
    exportedSubnets: Optional[List[Dict[str, Any]]] = None
    # List of the IPSec SLA policies for an organization
    items: Optional[List[Dict[str, Any]]] = None
    # List of VPN peers with their summaries
    merakiVpnPeers: Optional[List[Dict[str, Any]]] = None
    # Metadata relevant to the paginated dataset
    meta: Optional[Dict[str, Any]] = None
    # Network ID
    networkId: Optional[str] = None
    # Network name
    networkName: Optional[str] = None
    # The list of VPN peers
    peers: Optional[List[Dict[str, Any]]] = None
    # An ordered array of the firewall rules (not including the default rule)
    rules: Optional[List[Dict[str, Any]]] = None
    # Log the special default rule (boolean value - enable only if you've confi...
    syslogDefaultRule: Optional[bool] = None
    # Third Party VPN Peers
    thirdPartyVpnPeers: Optional[List[Dict[str, Any]]] = None
    # List of Uplink Information
    uplinks: Optional[List[Dict[str, Any]]] = None
    # VPN Mode
    vpnMode: Optional[str] = None
