"""Colocated tests for UserSensorAlertProfile — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import sensor_alert_profile


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserSensorAlertProfile can be constructed with all fields."""

    def test_defaults(self):
        obj = sensor_alert_profile.UserSensorAlertProfile()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserSensorAlertProfile -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = sensor_alert_profile.UserSensorAlertProfile(
            id='id_val',
            name='name_val',
            conditions=[{'key': 'value'}],
            schedule={'enabled': True},
            recipients={'enabled': True},
            message='message_val',
            include_sensor_url=True,
            serials=['item1', 'item2'],
        )
        api = user.to_api(_ctx())

        assert api.profileId == user.id
        assert api.name == user.name
        assert api.conditions == user.conditions
        assert api.schedule == user.schedule
        assert api.recipients == user.recipients
        assert api.message == user.message
        assert api.includeSensorUrl == user.include_sensor_url
        assert api.serials == user.serials

    def test_none_fields_omitted(self):
        user = sensor_alert_profile.UserSensorAlertProfile(id='id_val')
        api = user.to_api(_ctx())
        assert api.profileId == user.id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = sensor_alert_profile.UserSensorAlertProfile(network_id='network_id_val', id='id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

