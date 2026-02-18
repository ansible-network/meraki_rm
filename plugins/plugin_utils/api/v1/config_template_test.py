"""Colocated tests for APIConfigTemplate_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import config_template as config_template_api
from ...user_models import config_template as config_template_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = config_template_api.APIConfigTemplate_v1(
            id='id_val',
            name='name_val',
            productTypes=['item1', 'item2'],
            timeZone='timeZone_val',
            copyFromNetworkId='copyFromNetworkId_val',
        )
        user = api.to_ansible(_ctx())

        assert user.config_template_id == api.id
        assert user.name == api.name
        assert user.product_types == api.productTypes
        assert user.time_zone == api.timeZone
        assert user.copy_from_network_id == api.copyFromNetworkId


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = config_template_user.UserConfigTemplate(
            config_template_id='config_template_id_val',
            name='name_val',
            product_types=['item1', 'item2'],
            time_zone='time_zone_val',
            copy_from_network_id='copy_from_network_id_val',
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.config_template_id == original.config_template_id
        assert roundtripped.name == original.name
        assert roundtripped.product_types == original.product_types
        assert roundtripped.time_zone == original.time_zone
        assert roundtripped.copy_from_network_id == original.copy_from_network_id


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = config_template_api.APIConfigTemplate_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = config_template_api.APIConfigTemplate_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

