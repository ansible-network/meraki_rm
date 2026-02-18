"""Colocated tests for APIFloorPlan_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import floor_plan as floor_plan_api
from ...user_models import floor_plan as floor_plan_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = floor_plan_api.APIFloorPlan_v1(
            floorPlanId='floorPlanId_val',
            name='name_val',
            center={'enabled': True},
            bottomLeftCorner={'enabled': True},
            bottomRightCorner={'enabled': True},
            topLeftCorner={'enabled': True},
            topRightCorner={'enabled': True},
            width=1.5,
            height=1.5,
            floorNumber=1.5,
            imageContents='imageContents_val',
            imageExtension='imageExtension_val',
        )
        user = api.to_ansible(_ctx())

        assert user.floor_plan_id == api.floorPlanId
        assert user.name == api.name
        assert user.center == api.center
        assert user.bottom_left_corner == api.bottomLeftCorner
        assert user.bottom_right_corner == api.bottomRightCorner
        assert user.top_left_corner == api.topLeftCorner
        assert user.top_right_corner == api.topRightCorner
        assert user.width == api.width
        assert user.height == api.height
        assert user.floor_number == api.floorNumber
        assert user.image_contents == api.imageContents
        assert user.image_extension == api.imageExtension


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = floor_plan_user.UserFloorPlan(
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
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.floor_plan_id == original.floor_plan_id
        assert roundtripped.name == original.name
        assert roundtripped.center == original.center
        assert roundtripped.bottom_left_corner == original.bottom_left_corner
        assert roundtripped.bottom_right_corner == original.bottom_right_corner
        assert roundtripped.top_left_corner == original.top_left_corner
        assert roundtripped.top_right_corner == original.top_right_corner
        assert roundtripped.width == original.width
        assert roundtripped.height == original.height
        assert roundtripped.floor_number == original.floor_number
        assert roundtripped.image_contents == original.image_contents
        assert roundtripped.image_extension == original.image_extension


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = floor_plan_api.APIFloorPlan_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = floor_plan_api.APIFloorPlan_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

