"""User model for Meraki switch port."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchPort(BaseTransformMixin):
    """User-facing switch port model with snake_case fields."""

    # scope
    serial: Optional[str] = None
    # identity
    port_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    tags: Optional[List[str]] = None
    enabled: Optional[bool] = None
    type: Optional[str] = None
    vlan: Optional[int] = None
    voice_vlan: Optional[int] = None
    allowed_vlans: Optional[str] = None
    poe_enabled: Optional[bool] = None
    isolation_enabled: Optional[bool] = None
    rstp_enabled: Optional[bool] = None
    stp_guard: Optional[str] = None
    link_negotiation: Optional[str] = None
    port_schedule_id: Optional[str] = None
    udld: Optional[str] = None
    access_policy_type: Optional[str] = None
    access_policy_number: Optional[int] = None
    sticky_mac_allow_list: Optional[List[str]] = None
    sticky_mac_allow_list_limit: Optional[int] = None
    storm_control_enabled: Optional[bool] = None
    adaptive_policy_group_id: Optional[str] = None
    peer_sgt_capable: Optional[bool] = None
    flexible_stacking_enabled: Optional[bool] = None
    dai_trusted: Optional[bool] = None
    profile: Optional[Dict[str, Any]] = None

    _field_mapping = {
        'port_id': 'portId',
        'name': 'name',
        'tags': 'tags',
        'enabled': 'enabled',
        'type': 'type',
        'vlan': 'vlan',
        'voice_vlan': 'voiceVlan',
        'allowed_vlans': 'allowedVlans',
        'poe_enabled': 'poeEnabled',
        'isolation_enabled': 'isolationEnabled',
        'rstp_enabled': 'rstpEnabled',
        'stp_guard': 'stpGuard',
        'link_negotiation': 'linkNegotiation',
        'port_schedule_id': 'portScheduleId',
        'udld': 'udld',
        'access_policy_type': 'accessPolicyType',
        'access_policy_number': 'accessPolicyNumber',
        'sticky_mac_allow_list': 'stickyMacAllowList',
        'sticky_mac_allow_list_limit': 'stickyMacAllowListLimit',
        'storm_control_enabled': 'stormControlEnabled',
        'adaptive_policy_group_id': 'adaptivePolicyGroupId',
        'peer_sgt_capable': 'peerSgtCapable',
        'flexible_stacking_enabled': 'flexibleStackingEnabled',
        'dai_trusted': 'daiTrusted',
        'profile': 'profile',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.switch_port import APISwitchPort_v1
        return APISwitchPort_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
