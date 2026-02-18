"""User model for Meraki camera wireless profile."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserCameraWirelessProfile(BaseTransformMixin):
    """User-facing camera wireless profile model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    wireless_profile_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    identity: Optional[Dict[str, Any]] = None
    ssid: Optional[Dict[str, Any]] = None

    _field_mapping = {
        'wireless_profile_id': 'id',
        'name': 'name',
        'identity': 'identity',
        'ssid': 'ssid',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.camera_wireless_profile import APICameraWirelessProfile_v1
        return APICameraWirelessProfile_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
