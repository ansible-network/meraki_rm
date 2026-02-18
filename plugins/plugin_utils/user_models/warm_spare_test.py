"""Colocated tests for UserWarmSpare — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import warm_spare


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserWarmSpare can be constructed with all fields."""

    def test_defaults(self):
        obj = warm_spare.UserWarmSpare()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserWarmSpare -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = warm_spare.UserWarmSpare(
            enabled=True,
            spare_serial='spare_serial_val',
            uplink_mode='uplink_mode_val',
            virtual_ip1='virtual_ip1_val',
            virtual_ip2='virtual_ip2_val',
            wan1={'enabled': True},
            wan2={'enabled': True},
            primary_serial='primary_serial_val',
        )
        api = user.to_api(_ctx())

        assert api.enabled == user.enabled
        assert api.spareSerial == user.spare_serial
        assert api.uplinkMode == user.uplink_mode
        assert api.virtualIp1 == user.virtual_ip1
        assert api.virtualIp2 == user.virtual_ip2
        assert api.wan1 == user.wan1
        assert api.wan2 == user.wan2
        assert api.primarySerial == user.primary_serial

    def test_none_fields_omitted(self):
        user = warm_spare.UserWarmSpare(enabled=True)
        api = user.to_api(_ctx())
        assert api.enabled == user.enabled
        assert getattr(api, 'spareSerial', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = warm_spare.UserWarmSpare(network_id='network_id_val', enabled=True)
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

