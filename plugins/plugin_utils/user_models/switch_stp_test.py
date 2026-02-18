"""Colocated tests for UserSwitchStp — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import switch_stp


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserSwitchStp can be constructed with all fields."""

    def test_defaults(self):
        obj = switch_stp.UserSwitchStp()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserSwitchStp -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = switch_stp.UserSwitchStp(
            rstp_enabled=True,
            stp_bridge_priority=[{'key': 'value'}],
        )
        api = user.to_api(_ctx())

        assert api.rstpEnabled == user.rstp_enabled
        assert api.stpBridgePriority == user.stp_bridge_priority

    def test_none_fields_omitted(self):
        user = switch_stp.UserSwitchStp(rstp_enabled=True)
        api = user.to_api(_ctx())
        assert api.rstpEnabled == user.rstp_enabled
        assert getattr(api, 'stpBridgePriority', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = switch_stp.UserSwitchStp(network_id='network_id_val', rstp_enabled=True)
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

