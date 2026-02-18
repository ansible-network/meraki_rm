"""User model for Meraki floor plan."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserFloorPlan(BaseTransformMixin):
    """User-facing floor plan model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    floor_plan_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    center: Optional[Dict[str, Any]] = None
    bottom_left_corner: Optional[Dict[str, Any]] = None
    bottom_right_corner: Optional[Dict[str, Any]] = None
    top_left_corner: Optional[Dict[str, Any]] = None
    top_right_corner: Optional[Dict[str, Any]] = None
    width: Optional[float] = None
    height: Optional[float] = None
    floor_number: Optional[float] = None
    image_contents: Optional[str] = None
    image_extension: Optional[str] = None

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
        from ..api.v1.floor_plan import APIFloorPlan_v1
        return APIFloorPlan_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
