"""Versioned API model and transform mixin for Meraki organization config template (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.config_template import ConfigTemplate as GeneratedConfigTemplate

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'organizationId': ['organization_id'],
    'configTemplateId': ['config_template_id', 'id'],
}

# Fields for create
_CREATE_FIELDS = [
    'name', 'productTypes', 'timeZone', 'copyFromNetworkId',
]

# Fields for update (no id in body)
_UPDATE_FIELDS = [
    'name', 'productTypes', 'timeZone', 'copyFromNetworkId',
]


class ConfigTemplateTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki organization config template (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/organizations/{organizationId}/configTemplates',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['organizationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/organizations/{organizationId}/configTemplates',
                method='GET',
                fields=[],
                path_params=['organizationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/organizations/{organizationId}/configTemplates/{configTemplateId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['organizationId', 'configTemplateId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/organizations/{organizationId}/configTemplates/{configTemplateId}',
                method='DELETE',
                fields=[],
                path_params=['organizationId', 'configTemplateId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIConfigTemplate_v1(GeneratedConfigTemplate, ConfigTemplateTransformMixin_v1):
    """Versioned API model for Meraki organization config template (v1)."""

    _field_mapping = {
        'config_template_id': 'id',
        'name': 'name',
        'product_types': 'productTypes',
        'time_zone': 'timeZone',
        'copy_from_network_id': 'copyFromNetworkId',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.config_template import UserConfigTemplate
        return UserConfigTemplate
