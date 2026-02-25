"""User model for Meraki organization SAML settings."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSaml(BaseTransformMixin):
    """User-facing SAML settings model with snake_case fields."""

    MODULE_NAME = 'saml'
    SCOPE_PARAM = 'organization_id'
    SUPPORTS_DELETE = False

    # scope
    organization_id: Optional[str] = None
    # fields (singleton - no primary key)
    enabled: Optional[bool] = field(default=None, metadata={"description": "Whether SAML SSO is enabled."})
    consumer_url: Optional[str] = field(default=None, metadata={"description": "URL consuming SAML Identity Provider (IdP)."})
    slo_logout_url: Optional[str] = field(default=None, metadata={"description": "URL for redirect on sign out."})
    sso_login_url: Optional[str] = field(default=None, metadata={"description": "URL for redirect to log in again when session expires."})
    x509cert_sha1_fingerprint: Optional[str] = field(default=None, metadata={"description": "SHA1 fingerprint of the SAML certificate from IdP."})
    vision_consumer_url: Optional[str] = field(default=None, metadata={"description": "URL consuming SAML IdP for Meraki Vision Portal."})
    sp_initiated: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "SP-Initiated SSO settings."})

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
