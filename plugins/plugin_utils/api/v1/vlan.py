"""Versioned API model and transform mixin for Meraki appliance VLAN (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.vlan import Vlan as GeneratedVlan

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'vlanId': ['vlan_id', 'id'],
}

# All mutable fields for create (id required for create)
_CREATE_FIELDS = [
    'id', 'name', 'subnet', 'applianceIp', 'groupPolicyId',
    'templateVlanType', 'cidr', 'mask', 'dhcpHandling', 'dhcpRelayServerIps',
    'dhcpLeaseTime', 'dhcpBootOptionsEnabled', 'dhcpBootNextServer',
    'dhcpBootFilename', 'dhcpOptions', 'dnsNameservers', 'reservedIpRanges',
    'fixedIpAssignments', 'ipv6', 'mandatoryDhcp',
]

# All mutable fields for update (no id in body)
_UPDATE_FIELDS = [
    'name', 'subnet', 'applianceIp', 'groupPolicyId',
    'templateVlanType', 'cidr', 'mask', 'dhcpHandling', 'dhcpRelayServerIps',
    'dhcpLeaseTime', 'dhcpBootOptionsEnabled', 'dhcpBootNextServer',
    'dhcpBootFilename', 'dhcpOptions', 'dnsNameservers', 'reservedIpRanges',
    'fixedIpAssignments', 'ipv6', 'mandatoryDhcp',
]


class VlanTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki appliance VLAN (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/appliance/vlans',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/appliance/vlans/{vlanId}',
                method='GET',
                fields=[],
                path_params=['networkId', 'vlanId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/appliance/vlans',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/appliance/vlans/{vlanId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'vlanId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/appliance/vlans/{vlanId}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'vlanId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIVlan_v1(GeneratedVlan, VlanTransformMixin_v1):
    """Versioned API model for Meraki appliance VLAN (v1)."""

    _field_mapping = {
        'vlan_id': 'id',
        'name': 'name',
        'subnet': 'subnet',
        'appliance_ip': 'applianceIp',
        'group_policy_id': 'groupPolicyId',
        'template_vlan_type': 'templateVlanType',
        'cidr': 'cidr',
        'mask': 'mask',
        'dhcp_handling': 'dhcpHandling',
        'dhcp_relay_server_ips': 'dhcpRelayServerIps',
        'dhcp_lease_time': 'dhcpLeaseTime',
        'dhcp_boot_options_enabled': 'dhcpBootOptionsEnabled',
        'dhcp_boot_next_server': 'dhcpBootNextServer',
        'dhcp_boot_filename': 'dhcpBootFilename',
        'dhcp_options': 'dhcpOptions',
        'dns_nameservers': 'dnsNameservers',
        'reserved_ip_ranges': 'reservedIpRanges',
        'fixed_ip_assignments': 'fixedIpAssignments',
        'ipv6': 'ipv6',
        'mandatory_dhcp': 'mandatoryDhcp',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.vlan import UserVlan
        return UserVlan
