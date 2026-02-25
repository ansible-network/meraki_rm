"""User model for Meraki wireless RF profile."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserWirelessRfProfile(BaseTransformMixin):
    """User-facing wireless RF profile model with snake_case fields."""

    MODULE_NAME = 'wireless_rf_profile'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'rf_profile_id'

    # scope
    network_id: Optional[str] = None
    # identity
    rf_profile_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Name of the RF profile. Must be unique."})
    band_selection_type: Optional[str] = field(default=None, metadata={"description": "Band selection (ssid or ap)."})
    client_balancing_enabled: Optional[bool] = field(default=None, metadata={"description": "Steer clients to best available AP."})
    two_four_ghz_settings: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "2.4 GHz band settings."})
    five_ghz_settings: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "5 GHz band settings."})
    six_ghz_settings: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "6 GHz band settings."})
    transmission: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Radio transmission settings."})
    is_indoor_default: Optional[bool] = field(default=None, metadata={"description": "Set as default indoor profile."})
    is_outdoor_default: Optional[bool] = field(default=None, metadata={"description": "Set as default outdoor profile."})
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
