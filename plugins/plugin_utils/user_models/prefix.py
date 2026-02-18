"""User model for Meraki appliance prefix."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserPrefix(BaseTransformMixin):
    """User-facing prefix model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    static_delegated_prefix_id: Optional[str] = None
    # fields
    prefix: Optional[str] = None
    description: Optional[str] = None
    origin: Optional[Dict[str, Any]] = None

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
