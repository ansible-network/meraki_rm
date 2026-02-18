"""Generated API dataclass for Meraki camera camera_wireless_profile.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/camera/wirelessProfiles
    /networks/{networkId}/camera/wirelessProfiles/{wirelessProfileId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class CameraWirelessProfile:
    """Meraki camera camera_wireless_profile API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # The count of the applied devices.
    appliedDeviceCount: Optional[int] = None
    # The ID of the camera wireless profile.
    id: Optional[str] = None
    # The identity of the wireless profile. Required for creating wireless prof...
    identity: Optional[Dict[str, Any]] = None
    # The name of the camera wireless profile.
    name: Optional[str] = None
    # The details of the SSID config.
    ssid: Optional[Dict[str, Any]] = None
