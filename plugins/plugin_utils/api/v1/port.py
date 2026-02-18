"""Versioned API model and transform mixin for Meraki appliance port (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.port import Port as GeneratedPort

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'portId': ['port_id', 'number'],
}

# Mutable fields for update (read/update only - no create/delete)
_UPDATE_FIELDS = [
    'enabled', 'type', 'vlan', 'allowedVlans',
    'accessPolicy', 'dropUntaggedTraffic',
]


class PortTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki appliance port (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find': EndpointOperation(
                path='/networks/{networkId}/appliance/ports/{portId}',
                method='GET',
                fields=[],
                path_params=['networkId', 'portId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/appliance/ports',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/appliance/ports/{portId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'portId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APIPort_v1(GeneratedPort, PortTransformMixin_v1):
    """Versioned API model for Meraki appliance port (v1)."""

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
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.port import UserPort
        return UserPort
