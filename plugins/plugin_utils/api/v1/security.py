"""Versioned API model and transform mixin for Meraki appliance security (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.security import Security as GeneratedSecurity

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
}

# Mutable fields for update (singleton - intrusion endpoint)
_UPDATE_FIELDS = [
    'mode', 'idsRulesets', 'protectedNetworks',
]


class SecurityTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki appliance security (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find': EndpointOperation(
                path='/networks/{networkId}/appliance/security/intrusion',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/appliance/security/intrusion',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APISecurity_v1(GeneratedSecurity, SecurityTransformMixin_v1):
    """Versioned API model for Meraki appliance security (v1)."""

    _field_mapping = {
        'mode': 'mode',
        'ids_rulesets': 'idsRulesets',
        'protected_networks': 'protectedNetworks',
        'allowed_files': 'allowedFiles',
        'allowed_urls': 'allowedUrls',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.security import UserSecurity
        return UserSecurity
