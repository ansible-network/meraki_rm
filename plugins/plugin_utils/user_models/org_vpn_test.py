"""Colocated tests for UserOrgVpn — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import org_vpn


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserOrgVpn can be constructed with all fields."""

    def test_defaults(self):
        obj = org_vpn.UserOrgVpn()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserOrgVpn -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = org_vpn.UserOrgVpn(
            peers=[{'key': 'value'}],
            third_party_vpn_peers=[{'key': 'value'}],
        )
        api = user.to_api(_ctx())

        assert api.peers == user.peers
        assert api.thirdPartyVpnPeers == user.third_party_vpn_peers

    def test_none_fields_omitted(self):
        user = org_vpn.UserOrgVpn(peers=[{'key': 'value'}])
        api = user.to_api(_ctx())
        assert api.peers == user.peers
        assert getattr(api, 'thirdPartyVpnPeers', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = org_vpn.UserOrgVpn(organization_id='organization_id_val', peers=[{'key': 'value'}])
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'organization_id' not in api_field_names or getattr(api, 'organization_id', None) is None

