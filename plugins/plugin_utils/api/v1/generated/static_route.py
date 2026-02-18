"""Generated API dataclass for Meraki appliance static_route.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/appliance/staticRoutes
    /networks/{networkId}/appliance/staticRoutes/{staticRouteId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class StaticRoute:
    """Meraki appliance static_route API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # Whether the route is enabled or not
    enabled: Optional[bool] = None
    # Fixed DHCP IP assignments on the route
    fixedIpAssignments: Optional[Dict[str, Dict[str, Any]]] = None
    # Gateway IP address (next hop)
    gatewayIp: Optional[str] = None
    # Gateway VLAN ID
    gatewayVlanId: Optional[int] = None
    # Route ID
    id: Optional[str] = None
    # IP protocol version
    ipVersion: Optional[int] = None
    # Name of the route
    name: Optional[str] = None
    # Network ID
    networkId: Optional[str] = None
    # DHCP reserved IP ranges
    reservedIpRanges: Optional[List[Dict[str, Any]]] = None
    # Subnet of the route
    subnet: Optional[str] = None
