"""Versioned API model and transform mixin for Meraki auth user (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.meraki_auth_user import MerakiAuthUser as GeneratedMerakiAuthUser

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'merakiAuthUserId': ['meraki_auth_user_id', 'id'],
}

# All mutable fields for create
_CREATE_FIELDS = [
    'name', 'email', 'password', 'accountType', 'authorizations',
    'isAdmin', 'emailPasswordToUser',
]

# All mutable fields for update
_UPDATE_FIELDS = [
    'name', 'email', 'password', 'accountType', 'authorizations',
    'isAdmin', 'emailPasswordToUser',
]


class MerakiAuthUserTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki auth user (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/merakiAuthUsers',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/merakiAuthUsers/{merakiAuthUserId}',
                method='GET',
                fields=[],
                path_params=['networkId', 'merakiAuthUserId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/merakiAuthUsers',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/merakiAuthUsers/{merakiAuthUserId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'merakiAuthUserId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/merakiAuthUsers/{merakiAuthUserId}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'merakiAuthUserId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIMerakiAuthUser_v1(GeneratedMerakiAuthUser, MerakiAuthUserTransformMixin_v1):
    """Versioned API model for Meraki auth user (v1)."""

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
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.meraki_auth_user import UserMerakiAuthUser
        return UserMerakiAuthUser
