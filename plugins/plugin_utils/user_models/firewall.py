"""User model for Meraki appliance firewall."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserFirewall(BaseTransformMixin):
    """User-facing firewall model with snake_case fields."""

    MODULE_NAME = 'firewall'
    SUPPORTS_DELETE = False

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    rules: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "Ordered array of L3 firewall rules."})
    syslog_default_rule: Optional[bool] = field(default=None, metadata={"description": "Log the special default rule."})
    spoofing_protection: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Spoofing protection settings."})
    application_categories: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "L7 application categories and applications."})
    access: Optional[str] = field(default=None, metadata={"description": "Rule for which IPs are allowed to access."})
    allowed_ips: Optional[List[str]] = field(default=None, metadata={"description": "Array of allowed CIDRs."})
    service: Optional[str] = field(default=None, metadata={"description": "Appliance service name."})

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
