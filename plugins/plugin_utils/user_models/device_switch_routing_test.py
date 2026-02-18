"""Colocated tests for UserDeviceSwitchRouting — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import device_switch_routing


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserDeviceSwitchRouting can be constructed with all fields."""

    def test_defaults(self):
        obj = device_switch_routing.UserDeviceSwitchRouting()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserDeviceSwitchRouting -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = device_switch_routing.UserDeviceSwitchRouting(
            interface_id='interface_id_val',
            name='name_val',
            subnet='subnet_val',
            interface_ip='interface_ip_val',
            default_gateway='default_gateway_val',
            vlan_id=24,
            multicast_routing='multicast_routing_val',
            ospf_settings={'enabled': True},
            dhcp_mode='dhcp_mode_val',
            dhcp_relay_server_ips=['item1', 'item2'],
        )
        api = user.to_api(_ctx())

        assert api.interfaceId == user.interface_id
        assert api.name == user.name
        assert api.subnet == user.subnet
        assert api.interfaceIp == user.interface_ip
        assert api.defaultGateway == user.default_gateway
        assert api.vlanId == user.vlan_id
        assert api.multicastRouting == user.multicast_routing
        assert api.ospfSettings == user.ospf_settings
        assert api.dhcpMode == user.dhcp_mode
        assert api.dhcpRelayServerIps == user.dhcp_relay_server_ips

    def test_none_fields_omitted(self):
        user = device_switch_routing.UserDeviceSwitchRouting(interface_id='interface_id_val')
        api = user.to_api(_ctx())
        assert api.interfaceId == user.interface_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = device_switch_routing.UserDeviceSwitchRouting(serial='serial_val', interface_id='interface_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'serial' not in api_field_names or getattr(api, 'serial', None) is None

