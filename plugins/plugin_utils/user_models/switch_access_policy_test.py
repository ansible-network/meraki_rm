"""Colocated tests for UserSwitchAccessPolicy — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import switch_access_policy


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserSwitchAccessPolicy can be constructed with all fields."""

    def test_defaults(self):
        obj = switch_access_policy.UserSwitchAccessPolicy()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserSwitchAccessPolicy -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = switch_access_policy.UserSwitchAccessPolicy(
            access_policy_number='access_policy_number_val',
            name='name_val',
            access_policy_type='access_policy_type_val',
            host_mode='host_mode_val',
            radius_servers=[{'key': 'value'}],
            radius_accounting_servers=[{'key': 'value'}],
            radius_accounting_enabled=True,
            radius_coa_support_enabled=True,
            guest_vlan_id=24,
            dot1x={'enabled': True},
            radius_group_attribute='radius_group_attribute_val',
            url_redirect_walled_garden_enabled=True,
            url_redirect_walled_garden_ranges=['item1', 'item2'],
            voice_vlan_clients=True,
        )
        api = user.to_api(_ctx())

        assert api.accessPolicyNumber == user.access_policy_number
        assert api.name == user.name
        assert api.accessPolicyType == user.access_policy_type
        assert api.hostMode == user.host_mode
        assert api.radiusServers == user.radius_servers
        assert api.radiusAccountingServers == user.radius_accounting_servers
        assert api.radiusAccountingEnabled == user.radius_accounting_enabled
        assert api.radiusCoaSupportEnabled == user.radius_coa_support_enabled
        assert api.guestVlanId == user.guest_vlan_id
        assert api.dot1x == user.dot1x
        assert api.radiusGroupAttribute == user.radius_group_attribute
        assert api.urlRedirectWalledGardenEnabled == user.url_redirect_walled_garden_enabled
        assert api.urlRedirectWalledGardenRanges == user.url_redirect_walled_garden_ranges
        assert api.voiceVlanClients == user.voice_vlan_clients

    def test_none_fields_omitted(self):
        user = switch_access_policy.UserSwitchAccessPolicy(access_policy_number='access_policy_number_val')
        api = user.to_api(_ctx())
        assert api.accessPolicyNumber == user.access_policy_number
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = switch_access_policy.UserSwitchAccessPolicy(network_id='network_id_val', access_policy_number='access_policy_number_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

