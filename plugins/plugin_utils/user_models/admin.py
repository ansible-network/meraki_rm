"""User model for Meraki organization admin."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserAdmin(BaseTransformMixin):
    """User-facing admin model with snake_case fields."""

    # scope
    organization_id: Optional[str] = None
    # identity
    admin_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    email: Optional[str] = None
    org_access: Optional[str] = None
    tags: Optional[List[Dict[str, Any]]] = None
    networks: Optional[List[Dict[str, Any]]] = None
    authentication_method: Optional[str] = None
    account_status: Optional[str] = None
    two_factor_auth_enabled: Optional[bool] = None
    has_api_key: Optional[bool] = None
    last_active: Optional[str] = None

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
        from ..api.v1.admin import APIAdmin_v1
        return APIAdmin_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
