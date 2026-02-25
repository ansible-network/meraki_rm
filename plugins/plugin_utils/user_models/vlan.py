"""User model for Meraki appliance VLAN."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserVlan(BaseTransformMixin):
    """User-facing VLAN model with snake_case fields."""

    MODULE_NAME = 'vlan'
    CANONICAL_KEY = 'vlan_id'

    # scope
    network_id: Optional[str] = None
    # identity
    vlan_id: Optional[str] = field(default=None, metadata={"description": "VLAN ID (1-4094). Required for merged and deleted."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "VLAN name."})
    subnet: Optional[str] = field(default=None, metadata={"description": "Subnet (e.g., '192.168.1.0/24')."})
    appliance_ip: Optional[str] = field(default=None, metadata={"description": "Appliance IP on the VLAN."})
    group_policy_id: Optional[str] = field(default=None, metadata={"description": "Group policy ID."})
    template_vlan_type: Optional[str] = field(default=None, metadata={"description": "Type of subnetting for template networks."})
    cidr: Optional[str] = field(default=None, metadata={"description": "CIDR for template networks."})
    mask: Optional[int] = field(default=None, metadata={"description": "Mask for template networks."})
    dhcp_handling: Optional[str] = field(default=None, metadata={"description": "How the appliance handles DHCP requests on this VLAN."})
    dhcp_relay_server_ips: Optional[List[str]] = field(default=None, metadata={"description": "IPs of DHCP servers to relay requests to."})
    dhcp_lease_time: Optional[str] = field(default=None, metadata={"description": "DHCP lease term."})
    dhcp_boot_options_enabled: Optional[bool] = field(default=None, metadata={"description": "Use DHCP boot options."})
    dhcp_boot_next_server: Optional[str] = field(default=None, metadata={"description": "DHCP boot next server."})
    dhcp_boot_filename: Optional[str] = field(default=None, metadata={"description": "DHCP boot filename."})
    dhcp_options: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "DHCP options for responses."})
    dns_nameservers: Optional[str] = field(default=None, metadata={"description": "DNS nameservers for DHCP responses."})
    reserved_ip_ranges: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "Reserved IP ranges on the VLAN."})
    fixed_ip_assignments: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Fixed IP assignments."})
    ipv6: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "IPv6 configuration."})
    mandatory_dhcp: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Mandatory DHCP configuration."})

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
