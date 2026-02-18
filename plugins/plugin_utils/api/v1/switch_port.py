"""Versioned API model and transform mixin for Meraki switch port (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.switch_port import SwitchPort as GeneratedSwitchPort

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'serial': ['serial'],
    'portId': ['port_id'],
}

# Mutable fields for update (no create/delete - switch ports always exist)
_UPDATE_FIELDS = [
    'name', 'tags', 'enabled', 'type', 'vlan', 'voiceVlan', 'allowedVlans',
    'poeEnabled', 'isolationEnabled', 'rstpEnabled', 'stpGuard',
    'linkNegotiation', 'portScheduleId', 'udld',
    'accessPolicyType', 'accessPolicyNumber',
    'stickyMacAllowList', 'stickyMacAllowListLimit',
    'stormControlEnabled', 'adaptivePolicyGroupId',
    'peerSgtCapable', 'flexibleStackingEnabled', 'daiTrusted',
    'profile',
]


class SwitchPortTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki switch port (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find_all': EndpointOperation(
                path='/devices/{serial}/switch/ports',
                method='GET',
                fields=[],
                path_params=['serial'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'find': EndpointOperation(
                path='/devices/{serial}/switch/ports/{portId}',
                method='GET',
                fields=[],
                path_params=['serial', 'portId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=2,
            ),
            'update': EndpointOperation(
                path='/devices/{serial}/switch/ports/{portId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['serial', 'portId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APISwitchPort_v1(GeneratedSwitchPort, SwitchPortTransformMixin_v1):
    """Versioned API model for Meraki switch port (v1)."""

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
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.switch_port import UserSwitchPort
        return UserSwitchPort
