"""User model for Meraki appliance VPN."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserVpn(BaseTransformMixin):
    """User-facing VPN model with snake_case fields."""

    MODULE_NAME = 'vpn'
    SUPPORTS_DELETE = False

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    mode: Optional[str] = field(default=None, metadata={"description": "Site-to-site VPN mode."})
    hubs: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "List of VPN hubs, in order of preference."})
    subnets: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "List of subnets and their VPN presence."})
    subnet: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Configuration of subnet features."})
    enabled: Optional[bool] = field(default=None, metadata={"description": "Whether VPN is enabled."})
    as_number: Optional[int] = field(default=None, metadata={"description": "BGP autonomous system number."})
    ibgp_hold_timer: Optional[int] = field(default=None, metadata={"description": "iBGP hold time in seconds."})
    neighbors: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "List of eBGP neighbor configurations."})

    _field_mapping = {
        'mode': 'mode',
        'hubs': 'hubs',
        'subnets': 'subnets',
        'subnet': 'subnet',
        'enabled': 'enabled',
        'as_number': 'asNumber',
        'ibgp_hold_timer': 'ibgpHoldTimer',
        'neighbors': 'neighbors',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.vpn import APIVpn_v1
        return APIVpn_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
