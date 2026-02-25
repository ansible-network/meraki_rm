"""User model for Meraki organization configuration template."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserConfigTemplate(BaseTransformMixin):
    """User-facing configuration template model with snake_case fields."""

    MODULE_NAME = 'config_template'
    SCOPE_PARAM = 'organization_id'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'config_template_id'

    # scope
    organization_id: Optional[str] = None
    # identity
    config_template_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Name of the configuration template."})
    product_types: Optional[List[str]] = field(default=None, metadata={"description": "Product types (e.g. wireless, switch, appliance)."})
    time_zone: Optional[str] = field(default=None, metadata={"description": "Timezone of the configuration template."})
    copy_from_network_id: Optional[str] = field(default=None, metadata={"description": "Network or template ID to copy configuration from."})

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
