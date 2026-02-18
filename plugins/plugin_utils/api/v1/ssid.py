"""Versioned API model and transform mixin for Meraki wireless SSID (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.ssid import Ssid as GeneratedSsid

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'number': ['number'],
}

# Mutable fields for update (no create/delete - SSIDs 0-14 always exist)
_UPDATE_FIELDS = [
    'name', 'enabled', 'authMode', 'encryptionMode', 'psk',
    'wpaEncryptionMode', 'ipAssignmentMode', 'useVlanTagging',
    'defaultVlanId', 'vlanId', 'splashPage', 'bandSelection',
    'minBitrate', 'perClientBandwidthLimitUp', 'perClientBandwidthLimitDown',
    'perSsidBandwidthLimitUp', 'perSsidBandwidthLimitDown',
    'visible', 'availableOnAllAps', 'availabilityTags',
]


class SsidTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki wireless SSID (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find_all': EndpointOperation(
                path='/networks/{networkId}/wireless/ssids',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/wireless/ssids/{number}',
                method='GET',
                fields=[],
                path_params=['networkId', 'number'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=2,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/wireless/ssids/{number}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'number'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APISsid_v1(GeneratedSsid, SsidTransformMixin_v1):
    """Versioned API model for Meraki wireless SSID (v1)."""

    _field_mapping = {
        'number': 'number',
        'name': 'name',
        'enabled': 'enabled',
        'auth_mode': 'authMode',
        'encryption_mode': 'encryptionMode',
        'psk': 'psk',
        'wpa_encryption_mode': 'wpaEncryptionMode',
        'ip_assignment_mode': 'ipAssignmentMode',
        'use_vlan_tagging': 'useVlanTagging',
        'default_vlan_id': 'defaultVlanId',
        'vlan_id': 'vlanId',
        'splash_page': 'splashPage',
        'band_selection': 'bandSelection',
        'min_bitrate': 'minBitrate',
        'per_client_bandwidth_limit_up': 'perClientBandwidthLimitUp',
        'per_client_bandwidth_limit_down': 'perClientBandwidthLimitDown',
        'per_ssid_bandwidth_limit_up': 'perSsidBandwidthLimitUp',
        'per_ssid_bandwidth_limit_down': 'perSsidBandwidthLimitDown',
        'visible': 'visible',
        'available_on_all_aps': 'availableOnAllAps',
        'availability_tags': 'availabilityTags',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.ssid import UserSsid
        return UserSsid
