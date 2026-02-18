"""Drift-detection tests for generated TrafficShaping dataclass."""

from dataclasses import fields as dc_fields, is_dataclass
from . import traffic_shaping


class TestSchema:
    """TrafficShaping field inventory — catches regeneration drift."""

    def test_is_dataclass(self):
        assert is_dataclass(traffic_shaping.TrafficShaping)

    def test_expected_fields_exist(self):
        field_names = {f.name for f in dc_fields(traffic_shaping.TrafficShaping())}
        expected = {'custom', 'rules', 'maxJitter', 'defaultUplink', 'name', 'globalBandwidthLimits', 'maxLossPercentage', 'failoverAndFailback', 'customPerformanceClassId', 'defaultRulesEnabled', 'activeActiveAutoVpnEnabled', 'networkId', 'loadBalancingEnabled', 'bandwidthLimits', 'networkName', 'vpnTrafficUplinkPreferences', 'wanTrafficUplinkPreferences', 'majorApplications', 'maxLatency'}
        assert expected.issubset(field_names), f'Missing fields: {expected - field_names}'

    def test_all_fields_optional(self):
        """Every generated field should default to None (all Optional)."""
        obj = traffic_shaping.TrafficShaping()
        for f in dc_fields(obj):
            assert getattr(obj, f.name) is None, f'{f.name} is not None by default'

    def test_field_count(self):
        """Guard against silent field additions or removals."""
        assert len(dc_fields(traffic_shaping.TrafficShaping())) == 19


class TestSpecDrift:
    """Cross-reference dataclass fields against spec3.json response schemas."""

    SPEC_FIELDS = ['activeActiveAutoVpnEnabled', 'bandwidthLimits', 'custom', 'customPerformanceClassId', 'defaultRulesEnabled', 'defaultUplink', 'failoverAndFailback', 'globalBandwidthLimits', 'loadBalancingEnabled', 'majorApplications', 'maxJitter', 'maxLatency', 'maxLossPercentage', 'name', 'networkId', 'networkName', 'rules', 'vpnTrafficUplinkPreferences', 'wanTrafficUplinkPreferences']

    def test_dataclass_covers_spec(self):
        """Every spec response property should have a dataclass field."""
        dc_names = {f.name for f in dc_fields(traffic_shaping.TrafficShaping())}
        spec_set = set(self.SPEC_FIELDS)
        missing = spec_set - dc_names
        assert not missing, f'Spec fields missing from dataclass: {missing}'

    def test_dataclass_no_extra_fields(self):
        """Warn if the dataclass has fields not in the spec (may indicate stale fields)."""
        dc_names = {f.name for f in dc_fields(traffic_shaping.TrafficShaping())}
        spec_set = set(self.SPEC_FIELDS)
        extras = dc_names - spec_set
        assert not extras, (
            f'Dataclass has fields not in spec responses: {extras}. '
            f'These may be stale or from request-only schemas.'
        )

