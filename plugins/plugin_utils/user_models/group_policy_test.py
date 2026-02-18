"""Colocated tests for UserGroupPolicy — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import group_policy


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserGroupPolicy can be constructed with all fields."""

    def test_defaults(self):
        obj = group_policy.UserGroupPolicy()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserGroupPolicy -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = group_policy.UserGroupPolicy(
            group_policy_id='group_policy_id_val',
            name='name_val',
            bandwidth={'enabled': True},
            bonjour_forwarding={'enabled': True},
            content_filtering={'enabled': True},
            firewall_and_traffic_shaping={'enabled': True},
            scheduling={'enabled': True},
            splash_auth_settings='splash_auth_settings_val',
            vlan_tagging={'enabled': True},
        )
        api = user.to_api(_ctx())

        assert api.groupPolicyId == user.group_policy_id
        assert api.name == user.name
        assert api.bandwidth == user.bandwidth
        assert api.bonjourForwarding == user.bonjour_forwarding
        assert api.contentFiltering == user.content_filtering
        assert api.firewallAndTrafficShaping == user.firewall_and_traffic_shaping
        assert api.scheduling == user.scheduling
        assert api.splashAuthSettings == user.splash_auth_settings
        assert api.vlanTagging == user.vlan_tagging

    def test_none_fields_omitted(self):
        user = group_policy.UserGroupPolicy(group_policy_id='group_policy_id_val')
        api = user.to_api(_ctx())
        assert api.groupPolicyId == user.group_policy_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = group_policy.UserGroupPolicy(network_id='network_id_val', group_policy_id='group_policy_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

