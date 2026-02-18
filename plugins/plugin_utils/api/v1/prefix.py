"""Versioned API model and transform mixin for Meraki appliance prefix (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.prefix import Prefix as GeneratedPrefix

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'staticDelegatedPrefixId': ['static_delegated_prefix_id'],
}

# All mutable fields for create
_CREATE_FIELDS = [
    'prefix', 'description', 'origin',
]

# All mutable fields for update
_UPDATE_FIELDS = [
    'prefix', 'description', 'origin',
]


class PrefixTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki appliance prefix (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/appliance/prefixes/delegated/statics',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/appliance/prefixes/delegated/statics/{staticDelegatedPrefixId}',
                method='GET',
                fields=[],
                path_params=['networkId', 'staticDelegatedPrefixId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/appliance/prefixes/delegated/statics',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/appliance/prefixes/delegated/statics/{staticDelegatedPrefixId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'staticDelegatedPrefixId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/appliance/prefixes/delegated/statics/{staticDelegatedPrefixId}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'staticDelegatedPrefixId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIPrefix_v1(GeneratedPrefix, PrefixTransformMixin_v1):
    """Versioned API model for Meraki appliance prefix (v1)."""

    _field_mapping = {
        'static_delegated_prefix_id': 'staticDelegatedPrefixId',
        'prefix': 'prefix',
        'description': 'description',
        'origin': 'origin',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.prefix import UserPrefix
        return UserPrefix
