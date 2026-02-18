"""Colocated tests for APISwitchDhcpPolicy_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import switch_dhcp_policy as switch_dhcp_policy_api
from ...user_models import switch_dhcp_policy as switch_dhcp_policy_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = switch_dhcp_policy_api.APISwitchDhcpPolicy_v1(
            defaultPolicy='defaultPolicy_val',
            allowedServers=['item1', 'item2'],
            blockedServers=['item1', 'item2'],
            alwaysAllowedServers=['item1', 'item2'],
            arpInspection={'enabled': True},
            alerts={'enabled': True},
        )
        user = api.to_ansible(_ctx())

        assert user.default_policy == api.defaultPolicy
        assert user.allowed_servers == api.allowedServers
        assert user.blocked_servers == api.blockedServers
        assert user.always_allowed_servers == api.alwaysAllowedServers
        assert user.arp_inspection == api.arpInspection
        assert user.alerts == api.alerts


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = switch_dhcp_policy_user.UserSwitchDhcpPolicy(
            default_policy='default_policy_val',
            allowed_servers=['item1', 'item2'],
            blocked_servers=['item1', 'item2'],
            always_allowed_servers=['item1', 'item2'],
            arp_inspection={'enabled': True},
            alerts={'enabled': True},
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.default_policy == original.default_policy
        assert roundtripped.allowed_servers == original.allowed_servers
        assert roundtripped.blocked_servers == original.blocked_servers
        assert roundtripped.always_allowed_servers == original.always_allowed_servers
        assert roundtripped.arp_inspection == original.arp_inspection
        assert roundtripped.alerts == original.alerts


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = switch_dhcp_policy_api.APISwitchDhcpPolicy_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = switch_dhcp_policy_api.APISwitchDhcpPolicy_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

