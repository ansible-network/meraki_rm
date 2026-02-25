"""User model for Meraki network settings."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserNetworkSettings(BaseTransformMixin):
    """User-facing network settings model with snake_case fields."""

    MODULE_NAME = 'network_settings'
    SUPPORTS_DELETE = False

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    local_status_page_enabled: Optional[bool] = field(default=None, metadata={"description": "Enable local device status pages."})
    remote_status_page_enabled: Optional[bool] = field(default=None, metadata={"description": "Enable access to device status page via LAN IP."})
    local_status_page: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Local status page authentication options."})
    fips: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "FIPS options for the network."})
    named_vlans: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Named VLANs options."})
    secure_port: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "SecureConnect options."})
    reporting_enabled: Optional[bool] = field(default=None, metadata={"description": "Enable NetFlow traffic reporting."})
    mode: Optional[str] = field(default=None, metadata={"description": "Traffic analysis mode."})
    custom_pie_chart_items: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "Custom pie chart items for traffic reporting."})

    _field_mapping = {
        'local_status_page_enabled': 'localStatusPageEnabled',
        'remote_status_page_enabled': 'remoteStatusPageEnabled',
        'local_status_page': 'localStatusPage',
        'fips': 'fips',
        'named_vlans': 'namedVlans',
        'secure_port': 'securePort',
        'reporting_enabled': 'reportingEnabled',
        'mode': 'mode',
        'custom_pie_chart_items': 'customPieChartItems',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.network_settings import APINetworkSettings_v1
        return APINetworkSettings_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
