"""Versioned API model and transform mixin for Meraki organization SAML (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.saml import Saml as GeneratedSaml

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'organizationId': ['organization_id'],
}

# Mutable fields for update (singleton - GET/PUT only)
_UPDATE_FIELDS = [
    'enabled', 'consumerUrl', 'sloLogoutUrl', 'ssoLoginUrl',
    'x509certSha1Fingerprint', 'visionConsumerUrl', 'spInitiated',
]


class SamlTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki organization SAML settings (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find': EndpointOperation(
                path='/organizations/{organizationId}/saml',
                method='GET',
                fields=[],
                path_params=['organizationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/organizations/{organizationId}/saml',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['organizationId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APISaml_v1(GeneratedSaml, SamlTransformMixin_v1):
    """Versioned API model for Meraki organization SAML (v1)."""

    _field_mapping = {
        'enabled': 'enabled',
        'consumer_url': 'consumerUrl',
        'slo_logout_url': 'sloLogoutUrl',
        'sso_login_url': 'ssoLoginUrl',
        'x509cert_sha1_fingerprint': 'x509certSha1Fingerprint',
        'vision_consumer_url': 'visionConsumerUrl',
        'sp_initiated': 'spInitiated',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.saml import UserSaml
        return UserSaml
