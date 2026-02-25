"""User model for Meraki appliance RF profile."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserApplianceRfProfile(BaseTransformMixin):
    """User-facing appliance RF profile model with snake_case fields."""

    MODULE_NAME = 'appliance_rf_profile'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'rf_profile_id'

    # scope
    network_id: Optional[str] = None
    # identity
    rf_profile_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Name of the profile. Required for create."})
    two_four_ghz_settings: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Settings for 2.4GHz band."})
    five_ghz_settings: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Settings for 5GHz band."})
    per_ssid_settings: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Per-SSID radio settings by number."})
    assigned: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "Assigned RF profiles."})

    _field_mapping = {
        'rf_profile_id': 'id',
        'name': 'name',
        'two_four_ghz_settings': 'twoFourGhzSettings',
        'five_ghz_settings': 'fiveGhzSettings',
        'per_ssid_settings': 'perSsidSettings',
        'assigned': 'assigned',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.appliance_rf_profile import APIApplianceRfProfile_v1
        return APIApplianceRfProfile_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
