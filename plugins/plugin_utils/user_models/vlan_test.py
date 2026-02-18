"""Colocated tests for UserVlan — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import vlan


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserVlan can be constructed with all fields."""

    def test_defaults(self):
        obj = vlan.UserVlan()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserVlan -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = vlan.UserVlan(
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
        api = user.to_api(_ctx())

        assert api.id == user.vlan_id
        assert api.name == user.name
        assert api.subnet == user.subnet
        assert api.applianceIp == user.appliance_ip
        assert api.groupPolicyId == user.group_policy_id
        assert api.templateVlanType == user.template_vlan_type
        assert api.cidr == user.cidr
        assert api.mask == user.mask
        assert api.dhcpHandling == user.dhcp_handling
        assert api.dhcpRelayServerIps == user.dhcp_relay_server_ips
        assert api.dhcpLeaseTime == user.dhcp_lease_time
        assert api.dhcpBootOptionsEnabled == user.dhcp_boot_options_enabled
        assert api.dhcpBootNextServer == user.dhcp_boot_next_server
        assert api.dhcpBootFilename == user.dhcp_boot_filename
        assert api.dhcpOptions == user.dhcp_options
        assert api.dnsNameservers == user.dns_nameservers
        assert api.reservedIpRanges == user.reserved_ip_ranges
        assert api.fixedIpAssignments == user.fixed_ip_assignments
        assert api.ipv6 == user.ipv6
        assert api.mandatoryDhcp == user.mandatory_dhcp

    def test_none_fields_omitted(self):
        user = vlan.UserVlan(vlan_id='vlan_id_val')
        api = user.to_api(_ctx())
        assert api.id == user.vlan_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = vlan.UserVlan(network_id='network_id_val', vlan_id='vlan_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

