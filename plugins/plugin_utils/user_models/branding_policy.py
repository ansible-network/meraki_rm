"""User model for Meraki organization branding policy."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserBrandingPolicy(BaseTransformMixin):
    """User-facing branding policy model with snake_case fields."""

    # scope
    organization_id: Optional[str] = None
    # identity
    branding_policy_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    enabled: Optional[bool] = None
    admin_settings: Optional[Dict[str, Any]] = None
    help_settings: Optional[Dict[str, Any]] = None
    custom_logo: Optional[Dict[str, Any]] = None

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
