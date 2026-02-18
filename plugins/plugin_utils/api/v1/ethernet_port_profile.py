"""Versioned API model and transform mixin for Meraki wireless Ethernet port profile (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.ethernet_port_profile import EthernetPortProfile as GeneratedEthernetPortProfile

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'profileId': ['profile_id'],
}

_CREATE_FIELDS = ['name', 'ports', 'usbPorts']

_UPDATE_FIELDS = ['name', 'ports', 'usbPorts', 'isDefault']


class EthernetPortProfileTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki wireless Ethernet port profile (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/wireless/ethernet/ports/profiles',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/wireless/ethernet/ports/profiles/{profileId}',
                method='GET',
                fields=[],
                path_params=['networkId', 'profileId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=2,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/wireless/ethernet/ports/profiles',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/wireless/ethernet/ports/profiles/{profileId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'profileId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/wireless/ethernet/ports/profiles/{profileId}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'profileId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIEthernetPortProfile_v1(GeneratedEthernetPortProfile, EthernetPortProfileTransformMixin_v1):
    """Versioned API model for Meraki wireless Ethernet port profile (v1)."""

    _field_mapping = {
        'profile_id': 'profileId',
        'name': 'name',
        'ports': 'ports',
        'usb_ports': 'usbPorts',
        'is_default': 'isDefault',
        'serials': 'serials',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.ethernet_port_profile import UserEthernetPortProfile
        return UserEthernetPortProfile
