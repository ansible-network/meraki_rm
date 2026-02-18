"""Colocated tests for APIMqttBroker_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import mqtt_broker as mqtt_broker_api
from ...user_models import mqtt_broker as mqtt_broker_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = mqtt_broker_api.APIMqttBroker_v1(
            id='id_val',
            name='name_val',
            host='host_val',
            port=24,
            authentication={'enabled': True},
            security={'enabled': True},
        )
        user = api.to_ansible(_ctx())

        assert user.mqtt_broker_id == api.id
        assert user.name == api.name
        assert user.host == api.host
        assert user.port == api.port
        assert user.authentication == api.authentication
        assert user.security == api.security


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = mqtt_broker_user.UserMqttBroker(
            mqtt_broker_id='mqtt_broker_id_val',
            name='name_val',
            host='host_val',
            port=24,
            authentication={'enabled': True},
            security={'enabled': True},
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.mqtt_broker_id == original.mqtt_broker_id
        assert roundtripped.name == original.name
        assert roundtripped.host == original.host
        assert roundtripped.port == original.port
        assert roundtripped.authentication == original.authentication
        assert roundtripped.security == original.security


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = mqtt_broker_api.APIMqttBroker_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = mqtt_broker_api.APIMqttBroker_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

