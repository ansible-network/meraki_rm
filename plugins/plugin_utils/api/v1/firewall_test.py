"""Colocated tests for APIFirewall_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import firewall as firewall_api
from ...user_models import firewall as firewall_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = firewall_api.APIFirewall_v1(
            rules=[{'key': 'value'}],
            syslogDefaultRule=True,
            spoofingProtection={'enabled': True},
            applicationCategories=[{'key': 'value'}],
            access='access_val',
            allowedIps=['item1', 'item2'],
            service='service_val',
        )
        user = api.to_ansible(_ctx())

        assert user.rules == api.rules
        assert user.syslog_default_rule == api.syslogDefaultRule
        assert user.spoofing_protection == api.spoofingProtection
        assert user.application_categories == api.applicationCategories
        assert user.access == api.access
        assert user.allowed_ips == api.allowedIps
        assert user.service == api.service


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = firewall_user.UserFirewall(
            rules=[{'key': 'value'}],
            syslog_default_rule=True,
            spoofing_protection={'enabled': True},
            application_categories=[{'key': 'value'}],
            access='access_val',
            allowed_ips=['item1', 'item2'],
            service='service_val',
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.rules == original.rules
        assert roundtripped.syslog_default_rule == original.syslog_default_rule
        assert roundtripped.spoofing_protection == original.spoofing_protection
        assert roundtripped.application_categories == original.application_categories
        assert roundtripped.access == original.access
        assert roundtripped.allowed_ips == original.allowed_ips
        assert roundtripped.service == original.service


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = firewall_api.APIFirewall_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = firewall_api.APIFirewall_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

