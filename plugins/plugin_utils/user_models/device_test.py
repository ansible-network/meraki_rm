"""Colocated tests for UserDevice — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import device


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserDevice can be constructed with all fields."""

    def test_defaults(self):
        obj = device.UserDevice()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserDevice -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = device.UserDevice(
            name='name_val',
            tags=['item1', 'item2'],
            lat=1.5,
            lng=1.5,
            address='address_val',
            notes='notes_val',
            move_map_marker=True,
            floor_plan_id='floor_plan_id_val',
            switch_profile_id='switch_profile_id_val',
        )
        api = user.to_api(_ctx())

        assert api.name == user.name
        assert api.tags == user.tags
        assert api.lat == user.lat
        assert api.lng == user.lng
        assert api.address == user.address
        assert api.notes == user.notes
        assert api.moveMapMarker == user.move_map_marker
        assert api.floorPlanId == user.floor_plan_id
        assert api.switchProfileId == user.switch_profile_id

    def test_none_fields_omitted(self):
        user = device.UserDevice(name='name_val')
        api = user.to_api(_ctx())
        assert api.name == user.name
        assert getattr(api, 'tags', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = device.UserDevice(serial='serial_val', name='name_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'serial' not in api_field_names or getattr(api, 'serial', None) is None

