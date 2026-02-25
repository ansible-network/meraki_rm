"""User model for Meraki switch port."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchPort(BaseTransformMixin):
    """User-facing switch port model with snake_case fields."""

    MODULE_NAME = 'switch_port'
    SCOPE_PARAM = 'serial'
    SUPPORTS_DELETE = False

    # scope
    serial: Optional[str] = None
    # identity
    port_id: Optional[str] = field(default=None, metadata={"description": "Port number/ID."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Port name."})
    tags: Optional[List[str]] = field(default=None, metadata={"description": "Tags for the port."})
    enabled: Optional[bool] = field(default=None, metadata={"description": "Whether the port is enabled."})
    type: Optional[str] = field(default=None, metadata={"description": "Port type."})
    vlan: Optional[int] = field(default=None, metadata={"description": "VLAN number."})
    voice_vlan: Optional[int] = field(default=None, metadata={"description": "Voice VLAN number."})
    allowed_vlans: Optional[str] = field(default=None, metadata={"description": "Allowed VLANs (for trunk ports)."})
    poe_enabled: Optional[bool] = field(default=None, metadata={"description": "Power over Ethernet enabled."})
    isolation_enabled: Optional[bool] = field(default=None, metadata={"description": "Port isolation enabled."})
    rstp_enabled: Optional[bool] = field(default=None, metadata={"description": "RSTP enabled."})
    stp_guard: Optional[str] = field(default=None, metadata={"description": "STP guard setting."})
    link_negotiation: Optional[str] = field(default=None, metadata={"description": "Link speed negotiation."})
    port_schedule_id: Optional[str] = field(default=None, metadata={"description": "Port schedule ID."})
    udld: Optional[str] = field(default=None, metadata={"description": "Unidirectional Link Detection action."})
    access_policy_type: Optional[str] = field(default=None, metadata={"description": "Access policy type."})
    access_policy_number: Optional[int] = field(default=None, metadata={"description": "Access policy number."})
    sticky_mac_allow_list: Optional[List[str]] = field(default=None, metadata={"description": "Sticky MAC allow list."})
    sticky_mac_allow_list_limit: Optional[int] = field(default=None, metadata={"description": "Sticky MAC allow list limit."})
    storm_control_enabled: Optional[bool] = field(default=None, metadata={"description": "Storm control enabled."})
    adaptive_policy_group_id: Optional[str] = field(default=None, metadata={"description": "Adaptive policy group ID."})
    peer_sgt_capable: Optional[bool] = field(default=None, metadata={"description": "Peer SGT capable."})
    flexible_stacking_enabled: Optional[bool] = field(default=None, metadata={"description": "Flexible stacking enabled."})
    dai_trusted: Optional[bool] = field(default=None, metadata={"description": "DAI trusted."})
    profile: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Port profile."})

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
