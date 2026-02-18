"""Versioned API model and transform mixin for Meraki appliance warm spare (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.warm_spare import WarmSpare as GeneratedWarmSpare

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
}

# Mutable fields for update (singleton - no create/delete)
_UPDATE_FIELDS = [
    'enabled', 'spareSerial', 'uplinkMode', 'virtualIp1', 'virtualIp2',
    'wan1', 'wan2', 'primarySerial',
]


class WarmSpareTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki appliance warm spare (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find': EndpointOperation(
                path='/networks/{networkId}/appliance/warmSpare',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/appliance/warmSpare',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APIWarmSpare_v1(GeneratedWarmSpare, WarmSpareTransformMixin_v1):
    """Versioned API model for Meraki appliance warm spare (v1)."""

    _field_mapping = {
        'enabled': 'enabled',
        'spare_serial': 'spareSerial',
        'uplink_mode': 'uplinkMode',
        'virtual_ip1': 'virtualIp1',
        'virtual_ip2': 'virtualIp2',
        'wan1': 'wan1',
        'wan2': 'wan2',
        'primary_serial': 'primarySerial',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.warm_spare import UserWarmSpare
        return UserWarmSpare
