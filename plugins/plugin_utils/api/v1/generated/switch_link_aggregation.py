"""Generated API dataclass for Meraki switch switch_link_aggregation.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/switch/linkAggregations
    /networks/{networkId}/switch/linkAggregations/{linkAggregationId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SwitchLinkAggregation:
    """Meraki switch switch_link_aggregation API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # The ID for the link aggregation.
    id: Optional[str] = None
    # The ID for the link aggregation.
    switchPorts: Optional[List[Dict[str, Any]]] = None
    # Array of switch profile ports for creating aggregation group. Minimum 2 a...
    switchProfilePorts: Optional[List[Dict[str, Any]]] = None
