"""User model for Meraki auth user."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserMerakiAuthUser(BaseTransformMixin):
    """User-facing Meraki auth user model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    meraki_auth_user_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    account_type: Optional[str] = None
    authorizations: Optional[List[Dict[str, Any]]] = None
    is_admin: Optional[bool] = None
    email_password_to_user: Optional[bool] = None

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
