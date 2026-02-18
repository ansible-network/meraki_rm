"""Generated API dataclass for Meraki switch switch_qos_rule.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/switch/qosRules
    /networks/{networkId}/switch/qosRules/order
    /networks/{networkId}/switch/qosRules/{qosRuleId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SwitchQosRule:
    """Meraki switch switch_qos_rule API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # DSCP tag for the incoming packet. Set this to -1 to trust incoming DSCP. ...
    dscp: Optional[int] = None
    # The destination port of the incoming packet. Applicable only if protocol ...
    dstPort: Optional[int] = None
    # The destination port range of the incoming packet. Applicable only if pro...
    dstPortRange: Optional[str] = None
    # Qos Rule id
    id: Optional[str] = None
    # The protocol of the incoming packet. Can be one of "ANY", "TCP" or "UDP"....
    protocol: Optional[str] = None
    # Qos Rule ids
    ruleIds: Optional[List[str]] = None
    # The source port of the incoming packet. Applicable only if protocol is TC...
    srcPort: Optional[int] = None
    # The source port range of the incoming packet. Applicable only if protocol...
    srcPortRange: Optional[str] = None
    # The VLAN of the incoming packet. A null value will match any VLAN.
    vlan: Optional[int] = None
