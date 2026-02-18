"""Versioned API model and transform mixin for Meraki switch stack (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.switch_stack import SwitchStack as GeneratedSwitchStack

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'switchStackId': ['switch_stack_id', 'id'],
}

_CREATE_FIELDS = ['name', 'serials']

_UPDATE_FIELDS = ['name', 'serials', 'members', 'isMonitorOnly', 'virtualMac']


class SwitchStackTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki switch stack (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/switch/stacks',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/switch/stacks/{switchStackId}',
                method='GET',
                fields=[],
                path_params=['networkId', 'switchStackId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=2,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/switch/stacks',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/switch/stacks/{switchStackId}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'switchStackId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APISwitchStack_v1(GeneratedSwitchStack, SwitchStackTransformMixin_v1):
    """Versioned API model for Meraki switch stack (v1)."""

    _field_mapping = {
        'switch_stack_id': 'id',
        'name': 'name',
        'serials': 'serials',
        'members': 'members',
        'is_monitor_only': 'isMonitorOnly',
        'virtual_mac': 'virtualMac',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.switch_stack import UserSwitchStack
        return UserSwitchStack
