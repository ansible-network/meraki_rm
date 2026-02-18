"""User model for Meraki switch QoS rule."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchQosRule(BaseTransformMixin):
    """User-facing switch QoS rule model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    qos_rule_id: Optional[str] = None
    # fields
    dscp: Optional[int] = None
    vlan: Optional[int] = None
    protocol: Optional[str] = None
    src_port: Optional[int] = None
    dst_port: Optional[int] = None
    src_port_range: Optional[str] = None
    dst_port_range: Optional[str] = None

    _field_mapping = {
        'qos_rule_id': 'id',
        'dscp': 'dscp',
        'vlan': 'vlan',
        'protocol': 'protocol',
        'src_port': 'srcPort',
        'dst_port': 'dstPort',
        'src_port_range': 'srcPortRange',
        'dst_port_range': 'dstPortRange',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.switch_qos_rule import APISwitchQosRule_v1
        return APISwitchQosRule_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
