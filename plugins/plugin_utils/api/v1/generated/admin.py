"""Generated API dataclass for Meraki organization admin.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /organizations/{organizationId}/admins
    /organizations/{organizationId}/admins/{adminId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Admin:
    """Meraki organization admin API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # Status of the admin's account
    accountStatus: Optional[str] = None
    # Admin's authentication method
    authenticationMethod: Optional[str] = None
    # Admin's email address
    email: Optional[str] = None
    # Indicates whether the admin has an API key
    hasApiKey: Optional[bool] = None
    # Admin's ID
    id: Optional[str] = None
    # Time when the admin was last active
    lastActive: Optional[str] = None
    # Admin's username
    name: Optional[str] = None
    # Admin network access information
    networks: Optional[List[Dict[str, Any]]] = None
    # Admin's level of access to the organization
    orgAccess: Optional[str] = None
    # Admin tag information
    tags: Optional[List[Dict[str, Any]]] = None
    # Indicates whether two-factor authentication is enabled
    twoFactorAuthEnabled: Optional[bool] = None
