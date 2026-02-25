"""User model for Meraki appliance port."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserPort(BaseTransformMixin):
    """User-facing port model with snake_case fields."""

    MODULE_NAME = 'port'
    SUPPORTS_DELETE = False

    # scope
    network_id: Optional[str] = None
    # identity
    port_id: Optional[str] = field(default=None, metadata={"description": "Port ID (e.g., 1, 2, 3, 4). Required for merged, replaced."})
    # fields
    enabled: Optional[bool] = field(default=None, metadata={"description": "Whether the port is enabled."})
    type: Optional[str] = field(default=None, metadata={"description": "Port type (access or trunk)."})
    vlan: Optional[int] = field(default=None, metadata={"description": "Native VLAN (trunk) or access VLAN."})
    allowed_vlans: Optional[str] = field(default=None, metadata={"description": "Allowed VLANs (comma-delimited or 'all')."})
    access_policy: Optional[str] = field(default=None, metadata={"description": "Access policy name (access ports only)."})
    drop_untagged_traffic: Optional[bool] = field(default=None, metadata={"description": "Drop untagged traffic (trunk ports)."})

    _field_mapping = {
        'port_id': 'number',
        'enabled': 'enabled',
        'type': 'type',
        'vlan': 'vlan',
        'allowed_vlans': 'allowedVlans',
        'access_policy': 'accessPolicy',
        'drop_untagged_traffic': 'dropUntaggedTraffic',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.port import APIPort_v1
        return APIPort_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
