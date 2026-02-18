"""Colocated tests for UserFloorPlan — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import floor_plan


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserFloorPlan can be constructed with all fields."""

    def test_defaults(self):
        obj = floor_plan.UserFloorPlan()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserFloorPlan -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = floor_plan.UserFloorPlan(
            floor_plan_id='floor_plan_id_val',
            name='name_val',
            center={'enabled': True},
            bottom_left_corner={'enabled': True},
            bottom_right_corner={'enabled': True},
            top_left_corner={'enabled': True},
            top_right_corner={'enabled': True},
            width=1.5,
            height=1.5,
            floor_number=1.5,
            image_contents='image_contents_val',
            image_extension='image_extension_val',
        )
        api = user.to_api(_ctx())

        assert api.floorPlanId == user.floor_plan_id
        assert api.name == user.name
        assert api.center == user.center
        assert api.bottomLeftCorner == user.bottom_left_corner
        assert api.bottomRightCorner == user.bottom_right_corner
        assert api.topLeftCorner == user.top_left_corner
        assert api.topRightCorner == user.top_right_corner
        assert api.width == user.width
        assert api.height == user.height
        assert api.floorNumber == user.floor_number
        assert api.imageContents == user.image_contents
        assert api.imageExtension == user.image_extension

    def test_none_fields_omitted(self):
        user = floor_plan.UserFloorPlan(floor_plan_id='floor_plan_id_val')
        api = user.to_api(_ctx())
        assert api.floorPlanId == user.floor_plan_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = floor_plan.UserFloorPlan(network_id='network_id_val', floor_plan_id='floor_plan_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

