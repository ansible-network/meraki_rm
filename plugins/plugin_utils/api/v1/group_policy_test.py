"""Colocated tests for APIGroupPolicy_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import group_policy as group_policy_api
from ...user_models import group_policy as group_policy_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = group_policy_api.APIGroupPolicy_v1(
            groupPolicyId='groupPolicyId_val',
            name='name_val',
            bandwidth={'enabled': True},
            bonjourForwarding={'enabled': True},
            contentFiltering={'enabled': True},
            firewallAndTrafficShaping={'enabled': True},
            scheduling={'enabled': True},
            splashAuthSettings='splashAuthSettings_val',
            vlanTagging={'enabled': True},
        )
        user = api.to_ansible(_ctx())

        assert user.group_policy_id == api.groupPolicyId
        assert user.name == api.name
        assert user.bandwidth == api.bandwidth
        assert user.bonjour_forwarding == api.bonjourForwarding
        assert user.content_filtering == api.contentFiltering
        assert user.firewall_and_traffic_shaping == api.firewallAndTrafficShaping
        assert user.scheduling == api.scheduling
        assert user.splash_auth_settings == api.splashAuthSettings
        assert user.vlan_tagging == api.vlanTagging


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = group_policy_user.UserGroupPolicy(
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
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.group_policy_id == original.group_policy_id
        assert roundtripped.name == original.name
        assert roundtripped.bandwidth == original.bandwidth
        assert roundtripped.bonjour_forwarding == original.bonjour_forwarding
        assert roundtripped.content_filtering == original.content_filtering
        assert roundtripped.firewall_and_traffic_shaping == original.firewall_and_traffic_shaping
        assert roundtripped.scheduling == original.scheduling
        assert roundtripped.splash_auth_settings == original.splash_auth_settings
        assert roundtripped.vlan_tagging == original.vlan_tagging


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = group_policy_api.APIGroupPolicy_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = group_policy_api.APIGroupPolicy_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

