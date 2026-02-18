"""User model for Meraki wireless Air Marshal."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserAirMarshal(BaseTransformMixin):
    """User-facing Air Marshal model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    rule_id: Optional[str] = None
    # fields
    type: Optional[str] = None
    match: Optional[Dict[str, Any]] = None
    default_policy: Optional[str] = None
    ssid: Optional[str] = None
    bssids: Optional[List[Dict[str, Any]]] = None
    channels: Optional[List[int]] = None
    first_seen: Optional[int] = None
    last_seen: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    _field_mapping = {
        'rule_id': 'ruleId',
        'type': 'type',
        'match': 'match',
        'default_policy': 'defaultPolicy',
        'ssid': 'ssid',
        'bssids': 'bssids',
        'channels': 'channels',
        'first_seen': 'firstSeen',
        'last_seen': 'lastSeen',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.air_marshal import APIAirMarshal_v1
        return APIAirMarshal_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
