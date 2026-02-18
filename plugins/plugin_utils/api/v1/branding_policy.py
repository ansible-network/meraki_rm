"""Versioned API model and transform mixin for Meraki organization branding policy (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.branding_policy import BrandingPolicy as GeneratedBrandingPolicy

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'organizationId': ['organization_id'],
    'brandingPolicyId': ['branding_policy_id', 'id'],
}

# Fields for create
_CREATE_FIELDS = [
    'name', 'enabled', 'adminSettings', 'helpSettings', 'customLogo',
]

# Fields for update (no id in body)
_UPDATE_FIELDS = [
    'name', 'enabled', 'adminSettings', 'helpSettings', 'customLogo',
]


class BrandingPolicyTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki organization branding policy (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/organizations/{organizationId}/brandingPolicies',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['organizationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/organizations/{organizationId}/brandingPolicies',
                method='GET',
                fields=[],
                path_params=['organizationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/organizations/{organizationId}/brandingPolicies/{brandingPolicyId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['organizationId', 'brandingPolicyId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/organizations/{organizationId}/brandingPolicies/{brandingPolicyId}',
                method='DELETE',
                fields=[],
                path_params=['organizationId', 'brandingPolicyId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIBrandingPolicy_v1(GeneratedBrandingPolicy, BrandingPolicyTransformMixin_v1):
    """Versioned API model for Meraki organization branding policy (v1)."""

    # id from API response / path param (not in generated schema)
    id: Optional[str] = None

    _field_mapping = {
        'branding_policy_id': 'id',
        'name': 'name',
        'enabled': 'enabled',
        'admin_settings': 'adminSettings',
        'help_settings': 'helpSettings',
        'custom_logo': 'customLogo',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.branding_policy import UserBrandingPolicy
        return UserBrandingPolicy
