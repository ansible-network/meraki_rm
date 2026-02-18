"""Colocated tests for UserSwitchLinkAggregation — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import switch_link_aggregation


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserSwitchLinkAggregation can be constructed with all fields."""

    def test_defaults(self):
        obj = switch_link_aggregation.UserSwitchLinkAggregation()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserSwitchLinkAggregation -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = switch_link_aggregation.UserSwitchLinkAggregation(
            link_aggregation_id='link_aggregation_id_val',
            switch_ports=[{'key': 'value'}],
            switch_profile_ports=[{'key': 'value'}],
        )
        api = user.to_api(_ctx())

        assert api.id == user.link_aggregation_id
        assert api.switchPorts == user.switch_ports
        assert api.switchProfilePorts == user.switch_profile_ports

    def test_none_fields_omitted(self):
        user = switch_link_aggregation.UserSwitchLinkAggregation(link_aggregation_id='link_aggregation_id_val')
        api = user.to_api(_ctx())
        assert api.id == user.link_aggregation_id
        assert getattr(api, 'switchPorts', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = switch_link_aggregation.UserSwitchLinkAggregation(network_id='network_id_val', link_aggregation_id='link_aggregation_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

