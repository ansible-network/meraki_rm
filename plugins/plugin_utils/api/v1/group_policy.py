"""Versioned API model and transform mixin for Meraki group policy (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.group_policy import GroupPolicy as GeneratedGroupPolicy

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'groupPolicyId': ['group_policy_id', 'id'],
}

# All mutable fields for create
_CREATE_FIELDS = [
    'name', 'bandwidth', 'bonjourForwarding', 'contentFiltering',
    'firewallAndTrafficShaping', 'scheduling', 'splashAuthSettings', 'vlanTagging',
]

# All mutable fields for update
_UPDATE_FIELDS = [
    'name', 'bandwidth', 'bonjourForwarding', 'contentFiltering',
    'firewallAndTrafficShaping', 'scheduling', 'splashAuthSettings', 'vlanTagging',
]


class GroupPolicyTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki group policy (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/groupPolicies',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/groupPolicies/{groupPolicyId}',
                method='GET',
                fields=[],
                path_params=['networkId', 'groupPolicyId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/groupPolicies',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/groupPolicies/{groupPolicyId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'groupPolicyId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/groupPolicies/{groupPolicyId}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'groupPolicyId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIGroupPolicy_v1(GeneratedGroupPolicy, GroupPolicyTransformMixin_v1):
    """Versioned API model for Meraki group policy (v1)."""

    _field_mapping = {
        'group_policy_id': 'groupPolicyId',
        'name': 'name',
        'bandwidth': 'bandwidth',
        'bonjour_forwarding': 'bonjourForwarding',
        'content_filtering': 'contentFiltering',
        'firewall_and_traffic_shaping': 'firewallAndTrafficShaping',
        'scheduling': 'scheduling',
        'splash_auth_settings': 'splashAuthSettings',
        'vlan_tagging': 'vlanTagging',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.group_policy import UserGroupPolicy
        return UserGroupPolicy
