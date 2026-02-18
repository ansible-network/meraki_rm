"""Colocated tests for APIOrgVpn_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import org_vpn as org_vpn_api
from ...user_models import org_vpn as org_vpn_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = org_vpn_api.APIOrgVpn_v1(
            peers=[{'key': 'value'}],
            thirdPartyVpnPeers=[{'key': 'value'}],
        )
        user = api.to_ansible(_ctx())

        assert user.peers == api.peers
        assert user.third_party_vpn_peers == api.thirdPartyVpnPeers


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = org_vpn_user.UserOrgVpn(
            peers=[{'key': 'value'}],
            third_party_vpn_peers=[{'key': 'value'}],
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.peers == original.peers
        assert roundtripped.third_party_vpn_peers == original.third_party_vpn_peers


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = org_vpn_api.APIOrgVpn_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = org_vpn_api.APIOrgVpn_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

