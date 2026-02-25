"""User model for Meraki MQTT broker."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserMqttBroker(BaseTransformMixin):
    """User-facing MQTT broker model with snake_case fields."""

    MODULE_NAME = 'mqtt_broker'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'mqtt_broker_id'

    # scope
    network_id: Optional[str] = None
    # identity
    mqtt_broker_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Name of the MQTT broker."})
    host: Optional[str] = field(default=None, metadata={"description": "Host name or IP address of the MQTT broker."})
    port: Optional[int] = field(default=None, metadata={"description": "Port for the MQTT broker."})
    authentication: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Authentication settings."})
    security: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Security settings."})

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
