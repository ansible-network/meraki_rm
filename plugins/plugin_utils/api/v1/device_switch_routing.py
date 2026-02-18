"""Versioned API model and transform mixin for Meraki device switch routing interface (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.device_switch_routing import DeviceSwitchRouting as GeneratedDeviceSwitchRouting

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'serial': ['serial'],
    'interfaceId': ['interface_id', 'id'],
}

# All mutable fields for create
_CREATE_FIELDS = [
    'name', 'subnet', 'interfaceIp', 'defaultGateway', 'vlanId',
    'multicastRouting', 'ospfSettings', 'dhcpMode', 'dhcpRelayServerIps',
    'dhcpLeaseTime', 'dhcpOptions', 'dnsNameserversOption', 'dnsCustomNameservers',
    'fixedIpAssignments', 'reservedIpRanges', 'bootOptionsEnabled',
    'bootNextServer', 'bootFileName', 'ipv6', 'uplinkV4', 'uplinkV6',
]

# All mutable fields for update
_UPDATE_FIELDS = [
    'name', 'subnet', 'interfaceIp', 'defaultGateway', 'vlanId',
    'multicastRouting', 'ospfSettings', 'dhcpMode', 'dhcpRelayServerIps',
    'dhcpLeaseTime', 'dhcpOptions', 'dnsNameserversOption', 'dnsCustomNameservers',
    'fixedIpAssignments', 'reservedIpRanges', 'bootOptionsEnabled',
    'bootNextServer', 'bootFileName', 'ipv6', 'uplinkV4', 'uplinkV6',
]


class DeviceSwitchRoutingTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki device switch routing interface (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/devices/{serial}/switch/routing/interfaces',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['serial'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/devices/{serial}/switch/routing/interfaces/{interfaceId}',
                method='GET',
                fields=[],
                path_params=['serial', 'interfaceId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'find_all': EndpointOperation(
                path='/devices/{serial}/switch/routing/interfaces',
                method='GET',
                fields=[],
                path_params=['serial'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/devices/{serial}/switch/routing/interfaces/{interfaceId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['serial', 'interfaceId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/devices/{serial}/switch/routing/interfaces/{interfaceId}',
                method='DELETE',
                fields=[],
                path_params=['serial', 'interfaceId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIDeviceSwitchRouting_v1(GeneratedDeviceSwitchRouting, DeviceSwitchRoutingTransformMixin_v1):
    """Versioned API model for Meraki device switch routing interface (v1)."""

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
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.device_switch_routing import UserDeviceSwitchRouting
        return UserDeviceSwitchRouting
