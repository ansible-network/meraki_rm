"""Versioned API model and transform mixin for Meraki firmware upgrade (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.firmware_upgrade import FirmwareUpgrade as GeneratedFirmwareUpgrade

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
}

# Mutable fields for update (singleton)
_UPDATE_FIELDS = [
    'upgradeWindow', 'timezone', 'products',
]


class FirmwareUpgradeTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki firmware upgrade (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'find': EndpointOperation(
                path='/networks/{networkId}/firmwareUpgrades',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/firmwareUpgrades',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
        }


@dataclass
class APIFirmwareUpgrade_v1(GeneratedFirmwareUpgrade, FirmwareUpgradeTransformMixin_v1):
    """Versioned API model for Meraki firmware upgrade (v1)."""

    _field_mapping = {
        'upgrade_window': 'upgradeWindow',
        'timezone': 'timezone',
        'products': 'products',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.firmware_upgrade import UserFirmwareUpgrade
        return UserFirmwareUpgrade
