"""User model for Meraki wireless SSID."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSsid(BaseTransformMixin):
    """User-facing SSID model with snake_case fields."""

    MODULE_NAME = 'ssid'
    SUPPORTS_DELETE = False

    # scope
    network_id: Optional[str] = None
    # identity
    number: Optional[int] = field(default=None, metadata={"description": "SSID number (0-14). Required for merged and replaced."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "SSID name."})
    enabled: Optional[bool] = field(default=None, metadata={"description": "Whether the SSID is enabled."})
    auth_mode: Optional[str] = field(default=None, metadata={"description": "Authentication mode."})
    encryption_mode: Optional[str] = field(default=None, metadata={"description": "Encryption mode for the SSID."})
    psk: Optional[str] = field(default=None, metadata={"description": "Pre-shared key (for PSK auth). Write-only; not returned by API."})
    wpa_encryption_mode: Optional[str] = field(default=None, metadata={"description": "WPA encryption mode."})
    ip_assignment_mode: Optional[str] = field(default=None, metadata={"description": "Client IP assignment mode."})
    use_vlan_tagging: Optional[bool] = field(default=None, metadata={"description": "Whether to use VLAN tagging."})
    default_vlan_id: Optional[int] = field(default=None, metadata={"description": "Default VLAN ID for all other APs."})
    vlan_id: Optional[int] = field(default=None, metadata={"description": "VLAN ID for VLAN tagging."})
    splash_page: Optional[str] = field(default=None, metadata={"description": "Splash page type."})
    band_selection: Optional[str] = field(default=None, metadata={"description": "Band selection for the SSID."})
    min_bitrate: Optional[float] = field(default=None, metadata={"description": "Minimum bitrate in Mbps."})
    per_client_bandwidth_limit_up: Optional[int] = field(default=None, metadata={"description": "Per-client upload bandwidth limit in Kbps (0 = no limit)."})
    per_client_bandwidth_limit_down: Optional[int] = field(default=None, metadata={"description": "Per-client download bandwidth limit in Kbps (0 = no limit)."})
    per_ssid_bandwidth_limit_up: Optional[int] = field(default=None, metadata={"description": "Per-SSID upload bandwidth limit in Kbps (0 = no limit)."})
    per_ssid_bandwidth_limit_down: Optional[int] = field(default=None, metadata={"description": "Per-SSID download bandwidth limit in Kbps (0 = no limit)."})
    visible: Optional[bool] = field(default=None, metadata={"description": "Whether the SSID is advertised (visible) or hidden."})
    available_on_all_aps: Optional[bool] = field(default=None, metadata={"description": "Whether the SSID is broadcast on all APs."})
    availability_tags: Optional[List[str]] = field(default=None, metadata={"description": "AP tags for SSID availability (when available_on_all_aps is false)."})

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
