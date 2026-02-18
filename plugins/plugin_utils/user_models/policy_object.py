"""User model for Meraki organization policy object."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserPolicyObject(BaseTransformMixin):
    """User-facing policy object model with snake_case fields."""

    # scope
    organization_id: Optional[str] = None
    # identity
    policy_object_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    category: Optional[str] = None
    type: Optional[str] = None
    cidr: Optional[str] = None
    fqdn: Optional[str] = None
    ip: Optional[str] = None
    mask: Optional[str] = None
    group_ids: Optional[List[str]] = None
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
