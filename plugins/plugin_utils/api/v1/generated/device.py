"""Generated API dataclass for Meraki device device.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /devices/{serial}
    /organizations/{organizationId}/inventory/devices/{serial}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Device:
    """Meraki device device API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # Physical address of the device
    address: Optional[str] = None
    # Beacon Id parameters with an identifier and major and minor versions
    beaconIdParams: Optional[Dict[str, Any]] = None
    # Claimed time of the device
    claimedAt: Optional[str] = None
    # Country/region code from device, network, or store order
    countryCode: Optional[str] = None
    # Additional device information
    details: Optional[List[Dict[str, Any]]] = None
    # End of life information for the device
    eox: Optional[Dict[str, Any]] = None
    # Firmware version of the device
    firmware: Optional[str] = None
    # The floor plan to associate to this device. null disassociates the device...
    floorPlanId: Optional[str] = None
    # LAN IP address of the device
    lanIp: Optional[str] = None
    # Latitude of the device
    lat: Optional[float] = None
    # License expiration date of the device
    licenseExpirationDate: Optional[str] = None
    # Longitude of the device
    lng: Optional[float] = None
    # MAC address of the device
    mac: Optional[str] = None
    # Model of the device
    model: Optional[str] = None
    # Whether or not to set the latitude and longitude of a device based on the...
    moveMapMarker: Optional[bool] = None
    # Name of the device
    name: Optional[str] = None
    # ID of the network the device belongs to
    networkId: Optional[str] = None
    # Notes for the device, limited to 255 characters
    notes: Optional[str] = None
    # Order number of the device
    orderNumber: Optional[str] = None
    # Product type of the device
    productType: Optional[str] = None
    # Serial number of the device
    serial: Optional[str] = None
    # The ID of a switch template to bind to the device (for available switch t...
    switchProfileId: Optional[str] = None
    # List of tags assigned to the device
    tags: Optional[List[str]] = None
