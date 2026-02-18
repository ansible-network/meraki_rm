"""User model for Meraki organization configuration template."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserConfigTemplate(BaseTransformMixin):
    """User-facing configuration template model with snake_case fields."""

    # scope
    organization_id: Optional[str] = None
    # identity
    config_template_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    product_types: Optional[List[str]] = None
    time_zone: Optional[str] = None
    copy_from_network_id: Optional[str] = None

    _field_mapping = {
        'config_template_id': 'id',
        'name': 'name',
        'product_types': 'productTypes',
        'time_zone': 'timeZone',
        'copy_from_network_id': 'copyFromNetworkId',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.config_template import APIConfigTemplate_v1
        return APIConfigTemplate_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
