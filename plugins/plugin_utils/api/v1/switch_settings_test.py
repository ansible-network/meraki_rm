"""Colocated tests for APISwitchSettings_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import switch_settings as switch_settings_api
from ...user_models import switch_settings as switch_settings_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = switch_settings_api.APISwitchSettings_v1(
            defaultMtuSize=24,
            overrides=[{'key': 'value'}],
            broadcastThreshold=24,
            multicastThreshold=24,
            unknownUnicastThreshold=24,
            mappings=[{'key': 'value'}],
            useCombinedPower=True,
            powerExceptions=[{'key': 'value'}],
            enabled=True,
            vlanId=24,
            switches=[{'key': 'value'}],
            protocols=['item1', 'item2'],
        )
        user = api.to_ansible(_ctx())

        assert user.default_mtu_size == api.defaultMtuSize
        assert user.overrides == api.overrides
        assert user.broadcast_threshold == api.broadcastThreshold
        assert user.multicast_threshold == api.multicastThreshold
        assert user.unknown_unicast_threshold == api.unknownUnicastThreshold
        assert user.mappings == api.mappings
        assert user.use_combined_power == api.useCombinedPower
        assert user.power_exceptions == api.powerExceptions
        assert user.enabled == api.enabled
        assert user.vlan_id == api.vlanId
        assert user.switches == api.switches
        assert user.protocols == api.protocols


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = switch_settings_user.UserSwitchSettings(
            default_mtu_size=24,
            overrides=[{'key': 'value'}],
            broadcast_threshold=24,
            multicast_threshold=24,
            unknown_unicast_threshold=24,
            mappings=[{'key': 'value'}],
            use_combined_power=True,
            power_exceptions=[{'key': 'value'}],
            enabled=True,
            vlan_id=24,
            switches=[{'key': 'value'}],
            protocols=['item1', 'item2'],
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.default_mtu_size == original.default_mtu_size
        assert roundtripped.overrides == original.overrides
        assert roundtripped.broadcast_threshold == original.broadcast_threshold
        assert roundtripped.multicast_threshold == original.multicast_threshold
        assert roundtripped.unknown_unicast_threshold == original.unknown_unicast_threshold
        assert roundtripped.mappings == original.mappings
        assert roundtripped.use_combined_power == original.use_combined_power
        assert roundtripped.power_exceptions == original.power_exceptions
        assert roundtripped.enabled == original.enabled
        assert roundtripped.vlan_id == original.vlan_id
        assert roundtripped.switches == original.switches
        assert roundtripped.protocols == original.protocols


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = switch_settings_api.APISwitchSettings_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = switch_settings_api.APISwitchSettings_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

