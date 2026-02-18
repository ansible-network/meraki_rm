"""Colocated tests for APISwitchPort_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import switch_port as switch_port_api
from ...user_models import switch_port as switch_port_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = switch_port_api.APISwitchPort_v1(
            portId='portId_val',
            name='name_val',
            tags=['item1', 'item2'],
            enabled=True,
            type='type_val',
            vlan=24,
            voiceVlan=24,
            allowedVlans='allowedVlans_val',
            poeEnabled=True,
            isolationEnabled=True,
            rstpEnabled=True,
            stpGuard='stpGuard_val',
            linkNegotiation='linkNegotiation_val',
            portScheduleId='portScheduleId_val',
            udld='udld_val',
            accessPolicyType='accessPolicyType_val',
            accessPolicyNumber=24,
            stickyMacAllowList=['item1', 'item2'],
            stickyMacAllowListLimit=24,
            stormControlEnabled=True,
            adaptivePolicyGroupId='adaptivePolicyGroupId_val',
            peerSgtCapable=True,
            flexibleStackingEnabled=True,
            daiTrusted=True,
            profile={'enabled': True},
        )
        user = api.to_ansible(_ctx())

        assert user.port_id == api.portId
        assert user.name == api.name
        assert user.tags == api.tags
        assert user.enabled == api.enabled
        assert user.type == api.type
        assert user.vlan == api.vlan
        assert user.voice_vlan == api.voiceVlan
        assert user.allowed_vlans == api.allowedVlans
        assert user.poe_enabled == api.poeEnabled
        assert user.isolation_enabled == api.isolationEnabled
        assert user.rstp_enabled == api.rstpEnabled
        assert user.stp_guard == api.stpGuard
        assert user.link_negotiation == api.linkNegotiation
        assert user.port_schedule_id == api.portScheduleId
        assert user.udld == api.udld
        assert user.access_policy_type == api.accessPolicyType
        assert user.access_policy_number == api.accessPolicyNumber
        assert user.sticky_mac_allow_list == api.stickyMacAllowList
        assert user.sticky_mac_allow_list_limit == api.stickyMacAllowListLimit
        assert user.storm_control_enabled == api.stormControlEnabled
        assert user.adaptive_policy_group_id == api.adaptivePolicyGroupId
        assert user.peer_sgt_capable == api.peerSgtCapable
        assert user.flexible_stacking_enabled == api.flexibleStackingEnabled
        assert user.dai_trusted == api.daiTrusted
        assert user.profile == api.profile


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = switch_port_user.UserSwitchPort(
            port_id='port_id_val',
            name='name_val',
            tags=['item1', 'item2'],
            enabled=True,
            type='type_val',
            vlan=24,
            voice_vlan=24,
            allowed_vlans='allowed_vlans_val',
            poe_enabled=True,
            isolation_enabled=True,
            rstp_enabled=True,
            stp_guard='stp_guard_val',
            link_negotiation='link_negotiation_val',
            port_schedule_id='port_schedule_id_val',
            udld='udld_val',
            access_policy_type='access_policy_type_val',
            access_policy_number=24,
            sticky_mac_allow_list=['item1', 'item2'],
            sticky_mac_allow_list_limit=24,
            storm_control_enabled=True,
            adaptive_policy_group_id='adaptive_policy_group_id_val',
            peer_sgt_capable=True,
            flexible_stacking_enabled=True,
            dai_trusted=True,
            profile={'enabled': True},
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.port_id == original.port_id
        assert roundtripped.name == original.name
        assert roundtripped.tags == original.tags
        assert roundtripped.enabled == original.enabled
        assert roundtripped.type == original.type
        assert roundtripped.vlan == original.vlan
        assert roundtripped.voice_vlan == original.voice_vlan
        assert roundtripped.allowed_vlans == original.allowed_vlans
        assert roundtripped.poe_enabled == original.poe_enabled
        assert roundtripped.isolation_enabled == original.isolation_enabled
        assert roundtripped.rstp_enabled == original.rstp_enabled
        assert roundtripped.stp_guard == original.stp_guard
        assert roundtripped.link_negotiation == original.link_negotiation
        assert roundtripped.port_schedule_id == original.port_schedule_id
        assert roundtripped.udld == original.udld
        assert roundtripped.access_policy_type == original.access_policy_type
        assert roundtripped.access_policy_number == original.access_policy_number
        assert roundtripped.sticky_mac_allow_list == original.sticky_mac_allow_list
        assert roundtripped.sticky_mac_allow_list_limit == original.sticky_mac_allow_list_limit
        assert roundtripped.storm_control_enabled == original.storm_control_enabled
        assert roundtripped.adaptive_policy_group_id == original.adaptive_policy_group_id
        assert roundtripped.peer_sgt_capable == original.peer_sgt_capable
        assert roundtripped.flexible_stacking_enabled == original.flexible_stacking_enabled
        assert roundtripped.dai_trusted == original.dai_trusted
        assert roundtripped.profile == original.profile


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = switch_port_api.APISwitchPort_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = switch_port_api.APISwitchPort_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

