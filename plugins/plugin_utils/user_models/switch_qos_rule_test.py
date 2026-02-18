"""Colocated tests for UserSwitchQosRule — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import switch_qos_rule


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserSwitchQosRule can be constructed with all fields."""

    def test_defaults(self):
        obj = switch_qos_rule.UserSwitchQosRule()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserSwitchQosRule -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = switch_qos_rule.UserSwitchQosRule(
            qos_rule_id='qos_rule_id_val',
            dscp=24,
            vlan=24,
            protocol='protocol_val',
            src_port=24,
            dst_port=24,
            src_port_range='src_port_range_val',
            dst_port_range='dst_port_range_val',
        )
        api = user.to_api(_ctx())

        assert api.id == user.qos_rule_id
        assert api.dscp == user.dscp
        assert api.vlan == user.vlan
        assert api.protocol == user.protocol
        assert api.srcPort == user.src_port
        assert api.dstPort == user.dst_port
        assert api.srcPortRange == user.src_port_range
        assert api.dstPortRange == user.dst_port_range

    def test_none_fields_omitted(self):
        user = switch_qos_rule.UserSwitchQosRule(qos_rule_id='qos_rule_id_val')
        api = user.to_api(_ctx())
        assert api.id == user.qos_rule_id
        assert getattr(api, 'dscp', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = switch_qos_rule.UserSwitchQosRule(network_id='network_id_val', qos_rule_id='qos_rule_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

