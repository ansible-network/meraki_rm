"""Versioned API model and transform mixin for Meraki appliance SSID (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.appliance_ssid import ApplianceSsid as GeneratedApplianceSsid

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'number': ['number'],
}

# Mutable fields for update (read/update only - no create/delete)
_UPDATE_FIELDS = [
    'name', 'enabled', 'authMode', 'encryptionMode', 'psk',
    'defaultVlanId', 'visible', 'wpaEncryptionMode', 'radiusServers',
]


class ApplianceSsidTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki appliance SSID (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find': EndpointOperation(
                path='/networks/{networkId}/appliance/ssids/{number}',
                method='GET',
                fields=[],
                path_params=['networkId', 'number'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/appliance/ssids',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/appliance/ssids/{number}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'number'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APIApplianceSsid_v1(GeneratedApplianceSsid, ApplianceSsidTransformMixin_v1):
    """Versioned API model for Meraki appliance SSID (v1)."""

    _field_mapping = {
        'number': 'number',
        'name': 'name',
        'enabled': 'enabled',
        'auth_mode': 'authMode',
        'encryption_mode': 'encryptionMode',
        'psk': 'psk',
        'default_vlan_id': 'defaultVlanId',
        'visible': 'visible',
        'wpa_encryption_mode': 'wpaEncryptionMode',
        'radius_servers': 'radiusServers',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.appliance_ssid import UserApplianceSsid
        return UserApplianceSsid
