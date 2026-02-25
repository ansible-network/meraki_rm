"""User model for Meraki switch access policy."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchAccessPolicy(BaseTransformMixin):
    """User-facing switch access policy model with snake_case fields."""

    MODULE_NAME = 'switch_access_policy'
    CANONICAL_KEY = 'access_policy_number'

    # scope
    network_id: Optional[str] = None
    # identity
    access_policy_number: Optional[str] = field(default=None, metadata={"description": "Access policy number (identifier)."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Name of the access policy."})
    access_policy_type: Optional[str] = field(default=None, metadata={"description": "Access type of the policy."})
    host_mode: Optional[str] = field(default=None, metadata={"description": "Host mode for the access policy."})
    radius_servers: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "List of RADIUS servers for authentication."})
    radius_accounting_servers: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "List of RADIUS accounting servers."})
    radius_accounting_enabled: Optional[bool] = field(default=None, metadata={"description": "Enable RADIUS accounting."})
    radius_coa_support_enabled: Optional[bool] = field(default=None, metadata={"description": "Enable RADIUS CoA support."})
    guest_vlan_id: Optional[int] = field(default=None, metadata={"description": "Guest VLAN ID for unauthorized devices."})
    dot1x: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "802.1X settings."})
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
