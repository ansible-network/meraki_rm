"""User model for Meraki appliance firewall."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserFirewall(BaseTransformMixin):
    """User-facing firewall model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    rules: Optional[List[Dict[str, Any]]] = None
    syslog_default_rule: Optional[bool] = None
    spoofing_protection: Optional[Dict[str, Any]] = None
    application_categories: Optional[List[Dict[str, Any]]] = None
    access: Optional[str] = None
    allowed_ips: Optional[List[str]] = None
    service: Optional[str] = None

    _field_mapping = {
        'rules': 'rules',
        'syslog_default_rule': 'syslogDefaultRule',
        'spoofing_protection': 'spoofingProtection',
        'application_categories': 'applicationCategories',
        'access': 'access',
        'allowed_ips': 'allowedIps',
        'service': 'service',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.firewall import APIFirewall_v1
        return APIFirewall_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
