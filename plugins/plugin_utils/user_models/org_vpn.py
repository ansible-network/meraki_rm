"""User model for Meraki organization third-party VPN peers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserOrgVpn(BaseTransformMixin):
    """User-facing org VPN third-party peers model with snake_case fields."""

    # scope
    organization_id: Optional[str] = None
    # fields (singleton - no primary key)
    peers: Optional[List[Dict[str, Any]]] = None
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
