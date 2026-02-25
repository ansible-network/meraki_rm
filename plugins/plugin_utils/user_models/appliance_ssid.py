"""User model for Meraki appliance SSID."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserApplianceSsid(BaseTransformMixin):
    """User-facing appliance SSID model with snake_case fields."""

    MODULE_NAME = 'appliance_ssid'
    SUPPORTS_DELETE = False

    # scope
    network_id: Optional[str] = None
    # identity
    number: Optional[int] = field(default=None, metadata={"description": "SSID number (0-4). Required for merged, replaced."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Name of the SSID."})
    enabled: Optional[bool] = field(default=None, metadata={"description": "Whether the SSID is enabled."})
    auth_mode: Optional[str] = field(default=None, metadata={"description": "Association control method."})
    encryption_mode: Optional[str] = field(default=None, metadata={"description": "PSK encryption mode."})
    psk: Optional[str] = field(default=None, metadata={"description": "Passkey (auth_mode is psk)."})
    default_vlan_id: Optional[int] = field(default=None, metadata={"description": "VLAN ID associated with this SSID."})
    visible: Optional[bool] = field(default=None, metadata={"description": "Whether to advertise or hide this SSID."})
    wpa_encryption_mode: Optional[str] = field(default=None, metadata={"description": "WPA encryption mode."})
    radius_servers: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "RADIUS 802.1x servers for authentication."})

    _field_mapping = {
        'number': 'number',
        'name': 'name',
        'enabled': 'enabled',
        'auth_mode': 'authMode',
        'encryption_mode': 'encryptionMode',
        'psk': 'psk',
        'default_vlan_id': 'defaultVlanId',
        'visible': 'visible',
        'wpa_encryption_mode': 'wpaEncryptionMode',
        'radius_servers': 'radiusServers',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.appliance_ssid import APIApplianceSsid_v1
        return APIApplianceSsid_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
