"""Versioned API model and transform mixin for Meraki device (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.device import Device as GeneratedDevice

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'serial': ['serial'],
}

# Mutable fields for update (GET/PUT only - no create/delete)
_UPDATE_FIELDS = [
    'name', 'tags', 'lat', 'lng', 'address', 'notes',
    'moveMapMarker', 'floorPlanId', 'switchProfileId',
]


class DeviceTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki device (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find': EndpointOperation(
                path='/devices/{serial}',
                method='GET',
                fields=[],
                path_params=['serial'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/devices/{serial}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['serial'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APIDevice_v1(GeneratedDevice, DeviceTransformMixin_v1):
    """Versioned API model for Meraki device (v1)."""

    _field_mapping = {
        'name': 'name',
        'tags': 'tags',
        'lat': 'lat',
        'lng': 'lng',
        'address': 'address',
        'notes': 'notes',
        'move_map_marker': 'moveMapMarker',
        'floor_plan_id': 'floorPlanId',
        'switch_profile_id': 'switchProfileId',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.device import UserDevice
        return UserDevice
