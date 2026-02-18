"""Versioned API model and transform mixin for Meraki switch link aggregation (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.switch_link_aggregation import SwitchLinkAggregation as GeneratedSwitchLinkAggregation

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'linkAggregationId': ['link_aggregation_id', 'id'],
}

_CREATE_FIELDS = ['switchPorts', 'switchProfilePorts']

_UPDATE_FIELDS = ['switchPorts', 'switchProfilePorts']


class SwitchLinkAggregationTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki switch link aggregation (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/switch/linkAggregations',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/switch/linkAggregations/{linkAggregationId}',
                method='GET',
                fields=[],
                path_params=['networkId', 'linkAggregationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=2,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/switch/linkAggregations',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/switch/linkAggregations/{linkAggregationId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'linkAggregationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/switch/linkAggregations/{linkAggregationId}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'linkAggregationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APISwitchLinkAggregation_v1(GeneratedSwitchLinkAggregation, SwitchLinkAggregationTransformMixin_v1):
    """Versioned API model for Meraki switch link aggregation (v1)."""

    _field_mapping = {
        'link_aggregation_id': 'id',
        'switch_ports': 'switchPorts',
        'switch_profile_ports': 'switchProfilePorts',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.switch_link_aggregation import UserSwitchLinkAggregation
        return UserSwitchLinkAggregation
