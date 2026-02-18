"""User model for Meraki organization SAML settings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSaml(BaseTransformMixin):
    """User-facing SAML settings model with snake_case fields."""

    # scope
    organization_id: Optional[str] = None
    # fields (singleton - no primary key)
    enabled: Optional[bool] = None
    consumer_url: Optional[str] = None
    slo_logout_url: Optional[str] = None
    sso_login_url: Optional[str] = None
    x509cert_sha1_fingerprint: Optional[str] = None
    vision_consumer_url: Optional[str] = None
    sp_initiated: Optional[Dict[str, Any]] = None

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
        from ..api.v1.saml import APISaml_v1
        return APISaml_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
