"""Generated API dataclass for Meraki appliance appliance_ssid.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/appliance/ssids
    /networks/{networkId}/appliance/ssids/{number}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional


@dataclass
class ApplianceSsid:
    """Meraki appliance appliance_ssid API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    _FIELD_CONSTRAINTS: ClassVar[dict] = {
        'authMode': {'enum': ['8021x-meraki', '8021x-radius', 'open', 'psk']},
        'encryptionMode': {'enum': ['wep', 'wpa']},
        'wpaEncryptionMode': {'enum': ['WPA1 and WPA2', 'WPA2 only', 'WPA3 Transition Mode', 'WPA3 only']},
    }

    # The association control method for the SSID.
    authMode: Optional[str] = None
    # The VLAN ID of the VLAN associated to this SSID.
    defaultVlanId: Optional[int] = None
    # DHCP Enforced Deauthentication enables the disassociation of wireless cli...
    dhcpEnforcedDeauthentication: Optional[Dict[str, Any]] = None
    # The current setting for Protected Management Frames (802.11w).
    dot11w: Optional[Dict[str, Any]] = None
    # Whether or not the SSID is enabled.
    enabled: Optional[bool] = None
    # The psk encryption mode for the SSID.
    encryptionMode: Optional[str] = None
    # The name of the SSID.
    name: Optional[str] = None
    # The number of the SSID.
    number: Optional[int] = None
    # The passkey for the SSID. This param is only valid if the authMode is 'psk'.
    psk: Optional[str] = None
    # The RADIUS 802.1x servers to be used for authentication.
    radiusServers: Optional[List[Dict[str, Any]]] = None
    # Boolean indicating whether the MX should advertise or hide this SSID.
    visible: Optional[bool] = None
    # WPA encryption mode for the SSID.
    wpaEncryptionMode: Optional[str] = None
