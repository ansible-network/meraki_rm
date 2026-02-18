"""Colocated tests for APIEthernetPortProfile_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import ethernet_port_profile as ethernet_port_profile_api
from ...user_models import ethernet_port_profile as ethernet_port_profile_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = ethernet_port_profile_api.APIEthernetPortProfile_v1(
            profileId='profileId_val',
            name='name_val',
            ports=[{'key': 'value'}],
            usbPorts=[{'key': 'value'}],
            isDefault=True,
            serials=['item1', 'item2'],
        )
        user = api.to_ansible(_ctx())

        assert user.profile_id == api.profileId
        assert user.name == api.name
        assert user.ports == api.ports
        assert user.usb_ports == api.usbPorts
        assert user.is_default == api.isDefault
        assert user.serials == api.serials


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = ethernet_port_profile_user.UserEthernetPortProfile(
            profile_id='profile_id_val',
            name='name_val',
            ports=[{'key': 'value'}],
            usb_ports=[{'key': 'value'}],
            is_default=True,
            serials=['item1', 'item2'],
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.profile_id == original.profile_id
        assert roundtripped.name == original.name
        assert roundtripped.ports == original.ports
        assert roundtripped.usb_ports == original.usb_ports
        assert roundtripped.is_default == original.is_default
        assert roundtripped.serials == original.serials


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = ethernet_port_profile_api.APIEthernetPortProfile_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = ethernet_port_profile_api.APIEthernetPortProfile_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

