"""User model for Meraki organization third-party VPN peers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserOrgVpn(BaseTransformMixin):
    """User-facing org VPN third-party peers model with snake_case fields."""

    MODULE_NAME = 'org_vpn'
    SCOPE_PARAM = 'organization_id'
    SUPPORTS_DELETE = False

    # scope
    organization_id: Optional[str] = None
    # fields (singleton - no primary key)
    peers: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "List of third-party VPN peers."})
    third_party_vpn_peers: Optional[List[Dict[str, Any]]] = None

    _field_mapping = {
        'peers': 'peers',
        'third_party_vpn_peers': 'thirdPartyVpnPeers',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.org_vpn import APIOrgVpn_v1
        return APIOrgVpn_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
