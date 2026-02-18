"""Generated API dataclass for Meraki switch switch_port.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /devices/{serial}/switch/ports
    /devices/{serial}/switch/ports/cycle
    /devices/{serial}/switch/ports/statuses
    /devices/{serial}/switch/ports/statuses/packets
    /devices/{serial}/switch/ports/{portId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SwitchPort:
    """Meraki switch switch_port API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # The number of a custom access policy to configure on the switch port. Onl...
    accessPolicyNumber: Optional[int] = None
    # The type of the access policy of the switch port. Only applicable to acce...
    accessPolicyType: Optional[str] = None
    # The adaptive policy group data of the port.
    adaptivePolicyGroup: Optional[Dict[str, Any]] = None
    # The adaptive policy group ID that will be used to tag traffic through thi...
    adaptivePolicyGroupId: Optional[str] = None
    # The VLANs allowed on the switch port. Only applicable to trunk ports.
    allowedVlans: Optional[str] = None
    # The Cisco Discovery Protocol (CDP) information of the connected device.
    cdp: Optional[Dict[str, Any]] = None
    # The number of clients connected through this port.
    clientCount: Optional[int] = None
    # If true, ARP packets for this port will be considered trusted, and Dynami...
    daiTrusted: Optional[bool] = None
    # dot3az settings for the port
    dot3az: Optional[Dict[str, Any]] = None
    # The current duplex of a connected port.
    duplex: Optional[str] = None
    # The status of the switch port.
    enabled: Optional[bool] = None
    # All errors present on the port.
    errors: Optional[List[str]] = None
    # For supported switches (e.g. MS420/MS425), whether or not the port has fl...
    flexibleStackingEnabled: Optional[bool] = None
    # High speed port enablement settings for C9500-32QC
    highSpeed: Optional[Dict[str, Any]] = None
    # Whether the port is the switch's uplink.
    isUplink: Optional[bool] = None
    # The isolation status of the switch port.
    isolationEnabled: Optional[bool] = None
    # The link speed for the switch port.
    linkNegotiation: Optional[str] = None
    # Available link speeds for the switch port.
    linkNegotiationCapabilities: Optional[List[str]] = None
    # The Link Layer Discovery Protocol (LLDP) information of the connected dev...
    lldp: Optional[Dict[str, Any]] = None
    # Only devices with MAC addresses specified in this list will have access t...
    macAllowList: Optional[List[str]] = None
    # The maximum number of MAC addresses for regular MAC allow list. Only appl...
    macWhitelistLimit: Optional[int] = None
    # Port mirror
    mirror: Optional[Dict[str, Any]] = None
    # Expansion module
    module: Optional[Dict[str, Any]] = None
    # The name of the switch port.
    name: Optional[str] = None
    # The packet counts on the switch. Note that this data is collected periodi...
    packets: Optional[List[Dict[str, Any]]] = None
    # If true, Peer SGT is enabled for traffic through this switch port. Applic...
    peerSgtCapable: Optional[bool] = None
    # PoE status of the port.
    poe: Optional[Dict[str, Any]] = None
    # The PoE status of the switch port.
    poeEnabled: Optional[bool] = None
    # The identifier of the switch port.
    portId: Optional[str] = None
    # The ID of the port schedule. A value of null will clear the port schedule.
    portScheduleId: Optional[str] = None
    # List of switch ports
    ports: Optional[List[str]] = None
    # How much power (in watt-hours) has been delivered by this port during the...
    powerUsageInWh: Optional[float] = None
    # Profile attributes
    profile: Optional[Dict[str, Any]] = None
    # The rapid spanning tree protocol status.
    rstpEnabled: Optional[bool] = None
    # The port schedule data.
    schedule: Optional[Dict[str, Any]] = None
    # The Secure Port status of the port.
    securePort: Optional[Dict[str, Any]] = None
    # The Spanning Tree Protocol (STP) information of the connected device.
    spanningTree: Optional[Dict[str, Any]] = None
    # The current data transfer rate which the port is operating at.
    speed: Optional[str] = None
    # The current connection status of the port.
    status: Optional[str] = None
    # The initial list of MAC addresses for sticky Mac allow list. Only applica...
    stickyMacAllowList: Optional[List[str]] = None
    # The maximum number of MAC addresses for sticky MAC allow list. Only appli...
    stickyMacAllowListLimit: Optional[int] = None
    # The storm control status of the switch port.
    stormControlEnabled: Optional[bool] = None
    # The state of the STP guard ('disabled', 'root guard', 'bpdu guard' or 'lo...
    stpGuard: Optional[str] = None
    # The state of STP PortFast Trunk on the switch port.
    stpPortFastTrunk: Optional[bool] = None
    # The list of tags of the switch port.
    tags: Optional[List[str]] = None
    # A breakdown of the average speed of data that has passed through this por...
    trafficInKbps: Optional[Dict[str, Any]] = None
    # The type of the switch port ('access', 'trunk', 'stack', 'routed', 'svl' ...
    type: Optional[str] = None
    # The action to take when Unidirectional Link is detected (Alert only, Enfo...
    udld: Optional[str] = None
    # A breakdown of how many kilobytes have passed through this port during th...
    usageInKb: Optional[Dict[str, Any]] = None
    # The VLAN of the switch port. For a trunk port, this is the native VLAN. A...
    vlan: Optional[int] = None
    # The voice VLAN of the switch port. Only applicable to access ports.
    voiceVlan: Optional[int] = None
    # All warnings present on the port.
    warnings: Optional[List[str]] = None
