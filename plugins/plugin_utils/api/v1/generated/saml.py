"""Generated API dataclass for Meraki organization saml.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /organizations/{organizationId}/saml
    /organizations/{organizationId}/saml/idps
    /organizations/{organizationId}/saml/idps/{idpId}
    /organizations/{organizationId}/samlRoles
    /organizations/{organizationId}/samlRoles/{samlRoleId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Saml:
    """Meraki organization saml API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # The list of camera access privileges for SAML administrator
    camera: Optional[List[Dict[str, Any]]] = None
    # URL that is consuming SAML Identity Provider (IdP)
    consumerUrl: Optional[str] = None
    # Toggle depicting if SAML SSO settings are enabled
    enabled: Optional[bool] = None
    # ID associated with the SAML role
    id: Optional[str] = None
    # ID associated with the SAML Identity Provider (IdP)
    idpId: Optional[str] = None
    # The list of networks that the SAML administrator has privileges on
    networks: Optional[List[Dict[str, Any]]] = None
    # The privilege of the SAML administrator on the organization
    orgAccess: Optional[str] = None
    # The role of the SAML administrator
    role: Optional[str] = None
    # Dashboard will redirect users to this URL when they sign out.
    sloLogoutUrl: Optional[str] = None
    # SP-Initiated SSO settings
    spInitiated: Optional[Dict[str, Any]] = None
    # Dashboard will redirect users to this URL to log in again when their sess...
    ssoLoginUrl: Optional[str] = None
    # The list of tags that the SAML administrator has privleges on
    tags: Optional[List[Dict[str, Any]]] = None
    # URL that is consuming SAML Identity Provider (IdP) for Meraki Vision Portal
    visionConsumerUrl: Optional[str] = None
    # Fingerprint (SHA1) of the SAML certificate provided by your Identity Prov...
    x509certSha1Fingerprint: Optional[str] = None
