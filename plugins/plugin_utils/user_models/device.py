"""User model for Meraki device."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserDevice(BaseTransformMixin):
    """User-facing device model with snake_case fields."""

    MODULE_NAME = 'device'
    SCOPE_PARAM = 'serial'
    SUPPORTS_DELETE = False

    # scope
    serial: Optional[str] = None
    # fields (read/update only - no create/delete)
    name: Optional[str] = field(default=None, metadata={"description": "Name of the device."})
    tags: Optional[List[str]] = field(default=None, metadata={"description": "List of tags for the device."})
    lat: Optional[float] = field(default=None, metadata={"description": "Latitude of the device."})
    lng: Optional[float] = field(default=None, metadata={"description": "Longitude of the device."})
    address: Optional[str] = field(default=None, metadata={"description": "Physical address of the device."})
    notes: Optional[str] = field(default=None, metadata={"description": "Notes for the device (max 255 chars)."})
    move_map_marker: Optional[bool] = field(default=None, metadata={"description": "Set lat/lng from address."})
    floor_plan_id: Optional[str] = field(default=None, metadata={"description": "Floor plan to associate with the device."})
    switch_profile_id: Optional[str] = field(default=None, metadata={"description": "Switch template ID to bind to the device."})

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
