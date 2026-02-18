"""Generated API dataclass for Meraki switch switch_settings.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/switch/alternateManagementInterface
    /networks/{networkId}/switch/dscpToCosMappings
    /networks/{networkId}/switch/mtu
    /networks/{networkId}/switch/settings
    /networks/{networkId}/switch/stormControl
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SwitchSettings:
    """Meraki switch switch_settings API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # Broadcast threshold.
    broadcastThreshold: Optional[int] = None
    # MTU size for the entire network. Default value is 9578.
    defaultMtuSize: Optional[int] = None
    # Boolean value to enable or disable AMI configuration. If enabled, VLAN an...
    enabled: Optional[bool] = None
    # MAC blocklist
    macBlocklist: Optional[Dict[str, Any]] = None
    # An array of DSCP to CoS mappings. An empty array will reset the mappings ...
    mappings: Optional[List[Dict[str, Any]]] = None
    # Multicast threshold.
    multicastThreshold: Optional[int] = None
    # Override MTU size for individual switches or switch templates.       An e...
    overrides: Optional[List[Dict[str, Any]]] = None
    # Exceptions on a per switch basis to "useCombinedPower"
    powerExceptions: Optional[List[Dict[str, Any]]] = None
    # Can be one or more of the following values: 'radius', 'snmp' or 'syslog'
    protocols: Optional[List[str]] = None
    # Array of switch serial number and IP assignment. If parameter is present,...
    switches: Optional[List[Dict[str, Any]]] = None
    # Grouped traffic types
    treatTheseTrafficTypesAsOneThreshold: Optional[List[str]] = None
    # Unknown Unicast threshold.
    unknownUnicastThreshold: Optional[int] = None
    # Uplink client sampling
    uplinkClientSampling: Optional[Dict[str, Any]] = None
    # Settings related to uplink selection on IOS-XE switches.
    uplinkSelection: Optional[Dict[str, Any]] = None
    # The use Combined Power as the default behavior of secondary power supplie...
    useCombinedPower: Optional[bool] = None
    # Boolean value to use out-of-band management interface when configured
    useOobMgmt: Optional[bool] = None
    # Management VLAN
    vlan: Optional[int] = None
    # Alternate management VLAN, must be between 1 and 4094
    vlanId: Optional[int] = None
