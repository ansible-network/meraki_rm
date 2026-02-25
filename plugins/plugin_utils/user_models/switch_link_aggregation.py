"""User model for Meraki switch link aggregation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchLinkAggregation(BaseTransformMixin):
    """User-facing switch link aggregation model with snake_case fields."""

    MODULE_NAME = 'switch_link_aggregation'
    SYSTEM_KEY = 'link_aggregation_id'

    # scope
    network_id: Optional[str] = None
    # identity
    link_aggregation_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned aggregation ID. Discover via C(state=gathered)."})
    # fields
    switch_ports: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "Array of switch ports for the aggregation."})
    switch_profile_ports: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "Array of switch profile ports for creating aggregation."})

    _field_mapping = {
        'link_aggregation_id': 'id',
        'switch_ports': 'switchPorts',
        'switch_profile_ports': 'switchProfilePorts',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.switch_link_aggregation import APISwitchLinkAggregation_v1
        return APISwitchLinkAggregation_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
