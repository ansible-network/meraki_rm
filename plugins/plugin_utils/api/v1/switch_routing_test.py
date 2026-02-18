"""Colocated tests for APISwitchRouting_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import switch_routing as switch_routing_api
from ...user_models import switch_routing as switch_routing_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = switch_routing_api.APISwitchRouting_v1(
            defaultSettings={'enabled': True},
            overrides=[{'key': 'value'}],
            enabled=True,
            helloTimerInSeconds=24,
            deadTimerInSeconds=24,
            areas=[{'key': 'value'}],
            md5AuthenticationEnabled=True,
            md5AuthenticationKey={'enabled': True},
            v3={'enabled': True},
        )
        user = api.to_ansible(_ctx())

        assert user.default_settings == api.defaultSettings
        assert user.overrides == api.overrides
        assert user.enabled == api.enabled
        assert user.hello_timer_in_seconds == api.helloTimerInSeconds
        assert user.dead_timer_in_seconds == api.deadTimerInSeconds
        assert user.areas == api.areas
        assert user.md5_authentication_enabled == api.md5AuthenticationEnabled
        assert user.md5_authentication_key == api.md5AuthenticationKey
        assert user.v3 == api.v3


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = switch_routing_user.UserSwitchRouting(
            default_settings={'enabled': True},
            overrides=[{'key': 'value'}],
            enabled=True,
            hello_timer_in_seconds=24,
            dead_timer_in_seconds=24,
            areas=[{'key': 'value'}],
            md5_authentication_enabled=True,
            md5_authentication_key={'enabled': True},
            v3={'enabled': True},
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.default_settings == original.default_settings
        assert roundtripped.overrides == original.overrides
        assert roundtripped.enabled == original.enabled
        assert roundtripped.hello_timer_in_seconds == original.hello_timer_in_seconds
        assert roundtripped.dead_timer_in_seconds == original.dead_timer_in_seconds
        assert roundtripped.areas == original.areas
        assert roundtripped.md5_authentication_enabled == original.md5_authentication_enabled
        assert roundtripped.md5_authentication_key == original.md5_authentication_key
        assert roundtripped.v3 == original.v3


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = switch_routing_api.APISwitchRouting_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = switch_routing_api.APISwitchRouting_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

