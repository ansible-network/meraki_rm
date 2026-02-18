"""Versioned API model and transform mixin for Meraki network settings (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.network_settings import NetworkSettings as GeneratedNetworkSettings

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
}

# Mutable fields for update (singleton - main settings endpoint)
_UPDATE_FIELDS = [
    'localStatusPageEnabled', 'remoteStatusPageEnabled', 'localStatusPage',
    'fips', 'namedVlans', 'securePort', 'reportingEnabled', 'mode',
    'customPieChartItems',
]


class NetworkSettingsTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki network settings (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find': EndpointOperation(
                path='/networks/{networkId}/settings',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/settings',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APINetworkSettings_v1(GeneratedNetworkSettings, NetworkSettingsTransformMixin_v1):
    """Versioned API model for Meraki network settings (v1)."""

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
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.network_settings import UserNetworkSettings
        return UserNetworkSettings
