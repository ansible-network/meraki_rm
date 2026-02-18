"""User model for Meraki sensor alert profile."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSensorAlertProfile(BaseTransformMixin):
    """User-facing sensor alert profile model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity (API path uses 'id', response has profileId)
    id: Optional[str] = None
    # fields
    name: Optional[str] = None
    conditions: Optional[List[Dict[str, Any]]] = None
    schedule: Optional[Dict[str, Any]] = None
    recipients: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    include_sensor_url: Optional[bool] = None
    serials: Optional[List[str]] = None

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
