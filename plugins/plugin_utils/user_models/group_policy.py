"""User model for Meraki group policy."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserGroupPolicy(BaseTransformMixin):
    """User-facing group policy model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    group_policy_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    bandwidth: Optional[Dict[str, Any]] = None
    bonjour_forwarding: Optional[Dict[str, Any]] = None
    content_filtering: Optional[Dict[str, Any]] = None
    firewall_and_traffic_shaping: Optional[Dict[str, Any]] = None
    scheduling: Optional[Dict[str, Any]] = None
    splash_auth_settings: Optional[str] = None
    vlan_tagging: Optional[Dict[str, Any]] = None

    _field_mapping = {
        'group_policy_id': 'groupPolicyId',
        'name': 'name',
        'bandwidth': 'bandwidth',
        'bonjour_forwarding': 'bonjourForwarding',
        'content_filtering': 'contentFiltering',
        'firewall_and_traffic_shaping': 'firewallAndTrafficShaping',
        'scheduling': 'scheduling',
        'splash_auth_settings': 'splashAuthSettings',
        'vlan_tagging': 'vlanTagging',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.group_policy import APIGroupPolicy_v1
        return APIGroupPolicy_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
