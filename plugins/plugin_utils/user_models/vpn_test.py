"""Colocated tests for UserVpn — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import vpn


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserVpn can be constructed with all fields."""

    def test_defaults(self):
        obj = vpn.UserVpn()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserVpn -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = vpn.UserVpn(
            mode='mode_val',
            hubs=[{'key': 'value'}],
            subnets=[{'key': 'value'}],
            subnet={'enabled': True},
            enabled=True,
            as_number=24,
            ibgp_hold_timer=24,
            neighbors=[{'key': 'value'}],
        )
        api = user.to_api(_ctx())

        assert api.mode == user.mode
        assert api.hubs == user.hubs
        assert api.subnets == user.subnets
        assert api.subnet == user.subnet
        assert api.enabled == user.enabled
        assert api.asNumber == user.as_number
        assert api.ibgpHoldTimer == user.ibgp_hold_timer
        assert api.neighbors == user.neighbors

    def test_none_fields_omitted(self):
        user = vpn.UserVpn(mode='mode_val')
        api = user.to_api(_ctx())
        assert api.mode == user.mode
        assert getattr(api, 'hubs', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = vpn.UserVpn(network_id='network_id_val', mode='mode_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

