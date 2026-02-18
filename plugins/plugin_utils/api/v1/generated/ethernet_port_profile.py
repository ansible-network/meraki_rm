"""Generated API dataclass for Meraki wireless ethernet_port_profile.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/wireless/ethernet/ports/profiles
    /networks/{networkId}/wireless/ethernet/ports/profiles/assign
    /networks/{networkId}/wireless/ethernet/ports/profiles/setDefault
    /networks/{networkId}/wireless/ethernet/ports/profiles/{profileId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class EthernetPortProfile:
    """Meraki wireless ethernet_port_profile API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # Is default profile
    isDefault: Optional[bool] = None
    # AP port profile name
    name: Optional[str] = None
    # Ports config
    ports: Optional[List[Dict[str, Any]]] = None
    # AP port profile ID
    profileId: Optional[str] = None
    # List of AP serials
    serials: Optional[List[str]] = None
    # Usb ports config
    usbPorts: Optional[List[Dict[str, Any]]] = None
