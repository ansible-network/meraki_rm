"""Generated API dataclass for Meraki organization adaptive_policy.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /organizations/{organizationId}/adaptivePolicy/acls
    /organizations/{organizationId}/adaptivePolicy/acls/{aclId}
    /organizations/{organizationId}/adaptivePolicy/groups
    /organizations/{organizationId}/adaptivePolicy/groups/{id}
    /organizations/{organizationId}/adaptivePolicy/overview
    /organizations/{organizationId}/adaptivePolicy/policies
    /organizations/{organizationId}/adaptivePolicy/policies/{id}
    /organizations/{organizationId}/adaptivePolicy/settings
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class AdaptivePolicy:
    """Meraki organization adaptive_policy API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # ID of the adaptive policy ACL
    aclId: Optional[str] = None
    # The access control lists for the adaptive policy
    acls: Optional[List[Dict[str, Any]]] = None
    # The ID for the adaptive policy
    adaptivePolicyId: Optional[str] = None
    # The current amount of various adaptive policy objects.
    counts: Optional[Dict[str, Any]] = None
    # When the adaptive policy ACL was created
    createdAt: Optional[str] = None
    # Description of the adaptive policy ACL
    description: Optional[str] = None
    # The destination group for the given adaptive policy
    destinationGroup: Optional[Dict[str, Any]] = None
    # List of network IDs with adaptive policy enabled
    enabledNetworks: Optional[List[str]] = None
    # The ID of the adaptive policy group
    groupId: Optional[str] = None
    # IP version of adpative policy ACL
    ipVersion: Optional[str] = None
    # Whether the adaptive policy group is the default group
    isDefaultGroup: Optional[bool] = None
    # The rule to apply if there is no matching ACL
    lastEntryRule: Optional[str] = None
    # The current limits of various adaptive policy objects.
    limits: Optional[Dict[str, Any]] = None
    # Name of the adaptive policy ACL
    name: Optional[str] = None
    # The policy objects for the adaptive policy group
    policyObjects: Optional[List[Dict[str, Any]]] = None
    # List of required IP mappings for the adaptive policy group
    requiredIpMappings: Optional[List[str]] = None
    # An ordered array of the adaptive policy ACL rules
    rules: Optional[List[Dict[str, Any]]] = None
    # The security group tag for the adaptive policy group
    sgt: Optional[int] = None
    # The source group for the given adaptive policy
    sourceGroup: Optional[Dict[str, Any]] = None
    # When the adaptive policy ACL was last updated
    updatedAt: Optional[str] = None
