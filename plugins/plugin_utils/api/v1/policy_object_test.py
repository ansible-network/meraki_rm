"""Colocated tests for APIPolicyObject_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import policy_object as policy_object_api
from ...user_models import policy_object as policy_object_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = policy_object_api.APIPolicyObject_v1(
            id='id_val',
            name='name_val',
            category='category_val',
            type='type_val',
            cidr='cidr_val',
            fqdn='fqdn_val',
            ip='ip_val',
            mask='mask_val',
            groupIds=['item1', 'item2'],
            networkIds=['item1', 'item2'],
            objectIds=24,
        )
        user = api.to_ansible(_ctx())

        assert user.policy_object_id == api.id
        assert user.name == api.name
        assert user.category == api.category
        assert user.type == api.type
        assert user.cidr == api.cidr
        assert user.fqdn == api.fqdn
        assert user.ip == api.ip
        assert user.mask == api.mask
        assert user.group_ids == api.groupIds
        assert user.network_ids == api.networkIds
        assert user.object_ids == api.objectIds


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = policy_object_user.UserPolicyObject(
            policy_object_id='policy_object_id_val',
            name='name_val',
            category='category_val',
            type='type_val',
            cidr='cidr_val',
            fqdn='fqdn_val',
            ip='ip_val',
            mask='mask_val',
            group_ids=['item1', 'item2'],
            network_ids=['item1', 'item2'],
            object_ids=24,
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.policy_object_id == original.policy_object_id
        assert roundtripped.name == original.name
        assert roundtripped.category == original.category
        assert roundtripped.type == original.type
        assert roundtripped.cidr == original.cidr
        assert roundtripped.fqdn == original.fqdn
        assert roundtripped.ip == original.ip
        assert roundtripped.mask == original.mask
        assert roundtripped.group_ids == original.group_ids
        assert roundtripped.network_ids == original.network_ids
        assert roundtripped.object_ids == original.object_ids


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = policy_object_api.APIPolicyObject_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = policy_object_api.APIPolicyObject_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

