"""Colocated tests for APIVlanProfile_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import vlan_profile as vlan_profile_api
from ...user_models import vlan_profile as vlan_profile_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = vlan_profile_api.APIVlanProfile_v1(
            iname='iname_val',
            name='name_val',
            isDefault=True,
            vlanNames=[{'key': 'value'}],
            vlanGroups=[{'key': 'value'}],
            vlanProfile={'enabled': True},
        )
        user = api.to_ansible(_ctx())

        assert user.iname == api.iname
        assert user.name == api.name
        assert user.is_default == api.isDefault
        assert user.vlan_names == api.vlanNames
        assert user.vlan_groups == api.vlanGroups
        assert user.vlan_profile == api.vlanProfile


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = vlan_profile_user.UserVlanProfile(
            iname='iname_val',
            name='name_val',
            is_default=True,
            vlan_names=[{'key': 'value'}],
            vlan_groups=[{'key': 'value'}],
            vlan_profile={'enabled': True},
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.iname == original.iname
        assert roundtripped.name == original.name
        assert roundtripped.is_default == original.is_default
        assert roundtripped.vlan_names == original.vlan_names
        assert roundtripped.vlan_groups == original.vlan_groups
        assert roundtripped.vlan_profile == original.vlan_profile


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = vlan_profile_api.APIVlanProfile_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = vlan_profile_api.APIVlanProfile_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

