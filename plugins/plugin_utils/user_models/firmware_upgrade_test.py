"""Colocated tests for UserFirmwareUpgrade — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import firmware_upgrade


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserFirmwareUpgrade can be constructed with all fields."""

    def test_defaults(self):
        obj = firmware_upgrade.UserFirmwareUpgrade()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserFirmwareUpgrade -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = firmware_upgrade.UserFirmwareUpgrade(
            upgrade_window={'enabled': True},
            timezone='timezone_val',
            products={'enabled': True},
        )
        api = user.to_api(_ctx())

        assert api.upgradeWindow == user.upgrade_window
        assert api.timezone == user.timezone
        assert api.products == user.products

    def test_none_fields_omitted(self):
        user = firmware_upgrade.UserFirmwareUpgrade(upgrade_window={'enabled': True})
        api = user.to_api(_ctx())
        assert api.upgradeWindow == user.upgrade_window
        assert getattr(api, 'timezone', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = firmware_upgrade.UserFirmwareUpgrade(network_id='network_id_val', upgrade_window={'enabled': True})
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

