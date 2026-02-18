"""Generated API dataclass for Meraki network meraki_auth_user.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/merakiAuthUsers
    /networks/{networkId}/merakiAuthUsers/{merakiAuthUserId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional


@dataclass
class MerakiAuthUser:
    """Meraki network meraki_auth_user API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    _FIELD_CONSTRAINTS: ClassVar[dict] = {
        'accountType': {'enum': ['802.1X', 'Client VPN', 'Guest']},
    }

    # Authorization type for user.
    accountType: Optional[str] = None
    # User authorization info
    authorizations: Optional[List[Dict[str, Any]]] = None
    # Creation time of the user
    createdAt: Optional[str] = None
    # Email address of the user
    email: Optional[str] = None
    # Whether or not Meraki should email the password to user. Default is false.
    emailPasswordToUser: Optional[bool] = None
    # Meraki auth user id
    id: Optional[str] = None
    # Whether or not the user is a Dashboard administrator
    isAdmin: Optional[bool] = None
    # Name of the user
    name: Optional[str] = None
    # The password for this user account. Only required If the user is not a Da...
    password: Optional[str] = None
