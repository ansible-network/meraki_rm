"""User model for Meraki organization admin."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserAdmin(BaseTransformMixin):
    """User-facing admin model with snake_case fields."""

    MODULE_NAME = 'admin'
    SCOPE_PARAM = 'organization_id'
    CANONICAL_KEY = 'email'
    SYSTEM_KEY = 'admin_id'

    # scope
    organization_id: Optional[str] = None
    # identity
    admin_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(email). Provide only to disambiguate when duplicate emails exist."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Admin name."})
    email: Optional[str] = field(default=None, metadata={"description": "Admin email."})
    org_access: Optional[str] = field(default=None, metadata={"description": "Admin's level of access to the organization."})
    tags: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "List of tag-based access controls."})
    networks: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "List of network-based access controls."})
    authentication_method: Optional[str] = field(default=None, metadata={"description": "Admin's authentication method."})
    account_status: Optional[str] = field(default=None, metadata={"description": "Status of the admin's account."})
    two_factor_auth_enabled: Optional[bool] = field(default=None, metadata={"description": "Indicates whether two-factor authentication is enabled."})
    has_api_key: Optional[bool] = field(default=None, metadata={"description": "Indicates whether the admin has an API key."})
    last_active: Optional[str] = field(default=None, metadata={"description": "Time when the admin was last active."})

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
