"""Colocated tests for UserSwitchStack — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import switch_stack


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserSwitchStack can be constructed with all fields."""

    def test_defaults(self):
        obj = switch_stack.UserSwitchStack()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserSwitchStack -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = switch_stack.UserSwitchStack(
            switch_stack_id='switch_stack_id_val',
            name='name_val',
            serials=['item1', 'item2'],
            members=[{'key': 'value'}],
            is_monitor_only=True,
            virtual_mac='virtual_mac_val',
        )
        api = user.to_api(_ctx())

        assert api.id == user.switch_stack_id
        assert api.name == user.name
        assert api.serials == user.serials
        assert api.members == user.members
        assert api.isMonitorOnly == user.is_monitor_only
        assert api.virtualMac == user.virtual_mac

    def test_none_fields_omitted(self):
        user = switch_stack.UserSwitchStack(switch_stack_id='switch_stack_id_val')
        api = user.to_api(_ctx())
        assert api.id == user.switch_stack_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = switch_stack.UserSwitchStack(network_id='network_id_val', switch_stack_id='switch_stack_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

