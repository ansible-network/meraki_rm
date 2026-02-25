"""User model for Meraki switch QoS rule."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchQosRule(BaseTransformMixin):
    """User-facing switch QoS rule model with snake_case fields."""

    MODULE_NAME = 'switch_qos_rule'
    SYSTEM_KEY = 'qos_rule_id'

    # scope
    network_id: Optional[str] = None
    # identity
    qos_rule_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned rule ID. Discover via C(state=gathered)."})
    # fields
    dscp: Optional[int] = field(default=None, metadata={"description": "DSCP tag for incoming packet (-1 to trust incoming DSCP)."})
    vlan: Optional[int] = field(default=None, metadata={"description": "VLAN of incoming packet (null matches any VLAN)."})
    protocol: Optional[str] = field(default=None, metadata={"description": "Protocol (ANY, TCP, or UDP)."})
    src_port: Optional[int] = field(default=None, metadata={"description": "Source port (TCP/UDP only)."})
    dst_port: Optional[int] = field(default=None, metadata={"description": "Destination port (TCP/UDP only)."})
    src_port_range: Optional[str] = field(default=None, metadata={"description": "Source port range (TCP/UDP only)."})
    dst_port_range: Optional[str] = field(default=None, metadata={"description": "Destination port range (TCP/UDP only)."})

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
