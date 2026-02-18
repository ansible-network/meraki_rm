"""Versioned API model and transform mixin for Meraki wireless Air Marshal (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.air_marshal import AirMarshal as GeneratedAirMarshal

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'ruleId': ['rule_id'],
}

_CREATE_FIELDS = ['type', 'match', 'defaultPolicy']

_UPDATE_FIELDS = ['type', 'match', 'defaultPolicy']


class AirMarshalTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki wireless Air Marshal (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/wireless/airMarshal/rules',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/wireless/airMarshal/rules/{ruleId}',
                method='GET',
                fields=[],
                path_params=['networkId', 'ruleId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=2,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/wireless/airMarshal/rules',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/wireless/airMarshal/rules/{ruleId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'ruleId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/wireless/airMarshal/rules/{ruleId}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'ruleId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIAirMarshal_v1(GeneratedAirMarshal, AirMarshalTransformMixin_v1):
    """Versioned API model for Meraki wireless Air Marshal (v1)."""

    _field_mapping = {
        'rule_id': 'ruleId',
        'type': 'type',
        'match': 'match',
        'default_policy': 'defaultPolicy',
        'ssid': 'ssid',
        'bssids': 'bssids',
        'channels': 'channels',
        'first_seen': 'firstSeen',
        'last_seen': 'lastSeen',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.air_marshal import UserAirMarshal
        return UserAirMarshal
