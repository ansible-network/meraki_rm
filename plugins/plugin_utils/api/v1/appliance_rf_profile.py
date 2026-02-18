"""Versioned API model and transform mixin for Meraki appliance RF profile (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.appliance_rf_profile import ApplianceRfProfile as GeneratedApplianceRfProfile

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'rfProfileId': ['rf_profile_id', 'id'],
}

# All mutable fields for create (name required)
_CREATE_FIELDS = [
    'name', 'twoFourGhzSettings', 'fiveGhzSettings', 'perSsidSettings',
]

# All mutable fields for update (no id in body)
_UPDATE_FIELDS = [
    'name', 'twoFourGhzSettings', 'fiveGhzSettings', 'perSsidSettings',
]


class ApplianceRfProfileTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki appliance RF profile (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/appliance/rfProfiles',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/appliance/rfProfiles/{rfProfileId}',
                method='GET',
                fields=[],
                path_params=['networkId', 'rfProfileId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/appliance/rfProfiles',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/appliance/rfProfiles/{rfProfileId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'rfProfileId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/appliance/rfProfiles/{rfProfileId}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'rfProfileId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIApplianceRfProfile_v1(GeneratedApplianceRfProfile, ApplianceRfProfileTransformMixin_v1):
    """Versioned API model for Meraki appliance RF profile (v1)."""

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
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.appliance_rf_profile import UserApplianceRfProfile
        return UserApplianceRfProfile
