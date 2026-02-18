"""Versioned API model and transform mixin for Meraki appliance VPN (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.vpn import Vpn as GeneratedVpn

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
}

# Mutable fields for update (singleton - no create/delete)
_UPDATE_FIELDS = [
    'mode', 'hubs', 'subnets', 'subnet', 'enabled',
    'asNumber', 'ibgpHoldTimer', 'neighbors',
]


class VpnTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki appliance VPN (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find': EndpointOperation(
                path='/networks/{networkId}/appliance/vpn/siteToSiteVpn',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/appliance/vpn/siteToSiteVpn',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APIVpn_v1(GeneratedVpn, VpnTransformMixin_v1):
    """Versioned API model for Meraki appliance VPN (v1)."""

    _field_mapping = {
        'mode': 'mode',
        'hubs': 'hubs',
        'subnets': 'subnets',
        'subnet': 'subnet',
        'enabled': 'enabled',
        'as_number': 'asNumber',
        'ibgp_hold_timer': 'ibgpHoldTimer',
        'neighbors': 'neighbors',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.vpn import UserVpn
        return UserVpn
