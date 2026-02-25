"""User model for Meraki switch stack."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchStack(BaseTransformMixin):
    """User-facing switch stack model with snake_case fields."""

    MODULE_NAME = 'switch_stack'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'switch_stack_id'
    VALID_STATES = frozenset({'merged', 'deleted', 'gathered'})

    # scope
    network_id: Optional[str] = None
    # identity
    switch_stack_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Name of the switch stack."})
    serials: Optional[List[str]] = field(default=None, metadata={"description": "Serials of switches in the stack."})
    members: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "Members of the stack."})
    is_monitor_only: Optional[bool] = field(default=None, metadata={"description": "Whether stack is monitor only."})
    virtual_mac: Optional[str] = field(default=None, metadata={"description": "Virtual MAC address of the switch stack."})

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
