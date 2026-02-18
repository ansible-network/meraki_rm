"""Versioned API model and transform mixin for Meraki switch routing (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.switch_routing import SwitchRouting as GeneratedSwitchRouting

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
}

# Mutable fields for update (singleton - multicast + OSPF)
_UPDATE_FIELDS = [
    'defaultSettings', 'overrides', 'enabled', 'helloTimerInSeconds',
    'deadTimerInSeconds', 'areas', 'md5AuthenticationEnabled',
    'md5AuthenticationKey', 'v3',
]


class SwitchRoutingTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki switch routing (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find': EndpointOperation(
                path='/networks/{networkId}/switch/routing/ospf',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/switch/routing/ospf',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APISwitchRouting_v1(GeneratedSwitchRouting, SwitchRoutingTransformMixin_v1):
    """Versioned API model for Meraki switch routing (v1)."""

    _field_mapping = {
        'default_settings': 'defaultSettings',
        'overrides': 'overrides',
        'enabled': 'enabled',
        'hello_timer_in_seconds': 'helloTimerInSeconds',
        'dead_timer_in_seconds': 'deadTimerInSeconds',
        'areas': 'areas',
        'md5_authentication_enabled': 'md5AuthenticationEnabled',
        'md5_authentication_key': 'md5AuthenticationKey',
        'v3': 'v3',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.switch_routing import UserSwitchRouting
        return UserSwitchRouting
