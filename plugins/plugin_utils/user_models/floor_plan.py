"""User model for Meraki floor plan."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserFloorPlan(BaseTransformMixin):
    """User-facing floor plan model with snake_case fields."""

    MODULE_NAME = 'floor_plan'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'floor_plan_id'

    # scope
    network_id: Optional[str] = None
    # identity
    floor_plan_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Name of the floor plan."})
    center: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Center coordinates (lat/lng) of the floor plan."})
    bottom_left_corner: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Bottom left corner coordinates."})
    bottom_right_corner: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Bottom right corner coordinates."})
    top_left_corner: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Top left corner coordinates."})
    top_right_corner: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Top right corner coordinates."})
    width: Optional[float] = field(default=None, metadata={"description": "Width of the floor plan."})
    height: Optional[float] = field(default=None, metadata={"description": "Height of the floor plan."})
    floor_number: Optional[float] = field(default=None, metadata={"description": "Floor number within the building."})
    image_contents: Optional[str] = field(default=None, metadata={"description": "Base64 encoded floor plan image."})
    image_extension: Optional[str] = field(default=None, metadata={"description": "Image format (e.g., png, jpg)."})

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
