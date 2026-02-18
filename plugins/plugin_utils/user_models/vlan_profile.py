"""User model for Meraki VLAN profile."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserVlanProfile(BaseTransformMixin):
    """User-facing VLAN profile model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity (API uses iname in path)
    iname: Optional[str] = None
    # fields
    name: Optional[str] = None
    is_default: Optional[bool] = None
    vlan_names: Optional[List[Dict[str, Any]]] = None
    vlan_groups: Optional[List[Dict[str, Any]]] = None
    vlan_profile: Optional[Dict[str, Any]] = None

    _field_mapping = {
        'iname': 'iname',
        'name': 'name',
        'is_default': 'isDefault',
        'vlan_names': 'vlanNames',
        'vlan_groups': 'vlanGroups',
        'vlan_profile': 'vlanProfile',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.vlan_profile import APIVlanProfile_v1
        return APIVlanProfile_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
