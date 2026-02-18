"""Generated API dataclass for Meraki network group_policy.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/groupPolicies
    /networks/{networkId}/groupPolicies/{groupPolicyId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional


@dataclass
class GroupPolicy:
    """Meraki network group_policy API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    _FIELD_CONSTRAINTS: ClassVar[dict] = {
        'splashAuthSettings': {'enum': ['bypass', 'network default']},
    }

    # The bandwidth settings for clients bound to your group policy.
    bandwidth: Optional[Dict[str, Any]] = None
    # The Bonjour settings for your group policy. Only valid if your network ha...
    bonjourForwarding: Optional[Dict[str, Any]] = None
    # The content filtering settings for your group policy
    contentFiltering: Optional[Dict[str, Any]] = None
    # The firewall and traffic shaping rules and settings for your policy.
    firewallAndTrafficShaping: Optional[Dict[str, Any]] = None
    # The ID of the group policy
    groupPolicyId: Optional[str] = None
    # The name for your group policy. Required.
    name: Optional[str] = None
    # The schedule for the group policy. Schedules are applied to days of the w...
    scheduling: Optional[Dict[str, Any]] = None
    # Whether clients bound to your policy will bypass splash authorization or ...
    splashAuthSettings: Optional[str] = None
    # The VLAN tagging settings for your group policy. Only available if your n...
    vlanTagging: Optional[Dict[str, Any]] = None
