"""User model for Meraki appliance RF profile."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserApplianceRfProfile(BaseTransformMixin):
    """User-facing appliance RF profile model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    rf_profile_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    two_four_ghz_settings: Optional[Dict[str, Any]] = None
    five_ghz_settings: Optional[Dict[str, Any]] = None
    per_ssid_settings: Optional[Dict[str, Any]] = None
    assigned: Optional[List[Dict[str, Any]]] = None

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
