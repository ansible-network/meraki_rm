"""User model for Meraki appliance warm spare."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserWarmSpare(BaseTransformMixin):
    """User-facing warm spare model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    enabled: Optional[bool] = None
    spare_serial: Optional[str] = None
    uplink_mode: Optional[str] = None
    virtual_ip1: Optional[str] = None
    virtual_ip2: Optional[str] = None
    wan1: Optional[Dict[str, Any]] = None
    wan2: Optional[Dict[str, Any]] = None
    primary_serial: Optional[str] = None

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
