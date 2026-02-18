"""User model for Meraki wireless Ethernet port profile."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserEthernetPortProfile(BaseTransformMixin):
    """User-facing Ethernet port profile model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    profile_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    ports: Optional[List[Dict[str, Any]]] = None
    usb_ports: Optional[List[Dict[str, Any]]] = None
    is_default: Optional[bool] = None
    serials: Optional[List[str]] = None

    _field_mapping = {
        'profile_id': 'profileId',
        'name': 'name',
        'ports': 'ports',
        'usb_ports': 'usbPorts',
        'is_default': 'isDefault',
        'serials': 'serials',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.ethernet_port_profile import APIEthernetPortProfile_v1
        return APIEthernetPortProfile_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
