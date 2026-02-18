"""Colocated tests for UserEthernetPortProfile — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import ethernet_port_profile


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserEthernetPortProfile can be constructed with all fields."""

    def test_defaults(self):
        obj = ethernet_port_profile.UserEthernetPortProfile()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserEthernetPortProfile -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = ethernet_port_profile.UserEthernetPortProfile(
            profile_id='profile_id_val',
            name='name_val',
            ports=[{'key': 'value'}],
            usb_ports=[{'key': 'value'}],
            is_default=True,
            serials=['item1', 'item2'],
        )
        api = user.to_api(_ctx())

        assert api.profileId == user.profile_id
        assert api.name == user.name
        assert api.ports == user.ports
        assert api.usbPorts == user.usb_ports
        assert api.isDefault == user.is_default
        assert api.serials == user.serials

    def test_none_fields_omitted(self):
        user = ethernet_port_profile.UserEthernetPortProfile(profile_id='profile_id_val')
        api = user.to_api(_ctx())
        assert api.profileId == user.profile_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = ethernet_port_profile.UserEthernetPortProfile(network_id='network_id_val', profile_id='profile_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

