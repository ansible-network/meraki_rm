"""User model for Meraki switch STP."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchStp(BaseTransformMixin):
    """User-facing switch STP model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    rstp_enabled: Optional[bool] = None
    stp_bridge_priority: Optional[List[Dict[str, Any]]] = None

    _field_mapping = {
        'rstp_enabled': 'rstpEnabled',
        'stp_bridge_priority': 'stpBridgePriority',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.switch_stp import APISwitchStp_v1
        return APISwitchStp_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
