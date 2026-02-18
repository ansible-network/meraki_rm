"""Generated API dataclass for Meraki appliance warm_spare.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/appliance/warmSpare
    /networks/{networkId}/appliance/warmSpare/swap
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class WarmSpare:
    """Meraki appliance warm_spare API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # Is the warm spare enabled
    enabled: Optional[bool] = None
    # Serial number of the primary appliance
    primarySerial: Optional[str] = None
    # Serial number of the warm spare appliance
    spareSerial: Optional[str] = None
    # Uplink mode, either virtual or public
    uplinkMode: Optional[str] = None
    # The WAN 1 shared IP
    virtualIp1: Optional[str] = None
    # The WAN 2 shared IP
    virtualIp2: Optional[str] = None
    # WAN 1 IP and subnet
    wan1: Optional[Dict[str, Any]] = None
    # WAN 2 IP and subnet
    wan2: Optional[Dict[str, Any]] = None
