"""User model for Meraki firmware upgrade."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserFirmwareUpgrade(BaseTransformMixin):
    """User-facing firmware upgrade model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    upgrade_window: Optional[Dict[str, Any]] = None
    timezone: Optional[str] = None
    products: Optional[Dict[str, Any]] = None

    _field_mapping = {
        'upgrade_window': 'upgradeWindow',
        'timezone': 'timezone',
        'products': 'products',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.firmware_upgrade import APIFirmwareUpgrade_v1
        return APIFirmwareUpgrade_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
