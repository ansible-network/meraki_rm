"""Colocated tests for UserDeviceManagementInterface — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import device_management_interface


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserDeviceManagementInterface can be constructed with all fields."""

    def test_defaults(self):
        obj = device_management_interface.UserDeviceManagementInterface()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserDeviceManagementInterface -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = device_management_interface.UserDeviceManagementInterface(
            wan1={'enabled': True},
            wan2={'enabled': True},
            ddns_hostnames={'enabled': True},
        )
        api = user.to_api(_ctx())

        assert api.wan1 == user.wan1
        assert api.wan2 == user.wan2
        assert api.ddnsHostnames == user.ddns_hostnames

    def test_none_fields_omitted(self):
        user = device_management_interface.UserDeviceManagementInterface(wan1={'enabled': True})
        api = user.to_api(_ctx())
        assert api.wan1 == user.wan1
        assert getattr(api, 'wan2', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = device_management_interface.UserDeviceManagementInterface(serial='serial_val', wan1={'enabled': True})
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'serial' not in api_field_names or getattr(api, 'serial', None) is None

