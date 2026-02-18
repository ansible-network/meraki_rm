"""Colocated tests for APISwitchAccessPolicy_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import switch_access_policy as switch_access_policy_api
from ...user_models import switch_access_policy as switch_access_policy_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = switch_access_policy_api.APISwitchAccessPolicy_v1(
            accessPolicyNumber='accessPolicyNumber_val',
            name='name_val',
            accessPolicyType='accessPolicyType_val',
            hostMode='hostMode_val',
            radiusServers=[{'key': 'value'}],
            radiusAccountingServers=[{'key': 'value'}],
            radiusAccountingEnabled=True,
            radiusCoaSupportEnabled=True,
            guestVlanId=24,
            dot1x={'enabled': True},
            radiusGroupAttribute='radiusGroupAttribute_val',
            urlRedirectWalledGardenEnabled=True,
            urlRedirectWalledGardenRanges=['item1', 'item2'],
            voiceVlanClients=True,
        )
        user = api.to_ansible(_ctx())

        assert user.access_policy_number == api.accessPolicyNumber
        assert user.name == api.name
        assert user.access_policy_type == api.accessPolicyType
        assert user.host_mode == api.hostMode
        assert user.radius_servers == api.radiusServers
        assert user.radius_accounting_servers == api.radiusAccountingServers
        assert user.radius_accounting_enabled == api.radiusAccountingEnabled
        assert user.radius_coa_support_enabled == api.radiusCoaSupportEnabled
        assert user.guest_vlan_id == api.guestVlanId
        assert user.dot1x == api.dot1x
        assert user.radius_group_attribute == api.radiusGroupAttribute
        assert user.url_redirect_walled_garden_enabled == api.urlRedirectWalledGardenEnabled
        assert user.url_redirect_walled_garden_ranges == api.urlRedirectWalledGardenRanges
        assert user.voice_vlan_clients == api.voiceVlanClients


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = switch_access_policy_user.UserSwitchAccessPolicy(
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
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.access_policy_number == original.access_policy_number
        assert roundtripped.name == original.name
        assert roundtripped.access_policy_type == original.access_policy_type
        assert roundtripped.host_mode == original.host_mode
        assert roundtripped.radius_servers == original.radius_servers
        assert roundtripped.radius_accounting_servers == original.radius_accounting_servers
        assert roundtripped.radius_accounting_enabled == original.radius_accounting_enabled
        assert roundtripped.radius_coa_support_enabled == original.radius_coa_support_enabled
        assert roundtripped.guest_vlan_id == original.guest_vlan_id
        assert roundtripped.dot1x == original.dot1x
        assert roundtripped.radius_group_attribute == original.radius_group_attribute
        assert roundtripped.url_redirect_walled_garden_enabled == original.url_redirect_walled_garden_enabled
        assert roundtripped.url_redirect_walled_garden_ranges == original.url_redirect_walled_garden_ranges
        assert roundtripped.voice_vlan_clients == original.voice_vlan_clients


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = switch_access_policy_api.APISwitchAccessPolicy_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = switch_access_policy_api.APISwitchAccessPolicy_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

