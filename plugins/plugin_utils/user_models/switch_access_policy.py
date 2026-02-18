"""User model for Meraki switch access policy."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchAccessPolicy(BaseTransformMixin):
    """User-facing switch access policy model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    access_policy_number: Optional[str] = None
    # fields
    name: Optional[str] = None
    access_policy_type: Optional[str] = None
    host_mode: Optional[str] = None
    radius_servers: Optional[List[Dict[str, Any]]] = None
    radius_accounting_servers: Optional[List[Dict[str, Any]]] = None
    radius_accounting_enabled: Optional[bool] = None
    radius_coa_support_enabled: Optional[bool] = None
    guest_vlan_id: Optional[int] = None
    dot1x: Optional[Dict[str, Any]] = None
    radius_group_attribute: Optional[str] = None
    url_redirect_walled_garden_enabled: Optional[bool] = None
    url_redirect_walled_garden_ranges: Optional[List[str]] = None
    voice_vlan_clients: Optional[bool] = None

    _field_mapping = {
        'access_policy_number': 'accessPolicyNumber',
        'name': 'name',
        'access_policy_type': 'accessPolicyType',
        'host_mode': 'hostMode',
        'radius_servers': 'radiusServers',
        'radius_accounting_servers': 'radiusAccountingServers',
        'radius_accounting_enabled': 'radiusAccountingEnabled',
        'radius_coa_support_enabled': 'radiusCoaSupportEnabled',
        'guest_vlan_id': 'guestVlanId',
        'dot1x': 'dot1x',
        'radius_group_attribute': 'radiusGroupAttribute',
        'url_redirect_walled_garden_enabled': 'urlRedirectWalledGardenEnabled',
        'url_redirect_walled_garden_ranges': 'urlRedirectWalledGardenRanges',
        'voice_vlan_clients': 'voiceVlanClients',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.switch_access_policy import APISwitchAccessPolicy_v1
        return APISwitchAccessPolicy_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
