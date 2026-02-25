"""User model for Meraki group policy."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserGroupPolicy(BaseTransformMixin):
    """User-facing group policy model with snake_case fields."""

    MODULE_NAME = 'group_policy'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'group_policy_id'

    # scope
    network_id: Optional[str] = None
    # identity
    group_policy_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Name of the group policy. Required for create."})
    bandwidth: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Bandwidth settings for clients."})
    bonjour_forwarding: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Bonjour forwarding settings."})
    content_filtering: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Content filtering settings."})
    firewall_and_traffic_shaping: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Firewall and traffic shaping rules."})
    scheduling: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Schedule for the group policy."})
    splash_auth_settings: Optional[str] = field(default=None, metadata={"description": "Splash authorization bypass setting."})
    vlan_tagging: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "VLAN tagging settings."})

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
