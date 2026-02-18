"""User model for Meraki switch DHCP policy."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchDhcpPolicy(BaseTransformMixin):
    """User-facing switch DHCP policy model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    default_policy: Optional[str] = None
    allowed_servers: Optional[List[str]] = None
    blocked_servers: Optional[List[str]] = None
    always_allowed_servers: Optional[List[str]] = None
    arp_inspection: Optional[Dict[str, Any]] = None
    alerts: Optional[Dict[str, Any]] = None

    _field_mapping = {
        'default_policy': 'defaultPolicy',
        'allowed_servers': 'allowedServers',
        'blocked_servers': 'blockedServers',
        'always_allowed_servers': 'alwaysAllowedServers',
        'arp_inspection': 'arpInspection',
        'alerts': 'alerts',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.switch_dhcp_policy import APISwitchDhcpPolicy_v1
        return APISwitchDhcpPolicy_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
