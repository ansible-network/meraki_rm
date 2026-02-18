"""User model for Meraki switch link aggregation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchLinkAggregation(BaseTransformMixin):
    """User-facing switch link aggregation model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    link_aggregation_id: Optional[str] = None
    # fields
    switch_ports: Optional[List[Dict[str, Any]]] = None
    switch_profile_ports: Optional[List[Dict[str, Any]]] = None

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
