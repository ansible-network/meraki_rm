"""User model for Meraki sensor alert profile."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSensorAlertProfile(BaseTransformMixin):
    """User-facing sensor alert profile model with snake_case fields."""

    MODULE_NAME = 'sensor_alert_profile'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'id'

    # scope
    network_id: Optional[str] = None
    # identity (API path uses 'id', response has profileId)
    id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Name of the sensor alert profile."})
    conditions: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "List of conditions that trigger alerts."})
    schedule: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Sensor schedule for the alert profile."})
    recipients: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Recipients that receive alerts."})
    message: Optional[str] = field(default=None, metadata={"description": "Custom message for email and text alerts."})
    include_sensor_url: Optional[bool] = field(default=None, metadata={"description": "Include dashboard link to sensor in messages."})
    serials: Optional[List[str]] = field(default=None, metadata={"description": "Device serials assigned to this profile."})

    _field_mapping = {
        'id': 'profileId',
        'name': 'name',
        'conditions': 'conditions',
        'schedule': 'schedule',
        'recipients': 'recipients',
        'message': 'message',
        'include_sensor_url': 'includeSensorUrl',
        'serials': 'serials',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.sensor_alert_profile import APISensorAlertProfile_v1
        return APISensorAlertProfile_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
