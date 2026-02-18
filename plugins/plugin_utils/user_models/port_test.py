"""Colocated tests for UserPort — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import port


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserPort can be constructed with all fields."""

    def test_defaults(self):
        obj = port.UserPort()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserPort -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = port.UserPort(
            port_id='port_id_val',
            enabled=True,
            type='type_val',
            vlan=24,
            allowed_vlans='allowed_vlans_val',
            access_policy='access_policy_val',
            drop_untagged_traffic=True,
        )
        api = user.to_api(_ctx())

        assert api.number == user.port_id
        assert api.enabled == user.enabled
        assert api.type == user.type
        assert api.vlan == user.vlan
        assert api.allowedVlans == user.allowed_vlans
        assert api.accessPolicy == user.access_policy
        assert api.dropUntaggedTraffic == user.drop_untagged_traffic

    def test_none_fields_omitted(self):
        user = port.UserPort(port_id='port_id_val')
        api = user.to_api(_ctx())
        assert api.number == user.port_id
        assert getattr(api, 'enabled', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = port.UserPort(network_id='network_id_val', port_id='port_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

