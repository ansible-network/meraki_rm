"""Colocated tests for UserVlanProfile — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import vlan_profile


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserVlanProfile can be constructed with all fields."""

    def test_defaults(self):
        obj = vlan_profile.UserVlanProfile()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserVlanProfile -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = vlan_profile.UserVlanProfile(
            iname='iname_val',
            name='name_val',
            is_default=True,
            vlan_names=[{'key': 'value'}],
            vlan_groups=[{'key': 'value'}],
            vlan_profile={'enabled': True},
        )
        api = user.to_api(_ctx())

        assert api.iname == user.iname
        assert api.name == user.name
        assert api.isDefault == user.is_default
        assert api.vlanNames == user.vlan_names
        assert api.vlanGroups == user.vlan_groups
        assert api.vlanProfile == user.vlan_profile

    def test_none_fields_omitted(self):
        user = vlan_profile.UserVlanProfile(iname='iname_val')
        api = user.to_api(_ctx())
        assert api.iname == user.iname
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = vlan_profile.UserVlanProfile(network_id='network_id_val', iname='iname_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

