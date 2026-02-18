"""Generated API dataclass for Meraki appliance prefix.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/appliance/prefixes/delegated/statics
    /networks/{networkId}/appliance/prefixes/delegated/statics/{staticDelegatedPrefixId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Prefix:
    """Meraki appliance prefix API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # Prefix creation time.
    createdAt: Optional[str] = None
    # Identifying description for the prefix.
    description: Optional[str] = None
    # WAN1/WAN2/Independent prefix.
    origin: Optional[Dict[str, Any]] = None
    # IPv6 prefix/prefix length.
    prefix: Optional[str] = None
    # Static delegated prefix id.
    staticDelegatedPrefixId: Optional[str] = None
    # Prefix Updated time.
    updatedAt: Optional[str] = None
