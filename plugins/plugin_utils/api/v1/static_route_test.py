"""Colocated tests for APIStaticRoute_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import static_route as static_route_api
from ...user_models import static_route as static_route_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = static_route_api.APIStaticRoute_v1(
            id='id_val',
            name='name_val',
            subnet='subnet_val',
            gatewayIp='gatewayIp_val',
            gatewayVlanId=24,
            enabled=True,
            fixedIpAssignments={'k1': {'ip': '10.0.0.1', 'name': 'host'}},
            reservedIpRanges=[{'key': 'value'}],
            ipVersion=24,
        )
        user = api.to_ansible(_ctx())

        assert user.static_route_id == api.id
        assert user.name == api.name
        assert user.subnet == api.subnet
        assert user.gateway_ip == api.gatewayIp
        assert user.gateway_vlan_id == api.gatewayVlanId
        assert user.enabled == api.enabled
        assert user.fixed_ip_assignments == api.fixedIpAssignments
        assert user.reserved_ip_ranges == api.reservedIpRanges
        assert user.ip_version == api.ipVersion


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = static_route_user.UserStaticRoute(
            static_route_id='static_route_id_val',
            name='name_val',
            subnet='subnet_val',
            gateway_ip='gateway_ip_val',
            gateway_vlan_id=24,
            enabled=True,
            fixed_ip_assignments={'enabled': True},
            reserved_ip_ranges=[{'key': 'value'}],
            ip_version=24,
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.static_route_id == original.static_route_id
        assert roundtripped.name == original.name
        assert roundtripped.subnet == original.subnet
        assert roundtripped.gateway_ip == original.gateway_ip
        assert roundtripped.gateway_vlan_id == original.gateway_vlan_id
        assert roundtripped.enabled == original.enabled
        assert roundtripped.fixed_ip_assignments == original.fixed_ip_assignments
        assert roundtripped.reserved_ip_ranges == original.reserved_ip_ranges
        assert roundtripped.ip_version == original.ip_version


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = static_route_api.APIStaticRoute_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = static_route_api.APIStaticRoute_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

