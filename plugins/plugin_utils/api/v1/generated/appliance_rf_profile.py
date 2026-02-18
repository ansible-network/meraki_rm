"""Generated API dataclass for Meraki appliance appliance_rf_profile.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/appliance/rfProfiles
    /networks/{networkId}/appliance/rfProfiles/{rfProfileId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ApplianceRfProfile:
    """Meraki appliance appliance_rf_profile API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # RF Profiles
    assigned: Optional[List[Dict[str, Any]]] = None
    # Settings related to 5Ghz band
    fiveGhzSettings: Optional[Dict[str, Any]] = None
    # ID of the RF Profile.
    id: Optional[str] = None
    # The name of the new profile. Must be unique. This param is required on cr...
    name: Optional[str] = None
    # ID of network this RF Profile belongs in.
    networkId: Optional[str] = None
    # Per-SSID radio settings by number.
    perSsidSettings: Optional[Dict[str, Any]] = None
    # Settings related to 2.4Ghz band
    twoFourGhzSettings: Optional[Dict[str, Any]] = None
