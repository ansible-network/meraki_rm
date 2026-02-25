"""User model for Meraki appliance security."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSecurity(BaseTransformMixin):
    """User-facing security model with snake_case fields."""

    MODULE_NAME = 'security'
    SUPPORTS_DELETE = False

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    mode: Optional[str] = field(default=None, metadata={"description": "Intrusion detection mode."})
    ids_rulesets: Optional[str] = field(default=None, metadata={"description": "Intrusion detection ruleset."})
    protected_networks: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Networks included/excluded from detection."})
    allowed_files: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "Sha256 digests of files permitted by malware engine."})
    allowed_urls: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "URLs permitted by malware detection engine."})

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
