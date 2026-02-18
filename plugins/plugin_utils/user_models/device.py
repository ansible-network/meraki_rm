"""User model for Meraki device."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserDevice(BaseTransformMixin):
    """User-facing device model with snake_case fields."""

    # scope
    serial: Optional[str] = None
    # fields (read/update only - no create/delete)
    name: Optional[str] = None
    tags: Optional[List[str]] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    move_map_marker: Optional[bool] = None
    floor_plan_id: Optional[str] = None
    switch_profile_id: Optional[str] = None

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
        from ..api.v1.device import APIDevice_v1
        return APIDevice_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
