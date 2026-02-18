"""User model for Meraki network settings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserNetworkSettings(BaseTransformMixin):
    """User-facing network settings model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    local_status_page_enabled: Optional[bool] = None
    remote_status_page_enabled: Optional[bool] = None
    local_status_page: Optional[Dict[str, Any]] = None
    fips: Optional[Dict[str, Any]] = None
    named_vlans: Optional[Dict[str, Any]] = None
    secure_port: Optional[Dict[str, Any]] = None
    reporting_enabled: Optional[bool] = None
    mode: Optional[str] = None
    custom_pie_chart_items: Optional[List[Dict[str, Any]]] = None

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
