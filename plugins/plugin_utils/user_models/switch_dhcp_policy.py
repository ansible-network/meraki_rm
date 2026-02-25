"""User model for Meraki switch DHCP policy."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchDhcpPolicy(BaseTransformMixin):
    """User-facing switch DHCP policy model with snake_case fields."""

    MODULE_NAME = 'switch_dhcp_policy'
    SUPPORTS_DELETE = False

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    default_policy: Optional[str] = field(default=None, metadata={"description": "Default policy for new DHCP servers (allow or block)."})
    allowed_servers: Optional[List[str]] = field(default=None, metadata={"description": "MAC addresses of DHCP servers to permit."})
    blocked_servers: Optional[List[str]] = field(default=None, metadata={"description": "MAC addresses of DHCP servers to block."})
    always_allowed_servers: Optional[List[str]] = field(default=None, metadata={"description": "MAC addresses always allowed on the network."})
    arp_inspection: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Dynamic ARP Inspection settings."})
    alerts: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Email alert settings for DHCP servers."})

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
