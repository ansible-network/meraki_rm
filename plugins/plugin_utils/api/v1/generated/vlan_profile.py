"""Generated API dataclass for Meraki network vlan_profile.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/vlanProfiles
    /networks/{networkId}/vlanProfiles/assignments/byDevice
    /networks/{networkId}/vlanProfiles/assignments/reassign
    /networks/{networkId}/vlanProfiles/{iname}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class VlanProfile:
    """Meraki network vlan_profile API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # IName of the VLAN profile
    iname: Optional[str] = None
    # Boolean indicating the default VLAN Profile for any device that does not ...
    isDefault: Optional[bool] = None
    # MAC address of the device
    mac: Optional[str] = None
    # Name of the profile, string length must be from 1 to 255 characters
    name: Optional[str] = None
    # The product type
    productType: Optional[str] = None
    # Serial of the Device
    serial: Optional[str] = None
    # Array of Device Serials
    serials: Optional[List[str]] = None
    # The Switch Stack the device belongs to
    stack: Optional[Dict[str, Any]] = None
    # Array of Switch Stack IDs
    stackIds: Optional[List[str]] = None
    # An array of named VLANs
    vlanGroups: Optional[List[Dict[str, Any]]] = None
    # An array of named VLANs
    vlanNames: Optional[List[Dict[str, Any]]] = None
    # The VLAN Profile
    vlanProfile: Optional[Dict[str, Any]] = None
