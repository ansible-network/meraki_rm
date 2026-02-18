"""Colocated tests for APIOrgAlertProfile_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import org_alert_profile as org_alert_profile_api
from ...user_models import org_alert_profile as org_alert_profile_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = org_alert_profile_api.APIOrgAlertProfile_v1(
            id='id_val',
            type='type_val',
            enabled=True,
            alertCondition={'enabled': True},
            recipients={'enabled': True},
            networkTags=['item1', 'item2'],
            description='description_val',
        )
        user = api.to_ansible(_ctx())

        assert user.alert_config_id == api.id
        assert user.type == api.type
        assert user.enabled == api.enabled
        assert user.alert_condition == api.alertCondition
        assert user.recipients == api.recipients
        assert user.network_tags == api.networkTags
        assert user.description == api.description


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = org_alert_profile_user.UserOrgAlertProfile(
            alert_config_id='alert_config_id_val',
            type='type_val',
            enabled=True,
            alert_condition={'enabled': True},
            recipients={'enabled': True},
            network_tags=['item1', 'item2'],
            description='description_val',
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.alert_config_id == original.alert_config_id
        assert roundtripped.type == original.type
        assert roundtripped.enabled == original.enabled
        assert roundtripped.alert_condition == original.alert_condition
        assert roundtripped.recipients == original.recipients
        assert roundtripped.network_tags == original.network_tags
        assert roundtripped.description == original.description


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = org_alert_profile_api.APIOrgAlertProfile_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = org_alert_profile_api.APIOrgAlertProfile_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

