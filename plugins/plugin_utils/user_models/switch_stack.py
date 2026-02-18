"""User model for Meraki switch stack."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchStack(BaseTransformMixin):
    """User-facing switch stack model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    switch_stack_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    serials: Optional[List[str]] = None
    members: Optional[List[Dict[str, Any]]] = None
    is_monitor_only: Optional[bool] = None
    virtual_mac: Optional[str] = None

    _field_mapping = {
        'switch_stack_id': 'id',
        'name': 'name',
        'serials': 'serials',
        'members': 'members',
        'is_monitor_only': 'isMonitorOnly',
        'virtual_mac': 'virtualMac',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.switch_stack import APISwitchStack_v1
        return APISwitchStack_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
