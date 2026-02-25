"""User model for Meraki appliance warm spare."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserWarmSpare(BaseTransformMixin):
    """User-facing warm spare model with snake_case fields."""

    MODULE_NAME = 'warm_spare'
    SUPPORTS_DELETE = False

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    enabled: Optional[bool] = field(default=None, metadata={"description": "Whether warm spare is enabled."})
    spare_serial: Optional[str] = field(default=None, metadata={"description": "Serial number of the warm spare appliance."})
    uplink_mode: Optional[str] = field(default=None, metadata={"description": "Uplink mode (virtual or public)."})
    virtual_ip1: Optional[str] = field(default=None, metadata={"description": "WAN 1 shared IP."})
    virtual_ip2: Optional[str] = field(default=None, metadata={"description": "WAN 2 shared IP."})
    wan1: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "WAN 1 IP and subnet."})
    wan2: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "WAN 2 IP and subnet."})
    primary_serial: Optional[str] = field(default=None, metadata={"description": "Serial number of the primary appliance."})

    _field_mapping = {
        'enabled': 'enabled',
        'spare_serial': 'spareSerial',
        'uplink_mode': 'uplinkMode',
        'virtual_ip1': 'virtualIp1',
        'virtual_ip2': 'virtualIp2',
        'wan1': 'wan1',
        'wan2': 'wan2',
        'primary_serial': 'primarySerial',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.warm_spare import APIWarmSpare_v1
        return APIWarmSpare_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
