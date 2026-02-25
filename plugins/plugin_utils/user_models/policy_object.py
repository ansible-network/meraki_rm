"""User model for Meraki organization policy object."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserPolicyObject(BaseTransformMixin):
    """User-facing policy object model with snake_case fields."""

    MODULE_NAME = 'policy_object'
    SCOPE_PARAM = 'organization_id'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'policy_object_id'

    # scope
    organization_id: Optional[str] = None
    # identity
    policy_object_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Name of the policy object."})
    category: Optional[str] = field(default=None, metadata={"description": "Category of policy object."})
    type: Optional[str] = field(default=None, metadata={"description": "Type of policy object."})
    cidr: Optional[str] = field(default=None, metadata={"description": "CIDR value (for cidr type)."})
    fqdn: Optional[str] = field(default=None, metadata={"description": "Fully qualified domain name (for fqdn type)."})
    ip: Optional[str] = field(default=None, metadata={"description": "IP address (for ipAndMask type)."})
    mask: Optional[str] = field(default=None, metadata={"description": "Subnet mask (for ipAndMask type)."})
    group_ids: Optional[List[str]] = field(default=None, metadata={"description": "IDs of policy object groups this object belongs to."})
    network_ids: Optional[List[str]] = None
    object_ids: Optional[List[int]] = None

    _field_mapping = {
        'policy_object_id': 'id',
        'name': 'name',
        'category': 'category',
        'type': 'type',
        'cidr': 'cidr',
        'fqdn': 'fqdn',
        'ip': 'ip',
        'mask': 'mask',
        'group_ids': 'groupIds',
        'network_ids': 'networkIds',
        'object_ids': 'objectIds',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.policy_object import APIPolicyObject_v1
        return APIPolicyObject_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
