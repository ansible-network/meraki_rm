"""User model for Meraki appliance SSID."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserApplianceSsid(BaseTransformMixin):
    """User-facing appliance SSID model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    number: Optional[int] = None
    # fields
    name: Optional[str] = None
    enabled: Optional[bool] = None
    auth_mode: Optional[str] = None
    encryption_mode: Optional[str] = None
    psk: Optional[str] = None
    default_vlan_id: Optional[int] = None
    visible: Optional[bool] = None
    wpa_encryption_mode: Optional[str] = None
    radius_servers: Optional[List[Dict[str, Any]]] = None

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
