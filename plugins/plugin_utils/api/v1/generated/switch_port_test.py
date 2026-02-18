"""Drift-detection tests for generated SwitchPort dataclass."""

from dataclasses import fields as dc_fields, is_dataclass
from . import switch_port


class TestSchema:
    """SwitchPort field inventory — catches regeneration drift."""

    def test_is_dataclass(self):
        assert is_dataclass(switch_port.SwitchPort)

    def test_expected_fields_exist(self):
        field_names = {f.name for f in dc_fields(switch_port.SwitchPort())}
        expected = {'poe', 'enabled', 'ports', 'duplex', 'adaptivePolicyGroupId', 'status', 'stpGuard', 'speed', 'mirror', 'profile', 'stormControlEnabled', 'stpPortFastTrunk', 'usageInKb', 'linkNegotiationCapabilities', 'adaptivePolicyGroup', 'highSpeed', 'name', 'portId', 'flexibleStackingEnabled', 'clientCount', 'errors', 'rstpEnabled', 'isolationEnabled', 'isUplink', 'lldp', 'peerSgtCapable', 'voiceVlan', 'portScheduleId', 'vlan', 'warnings', 'allowedVlans', 'accessPolicyType', 'packets', 'cdp', 'schedule', 'tags', 'securePort', 'dot3az', 'trafficInKbps', 'udld', 'macWhitelistLimit', 'macAllowList', 'spanningTree', 'accessPolicyNumber', 'module', 'type', 'daiTrusted', 'powerUsageInWh', 'poeEnabled', 'linkNegotiation', 'stickyMacAllowList', 'stickyMacAllowListLimit'}
        assert expected.issubset(field_names), f'Missing fields: {expected - field_names}'

    def test_all_fields_optional(self):
        """Every generated field should default to None (all Optional)."""
        obj = switch_port.SwitchPort()
        for f in dc_fields(obj):
            assert getattr(obj, f.name) is None, f'{f.name} is not None by default'

    def test_field_count(self):
        """Guard against silent field additions or removals."""
        assert len(dc_fields(switch_port.SwitchPort())) == 52


class TestSpecDrift:
    """Cross-reference dataclass fields against spec3.json response schemas."""

    SPEC_FIELDS = ['accessPolicyNumber', 'accessPolicyType', 'adaptivePolicyGroup', 'adaptivePolicyGroupId', 'allowedVlans', 'cdp', 'clientCount', 'daiTrusted', 'dot3az', 'duplex', 'enabled', 'errors', 'flexibleStackingEnabled', 'highSpeed', 'isUplink', 'isolationEnabled', 'linkNegotiation', 'linkNegotiationCapabilities', 'lldp', 'macAllowList', 'macWhitelistLimit', 'mirror', 'module', 'name', 'packets', 'peerSgtCapable', 'poe', 'poeEnabled', 'portId', 'portScheduleId', 'ports', 'powerUsageInWh', 'profile', 'rstpEnabled', 'schedule', 'securePort', 'spanningTree', 'speed', 'status', 'stickyMacAllowList', 'stickyMacAllowListLimit', 'stormControlEnabled', 'stpGuard', 'stpPortFastTrunk', 'tags', 'trafficInKbps', 'type', 'udld', 'usageInKb', 'vlan', 'voiceVlan', 'warnings']

    def test_dataclass_covers_spec(self):
        """Every spec response property should have a dataclass field."""
        dc_names = {f.name for f in dc_fields(switch_port.SwitchPort())}
        spec_set = set(self.SPEC_FIELDS)
        missing = spec_set - dc_names
        assert not missing, f'Spec fields missing from dataclass: {missing}'

    def test_dataclass_no_extra_fields(self):
        """Warn if the dataclass has fields not in the spec (may indicate stale fields)."""
        dc_names = {f.name for f in dc_fields(switch_port.SwitchPort())}
        spec_set = set(self.SPEC_FIELDS)
        extras = dc_names - spec_set
        assert not extras, (
            f'Dataclass has fields not in spec responses: {extras}. '
            f'These may be stale or from request-only schemas.'
        )

