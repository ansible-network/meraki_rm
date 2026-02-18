"""Colocated tests for APIDeviceSwitchRouting_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import device_switch_routing as device_switch_routing_api
from ...user_models import device_switch_routing as device_switch_routing_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = device_switch_routing_api.APIDeviceSwitchRouting_v1(
            interfaceId='interfaceId_val',
            name='name_val',
            subnet='subnet_val',
            interfaceIp='interfaceIp_val',
            defaultGateway='defaultGateway_val',
            vlanId=24,
            multicastRouting='multicastRouting_val',
            ospfSettings={'enabled': True},
            dhcpMode='dhcpMode_val',
            dhcpRelayServerIps=['item1', 'item2'],
        )
        user = api.to_ansible(_ctx())

        assert user.interface_id == api.interfaceId
        assert user.name == api.name
        assert user.subnet == api.subnet
        assert user.interface_ip == api.interfaceIp
        assert user.default_gateway == api.defaultGateway
        assert user.vlan_id == api.vlanId
        assert user.multicast_routing == api.multicastRouting
        assert user.ospf_settings == api.ospfSettings
        assert user.dhcp_mode == api.dhcpMode
        assert user.dhcp_relay_server_ips == api.dhcpRelayServerIps


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = device_switch_routing_user.UserDeviceSwitchRouting(
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
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.interface_id == original.interface_id
        assert roundtripped.name == original.name
        assert roundtripped.subnet == original.subnet
        assert roundtripped.interface_ip == original.interface_ip
        assert roundtripped.default_gateway == original.default_gateway
        assert roundtripped.vlan_id == original.vlan_id
        assert roundtripped.multicast_routing == original.multicast_routing
        assert roundtripped.ospf_settings == original.ospf_settings
        assert roundtripped.dhcp_mode == original.dhcp_mode
        assert roundtripped.dhcp_relay_server_ips == original.dhcp_relay_server_ips


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = device_switch_routing_api.APIDeviceSwitchRouting_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = device_switch_routing_api.APIDeviceSwitchRouting_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

