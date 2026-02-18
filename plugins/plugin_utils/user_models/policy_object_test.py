"""Colocated tests for UserPolicyObject — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import policy_object


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserPolicyObject can be constructed with all fields."""

    def test_defaults(self):
        obj = policy_object.UserPolicyObject()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserPolicyObject -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = policy_object.UserPolicyObject(
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
        api = user.to_api(_ctx())

        assert api.id == user.policy_object_id
        assert api.name == user.name
        assert api.category == user.category
        assert api.type == user.type
        assert api.cidr == user.cidr
        assert api.fqdn == user.fqdn
        assert api.ip == user.ip
        assert api.mask == user.mask
        assert api.groupIds == user.group_ids
        assert api.networkIds == user.network_ids
        assert api.objectIds == user.object_ids

    def test_none_fields_omitted(self):
        user = policy_object.UserPolicyObject(policy_object_id='policy_object_id_val')
        api = user.to_api(_ctx())
        assert api.id == user.policy_object_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = policy_object.UserPolicyObject(organization_id='organization_id_val', policy_object_id='policy_object_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'organization_id' not in api_field_names or getattr(api, 'organization_id', None) is None

