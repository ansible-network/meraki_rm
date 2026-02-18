"""Versioned API model and transform mixin for Meraki organization VPN (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.org_vpn import OrgVpn as GeneratedOrgVpn

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'organizationId': ['organization_id'],
}

# Mutable fields for update (singleton - GET/PUT only)
# Meraki API PUT body is {"peers": [...]}
_UPDATE_FIELDS = [
    'peers',
]


class OrgVpnTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki organization VPN third-party peers (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find': EndpointOperation(
                path='/organizations/{organizationId}/appliance/vpn/thirdPartyVPNPeers',
                method='GET',
                fields=[],
                path_params=['organizationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/organizations/{organizationId}/appliance/vpn/thirdPartyVPNPeers',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['organizationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APIOrgVpn_v1(GeneratedOrgVpn, OrgVpnTransformMixin_v1):
    """Versioned API model for Meraki organization VPN (v1)."""

    _field_mapping = {
        'peers': 'peers',
        'third_party_vpn_peers': 'thirdPartyVpnPeers',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.org_vpn import UserOrgVpn
        return UserOrgVpn
