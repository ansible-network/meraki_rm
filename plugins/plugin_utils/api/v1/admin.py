"""Versioned API model and transform mixin for Meraki organization admin (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.admin import Admin as GeneratedAdmin

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'organizationId': ['organization_id'],
    'adminId': ['admin_id', 'id'],
}

# Fields for create (email, name, orgAccess required per API)
_CREATE_FIELDS = [
    'email', 'name', 'orgAccess', 'tags', 'networks', 'authenticationMethod',
]

# Fields for update (no id in body)
_UPDATE_FIELDS = [
    'name', 'orgAccess', 'tags', 'networks', 'authenticationMethod',
]


class AdminTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki organization admin (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/organizations/{organizationId}/admins',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['organizationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/organizations/{organizationId}/admins',
                method='GET',
                fields=[],
                path_params=['organizationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/organizations/{organizationId}/admins/{adminId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['organizationId', 'adminId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/organizations/{organizationId}/admins/{adminId}',
                method='DELETE',
                fields=[],
                path_params=['organizationId', 'adminId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIAdmin_v1(GeneratedAdmin, AdminTransformMixin_v1):
    """Versioned API model for Meraki organization admin (v1)."""

    _field_mapping = {
        'admin_id': 'id',
        'name': 'name',
        'email': 'email',
        'org_access': 'orgAccess',
        'tags': 'tags',
        'networks': 'networks',
        'authentication_method': 'authenticationMethod',
        'account_status': 'accountStatus',
        'two_factor_auth_enabled': 'twoFactorAuthEnabled',
        'has_api_key': 'hasApiKey',
        'last_active': 'lastActive',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.admin import UserAdmin
        return UserAdmin
