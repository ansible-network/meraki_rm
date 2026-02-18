"""Versioned API model and transform mixin for Meraki device management interface (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.device_management_interface import DeviceManagementInterface as GeneratedDeviceManagementInterface

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'serial': ['serial'],
}

# Mutable fields for update (singleton)
_UPDATE_FIELDS = [
    'wan1', 'wan2', 'ddnsHostnames',
]


class DeviceManagementInterfaceTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki device management interface (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find': EndpointOperation(
                path='/devices/{serial}/managementInterface',
                method='GET',
                fields=[],
                path_params=['serial'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/devices/{serial}/managementInterface',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['serial'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APIDeviceManagementInterface_v1(GeneratedDeviceManagementInterface, DeviceManagementInterfaceTransformMixin_v1):
    """Versioned API model for Meraki device management interface (v1)."""

    _field_mapping = {
        'wan1': 'wan1',
        'wan2': 'wan2',
        'ddns_hostnames': 'ddnsHostnames',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.device_management_interface import UserDeviceManagementInterface
        return UserDeviceManagementInterface
