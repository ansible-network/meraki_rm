"""User model for Meraki organization alert profile."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserOrgAlertProfile(BaseTransformMixin):
    """User-facing alert profile model with snake_case fields."""

    MODULE_NAME = 'org_alert_profile'
    SCOPE_PARAM = 'organization_id'
    SYSTEM_KEY = 'alert_config_id'

    # scope
    organization_id: Optional[str] = None
    # identity
    alert_config_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned config ID. Discover via C(state=gathered)."})
    # fields
    type: Optional[str] = field(default=None, metadata={"description": "The alert type."})
    enabled: Optional[bool] = field(default=None, metadata={"description": "Whether the alert is enabled."})
    alert_condition: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Conditions that determine if the alert triggers."})
    recipients: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Recipients that receive the alert."})
    network_tags: Optional[List[str]] = field(default=None, metadata={"description": "Network tags to monitor for the alert."})
    description: Optional[str] = field(default=None, metadata={"description": "User-supplied description of the alert."})

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
