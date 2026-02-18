"""Generated API dataclass for Meraki appliance port.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/appliance/ports
    /networks/{networkId}/appliance/ports/{portId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Port:
    """Meraki appliance port API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # The name of the policy. Only applicable to Access ports.
    accessPolicy: Optional[str] = None
    # Comma-delimited list of the VLAN ID's allowed on the port, or 'all' to pe...
    allowedVlans: Optional[str] = None
    # Whether the trunk port can drop all untagged traffic.
    dropUntaggedTraffic: Optional[bool] = None
    # The status of the port
    enabled: Optional[bool] = None
    # Number of the port
    number: Optional[int] = None
    # The type of the port: 'access' or 'trunk'.
    type: Optional[str] = None
    # Native VLAN when the port is in Trunk mode. Access VLAN when the port is ...
    vlan: Optional[int] = None
