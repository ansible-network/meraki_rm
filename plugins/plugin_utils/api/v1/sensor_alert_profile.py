"""Versioned API model and transform mixin for Meraki sensor alert profile (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.sensor_alert_profile import SensorAlertProfile as GeneratedSensorAlertProfile

# Path param aliases for snake_case user model -> camelCase API path
# API path uses 'id', response body uses profileId
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'id': ['id', 'profile_id'],
}

# All mutable fields for create (profileId in response, id in path)
_CREATE_FIELDS = [
    'name', 'conditions', 'schedule', 'recipients', 'message',
    'includeSensorUrl', 'serials',
]

# All mutable fields for update
_UPDATE_FIELDS = [
    'name', 'conditions', 'schedule', 'recipients', 'message',
    'includeSensorUrl', 'serials',
]


class SensorAlertProfileTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki sensor alert profile (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/sensor/alerts/profiles',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/sensor/alerts/profiles/{id}',
                method='GET',
                fields=[],
                path_params=['networkId', 'id'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/sensor/alerts/profiles',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/sensor/alerts/profiles/{id}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'id'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/sensor/alerts/profiles/{id}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'id'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APISensorAlertProfile_v1(GeneratedSensorAlertProfile, SensorAlertProfileTransformMixin_v1):
    """Versioned API model for Meraki sensor alert profile (v1)."""

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
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.sensor_alert_profile import UserSensorAlertProfile
        return UserSensorAlertProfile
