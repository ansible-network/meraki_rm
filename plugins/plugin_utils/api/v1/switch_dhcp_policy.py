"""Versioned API model and transform mixin for Meraki switch DHCP policy (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.switch_dhcp_policy import SwitchDhcpPolicy as GeneratedSwitchDhcpPolicy

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
}

# Mutable fields for update (singleton - GET/PUT only)
_UPDATE_FIELDS = [
    'defaultPolicy', 'allowedServers', 'blockedServers', 'alwaysAllowedServers',
    'arpInspection', 'alerts',
]


class SwitchDhcpPolicyTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki switch DHCP policy (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find': EndpointOperation(
                path='/networks/{networkId}/switch/dhcpServerPolicy',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/switch/dhcpServerPolicy',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APISwitchDhcpPolicy_v1(GeneratedSwitchDhcpPolicy, SwitchDhcpPolicyTransformMixin_v1):
    """Versioned API model for Meraki switch DHCP policy (v1)."""

    _field_mapping = {
        'default_policy': 'defaultPolicy',
        'allowed_servers': 'allowedServers',
        'blocked_servers': 'blockedServers',
        'always_allowed_servers': 'alwaysAllowedServers',
        'arp_inspection': 'arpInspection',
        'alerts': 'alerts',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.switch_dhcp_policy import UserSwitchDhcpPolicy
        return UserSwitchDhcpPolicy
