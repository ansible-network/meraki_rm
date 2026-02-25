"""User model for Meraki auth user."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserMerakiAuthUser(BaseTransformMixin):
    """User-facing Meraki auth user model with snake_case fields."""

    MODULE_NAME = 'meraki_auth_user'
    CANONICAL_KEY = 'email'
    SYSTEM_KEY = 'meraki_auth_user_id'

    # scope
    network_id: Optional[str] = None
    # identity
    meraki_auth_user_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(email). Provide only to disambiguate when duplicate emails exist."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Name of the user."})
    email: Optional[str] = field(default=None, metadata={"description": "Email address of the user."})
    password: Optional[str] = field(default=None, metadata={"description": "Password for the user account."})
    account_type: Optional[str] = field(default=None, metadata={"description": "Authorization type for user."})
    authorizations: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "User authorization info."})
    is_admin: Optional[bool] = field(default=None, metadata={"description": "Whether the user is a Dashboard administrator."})
    email_password_to_user: Optional[bool] = field(default=None, metadata={"description": "Whether Meraki should email the password to user."})

    _field_mapping = {
        'meraki_auth_user_id': 'id',
        'name': 'name',
        'email': 'email',
        'password': 'password',
        'account_type': 'accountType',
        'authorizations': 'authorizations',
        'is_admin': 'isAdmin',
        'email_password_to_user': 'emailPasswordToUser',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.meraki_auth_user import APIMerakiAuthUser_v1
        return APIMerakiAuthUser_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
