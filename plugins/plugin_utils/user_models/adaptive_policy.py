"""User model for Meraki organization adaptive policy settings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserAdaptivePolicy(BaseTransformMixin):
    """User-facing adaptive policy settings model with snake_case fields."""

    # scope
    organization_id: Optional[str] = None
    # fields (singleton - no primary key)
    enabled_networks: Optional[List[str]] = None
    last_entry_rule: Optional[str] = None

    _field_mapping = {
        'enabled_networks': 'enabledNetworks',
        'last_entry_rule': 'lastEntryRule',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.adaptive_policy import APIAdaptivePolicy_v1
        return APIAdaptivePolicy_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
