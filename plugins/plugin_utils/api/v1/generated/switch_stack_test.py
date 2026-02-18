"""Drift-detection tests for generated SwitchStack dataclass."""

from dataclasses import fields as dc_fields, is_dataclass
from . import switch_stack


class TestSchema:
    """SwitchStack field inventory — catches regeneration drift."""

    def test_is_dataclass(self):
        assert is_dataclass(switch_stack.SwitchStack)

    def test_expected_fields_exist(self):
        field_names = {f.name for f in dc_fields(switch_stack.SwitchStack())}
        expected = {'interfaceId', 'multicastRouting', 'staticRouteId', 'dhcpOptions', 'advertiseViaOspfEnabled', 'uplinkV4', 'managementNextHop', 'serials', 'dhcpLeaseTime', 'id', 'switchPortId', 'preferOverOspfRoutesEnabled', 'workflowId', 'virtualMac', 'isMonitorOnly', 'fixedIpAssignments', 'mode', 'name', 'ospfSettings', 'dnsCustomNameservers', 'defaultGateway', 'uplinkV6', 'vlanId', 'interfaceIp', 'bootNextServer', 'ipv6', 'vrf', 'subnet', 'members', 'bootFileName', 'dhcpMode', 'loopback', 'bootOptionsEnabled', 'dnsNameserversOption', 'serial', 'nextHopIp', 'dhcpRelayServerIps', 'ospfV3', 'reservedIpRanges'}
        assert expected.issubset(field_names), f'Missing fields: {expected - field_names}'

    def test_all_fields_optional(self):
        """Every generated field should default to None (all Optional)."""
        obj = switch_stack.SwitchStack()
        for f in dc_fields(obj):
            assert getattr(obj, f.name) is None, f'{f.name} is not None by default'

    def test_field_count(self):
        """Guard against silent field additions or removals."""
        assert len(dc_fields(switch_stack.SwitchStack())) == 39


class TestSpecDrift:
    """Cross-reference dataclass fields against spec3.json response schemas."""

    SPEC_FIELDS = ['advertiseViaOspfEnabled', 'bootFileName', 'bootNextServer', 'bootOptionsEnabled', 'defaultGateway', 'dhcpLeaseTime', 'dhcpMode', 'dhcpOptions', 'dhcpRelayServerIps', 'dnsCustomNameservers', 'dnsNameserversOption', 'fixedIpAssignments', 'id', 'interfaceId', 'interfaceIp', 'ipv6', 'isMonitorOnly', 'loopback', 'managementNextHop', 'members', 'mode', 'multicastRouting', 'name', 'nextHopIp', 'ospfSettings', 'ospfV3', 'preferOverOspfRoutesEnabled', 'reservedIpRanges', 'serial', 'serials', 'staticRouteId', 'subnet', 'switchPortId', 'uplinkV4', 'uplinkV6', 'virtualMac', 'vlanId', 'vrf', 'workflowId']

    def test_dataclass_covers_spec(self):
        """Every spec response property should have a dataclass field."""
        dc_names = {f.name for f in dc_fields(switch_stack.SwitchStack())}
        spec_set = set(self.SPEC_FIELDS)
        missing = spec_set - dc_names
        assert not missing, f'Spec fields missing from dataclass: {missing}'

    def test_dataclass_no_extra_fields(self):
        """Warn if the dataclass has fields not in the spec (may indicate stale fields)."""
        dc_names = {f.name for f in dc_fields(switch_stack.SwitchStack())}
        spec_set = set(self.SPEC_FIELDS)
        extras = dc_names - spec_set
        assert not extras, (
            f'Dataclass has fields not in spec responses: {extras}. '
            f'These may be stale or from request-only schemas.'
        )

