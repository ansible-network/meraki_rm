"""Generated API dataclass for Meraki wireless wireless_rf_profile.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/wireless/rfProfiles
    /networks/{networkId}/wireless/rfProfiles/{rfProfileId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class WirelessRfProfile:
    """Meraki wireless wireless_rf_profile API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # Settings that will be enabled if selectionType is set to 'ap'.
    apBandSettings: Optional[Dict[str, Any]] = None
    # Band selection can be set to either 'ssid' or 'ap'. This param is require...
    bandSelectionType: Optional[str] = None
    # Steers client to best available access point. Can be either true or false...
    clientBalancingEnabled: Optional[bool] = None
    # Settings related to 5Ghz band
    fiveGhzSettings: Optional[Dict[str, Any]] = None
    # Flex radio settings.
    flexRadios: Optional[Dict[str, Any]] = None
    # The name of the new profile. Must be unique.
    id: Optional[str] = None
    # Set this profile as the default indoor rf profile. If the profile ID is o...
    isIndoorDefault: Optional[bool] = None
    # Set this profile as the default outdoor rf profile. If the profile ID is ...
    isOutdoorDefault: Optional[bool] = None
    # Minimum bitrate can be set to either 'band' or 'ssid'. Defaults to band.
    minBitrateType: Optional[str] = None
    # The name of the new profile. Must be unique. This param is required on cr...
    name: Optional[str] = None
    # The network ID of the RF Profile
    networkId: Optional[str] = None
    # Per-SSID radio settings by number.
    perSsidSettings: Optional[Dict[str, Any]] = None
    # Settings related to 6Ghz band. Only applicable to networks with 6Ghz capa...
    sixGhzSettings: Optional[Dict[str, Any]] = None
    # Settings related to radio transmission.
    transmission: Optional[Dict[str, Any]] = None
    # Settings related to 2.4Ghz band
    twoFourGhzSettings: Optional[Dict[str, Any]] = None
