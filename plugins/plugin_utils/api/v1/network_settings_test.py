"""Colocated tests for APINetworkSettings_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import network_settings as network_settings_api
from ...user_models import network_settings as network_settings_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = network_settings_api.APINetworkSettings_v1(
            localStatusPageEnabled=True,
            remoteStatusPageEnabled=True,
            localStatusPage={'enabled': True},
            fips={'enabled': True},
            namedVlans={'enabled': True},
            securePort={'enabled': True},
            reportingEnabled=True,
            mode='mode_val',
            customPieChartItems=[{'key': 'value'}],
        )
        user = api.to_ansible(_ctx())

        assert user.local_status_page_enabled == api.localStatusPageEnabled
        assert user.remote_status_page_enabled == api.remoteStatusPageEnabled
        assert user.local_status_page == api.localStatusPage
        assert user.fips == api.fips
        assert user.named_vlans == api.namedVlans
        assert user.secure_port == api.securePort
        assert user.reporting_enabled == api.reportingEnabled
        assert user.mode == api.mode
        assert user.custom_pie_chart_items == api.customPieChartItems


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = network_settings_user.UserNetworkSettings(
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
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.local_status_page_enabled == original.local_status_page_enabled
        assert roundtripped.remote_status_page_enabled == original.remote_status_page_enabled
        assert roundtripped.local_status_page == original.local_status_page
        assert roundtripped.fips == original.fips
        assert roundtripped.named_vlans == original.named_vlans
        assert roundtripped.secure_port == original.secure_port
        assert roundtripped.reporting_enabled == original.reporting_enabled
        assert roundtripped.mode == original.mode
        assert roundtripped.custom_pie_chart_items == original.custom_pie_chart_items


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = network_settings_api.APINetworkSettings_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = network_settings_api.APINetworkSettings_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

