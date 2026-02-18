"""User model for Meraki appliance port."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserPort(BaseTransformMixin):
    """User-facing port model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    port_id: Optional[str] = None
    # fields
    enabled: Optional[bool] = None
    type: Optional[str] = None
    vlan: Optional[int] = None
    allowed_vlans: Optional[str] = None
    access_policy: Optional[str] = None
    drop_untagged_traffic: Optional[bool] = None

    _field_mapping = {
        'port_id': 'number',
        'enabled': 'enabled',
        'type': 'type',
        'vlan': 'vlan',
        'allowed_vlans': 'allowedVlans',
        'access_policy': 'accessPolicy',
        'drop_untagged_traffic': 'dropUntaggedTraffic',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.port import APIPort_v1
        return APIPort_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
