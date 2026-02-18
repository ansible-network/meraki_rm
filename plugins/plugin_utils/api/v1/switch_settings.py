"""Versioned API model and transform mixin for Meraki switch settings (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.switch_settings import SwitchSettings as GeneratedSwitchSettings

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
}

# Mutable fields for update (singleton - consolidated settings)
_UPDATE_FIELDS = [
    'defaultMtuSize', 'overrides', 'broadcastThreshold', 'multicastThreshold',
    'unknownUnicastThreshold', 'mappings', 'useCombinedPower', 'powerExceptions',
    'enabled', 'vlanId', 'switches', 'protocols',
]


class SwitchSettingsTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki switch settings (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find': EndpointOperation(
                path='/networks/{networkId}/switch/settings',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/switch/settings',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APISwitchSettings_v1(GeneratedSwitchSettings, SwitchSettingsTransformMixin_v1):
    """Versioned API model for Meraki switch settings (v1)."""

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
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.switch_settings import UserSwitchSettings
        return UserSwitchSettings
