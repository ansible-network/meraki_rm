"""User model for Meraki switch settings."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchSettings(BaseTransformMixin):
    """User-facing switch settings model with snake_case fields."""

    MODULE_NAME = 'switch_settings'
    SUPPORTS_DELETE = False

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    default_mtu_size: Optional[int] = field(default=None, metadata={"description": "MTU size for the entire network."})
    overrides: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "Override MTU for individual switches."})
    broadcast_threshold: Optional[int] = field(default=None, metadata={"description": "Broadcast storm control threshold."})
    multicast_threshold: Optional[int] = field(default=None, metadata={"description": "Multicast storm control threshold."})
    unknown_unicast_threshold: Optional[int] = field(default=None, metadata={"description": "Unknown unicast storm control threshold."})
    mappings: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "DSCP to CoS mappings."})
    use_combined_power: Optional[bool] = field(default=None, metadata={"description": "Use combined power for secondary power supplies."})
    power_exceptions: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "Per-switch power exceptions."})
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
