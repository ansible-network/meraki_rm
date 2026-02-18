"""Versioned API model and transform mixin for Meraki floor plan (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.floor_plan import FloorPlan as GeneratedFloorPlan

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'floorPlanId': ['floor_plan_id', 'id'],
}

# All mutable fields for create
_CREATE_FIELDS = [
    'name', 'center', 'bottomLeftCorner', 'bottomRightCorner',
    'topLeftCorner', 'topRightCorner', 'width', 'height', 'floorNumber',
    'imageContents', 'imageExtension',
]

# All mutable fields for update
_UPDATE_FIELDS = [
    'name', 'center', 'bottomLeftCorner', 'bottomRightCorner',
    'topLeftCorner', 'topRightCorner', 'width', 'height', 'floorNumber',
    'imageContents', 'imageExtension',
]


class FloorPlanTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki floor plan (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/floorPlans',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/floorPlans/{floorPlanId}',
                method='GET',
                fields=[],
                path_params=['networkId', 'floorPlanId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/floorPlans',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/floorPlans/{floorPlanId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'floorPlanId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/floorPlans/{floorPlanId}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'floorPlanId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIFloorPlan_v1(GeneratedFloorPlan, FloorPlanTransformMixin_v1):
    """Versioned API model for Meraki floor plan (v1)."""

    _field_mapping = {
        'floor_plan_id': 'floorPlanId',
        'name': 'name',
        'center': 'center',
        'bottom_left_corner': 'bottomLeftCorner',
        'bottom_right_corner': 'bottomRightCorner',
        'top_left_corner': 'topLeftCorner',
        'top_right_corner': 'topRightCorner',
        'width': 'width',
        'height': 'height',
        'floor_number': 'floorNumber',
        'image_contents': 'imageContents',
        'image_extension': 'imageExtension',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.floor_plan import UserFloorPlan
        return UserFloorPlan
