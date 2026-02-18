"""Generated API dataclass for Meraki switch switch_acl.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/switch/accessControlLists
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SwitchAcl:
    """Meraki switch switch_acl API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # An ordered array of the access control list rules
    rules: Optional[List[Dict[str, Any]]] = None
