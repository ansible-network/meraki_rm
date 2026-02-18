"""Generated API dataclass for Meraki switch switch_stp.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/switch/stp
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SwitchStp:
    """Meraki switch switch_stp API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # The spanning tree protocol status in network
    rstpEnabled: Optional[bool] = None
    # STP bridge priority for switches/stacks or switch templates. An empty arr...
    stpBridgePriority: Optional[List[Dict[str, Any]]] = None
