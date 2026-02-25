"""User model for Meraki switch STP."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchStp(BaseTransformMixin):
    """User-facing switch STP model with snake_case fields."""

    MODULE_NAME = 'switch_stp'
    SUPPORTS_DELETE = False

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    rstp_enabled: Optional[bool] = field(default=None, metadata={"description": "Enable RSTP (Rapid Spanning Tree Protocol)."})
    stp_bridge_priority: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "STP bridge priority for switches/stacks or templates."})

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
