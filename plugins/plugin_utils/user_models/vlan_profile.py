"""User model for Meraki VLAN profile."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserVlanProfile(BaseTransformMixin):
    """User-facing VLAN profile model with snake_case fields."""

    MODULE_NAME = 'vlan_profile'
    CANONICAL_KEY = 'iname'

    # scope
    network_id: Optional[str] = None
    # identity (API uses iname in path)
    iname: Optional[str] = field(default=None, metadata={"description": "VLAN profile iname (primary key). Required for merged, replaced, deleted."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Name of the profile (1-255 chars)."})
    is_default: Optional[bool] = field(default=None, metadata={"description": "Whether this is the default VLAN profile."})
    vlan_names: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "Array of named VLANs."})
    vlan_groups: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "Array of named VLAN groups."})
    vlan_profile: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "VLAN profile configuration."})

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
