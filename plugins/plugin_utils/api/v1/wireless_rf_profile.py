"""Versioned API model and transform mixin for Meraki wireless RF profile (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.wireless_rf_profile import WirelessRfProfile as GeneratedWirelessRfProfile

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'rfProfileId': ['rf_profile_id', 'id'],
}

_CREATE_FIELDS = [
    'name', 'bandSelectionType', 'clientBalancingEnabled',
    'twoFourGhzSettings', 'fiveGhzSettings', 'sixGhzSettings',
    'transmission', 'apBandSettings', 'perSsidSettings',
    'minBitrateType', 'flexRadios',
]

_UPDATE_FIELDS = [
    'name', 'bandSelectionType', 'clientBalancingEnabled',
    'twoFourGhzSettings', 'fiveGhzSettings', 'sixGhzSettings',
    'transmission', 'apBandSettings', 'perSsidSettings',
    'minBitrateType', 'flexRadios', 'isIndoorDefault', 'isOutdoorDefault',
]


class WirelessRfProfileTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki wireless RF profile (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/wireless/rfProfiles',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/wireless/rfProfiles/{rfProfileId}',
                method='GET',
                fields=[],
                path_params=['networkId', 'rfProfileId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=2,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/wireless/rfProfiles',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/wireless/rfProfiles/{rfProfileId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'rfProfileId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/wireless/rfProfiles/{rfProfileId}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'rfProfileId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIWirelessRfProfile_v1(GeneratedWirelessRfProfile, WirelessRfProfileTransformMixin_v1):
    """Versioned API model for Meraki wireless RF profile (v1)."""

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
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.wireless_rf_profile import UserWirelessRfProfile
        return UserWirelessRfProfile
