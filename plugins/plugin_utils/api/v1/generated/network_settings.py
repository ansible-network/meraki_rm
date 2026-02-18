"""Generated API dataclass for Meraki network network_settings.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/alerts/settings
    /networks/{networkId}/netflow
    /networks/{networkId}/settings
    /networks/{networkId}/snmp
    /networks/{networkId}/syslogServers
    /networks/{networkId}/trafficAnalysis
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class NetworkSettings:
    """Meraki network network_settings API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # The type of SNMP access. Can be one of 'none' (disabled), 'community' (V1...
    access: Optional[str] = None
    # Alert-specific configuration for each type. Only alerts that pertain to t...
    alerts: Optional[List[Dict[str, Any]]] = None
    # The IPv4 address of the NetFlow collector.
    collectorIp: Optional[str] = None
    # The port that the NetFlow collector will be listening on.
    collectorPort: Optional[int] = None
    # SNMP community string if access is 'community'.
    communityString: Optional[str] = None
    # The list of items that make up the custom pie chart for traffic reporting.
    customPieChartItems: Optional[List[Dict[str, Any]]] = None
    # The network-wide destinations for all alerts on the network.
    defaultDestinations: Optional[Dict[str, Any]] = None
    # The port that the Encrypted Traffic Analytics collector will be listening...
    etaDstPort: Optional[int] = None
    # Boolean indicating whether Encrypted Traffic Analytics is enabled (true) ...
    etaEnabled: Optional[bool] = None
    # A hash of FIPS options applied to the Network
    fips: Optional[Dict[str, Any]] = None
    # A hash of Local Status page(s)' authentication options applied to the Net...
    localStatusPage: Optional[Dict[str, Any]] = None
    # Enables / disables the local device status pages (<a target='_blank' href...
    localStatusPageEnabled: Optional[bool] = None
    # The traffic analysis mode for the network. Can be one of 'disabled' (do n...
    mode: Optional[str] = None
    # Mute alerts under certain conditions
    muting: Optional[Dict[str, Any]] = None
    # A hash of Named VLANs options applied to the Network.
    namedVlans: Optional[Dict[str, Any]] = None
    # Enables / disables access to the device status page (<a target='_blank'>h...
    remoteStatusPageEnabled: Optional[bool] = None
    # Boolean indicating whether NetFlow traffic reporting is enabled (true) or...
    reportingEnabled: Optional[bool] = None
    # A hash of SecureConnect options applied to the Network.
    securePort: Optional[Dict[str, Any]] = None
    # List of the syslog servers for this network
    servers: Optional[List[Dict[str, Any]]] = None
    # SNMP settings if access is 'users'.
    users: Optional[List[Dict[str, Any]]] = None
