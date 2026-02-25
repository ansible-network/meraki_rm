"""User model for Meraki device switch routing interface."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserDeviceSwitchRouting(BaseTransformMixin):
    """User-facing device switch routing interface model with snake_case fields."""

    MODULE_NAME = 'device_switch_routing'
    SCOPE_PARAM = 'serial'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'interface_id'

    # scope
    serial: Optional[str] = None
    # identity
    interface_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Interface name."})
    subnet: Optional[str] = field(default=None, metadata={"description": "IPv4 subnet."})
    interface_ip: Optional[str] = field(default=None, metadata={"description": "IPv4 address."})
    default_gateway: Optional[str] = field(default=None, metadata={"description": "IPv4 default gateway."})
    vlan_id: Optional[int] = field(default=None, metadata={"description": "VLAN ID."})
    multicast_routing: Optional[str] = field(default=None, metadata={"description": "Multicast routing status."})
    ospf_settings: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "IPv4 OSPF settings."})
    dhcp_mode: Optional[str] = field(default=None, metadata={"description": "DHCP mode for the interface."})
    dhcp_relay_server_ips: Optional[List[str]] = field(default=None, metadata={"description": "DHCP relay server IPs."})

    _field_mapping = {
        'interface_id': 'interfaceId',
        'name': 'name',
        'subnet': 'subnet',
        'interface_ip': 'interfaceIp',
        'default_gateway': 'defaultGateway',
        'vlan_id': 'vlanId',
        'multicast_routing': 'multicastRouting',
        'ospf_settings': 'ospfSettings',
        'dhcp_mode': 'dhcpMode',
        'dhcp_relay_server_ips': 'dhcpRelayServerIps',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.device_switch_routing import APIDeviceSwitchRouting_v1
        return APIDeviceSwitchRouting_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
