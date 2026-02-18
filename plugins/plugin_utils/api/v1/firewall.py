"""Versioned API model and transform mixin for Meraki appliance firewall (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.firewall import Firewall as GeneratedFirewall

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
}

# Mutable fields for update (singleton - no create/delete)
_UPDATE_FIELDS = [
    'rules', 'syslogDefaultRule', 'spoofingProtection',
    'applicationCategories', 'access', 'allowedIps', 'service',
]


class FirewallTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki appliance firewall (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find': EndpointOperation(
                path='/networks/{networkId}/appliance/firewall/l3FirewallRules',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/appliance/firewall/l3FirewallRules',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APIFirewall_v1(GeneratedFirewall, FirewallTransformMixin_v1):
    """Versioned API model for Meraki appliance firewall (v1)."""

    _field_mapping = {
        'rules': 'rules',
        'syslog_default_rule': 'syslogDefaultRule',
        'spoofing_protection': 'spoofingProtection',
        'application_categories': 'applicationCategories',
        'access': 'access',
        'allowed_ips': 'allowedIps',
        'service': 'service',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.firewall import UserFirewall
        return UserFirewall
