"""Versioned API model and transform mixin for Meraki VLAN profile (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.vlan_profile import VlanProfile as GeneratedVlanProfile

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'iname': ['iname'],
}

# All mutable fields for create (iname required for create)
_CREATE_FIELDS = [
    'iname', 'name', 'isDefault', 'vlanNames', 'vlanGroups', 'vlanProfile',
]

# All mutable fields for update
_UPDATE_FIELDS = [
    'name', 'isDefault', 'vlanNames', 'vlanGroups', 'vlanProfile',
]


class VlanProfileTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki VLAN profile (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/vlanProfiles',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/vlanProfiles/{iname}',
                method='GET',
                fields=[],
                path_params=['networkId', 'iname'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/vlanProfiles',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/vlanProfiles/{iname}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'iname'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/vlanProfiles/{iname}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'iname'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIVlanProfile_v1(GeneratedVlanProfile, VlanProfileTransformMixin_v1):
    """Versioned API model for Meraki VLAN profile (v1)."""

    _field_mapping = {
        'iname': 'iname',
        'name': 'name',
        'is_default': 'isDefault',
        'vlan_names': 'vlanNames',
        'vlan_groups': 'vlanGroups',
        'vlan_profile': 'vlanProfile',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.vlan_profile import UserVlanProfile
        return UserVlanProfile
