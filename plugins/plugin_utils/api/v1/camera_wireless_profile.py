"""Versioned API model and transform mixin for Meraki camera wireless profile (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.camera_wireless_profile import CameraWirelessProfile as GeneratedCameraWirelessProfile

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'wirelessProfileId': ['wireless_profile_id', 'id'],
}

# All mutable fields for create (id required for create)
_CREATE_FIELDS = [
    'id', 'name', 'identity', 'ssid',
]

# All mutable fields for update (no id in body)
_UPDATE_FIELDS = [
    'name', 'identity', 'ssid',
]


class CameraWirelessProfileTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki camera wireless profile (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/camera/wirelessProfiles',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/camera/wirelessProfiles/{wirelessProfileId}',
                method='GET',
                fields=[],
                path_params=['networkId', 'wirelessProfileId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/camera/wirelessProfiles',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/camera/wirelessProfiles/{wirelessProfileId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'wirelessProfileId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/camera/wirelessProfiles/{wirelessProfileId}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'wirelessProfileId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APICameraWirelessProfile_v1(GeneratedCameraWirelessProfile, CameraWirelessProfileTransformMixin_v1):
    """Versioned API model for Meraki camera wireless profile (v1)."""

    _field_mapping = {
        'wireless_profile_id': 'id',
        'name': 'name',
        'identity': 'identity',
        'ssid': 'ssid',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.camera_wireless_profile import UserCameraWirelessProfile
        return UserCameraWirelessProfile
