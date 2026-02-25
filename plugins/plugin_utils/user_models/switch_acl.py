"""User model for Meraki switch ACL."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchAcl(BaseTransformMixin):
    """User-facing switch ACL model with snake_case fields."""

    MODULE_NAME = 'switch_acl'
    SUPPORTS_DELETE = False

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    rules: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "Ordered array of access control list rules."})

    _field_mapping = {
        'rules': 'rules',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.switch_acl import APISwitchAcl_v1
        return APISwitchAcl_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
