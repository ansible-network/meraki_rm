"""Generated API dataclass for Meraki device device_management_interface.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /devices/{serial}/managementInterface
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DeviceManagementInterface:
    """Meraki device device_management_interface API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # Dynamic DNS hostnames.
    ddnsHostnames: Optional[Dict[str, Any]] = None
    # WAN 1 settings
    wan1: Optional[Dict[str, Any]] = None
    # WAN 2 settings (only for MX devices)
    wan2: Optional[Dict[str, Any]] = None
