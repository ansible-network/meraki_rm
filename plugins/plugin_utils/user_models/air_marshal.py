"""User model for Meraki wireless Air Marshal."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserAirMarshal(BaseTransformMixin):
    """User-facing Air Marshal model with snake_case fields."""

    MODULE_NAME = 'air_marshal'
    SYSTEM_KEY = 'rule_id'
    VALID_STATES = frozenset({'merged', 'replaced', 'deleted'})

    # scope
    network_id: Optional[str] = None
    # identity
    rule_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned rule ID. Discover via C(state=gathered)."})
    # fields
    type: Optional[str] = field(default=None, metadata={"description": "Rule type (allow, block, or alert)."})
    match: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Rule specification/match criteria."})
    default_policy: Optional[str] = field(default=None, metadata={"description": "Default policy for rogue networks."})
    ssid: Optional[str] = field(default=None, metadata={"description": "SSID name for the rule."})
    bssids: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "BSSIDs broadcasting the SSID."})
    channels: Optional[List[int]] = field(default=None, metadata={"description": "Channels where SSID was observed."})
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
