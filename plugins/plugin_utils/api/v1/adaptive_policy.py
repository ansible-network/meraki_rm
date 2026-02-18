"""Versioned API model and transform mixin for Meraki organization adaptive policy (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.adaptive_policy import AdaptivePolicy as GeneratedAdaptivePolicy

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'organizationId': ['organization_id'],
}

# Mutable fields for update (singleton - GET/PUT only)
_UPDATE_FIELDS = [
    'enabledNetworks', 'lastEntryRule',
]


class AdaptivePolicyTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki organization adaptive policy settings (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find': EndpointOperation(
                path='/organizations/{organizationId}/adaptivePolicy/settings',
                method='GET',
                fields=[],
                path_params=['organizationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/organizations/{organizationId}/adaptivePolicy/settings',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['organizationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APIAdaptivePolicy_v1(GeneratedAdaptivePolicy, AdaptivePolicyTransformMixin_v1):
    """Versioned API model for Meraki organization adaptive policy (v1)."""

    _field_mapping = {
        'enabled_networks': 'enabledNetworks',
        'last_entry_rule': 'lastEntryRule',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.adaptive_policy import UserAdaptivePolicy
        return UserAdaptivePolicy
