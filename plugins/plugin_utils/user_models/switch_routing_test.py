"""Colocated tests for UserSwitchRouting — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import switch_routing


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserSwitchRouting can be constructed with all fields."""

    def test_defaults(self):
        obj = switch_routing.UserSwitchRouting()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserSwitchRouting -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = switch_routing.UserSwitchRouting(
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
        api = user.to_api(_ctx())

        assert api.defaultSettings == user.default_settings
        assert api.overrides == user.overrides
        assert api.enabled == user.enabled
        assert api.helloTimerInSeconds == user.hello_timer_in_seconds
        assert api.deadTimerInSeconds == user.dead_timer_in_seconds
        assert api.areas == user.areas
        assert api.md5AuthenticationEnabled == user.md5_authentication_enabled
        assert api.md5AuthenticationKey == user.md5_authentication_key
        assert api.v3 == user.v3

    def test_none_fields_omitted(self):
        user = switch_routing.UserSwitchRouting(default_settings={'enabled': True})
        api = user.to_api(_ctx())
        assert api.defaultSettings == user.default_settings
        assert getattr(api, 'overrides', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = switch_routing.UserSwitchRouting(network_id='network_id_val', default_settings={'enabled': True})
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

