"""User model for Meraki organization alert profile."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserOrgAlertProfile(BaseTransformMixin):
    """User-facing alert profile model with snake_case fields."""

    # scope
    organization_id: Optional[str] = None
    # identity
    alert_config_id: Optional[str] = None
    # fields
    type: Optional[str] = None
    enabled: Optional[bool] = None
    alert_condition: Optional[Dict[str, Any]] = None
    recipients: Optional[Dict[str, Any]] = None
    network_tags: Optional[List[str]] = None
    description: Optional[str] = None

    _field_mapping = {
        'alert_config_id': 'id',
        'type': 'type',
        'enabled': 'enabled',
        'alert_condition': 'alertCondition',
        'recipients': 'recipients',
        'network_tags': 'networkTags',
        'description': 'description',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.org_alert_profile import APIOrgAlertProfile_v1
        return APIOrgAlertProfile_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
