"""User model for Meraki appliance VPN."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserVpn(BaseTransformMixin):
    """User-facing VPN model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    mode: Optional[str] = None
    hubs: Optional[List[Dict[str, Any]]] = None
    subnets: Optional[List[Dict[str, Any]]] = None
    subnet: Optional[Dict[str, Any]] = None
    enabled: Optional[bool] = None
    as_number: Optional[int] = None
    ibgp_hold_timer: Optional[int] = None
    neighbors: Optional[List[Dict[str, Any]]] = None

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
