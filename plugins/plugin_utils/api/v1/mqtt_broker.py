"""Versioned API model and transform mixin for Meraki MQTT broker (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.mqtt_broker import MqttBroker as GeneratedMqttBroker

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'mqttBrokerId': ['mqtt_broker_id', 'id'],
}

# All mutable fields for create
_CREATE_FIELDS = [
    'name', 'host', 'port', 'authentication', 'security',
]

# All mutable fields for update
_UPDATE_FIELDS = [
    'name', 'host', 'port', 'authentication', 'security',
]


class MqttBrokerTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki MQTT broker (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/mqttBrokers',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/mqttBrokers/{mqttBrokerId}',
                method='GET',
                fields=[],
                path_params=['networkId', 'mqttBrokerId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/mqttBrokers',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/mqttBrokers/{mqttBrokerId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'mqttBrokerId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/mqttBrokers/{mqttBrokerId}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'mqttBrokerId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIMqttBroker_v1(GeneratedMqttBroker, MqttBrokerTransformMixin_v1):
    """Versioned API model for Meraki MQTT broker (v1)."""

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
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.mqtt_broker import UserMqttBroker
        return UserMqttBroker
