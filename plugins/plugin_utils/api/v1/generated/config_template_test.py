"""Drift-detection tests for generated ConfigTemplate dataclass."""

from dataclasses import fields as dc_fields, is_dataclass
from . import config_template


class TestSchema:
    """ConfigTemplate field inventory — catches regeneration drift."""

    def test_is_dataclass(self):
        assert is_dataclass(config_template.ConfigTemplate)

    def test_expected_fields_exist(self):
        field_names = {f.name for f in dc_fields(config_template.ConfigTemplate())}
        expected = {'enabled', 'switchProfileId', 'stpGuard', 'timeZone', 'mirror', 'profile', 'stormControlEnabled', 'stpPortFastTrunk', 'linkNegotiationCapabilities', 'highSpeed', 'id', 'name', 'portId', 'flexibleStackingEnabled', 'rstpEnabled', 'isolationEnabled', 'voiceVlan', 'portScheduleId', 'vlan', 'allowedVlans', 'model', 'accessPolicyType', 'schedule', 'tags', 'udld', 'dot3az', 'copyFromNetworkId', 'macWhitelistLimit', 'macAllowList', 'accessPolicyNumber', 'module', 'type', 'daiTrusted', 'productTypes', 'poeEnabled', 'linkNegotiation', 'stickyMacAllowList', 'stickyMacAllowListLimit'}
        assert expected.issubset(field_names), f'Missing fields: {expected - field_names}'

    def test_all_fields_optional(self):
        """Every generated field should default to None (all Optional)."""
        obj = config_template.ConfigTemplate()
        for f in dc_fields(obj):
            assert getattr(obj, f.name) is None, f'{f.name} is not None by default'

    def test_field_count(self):
        """Guard against silent field additions or removals."""
        assert len(dc_fields(config_template.ConfigTemplate())) == 38


class TestSpecDrift:
    """Cross-reference dataclass fields against spec3.json response schemas."""

    SPEC_FIELDS = ['accessPolicyNumber', 'accessPolicyType', 'allowedVlans', 'copyFromNetworkId', 'daiTrusted', 'dot3az', 'enabled', 'flexibleStackingEnabled', 'highSpeed', 'id', 'isolationEnabled', 'linkNegotiation', 'linkNegotiationCapabilities', 'macAllowList', 'macWhitelistLimit', 'mirror', 'model', 'module', 'name', 'poeEnabled', 'portId', 'portScheduleId', 'productTypes', 'profile', 'rstpEnabled', 'schedule', 'stickyMacAllowList', 'stickyMacAllowListLimit', 'stormControlEnabled', 'stpGuard', 'stpPortFastTrunk', 'switchProfileId', 'tags', 'timeZone', 'type', 'udld', 'vlan', 'voiceVlan']

    def test_dataclass_covers_spec(self):
        """Every spec response property should have a dataclass field."""
        dc_names = {f.name for f in dc_fields(config_template.ConfigTemplate())}
        spec_set = set(self.SPEC_FIELDS)
        missing = spec_set - dc_names
        assert not missing, f'Spec fields missing from dataclass: {missing}'

    def test_dataclass_no_extra_fields(self):
        """Warn if the dataclass has fields not in the spec (may indicate stale fields)."""
        dc_names = {f.name for f in dc_fields(config_template.ConfigTemplate())}
        spec_set = set(self.SPEC_FIELDS)
        extras = dc_names - spec_set
        assert not extras, (
            f'Dataclass has fields not in spec responses: {extras}. '
            f'These may be stale or from request-only schemas.'
        )

