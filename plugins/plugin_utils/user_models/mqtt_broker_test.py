"""Colocated tests for UserMqttBroker — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import mqtt_broker


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserMqttBroker can be constructed with all fields."""

    def test_defaults(self):
        obj = mqtt_broker.UserMqttBroker()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserMqttBroker -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = mqtt_broker.UserMqttBroker(
            mqtt_broker_id='mqtt_broker_id_val',
            name='name_val',
            host='host_val',
            port=24,
            authentication={'enabled': True},
            security={'enabled': True},
        )
        api = user.to_api(_ctx())

        assert api.id == user.mqtt_broker_id
        assert api.name == user.name
        assert api.host == user.host
        assert api.port == user.port
        assert api.authentication == user.authentication
        assert api.security == user.security

    def test_none_fields_omitted(self):
        user = mqtt_broker.UserMqttBroker(mqtt_broker_id='mqtt_broker_id_val')
        api = user.to_api(_ctx())
        assert api.id == user.mqtt_broker_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = mqtt_broker.UserMqttBroker(network_id='network_id_val', mqtt_broker_id='mqtt_broker_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

