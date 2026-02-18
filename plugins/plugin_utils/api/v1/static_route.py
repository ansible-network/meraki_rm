"""Versioned API model and transform mixin for Meraki appliance static route (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.static_route import StaticRoute as GeneratedStaticRoute

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'staticRouteId': ['static_route_id', 'id'],
}

# All mutable fields for create (id not in body for create - assigned by API)
_CREATE_FIELDS = [
    'name', 'subnet', 'gatewayIp', 'gatewayVlanId', 'enabled',
    'fixedIpAssignments', 'reservedIpRanges', 'ipVersion',
]

# All mutable fields for update (no id in body)
_UPDATE_FIELDS = [
    'name', 'subnet', 'gatewayIp', 'gatewayVlanId', 'enabled',
    'fixedIpAssignments', 'reservedIpRanges', 'ipVersion',
]


class StaticRouteTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki appliance static route (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/appliance/staticRoutes',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/appliance/staticRoutes/{staticRouteId}',
                method='GET',
                fields=[],
                path_params=['networkId', 'staticRouteId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/appliance/staticRoutes',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/appliance/staticRoutes/{staticRouteId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'staticRouteId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/appliance/staticRoutes/{staticRouteId}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'staticRouteId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIStaticRoute_v1(GeneratedStaticRoute, StaticRouteTransformMixin_v1):
    """Versioned API model for Meraki appliance static route (v1)."""

    _field_mapping = {
        'static_route_id': 'id',
        'name': 'name',
        'subnet': 'subnet',
        'gateway_ip': 'gatewayIp',
        'gateway_vlan_id': 'gatewayVlanId',
        'enabled': 'enabled',
        'fixed_ip_assignments': 'fixedIpAssignments',
        'reserved_ip_ranges': 'reservedIpRanges',
        'ip_version': 'ipVersion',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.static_route import UserStaticRoute
        return UserStaticRoute
