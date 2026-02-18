"""Colocated tests for UserStaticRoute — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import static_route


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserStaticRoute can be constructed with all fields."""

    def test_defaults(self):
        obj = static_route.UserStaticRoute()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserStaticRoute -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = static_route.UserStaticRoute(
            static_route_id='static_route_id_val',
            name='name_val',
            subnet='subnet_val',
            gateway_ip='gateway_ip_val',
            gateway_vlan_id=24,
            enabled=True,
            fixed_ip_assignments={'enabled': True},
            reserved_ip_ranges=[{'key': 'value'}],
            ip_version=24,
        )
        api = user.to_api(_ctx())

        assert api.id == user.static_route_id
        assert api.name == user.name
        assert api.subnet == user.subnet
        assert api.gatewayIp == user.gateway_ip
        assert api.gatewayVlanId == user.gateway_vlan_id
        assert api.enabled == user.enabled
        assert api.fixedIpAssignments == user.fixed_ip_assignments
        assert api.reservedIpRanges == user.reserved_ip_ranges
        assert api.ipVersion == user.ip_version

    def test_none_fields_omitted(self):
        user = static_route.UserStaticRoute(static_route_id='static_route_id_val')
        api = user.to_api(_ctx())
        assert api.id == user.static_route_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = static_route.UserStaticRoute(network_id='network_id_val', static_route_id='static_route_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

