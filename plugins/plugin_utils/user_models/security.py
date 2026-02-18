"""User model for Meraki appliance security."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSecurity(BaseTransformMixin):
    """User-facing security model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    mode: Optional[str] = None
    ids_rulesets: Optional[str] = None
    protected_networks: Optional[Dict[str, Any]] = None
    allowed_files: Optional[List[Dict[str, Any]]] = None
    allowed_urls: Optional[List[Dict[str, Any]]] = None

    _field_mapping = {
        'mode': 'mode',
        'ids_rulesets': 'idsRulesets',
        'protected_networks': 'protectedNetworks',
        'allowed_files': 'allowedFiles',
        'allowed_urls': 'allowedUrls',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.security import APISecurity_v1
        return APISecurity_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
