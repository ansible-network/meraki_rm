"""Colocated tests for APISensorAlertProfile_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import sensor_alert_profile as sensor_alert_profile_api
from ...user_models import sensor_alert_profile as sensor_alert_profile_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = sensor_alert_profile_api.APISensorAlertProfile_v1(
            profileId='profileId_val',
            name='name_val',
            conditions=[{'key': 'value'}],
            schedule={'enabled': True},
            recipients={'enabled': True},
            message='message_val',
            includeSensorUrl=True,
            serials=['item1', 'item2'],
        )
        user = api.to_ansible(_ctx())

        assert user.id == api.profileId
        assert user.name == api.name
        assert user.conditions == api.conditions
        assert user.schedule == api.schedule
        assert user.recipients == api.recipients
        assert user.message == api.message
        assert user.include_sensor_url == api.includeSensorUrl
        assert user.serials == api.serials


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = sensor_alert_profile_user.UserSensorAlertProfile(
            id='id_val',
            name='name_val',
            conditions=[{'key': 'value'}],
            schedule={'enabled': True},
            recipients={'enabled': True},
            message='message_val',
            include_sensor_url=True,
            serials=['item1', 'item2'],
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.id == original.id
        assert roundtripped.name == original.name
        assert roundtripped.conditions == original.conditions
        assert roundtripped.schedule == original.schedule
        assert roundtripped.recipients == original.recipients
        assert roundtripped.message == original.message
        assert roundtripped.include_sensor_url == original.include_sensor_url
        assert roundtripped.serials == original.serials


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = sensor_alert_profile_api.APISensorAlertProfile_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = sensor_alert_profile_api.APISensorAlertProfile_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

