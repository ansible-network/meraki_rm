"""User model for Meraki appliance VLAN."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserVlan(BaseTransformMixin):
    """User-facing VLAN model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    vlan_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    subnet: Optional[str] = None
    appliance_ip: Optional[str] = None
    group_policy_id: Optional[str] = None
    template_vlan_type: Optional[str] = None
    cidr: Optional[str] = None
    mask: Optional[int] = None
    dhcp_handling: Optional[str] = None
    dhcp_relay_server_ips: Optional[List[str]] = None
    dhcp_lease_time: Optional[str] = None
    dhcp_boot_options_enabled: Optional[bool] = None
    dhcp_boot_next_server: Optional[str] = None
    dhcp_boot_filename: Optional[str] = None
    dhcp_options: Optional[List[Dict[str, Any]]] = None
    dns_nameservers: Optional[str] = None
    reserved_ip_ranges: Optional[List[Dict[str, Any]]] = None
    fixed_ip_assignments: Optional[Dict[str, Any]] = None
    ipv6: Optional[Dict[str, Any]] = None
    mandatory_dhcp: Optional[Dict[str, Any]] = None

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
        from ..api.v1.vlan import APIVlan_v1
        return APIVlan_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
