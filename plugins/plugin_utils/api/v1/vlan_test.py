"""Colocated tests for APIVlan_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import vlan as vlan_api
from ...user_models import vlan as vlan_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = vlan_api.APIVlan_v1(
            id='id_val',
            name='name_val',
            subnet='subnet_val',
            applianceIp='applianceIp_val',
            groupPolicyId='groupPolicyId_val',
            templateVlanType='templateVlanType_val',
            cidr='cidr_val',
            mask=24,
            dhcpHandling='dhcpHandling_val',
            dhcpRelayServerIps=['item1', 'item2'],
            dhcpLeaseTime='dhcpLeaseTime_val',
            dhcpBootOptionsEnabled=True,
            dhcpBootNextServer='dhcpBootNextServer_val',
            dhcpBootFilename='dhcpBootFilename_val',
            dhcpOptions=[{'key': 'value'}],
            dnsNameservers='dnsNameservers_val',
            reservedIpRanges=[{'key': 'value'}],
            fixedIpAssignments={'k1': {'ip': '10.0.0.1', 'name': 'host'}},
            ipv6={'enabled': True},
            mandatoryDhcp={'enabled': True},
        )
        user = api.to_ansible(_ctx())

        assert user.vlan_id == api.id
        assert user.name == api.name
        assert user.subnet == api.subnet
        assert user.appliance_ip == api.applianceIp
        assert user.group_policy_id == api.groupPolicyId
        assert user.template_vlan_type == api.templateVlanType
        assert user.cidr == api.cidr
        assert user.mask == api.mask
        assert user.dhcp_handling == api.dhcpHandling
        assert user.dhcp_relay_server_ips == api.dhcpRelayServerIps
        assert user.dhcp_lease_time == api.dhcpLeaseTime
        assert user.dhcp_boot_options_enabled == api.dhcpBootOptionsEnabled
        assert user.dhcp_boot_next_server == api.dhcpBootNextServer
        assert user.dhcp_boot_filename == api.dhcpBootFilename
        assert user.dhcp_options == api.dhcpOptions
        assert user.dns_nameservers == api.dnsNameservers
        assert user.reserved_ip_ranges == api.reservedIpRanges
        assert user.fixed_ip_assignments == api.fixedIpAssignments
        assert user.ipv6 == api.ipv6
        assert user.mandatory_dhcp == api.mandatoryDhcp


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = vlan_user.UserVlan(
            vlan_id='vlan_id_val',
            name='name_val',
            subnet='subnet_val',
            appliance_ip='appliance_ip_val',
            group_policy_id='group_policy_id_val',
            template_vlan_type='template_vlan_type_val',
            cidr='cidr_val',
            mask=24,
            dhcp_handling='dhcp_handling_val',
            dhcp_relay_server_ips=['item1', 'item2'],
            dhcp_lease_time='dhcp_lease_time_val',
            dhcp_boot_options_enabled=True,
            dhcp_boot_next_server='dhcp_boot_next_server_val',
            dhcp_boot_filename='dhcp_boot_filename_val',
            dhcp_options=[{'key': 'value'}],
            dns_nameservers='dns_nameservers_val',
            reserved_ip_ranges=[{'key': 'value'}],
            fixed_ip_assignments={'enabled': True},
            ipv6={'enabled': True},
            mandatory_dhcp={'enabled': True},
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.vlan_id == original.vlan_id
        assert roundtripped.name == original.name
        assert roundtripped.subnet == original.subnet
        assert roundtripped.appliance_ip == original.appliance_ip
        assert roundtripped.group_policy_id == original.group_policy_id
        assert roundtripped.template_vlan_type == original.template_vlan_type
        assert roundtripped.cidr == original.cidr
        assert roundtripped.mask == original.mask
        assert roundtripped.dhcp_handling == original.dhcp_handling
        assert roundtripped.dhcp_relay_server_ips == original.dhcp_relay_server_ips
        assert roundtripped.dhcp_lease_time == original.dhcp_lease_time
        assert roundtripped.dhcp_boot_options_enabled == original.dhcp_boot_options_enabled
        assert roundtripped.dhcp_boot_next_server == original.dhcp_boot_next_server
        assert roundtripped.dhcp_boot_filename == original.dhcp_boot_filename
        assert roundtripped.dhcp_options == original.dhcp_options
        assert roundtripped.dns_nameservers == original.dns_nameservers
        assert roundtripped.reserved_ip_ranges == original.reserved_ip_ranges
        assert roundtripped.fixed_ip_assignments == original.fixed_ip_assignments
        assert roundtripped.ipv6 == original.ipv6
        assert roundtripped.mandatory_dhcp == original.mandatory_dhcp


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = vlan_api.APIVlan_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = vlan_api.APIVlan_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

