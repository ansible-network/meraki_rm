"""Generated API dataclass for Meraki appliance firewall.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/appliance/firewall/cellularFirewallRules
    /networks/{networkId}/appliance/firewall/firewalledServices
    /networks/{networkId}/appliance/firewall/firewalledServices/{service}
    /networks/{networkId}/appliance/firewall/inboundCellularFirewallRules
    /networks/{networkId}/appliance/firewall/inboundFirewallRules
    /networks/{networkId}/appliance/firewall/l3FirewallRules
    /networks/{networkId}/appliance/firewall/l7FirewallRules
    /networks/{networkId}/appliance/firewall/l7FirewallRules/applicationCategories
    /networks/{networkId}/appliance/firewall/multicastForwarding
    /networks/{networkId}/appliance/firewall/oneToManyNatRules
    /networks/{networkId}/appliance/firewall/oneToOneNatRules
    /networks/{networkId}/appliance/firewall/portForwardingRules
    /networks/{networkId}/appliance/firewall/settings
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Firewall:
    """Meraki appliance firewall API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # Network details
    network: Optional[Dict[str, Any]] = None
    # A string indicating the rule for which IPs are allowed to use the specifi...
    access: Optional[str] = None
    # An array of allowed CIDRs that can access the service
    allowedIps: Optional[List[str]] = None
    # The L7 firewall application categories and their associated applications ...
    applicationCategories: Optional[List[Dict[str, Any]]] = None
    # An ordered array of the firewall rules (not including the default rule)
    rules: Optional[List[Dict[str, Any]]] = None
    # Appliance service name
    service: Optional[str] = None
    # Spoofing protection settings
    spoofingProtection: Optional[Dict[str, Any]] = None
    # Log the special default rule (boolean value - enable only if you've confi...
    syslogDefaultRule: Optional[bool] = None
