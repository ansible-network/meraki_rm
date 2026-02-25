"""User model for Meraki wireless Ethernet port profile."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserEthernetPortProfile(BaseTransformMixin):
    """User-facing Ethernet port profile model with snake_case fields."""

    MODULE_NAME = 'ethernet_port_profile'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'profile_id'

    # scope
    network_id: Optional[str] = None
    # identity
    profile_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "AP port profile name."})
    ports: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "Ports configuration."})
    usb_ports: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "USB ports configuration."})
    is_default: Optional[bool] = field(default=None, metadata={"description": "Whether this is the default profile."})
    serials: Optional[List[str]] = field(default=None, metadata={"description": "List of AP serials to assign."})

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
