"""User model for Meraki device management interface."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserDeviceManagementInterface(BaseTransformMixin):
    """User-facing device management interface model with snake_case fields."""

    # scope
    serial: Optional[str] = None
    # fields (singleton - no primary key)
    wan1: Optional[Dict[str, Any]] = None
    wan2: Optional[Dict[str, Any]] = None
    ddns_hostnames: Optional[Dict[str, Any]] = None

    _field_mapping = {
        'wan1': 'wan1',
        'wan2': 'wan2',
        'ddns_hostnames': 'ddnsHostnames',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.device_management_interface import APIDeviceManagementInterface_v1
        return APIDeviceManagementInterface_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
