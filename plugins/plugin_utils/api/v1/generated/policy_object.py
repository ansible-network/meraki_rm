"""Generated API dataclass for Meraki organization policy_object.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /organizations/{organizationId}/policyObjects
    /organizations/{organizationId}/policyObjects/groups
    /organizations/{organizationId}/policyObjects/groups/{policyObjectGroupId}
    /organizations/{organizationId}/policyObjects/{policyObjectId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class PolicyObject:
    """Meraki organization policy_object API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # Category of a policy object (one of: adaptivePolicy, network)
    category: Optional[str] = None
    # CIDR Value of a policy object
    cidr: Optional[str] = None
    # Time Stamp of policy object creation.
    createdAt: Optional[str] = None
    # Fully qualified domain name of policy object (e.g. "example.com")
    fqdn: Optional[str] = None
    # The IDs of policy object groups the policy object belongs to.
    groupIds: Optional[List[str]] = None
    # Policy object ID
    id: Optional[str] = None
    # IP Address of a policy object (e.g. "1.2.3.4")
    ip: Optional[str] = None
    # Mask of a policy object (e.g. "255.255.0.0")
    mask: Optional[str] = None
    # Name of policy object (alphanumeric, space, dash, or underscore character...
    name: Optional[str] = None
    # The IDs of the networks that use the policy object.
    networkIds: Optional[List[str]] = None
    # Policy objects associated with Network Object Group or Port Object Group
    objectIds: Optional[List[int]] = None
    # Type of a policy object (one of: adaptivePolicyIpv4Cidr, cidr, fqdn, ipAn...
    type: Optional[str] = None
    # Time Stamp of policy object updation.
    updatedAt: Optional[str] = None
