"""User model for Meraki firmware upgrade."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserFirmwareUpgrade(BaseTransformMixin):
    """User-facing firmware upgrade model with snake_case fields."""

    MODULE_NAME = 'firmware_upgrade'
    SUPPORTS_DELETE = False

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    upgrade_window: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Upgrade window (dayOfWeek, hourOfDay)."})
    timezone: Optional[str] = field(default=None, metadata={"description": "Timezone for the network."})
    products: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Product-specific upgrade settings (wireless, appliance, switch, camera)."})

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
