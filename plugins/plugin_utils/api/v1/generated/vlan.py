"""Generated API dataclass for Meraki appliance vlan.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/appliance/vlans
    /networks/{networkId}/appliance/vlans/settings
    /networks/{networkId}/appliance/vlans/{vlanId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional


@dataclass
class Vlan:
    """Meraki appliance vlan API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    _FIELD_CONSTRAINTS: ClassVar[dict] = {
        'dhcpHandling': {'enum': ['Do not respond to DHCP requests', 'Relay DHCP to another server', 'Run a DHCP server']},
        'dhcpLeaseTime': {'enum': ['1 day', '1 hour', '1 week', '12 hours', '30 minutes', '4 hours']},
        'templateVlanType': {'enum': ['same', 'unique']},
    }

    # The local IP of the appliance on the VLAN
    applianceIp: Optional[str] = None
    # CIDR of the pool of subnets. Applicable only for template network. Each n...
    cidr: Optional[str] = None
    # DHCP boot option for boot filename
    dhcpBootFilename: Optional[str] = None
    # DHCP boot option to direct boot clients to the server to load the boot fi...
    dhcpBootNextServer: Optional[str] = None
    # Use DHCP boot options specified in other properties
    dhcpBootOptionsEnabled: Optional[bool] = None
    # The appliance's handling of DHCP requests on this VLAN. One of: 'Run a DH...
    dhcpHandling: Optional[str] = None
    # The term of DHCP leases if the appliance is running a DHCP server on this...
    dhcpLeaseTime: Optional[str] = None
    # The list of DHCP options that will be included in DHCP responses. Each ob...
    dhcpOptions: Optional[List[Dict[str, Any]]] = None
    # The IPs of the DHCP servers that DHCP requests should be relayed to
    dhcpRelayServerIps: Optional[List[str]] = None
    # The DNS nameservers used for DHCP responses, either "upstream_dns", "goog...
    dnsNameservers: Optional[str] = None
    # The DHCP fixed IP assignments on the VLAN. This should be an object that ...
    fixedIpAssignments: Optional[Dict[str, Dict[str, Any]]] = None
    # The id of the desired group policy to apply to the VLAN
    groupPolicyId: Optional[str] = None
    # The VLAN ID of the VLAN
    id: Optional[str] = None
    # The interface ID of the VLAN
    interfaceId: Optional[str] = None
    # IPv6 configuration on the VLAN
    ipv6: Optional[Dict[str, Any]] = None
    # Mandatory DHCP will enforce that clients connecting to this VLAN must use...
    mandatoryDhcp: Optional[Dict[str, Any]] = None
    # Mask used for the subnet of all bound to the template networks. Applicabl...
    mask: Optional[int] = None
    # The name of the VLAN
    name: Optional[str] = None
    # The DHCP reserved IP ranges on the VLAN
    reservedIpRanges: Optional[List[Dict[str, Any]]] = None
    # The subnet of the VLAN
    subnet: Optional[str] = None
    # Type of subnetting of the VLAN. Applicable only for template network.
    templateVlanType: Optional[str] = None
    # Boolean indicating whether VLANs are enabled (true) or disabled (false) f...
    vlansEnabled: Optional[bool] = None
    # The translated VPN subnet if VPN and VPN subnet translation are enabled o...
    vpnNatSubnet: Optional[str] = None
