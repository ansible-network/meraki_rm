"""Colocated tests for UserFirewall — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import firewall


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserFirewall can be constructed with all fields."""

    def test_defaults(self):
        obj = firewall.UserFirewall()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserFirewall -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = firewall.UserFirewall(
            rules=[{'key': 'value'}],
            syslog_default_rule=True,
            spoofing_protection={'enabled': True},
            application_categories=[{'key': 'value'}],
            access='access_val',
            allowed_ips=['item1', 'item2'],
            service='service_val',
        )
        api = user.to_api(_ctx())

        assert api.rules == user.rules
        assert api.syslogDefaultRule == user.syslog_default_rule
        assert api.spoofingProtection == user.spoofing_protection
        assert api.applicationCategories == user.application_categories
        assert api.access == user.access
        assert api.allowedIps == user.allowed_ips
        assert api.service == user.service

    def test_none_fields_omitted(self):
        user = firewall.UserFirewall(rules=[{'key': 'value'}])
        api = user.to_api(_ctx())
        assert api.rules == user.rules
        assert getattr(api, 'syslogDefaultRule', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = firewall.UserFirewall(network_id='network_id_val', rules=[{'key': 'value'}])
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

