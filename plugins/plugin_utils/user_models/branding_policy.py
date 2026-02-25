"""User model for Meraki organization branding policy."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserBrandingPolicy(BaseTransformMixin):
    """User-facing branding policy model with snake_case fields."""

    MODULE_NAME = 'branding_policy'
    SCOPE_PARAM = 'organization_id'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'branding_policy_id'

    # scope
    organization_id: Optional[str] = None
    # identity
    branding_policy_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Name of the branding policy."})
    enabled: Optional[bool] = field(default=None, metadata={"description": "Whether the policy is enabled."})
    admin_settings: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Settings for which kinds of admins this policy applies to."})
    help_settings: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Modifications to Help page features."})
    custom_logo: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Custom logo properties."})

    _field_mapping = {
        'branding_policy_id': 'id',
        'name': 'name',
        'enabled': 'enabled',
        'admin_settings': 'adminSettings',
        'help_settings': 'helpSettings',
        'custom_logo': 'customLogo',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.branding_policy import APIBrandingPolicy_v1
        return APIBrandingPolicy_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
