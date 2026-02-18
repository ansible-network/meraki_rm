"""Colocated tests for APISwitchLinkAggregation_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import switch_link_aggregation as switch_link_aggregation_api
from ...user_models import switch_link_aggregation as switch_link_aggregation_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = switch_link_aggregation_api.APISwitchLinkAggregation_v1(
            id='id_val',
            switchPorts=[{'key': 'value'}],
            switchProfilePorts=[{'key': 'value'}],
        )
        user = api.to_ansible(_ctx())

        assert user.link_aggregation_id == api.id
        assert user.switch_ports == api.switchPorts
        assert user.switch_profile_ports == api.switchProfilePorts


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = switch_link_aggregation_user.UserSwitchLinkAggregation(
            link_aggregation_id='link_aggregation_id_val',
            switch_ports=[{'key': 'value'}],
            switch_profile_ports=[{'key': 'value'}],
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.link_aggregation_id == original.link_aggregation_id
        assert roundtripped.switch_ports == original.switch_ports
        assert roundtripped.switch_profile_ports == original.switch_profile_ports


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = switch_link_aggregation_api.APISwitchLinkAggregation_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = switch_link_aggregation_api.APISwitchLinkAggregation_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

