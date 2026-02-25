"""User model for Meraki camera wireless profile."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserCameraWirelessProfile(BaseTransformMixin):
    """User-facing camera wireless profile model with snake_case fields."""

    MODULE_NAME = 'camera_wireless_profile'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'wireless_profile_id'

    # scope
    network_id: Optional[str] = None
    # identity
    wireless_profile_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Name of the camera wireless profile."})
    identity: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Identity of the wireless profile (required for create)."})
    ssid: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "SSID configuration details."})

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
