"""Generated API dataclass for Meraki organization org_alert_profile.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /organizations/{organizationId}/alerts/profiles
    /organizations/{organizationId}/alerts/profiles/{alertConfigId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional


@dataclass
class OrgAlertProfile:
    """Meraki organization org_alert_profile API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    _FIELD_CONSTRAINTS: ClassVar[dict] = {
        'type': {'enum': ['appOutage', 'voipJitter', 'voipMos', 'voipPacketLoss', 'wanLatency', 'wanPacketLoss', 'wanStatus', 'wanUtilization']},
    }

    # The conditions that determine if the alert triggers
    alertCondition: Optional[Dict[str, Any]] = None
    # User supplied description of the alert
    description: Optional[str] = None
    # Is the alert config enabled
    enabled: Optional[bool] = None
    # The alert config ID
    id: Optional[str] = None
    # Networks with these tags will be monitored for the alert
    networkTags: Optional[List[str]] = None
    # List of recipients that will recieve the alert.
    recipients: Optional[Dict[str, Any]] = None
    # The alert type
    type: Optional[str] = None
