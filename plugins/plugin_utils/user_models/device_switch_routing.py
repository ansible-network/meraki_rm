"""User model for Meraki device switch routing interface."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserDeviceSwitchRouting(BaseTransformMixin):
    """User-facing device switch routing interface model with snake_case fields."""

    # scope
    serial: Optional[str] = None
    # identity
    interface_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    subnet: Optional[str] = None
    interface_ip: Optional[str] = None
    default_gateway: Optional[str] = None
    vlan_id: Optional[int] = None
    multicast_routing: Optional[str] = None
    ospf_settings: Optional[Dict[str, Any]] = None
    dhcp_mode: Optional[str] = None
    dhcp_relay_server_ips: Optional[List[str]] = None

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
