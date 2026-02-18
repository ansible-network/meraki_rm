"""Colocated tests for APIDevice_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import device as device_api
from ...user_models import device as device_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = device_api.APIDevice_v1(
            name='name_val',
            tags=['item1', 'item2'],
            lat=1.5,
            lng=1.5,
            address='address_val',
            notes='notes_val',
            moveMapMarker=True,
            floorPlanId='floorPlanId_val',
            switchProfileId='switchProfileId_val',
        )
        user = api.to_ansible(_ctx())

        assert user.name == api.name
        assert user.tags == api.tags
        assert user.lat == api.lat
        assert user.lng == api.lng
        assert user.address == api.address
        assert user.notes == api.notes
        assert user.move_map_marker == api.moveMapMarker
        assert user.floor_plan_id == api.floorPlanId
        assert user.switch_profile_id == api.switchProfileId


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = device_user.UserDevice(
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
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.name == original.name
        assert roundtripped.tags == original.tags
        assert roundtripped.lat == original.lat
        assert roundtripped.lng == original.lng
        assert roundtripped.address == original.address
        assert roundtripped.notes == original.notes
        assert roundtripped.move_map_marker == original.move_map_marker
        assert roundtripped.floor_plan_id == original.floor_plan_id
        assert roundtripped.switch_profile_id == original.switch_profile_id


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = device_api.APIDevice_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = device_api.APIDevice_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

