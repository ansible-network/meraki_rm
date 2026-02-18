"""Generated API dataclass for Meraki wireless air_marshal.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/wireless/airMarshal
    /networks/{networkId}/wireless/airMarshal/rules
    /networks/{networkId}/wireless/airMarshal/rules/{ruleId}
    /networks/{networkId}/wireless/airMarshal/settings
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional


@dataclass
class AirMarshal:
    """Meraki wireless air_marshal API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    _FIELD_CONSTRAINTS: ClassVar[dict] = {
        'defaultPolicy': {'enum': ['allow', 'block']},
        'type': {'enum': ['alert', 'allow', 'block']},
    }

    # BSSIDs broadcasting the SSID
    bssids: Optional[List[Dict[str, Any]]] = None
    # Channels where the SSID was observed
    channels: Optional[List[int]] = None
    # Created at timestamp
    createdAt: Optional[str] = None
    # Allows clients to access rogue networks. Blocked by default.
    defaultPolicy: Optional[str] = None
    # First time the SSID was observed (epoch seconds)
    firstSeen: Optional[int] = None
    # Most recent time the SSID was observed (epoch seconds)
    lastSeen: Optional[int] = None
    # Object describing the rule specification.
    match: Optional[Dict[str, Any]] = None
    # Network details
    network: Optional[Dict[str, Any]] = None
    # The network ID
    networkId: Optional[str] = None
    # Indicates whether or not clients are allowed to       connect to rogue SS...
    ruleId: Optional[str] = None
    # SSID name
    ssid: Optional[str] = None
    # Indicates if this rule will allow, block, or alert.
    type: Optional[str] = None
    # Updated at timestamp
    updatedAt: Optional[str] = None
    # Last time observed on the SSID (epoch seconds)
    wiredLastSeen: Optional[int] = None
    # MAC addresses observed on the SSID
    wiredMacs: Optional[List[str]] = None
    # VLAN IDs observed on the SSID
    wiredVlans: Optional[List[int]] = None
