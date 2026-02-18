"""Versioned API model and transform mixin for Meraki organization policy object (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.policy_object import PolicyObject as GeneratedPolicyObject

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'organizationId': ['organization_id'],
    'policyObjectId': ['policy_object_id', 'id'],
}

# Fields for create
_CREATE_FIELDS = [
    'name', 'category', 'type', 'cidr', 'fqdn', 'ip', 'mask',
    'groupIds', 'networkIds', 'objectIds',
]

# Fields for update (no id in body)
_UPDATE_FIELDS = [
    'name', 'category', 'type', 'cidr', 'fqdn', 'ip', 'mask',
    'groupIds', 'networkIds', 'objectIds',
]


class PolicyObjectTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki organization policy object (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/organizations/{organizationId}/policyObjects',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['organizationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/organizations/{organizationId}/policyObjects',
                method='GET',
                fields=[],
                path_params=['organizationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/organizations/{organizationId}/policyObjects/{policyObjectId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['organizationId', 'policyObjectId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/organizations/{organizationId}/policyObjects/{policyObjectId}',
                method='DELETE',
                fields=[],
                path_params=['organizationId', 'policyObjectId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIPolicyObject_v1(GeneratedPolicyObject, PolicyObjectTransformMixin_v1):
    """Versioned API model for Meraki organization policy object (v1)."""

    _field_mapping = {
        'policy_object_id': 'id',
        'name': 'name',
        'category': 'category',
        'type': 'type',
        'cidr': 'cidr',
        'fqdn': 'fqdn',
        'ip': 'ip',
        'mask': 'mask',
        'group_ids': 'groupIds',
        'network_ids': 'networkIds',
        'object_ids': 'objectIds',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.policy_object import UserPolicyObject
        return UserPolicyObject
