"""Colocated tests for UserNetworkSettings — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import network_settings


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserNetworkSettings can be constructed with all fields."""

    def test_defaults(self):
        obj = network_settings.UserNetworkSettings()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserNetworkSettings -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = network_settings.UserNetworkSettings(
            local_status_page_enabled=True,
            remote_status_page_enabled=True,
            local_status_page={'enabled': True},
            fips={'enabled': True},
            named_vlans={'enabled': True},
            secure_port={'enabled': True},
            reporting_enabled=True,
            mode='mode_val',
            custom_pie_chart_items=[{'key': 'value'}],
        )
        api = user.to_api(_ctx())

        assert api.localStatusPageEnabled == user.local_status_page_enabled
        assert api.remoteStatusPageEnabled == user.remote_status_page_enabled
        assert api.localStatusPage == user.local_status_page
        assert api.fips == user.fips
        assert api.namedVlans == user.named_vlans
        assert api.securePort == user.secure_port
        assert api.reportingEnabled == user.reporting_enabled
        assert api.mode == user.mode
        assert api.customPieChartItems == user.custom_pie_chart_items

    def test_none_fields_omitted(self):
        user = network_settings.UserNetworkSettings(local_status_page_enabled=True)
        api = user.to_api(_ctx())
        assert api.localStatusPageEnabled == user.local_status_page_enabled
        assert getattr(api, 'remoteStatusPageEnabled', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = network_settings.UserNetworkSettings(network_id='network_id_val', local_status_page_enabled=True)
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

