"""User model for Meraki switch settings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchSettings(BaseTransformMixin):
    """User-facing switch settings model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    default_mtu_size: Optional[int] = None
    overrides: Optional[List[Dict[str, Any]]] = None
    broadcast_threshold: Optional[int] = None
    multicast_threshold: Optional[int] = None
    unknown_unicast_threshold: Optional[int] = None
    mappings: Optional[List[Dict[str, Any]]] = None
    use_combined_power: Optional[bool] = None
    power_exceptions: Optional[List[Dict[str, Any]]] = None
    enabled: Optional[bool] = None
    vlan_id: Optional[int] = None
    switches: Optional[List[Dict[str, Any]]] = None
    protocols: Optional[List[str]] = None

    _field_mapping = {
        'default_mtu_size': 'defaultMtuSize',
        'overrides': 'overrides',
        'broadcast_threshold': 'broadcastThreshold',
        'multicast_threshold': 'multicastThreshold',
        'unknown_unicast_threshold': 'unknownUnicastThreshold',
        'mappings': 'mappings',
        'use_combined_power': 'useCombinedPower',
        'power_exceptions': 'powerExceptions',
        'enabled': 'enabled',
        'vlan_id': 'vlanId',
        'switches': 'switches',
        'protocols': 'protocols',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.switch_settings import APISwitchSettings_v1
        return APISwitchSettings_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
