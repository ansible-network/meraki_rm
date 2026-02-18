"""Generated API dataclass for Meraki sensor sensor_alert_profile.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/sensor/alerts/profiles
    /networks/{networkId}/sensor/alerts/profiles/{id}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SensorAlertProfile:
    """Meraki sensor sensor_alert_profile API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # List of conditions that will cause the profile to send an alert.
    conditions: Optional[List[Dict[str, Any]]] = None
    # Include dashboard link to sensor in messages (default: true).
    includeSensorUrl: Optional[bool] = None
    # A custom message that will appear in email and text message alerts.
    message: Optional[str] = None
    # Name of the sensor alert profile.
    name: Optional[str] = None
    # ID of the sensor alert profile.
    profileId: Optional[str] = None
    # List of recipients that will receive the alert.
    recipients: Optional[Dict[str, Any]] = None
    # The sensor schedule to use with the alert profile.
    schedule: Optional[Dict[str, Any]] = None
    # List of device serials assigned to this sensor alert profile.
    serials: Optional[List[str]] = None
