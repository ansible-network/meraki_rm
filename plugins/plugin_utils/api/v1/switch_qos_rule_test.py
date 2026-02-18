"""Colocated tests for APISwitchQosRule_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import switch_qos_rule as switch_qos_rule_api
from ...user_models import switch_qos_rule as switch_qos_rule_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = switch_qos_rule_api.APISwitchQosRule_v1(
            id='id_val',
            dscp=24,
            vlan=24,
            protocol='protocol_val',
            srcPort=24,
            dstPort=24,
            srcPortRange='srcPortRange_val',
            dstPortRange='dstPortRange_val',
        )
        user = api.to_ansible(_ctx())

        assert user.qos_rule_id == api.id
        assert user.dscp == api.dscp
        assert user.vlan == api.vlan
        assert user.protocol == api.protocol
        assert user.src_port == api.srcPort
        assert user.dst_port == api.dstPort
        assert user.src_port_range == api.srcPortRange
        assert user.dst_port_range == api.dstPortRange


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = switch_qos_rule_user.UserSwitchQosRule(
            qos_rule_id='qos_rule_id_val',
            dscp=24,
            vlan=24,
            protocol='protocol_val',
            src_port=24,
            dst_port=24,
            src_port_range='src_port_range_val',
            dst_port_range='dst_port_range_val',
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.qos_rule_id == original.qos_rule_id
        assert roundtripped.dscp == original.dscp
        assert roundtripped.vlan == original.vlan
        assert roundtripped.protocol == original.protocol
        assert roundtripped.src_port == original.src_port
        assert roundtripped.dst_port == original.dst_port
        assert roundtripped.src_port_range == original.src_port_range
        assert roundtripped.dst_port_range == original.dst_port_range


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = switch_qos_rule_api.APISwitchQosRule_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = switch_qos_rule_api.APISwitchQosRule_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

