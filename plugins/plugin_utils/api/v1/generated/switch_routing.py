"""Generated API dataclass for Meraki switch switch_routing.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/switch/routing/multicast
    /networks/{networkId}/switch/routing/multicast/rendezvousPoints
    /networks/{networkId}/switch/routing/multicast/rendezvousPoints/{rendezvousPointId}
    /networks/{networkId}/switch/routing/ospf
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SwitchRouting:
    """Meraki switch switch_routing API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # OSPF areas
    areas: Optional[List[Dict[str, Any]]] = None
    # Time interval to determine when the peer will be declared inactive/dead. ...
    deadTimerInSeconds: Optional[int] = None
    # Default multicast setting for entire network. IGMP snooping and Flood unk...
    defaultSettings: Optional[Dict[str, Any]] = None
    # Boolean value to enable or disable OSPF routing. OSPF routing is disabled...
    enabled: Optional[bool] = None
    # Time interval in seconds at which hello packet will be sent to OSPF neigh...
    helloTimerInSeconds: Optional[int] = None
    # The IP address of the interface to use.
    interfaceIp: Optional[str] = None
    # The name of the interface to use.
    interfaceName: Optional[str] = None
    # Boolean value to enable or disable MD5 authentication. MD5 authentication...
    md5AuthenticationEnabled: Optional[bool] = None
    # MD5 authentication credentials. This param is only relevant if md5Authent...
    md5AuthenticationKey: Optional[Dict[str, Any]] = None
    # 'Any', or the IP address of a multicast group.
    multicastGroup: Optional[str] = None
    # Array of paired switches/stacks/profiles and corresponding multicast sett...
    overrides: Optional[List[Dict[str, Any]]] = None
    # The id.
    rendezvousPointId: Optional[str] = None
    # The serial.
    serial: Optional[str] = None
    # OSPF v3 configuration
    v3: Optional[Dict[str, Any]] = None
    # The VRF with PIM enabled L3 interface
    vrf: Optional[Dict[str, Any]] = None
