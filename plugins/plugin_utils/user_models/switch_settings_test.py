"""Colocated tests for UserSwitchSettings — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import switch_settings


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserSwitchSettings can be constructed with all fields."""

    def test_defaults(self):
        obj = switch_settings.UserSwitchSettings()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserSwitchSettings -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = switch_settings.UserSwitchSettings(
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
        api = user.to_api(_ctx())

        assert api.defaultMtuSize == user.default_mtu_size
        assert api.overrides == user.overrides
        assert api.broadcastThreshold == user.broadcast_threshold
        assert api.multicastThreshold == user.multicast_threshold
        assert api.unknownUnicastThreshold == user.unknown_unicast_threshold
        assert api.mappings == user.mappings
        assert api.useCombinedPower == user.use_combined_power
        assert api.powerExceptions == user.power_exceptions
        assert api.enabled == user.enabled
        assert api.vlanId == user.vlan_id
        assert api.switches == user.switches
        assert api.protocols == user.protocols

    def test_none_fields_omitted(self):
        user = switch_settings.UserSwitchSettings(default_mtu_size=24)
        api = user.to_api(_ctx())
        assert api.defaultMtuSize == user.default_mtu_size
        assert getattr(api, 'overrides', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = switch_settings.UserSwitchSettings(network_id='network_id_val', default_mtu_size=24)
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

