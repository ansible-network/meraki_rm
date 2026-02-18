"""Generated API dataclass for Meraki switch switch_dhcp_policy.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/switch/dhcpServerPolicy
    /networks/{networkId}/switch/dhcpServerPolicy/arpInspection/trustedServers
    /networks/{networkId}/switch/dhcpServerPolicy/arpInspection/trustedServers/{trustedServerId}
    /networks/{networkId}/switch/dhcpServerPolicy/arpInspection/warnings/byDevice
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional


@dataclass
class SwitchDhcpPolicy:
    """Meraki switch switch_dhcp_policy API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    _FIELD_CONSTRAINTS: ClassVar[dict] = {
        'defaultPolicy': {'enum': ['allow', 'block']},
    }

    # Email alert settings for DHCP servers
    alerts: Optional[Dict[str, Any]] = None
    # List the MAC addresses of DHCP servers to permit on the network when defa...
    allowedServers: Optional[List[str]] = None
    # List the MAC addresses of DHCP servers that are always allowed on the net...
    alwaysAllowedServers: Optional[List[str]] = None
    # Dynamic ARP Inspection settings
    arpInspection: Optional[Dict[str, Any]] = None
    # List the MAC addresses of DHCP servers to block on the network when defau...
    blockedServers: Optional[List[str]] = None
    # 'allow' or 'block' new DHCP servers. Default value is 'allow'.
    defaultPolicy: Optional[str] = None
    # Whether this switch has a trusted DAI port. Always false if supportsInspe...
    hasTrustedPort: Optional[bool] = None
    # IPv4 attributes of the trusted server.
    ipv4: Optional[Dict[str, Any]] = None
    # Mac address of the trusted server.
    mac: Optional[str] = None
    # Switch name.
    name: Optional[str] = None
    # Switch serial.
    serial: Optional[str] = None
    # Whether this switch supports Dynamic ARP Inspection.
    supportsInspection: Optional[bool] = None
    # ID of the trusted server.
    trustedServerId: Optional[str] = None
    # Url link to switch.
    url: Optional[str] = None
    # Vlan ID of the trusted server.
    vlan: Optional[int] = None
