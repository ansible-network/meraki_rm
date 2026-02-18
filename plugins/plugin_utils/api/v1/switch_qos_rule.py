"""Versioned API model and transform mixin for Meraki switch QoS rule (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.switch_qos_rule import SwitchQosRule as GeneratedSwitchQosRule

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'qosRuleId': ['qos_rule_id', 'id'],
}

_CREATE_FIELDS = [
    'dscp', 'vlan', 'protocol', 'srcPort', 'dstPort',
    'srcPortRange', 'dstPortRange',
]

_UPDATE_FIELDS = [
    'dscp', 'vlan', 'protocol', 'srcPort', 'dstPort',
    'srcPortRange', 'dstPortRange',
]


class SwitchQosRuleTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki switch QoS rule (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/switch/qosRules',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/switch/qosRules/{qosRuleId}',
                method='GET',
                fields=[],
                path_params=['networkId', 'qosRuleId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=2,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/switch/qosRules',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/switch/qosRules/{qosRuleId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'qosRuleId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/switch/qosRules/{qosRuleId}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'qosRuleId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APISwitchQosRule_v1(GeneratedSwitchQosRule, SwitchQosRuleTransformMixin_v1):
    """Versioned API model for Meraki switch QoS rule (v1)."""

    _field_mapping = {
        'qos_rule_id': 'id',
        'dscp': 'dscp',
        'vlan': 'vlan',
        'protocol': 'protocol',
        'src_port': 'srcPort',
        'dst_port': 'dstPort',
        'src_port_range': 'srcPortRange',
        'dst_port_range': 'dstPortRange',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.switch_qos_rule import UserSwitchQosRule
        return UserSwitchQosRule
