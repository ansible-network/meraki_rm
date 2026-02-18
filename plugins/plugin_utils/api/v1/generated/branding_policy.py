"""Generated API dataclass for Meraki organization branding_policy.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /organizations/{organizationId}/brandingPolicies
    /organizations/{organizationId}/brandingPolicies/priorities
    /organizations/{organizationId}/brandingPolicies/{brandingPolicyId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class BrandingPolicy:
    """Meraki organization branding_policy API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # Settings for describing which kinds of admins this policy applies to.
    adminSettings: Optional[Dict[str, Any]] = None
    # An ordered list of branding policy IDs that determines the priority order...
    brandingPolicyIds: Optional[List[str]] = None
    # Properties describing the custom logo attached to the branding policy.
    customLogo: Optional[Dict[str, Any]] = None
    # Boolean indicating whether this policy is enabled.
    enabled: Optional[bool] = None
    # Settings for describing the modifications to various Help page features. ...
    helpSettings: Optional[Dict[str, Any]] = None
    # Name of the Dashboard branding policy.
    name: Optional[str] = None
