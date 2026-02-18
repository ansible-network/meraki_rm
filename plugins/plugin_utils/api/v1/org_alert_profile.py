"""Versioned API model and transform mixin for Meraki organization alert profile (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.org_alert_profile import OrgAlertProfile as GeneratedOrgAlertProfile

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'organizationId': ['organization_id'],
    'alertConfigId': ['alert_config_id', 'id'],
}

# Fields for create
_CREATE_FIELDS = [
    'type', 'enabled', 'alertCondition', 'recipients', 'networkTags', 'description',
]

# Fields for update (no id in body)
_UPDATE_FIELDS = [
    'type', 'enabled', 'alertCondition', 'recipients', 'networkTags', 'description',
]


class OrgAlertProfileTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki organization alert profile (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/organizations/{organizationId}/alerts/profiles',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['organizationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/organizations/{organizationId}/alerts/profiles',
                method='GET',
                fields=[],
                path_params=['organizationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/organizations/{organizationId}/alerts/profiles/{alertConfigId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['organizationId', 'alertConfigId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/organizations/{organizationId}/alerts/profiles/{alertConfigId}',
                method='DELETE',
                fields=[],
                path_params=['organizationId', 'alertConfigId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIOrgAlertProfile_v1(GeneratedOrgAlertProfile, OrgAlertProfileTransformMixin_v1):
    """Versioned API model for Meraki organization alert profile (v1)."""

    _field_mapping = {
        'alert_config_id': 'id',
        'type': 'type',
        'enabled': 'enabled',
        'alert_condition': 'alertCondition',
        'recipients': 'recipients',
        'network_tags': 'networkTags',
        'description': 'description',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.org_alert_profile import UserOrgAlertProfile
        return UserOrgAlertProfile
