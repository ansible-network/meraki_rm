"""User model for Meraki wireless RF profile."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserWirelessRfProfile(BaseTransformMixin):
    """User-facing wireless RF profile model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    rf_profile_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    band_selection_type: Optional[str] = None
    client_balancing_enabled: Optional[bool] = None
    two_four_ghz_settings: Optional[Dict[str, Any]] = None
    five_ghz_settings: Optional[Dict[str, Any]] = None
    six_ghz_settings: Optional[Dict[str, Any]] = None
    transmission: Optional[Dict[str, Any]] = None
    is_indoor_default: Optional[bool] = None
    is_outdoor_default: Optional[bool] = None
    ap_band_settings: Optional[Dict[str, Any]] = None
    per_ssid_settings: Optional[Dict[str, Any]] = None
    min_bitrate_type: Optional[str] = None

    _field_mapping = {
        'rf_profile_id': 'id',
        'name': 'name',
        'band_selection_type': 'bandSelectionType',
        'client_balancing_enabled': 'clientBalancingEnabled',
        'two_four_ghz_settings': 'twoFourGhzSettings',
        'five_ghz_settings': 'fiveGhzSettings',
        'six_ghz_settings': 'sixGhzSettings',
        'transmission': 'transmission',
        'is_indoor_default': 'isIndoorDefault',
        'is_outdoor_default': 'isOutdoorDefault',
        'ap_band_settings': 'apBandSettings',
        'per_ssid_settings': 'perSsidSettings',
        'min_bitrate_type': 'minBitrateType',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.wireless_rf_profile import APIWirelessRfProfile_v1
        return APIWirelessRfProfile_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
