"""Generated API dataclass for Meraki appliance security.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/appliance/security/events
    /networks/{networkId}/appliance/security/intrusion
    /networks/{networkId}/appliance/security/malware
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional


@dataclass
class Security:
    """Meraki appliance security API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    _FIELD_CONSTRAINTS: ClassVar[dict] = {
        'idsRulesets': {'enum': ['balanced', 'connectivity', 'security']},
        'mode': {'enum': ['detection', 'disabled', 'prevention']},
    }

    # Sha256 digests of files permitted by the malware detection engine
    allowedFiles: Optional[List[Dict[str, Any]]] = None
    # URLs permitted by the malware detection engine
    allowedUrls: Optional[List[Dict[str, Any]]] = None
    # Intrusion detection ruleset
    idsRulesets: Optional[str] = None
    # Intrusion detection mode
    mode: Optional[str] = None
    # Networks included in and excluded from the detection engine
    protectedNetworks: Optional[Dict[str, Any]] = None
