"""Versioned API model and transform mixin for Meraki switch access policy (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.switch_access_policy import SwitchAccessPolicy as GeneratedSwitchAccessPolicy

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'accessPolicyNumber': ['access_policy_number'],
}

_CREATE_FIELDS = [
    'accessPolicyNumber', 'name', 'accessPolicyType', 'hostMode',
    'radiusServers', 'radiusAccountingServers', 'radiusAccountingEnabled',
    'radiusCoaSupportEnabled', 'guestVlanId', 'dot1x', 'radiusGroupAttribute',
    'urlRedirectWalledGardenEnabled', 'urlRedirectWalledGardenRanges',
    'voiceVlanClients',
]

_UPDATE_FIELDS = [
    'name', 'accessPolicyType', 'hostMode', 'radiusServers',
    'radiusAccountingServers', 'radiusAccountingEnabled',
    'radiusCoaSupportEnabled', 'guestVlanId', 'dot1x', 'radiusGroupAttribute',
    'urlRedirectWalledGardenEnabled', 'urlRedirectWalledGardenRanges',
    'voiceVlanClients',
]


class SwitchAccessPolicyTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki switch access policy (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/switch/accessPolicies',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/switch/accessPolicies/{accessPolicyNumber}',
                method='GET',
                fields=[],
                path_params=['networkId', 'accessPolicyNumber'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=2,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/switch/accessPolicies',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/switch/accessPolicies/{accessPolicyNumber}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'accessPolicyNumber'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/switch/accessPolicies/{accessPolicyNumber}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'accessPolicyNumber'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APISwitchAccessPolicy_v1(GeneratedSwitchAccessPolicy, SwitchAccessPolicyTransformMixin_v1):
    """Versioned API model for Meraki switch access policy (v1)."""

    _field_mapping = {
        'access_policy_number': 'accessPolicyNumber',
        'name': 'name',
        'access_policy_type': 'accessPolicyType',
        'host_mode': 'hostMode',
        'radius_servers': 'radiusServers',
        'radius_accounting_servers': 'radiusAccountingServers',
        'radius_accounting_enabled': 'radiusAccountingEnabled',
        'radius_coa_support_enabled': 'radiusCoaSupportEnabled',
        'guest_vlan_id': 'guestVlanId',
        'dot1x': 'dot1x',
        'radius_group_attribute': 'radiusGroupAttribute',
        'url_redirect_walled_garden_enabled': 'urlRedirectWalledGardenEnabled',
        'url_redirect_walled_garden_ranges': 'urlRedirectWalledGardenRanges',
        'voice_vlan_clients': 'voiceVlanClients',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.switch_access_policy import UserSwitchAccessPolicy
        return UserSwitchAccessPolicy
