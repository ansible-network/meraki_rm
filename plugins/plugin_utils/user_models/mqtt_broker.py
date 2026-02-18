"""User model for Meraki MQTT broker."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserMqttBroker(BaseTransformMixin):
    """User-facing MQTT broker model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    mqtt_broker_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    authentication: Optional[Dict[str, Any]] = None
    security: Optional[Dict[str, Any]] = None

    _field_mapping = {
        'mqtt_broker_id': 'id',
        'name': 'name',
        'host': 'host',
        'port': 'port',
        'authentication': 'authentication',
        'security': 'security',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.mqtt_broker import APIMqttBroker_v1
        return APIMqttBroker_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
