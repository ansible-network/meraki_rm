"""User model for Meraki appliance prefix."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserPrefix(BaseTransformMixin):
    """User-facing prefix model with snake_case fields."""

    MODULE_NAME = 'prefix'
    CANONICAL_KEY = 'prefix'
    SYSTEM_KEY = 'static_delegated_prefix_id'

    # scope
    network_id: Optional[str] = None
    # identity
    static_delegated_prefix_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(prefix). Provide only to disambiguate when duplicate prefixes exist."})
    # fields
    prefix: Optional[str] = field(default=None, metadata={"description": "IPv6 prefix/prefix length."})
    description: Optional[str] = field(default=None, metadata={"description": "Identifying description for the prefix."})
    origin: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "WAN1/WAN2/Independent prefix configuration."})

    _field_mapping = {
        'static_delegated_prefix_id': 'staticDelegatedPrefixId',
        'prefix': 'prefix',
        'description': 'description',
        'origin': 'origin',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.prefix import APIPrefix_v1
        return APIPrefix_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
