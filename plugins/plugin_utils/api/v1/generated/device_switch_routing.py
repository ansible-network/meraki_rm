"""Generated API dataclass for Meraki device device_switch_routing.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /devices/{serial}/switch/routing/interfaces
    /devices/{serial}/switch/routing/interfaces/{interfaceId}
    /devices/{serial}/switch/routing/interfaces/{interfaceId}/dhcp
    /devices/{serial}/switch/routing/staticRoutes
    /devices/{serial}/switch/routing/staticRoutes/{staticRouteId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DeviceSwitchRouting:
    """Meraki device device_switch_routing API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # The identifier of a layer 3 static route
    staticRouteId: Optional[str] = None
    # Option to advertise static routes via OSPF
    advertiseViaOspfEnabled: Optional[bool] = None
    # The PXE boot server file name for the DHCP server running on the switch s...
    bootFileName: Optional[str] = None
    # The PXE boot server IP for the DHCP server running on the switch stack in...
    bootNextServer: Optional[str] = None
    # Enable DHCP boot options to provide PXE boot options configs for the dhcp...
    bootOptionsEnabled: Optional[bool] = None
    # IPv4 default gateway
    defaultGateway: Optional[str] = None
    # The DHCP lease time config for the dhcp server running on the switch stac...
    dhcpLeaseTime: Optional[str] = None
    # The DHCP mode options for the switch stack interface ('dhcpDisabled', 'dh...
    dhcpMode: Optional[str] = None
    # Array of DHCP options consisting of code, type and value for the DHCP ser...
    dhcpOptions: Optional[List[Dict[str, Any]]] = None
    # The DHCP relay server IPs to which DHCP packets would get relayed for the...
    dhcpRelayServerIps: Optional[List[str]] = None
    # The DHCP name server IPs when DHCP name server option is 'custom'
    dnsCustomNameservers: Optional[List[str]] = None
    # The DHCP name server option for the dhcp server running on the switch sta...
    dnsNameserversOption: Optional[str] = None
    # Array of DHCP reserved IP assignments for the DHCP server running on the ...
    fixedIpAssignments: Optional[List[Dict[str, Any]]] = None
    # The ID
    interfaceId: Optional[str] = None
    # IPv4 address
    interfaceIp: Optional[str] = None
    # IPv6 addressing
    ipv6: Optional[Dict[str, Any]] = None
    # Loopback Interface settings
    loopback: Optional[Dict[str, Any]] = None
    # Optional fallback IP address for management traffic
    managementNextHop: Optional[str] = None
    # The mode
    mode: Optional[str] = None
    # Multicast routing status
    multicastRouting: Optional[str] = None
    # The name
    name: Optional[str] = None
    # The IP address of the router to which traffic for this destination networ...
    nextHopIp: Optional[str] = None
    # IPv4 OSPF Settings
    ospfSettings: Optional[Dict[str, Any]] = None
    # IPv6 OSPF Settings
    ospfV3: Optional[Dict[str, Any]] = None
    # Option to prefer static routes over OSPF routes
    preferOverOspfRoutesEnabled: Optional[bool] = None
    # Array of DHCP reserved IP assignments for the DHCP server running on the ...
    reservedIpRanges: Optional[List[Dict[str, Any]]] = None
    # Device serial
    serial: Optional[str] = None
    # IPv4 subnet
    subnet: Optional[str] = None
    # Switch Port ID when in Routed mode
    switchPortId: Optional[str] = None
    # When true, this interface is used as static IPv4 uplink
    uplinkV4: Optional[bool] = None
    # When true, this interface is used as static IPv6 uplink
    uplinkV6: Optional[bool] = None
    # VLAN ID
    vlanId: Optional[int] = None
    # VRF settings. Included on networks with IOS XE 17.18 or higher
    vrf: Optional[Dict[str, Any]] = None
