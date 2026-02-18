"""Colocated tests for UserSwitchPort — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import switch_port


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserSwitchPort can be constructed with all fields."""

    def test_defaults(self):
        obj = switch_port.UserSwitchPort()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserSwitchPort -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = switch_port.UserSwitchPort(
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
        api = user.to_api(_ctx())

        assert api.portId == user.port_id
        assert api.name == user.name
        assert api.tags == user.tags
        assert api.enabled == user.enabled
        assert api.type == user.type
        assert api.vlan == user.vlan
        assert api.voiceVlan == user.voice_vlan
        assert api.allowedVlans == user.allowed_vlans
        assert api.poeEnabled == user.poe_enabled
        assert api.isolationEnabled == user.isolation_enabled
        assert api.rstpEnabled == user.rstp_enabled
        assert api.stpGuard == user.stp_guard
        assert api.linkNegotiation == user.link_negotiation
        assert api.portScheduleId == user.port_schedule_id
        assert api.udld == user.udld
        assert api.accessPolicyType == user.access_policy_type
        assert api.accessPolicyNumber == user.access_policy_number
        assert api.stickyMacAllowList == user.sticky_mac_allow_list
        assert api.stickyMacAllowListLimit == user.sticky_mac_allow_list_limit
        assert api.stormControlEnabled == user.storm_control_enabled
        assert api.adaptivePolicyGroupId == user.adaptive_policy_group_id
        assert api.peerSgtCapable == user.peer_sgt_capable
        assert api.flexibleStackingEnabled == user.flexible_stacking_enabled
        assert api.daiTrusted == user.dai_trusted
        assert api.profile == user.profile

    def test_none_fields_omitted(self):
        user = switch_port.UserSwitchPort(port_id='port_id_val')
        api = user.to_api(_ctx())
        assert api.portId == user.port_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = switch_port.UserSwitchPort(serial='serial_val', port_id='port_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'serial' not in api_field_names or getattr(api, 'serial', None) is None

