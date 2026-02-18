"""User model for Meraki wireless SSID."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSsid(BaseTransformMixin):
    """User-facing SSID model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    number: Optional[int] = None
    # fields
    name: Optional[str] = None
    enabled: Optional[bool] = None
    auth_mode: Optional[str] = None
    encryption_mode: Optional[str] = None
    psk: Optional[str] = None
    wpa_encryption_mode: Optional[str] = None
    ip_assignment_mode: Optional[str] = None
    use_vlan_tagging: Optional[bool] = None
    default_vlan_id: Optional[int] = None
    vlan_id: Optional[int] = None
    splash_page: Optional[str] = None
    band_selection: Optional[str] = None
    min_bitrate: Optional[float] = None
    per_client_bandwidth_limit_up: Optional[int] = None
    per_client_bandwidth_limit_down: Optional[int] = None
    per_ssid_bandwidth_limit_up: Optional[int] = None
    per_ssid_bandwidth_limit_down: Optional[int] = None
    visible: Optional[bool] = None
    available_on_all_aps: Optional[bool] = None
    availability_tags: Optional[List[str]] = None

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
        from ..api.v1.ssid import APISsid_v1
        return APISsid_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
