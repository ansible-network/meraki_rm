"""Colocated tests for APISsid_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import ssid as ssid_api
from ...user_models import ssid as ssid_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = ssid_api.APISsid_v1(
            number=24,
            name='name_val',
            enabled=True,
            authMode='authMode_val',
            encryptionMode='encryptionMode_val',
            psk='psk_val',
            wpaEncryptionMode='wpaEncryptionMode_val',
            ipAssignmentMode='ipAssignmentMode_val',
            useVlanTagging=True,
            defaultVlanId=24,
            vlanId=24,
            splashPage='splashPage_val',
            bandSelection='bandSelection_val',
            minBitrate=24,
            perClientBandwidthLimitUp=24,
            perClientBandwidthLimitDown=24,
            perSsidBandwidthLimitUp=24,
            perSsidBandwidthLimitDown=24,
            visible=True,
            availableOnAllAps=True,
            availabilityTags=['item1', 'item2'],
        )
        user = api.to_ansible(_ctx())

        assert user.number == api.number
        assert user.name == api.name
        assert user.enabled == api.enabled
        assert user.auth_mode == api.authMode
        assert user.encryption_mode == api.encryptionMode
        assert user.psk == api.psk
        assert user.wpa_encryption_mode == api.wpaEncryptionMode
        assert user.ip_assignment_mode == api.ipAssignmentMode
        assert user.use_vlan_tagging == api.useVlanTagging
        assert user.default_vlan_id == api.defaultVlanId
        assert user.vlan_id == api.vlanId
        assert user.splash_page == api.splashPage
        assert user.band_selection == api.bandSelection
        assert user.min_bitrate == api.minBitrate
        assert user.per_client_bandwidth_limit_up == api.perClientBandwidthLimitUp
        assert user.per_client_bandwidth_limit_down == api.perClientBandwidthLimitDown
        assert user.per_ssid_bandwidth_limit_up == api.perSsidBandwidthLimitUp
        assert user.per_ssid_bandwidth_limit_down == api.perSsidBandwidthLimitDown
        assert user.visible == api.visible
        assert user.available_on_all_aps == api.availableOnAllAps
        assert user.availability_tags == api.availabilityTags


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = ssid_user.UserSsid(
            number=24,
            name='name_val',
            enabled=True,
            auth_mode='auth_mode_val',
            encryption_mode='encryption_mode_val',
            psk='psk_val',
            wpa_encryption_mode='wpa_encryption_mode_val',
            ip_assignment_mode='ip_assignment_mode_val',
            use_vlan_tagging=True,
            default_vlan_id=24,
            vlan_id=24,
            splash_page='splash_page_val',
            band_selection='band_selection_val',
            min_bitrate=1.5,
            per_client_bandwidth_limit_up=24,
            per_client_bandwidth_limit_down=24,
            per_ssid_bandwidth_limit_up=24,
            per_ssid_bandwidth_limit_down=24,
            visible=True,
            available_on_all_aps=True,
            availability_tags=['item1', 'item2'],
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.number == original.number
        assert roundtripped.name == original.name
        assert roundtripped.enabled == original.enabled
        assert roundtripped.auth_mode == original.auth_mode
        assert roundtripped.encryption_mode == original.encryption_mode
        assert roundtripped.psk == original.psk
        assert roundtripped.wpa_encryption_mode == original.wpa_encryption_mode
        assert roundtripped.ip_assignment_mode == original.ip_assignment_mode
        assert roundtripped.use_vlan_tagging == original.use_vlan_tagging
        assert roundtripped.default_vlan_id == original.default_vlan_id
        assert roundtripped.vlan_id == original.vlan_id
        assert roundtripped.splash_page == original.splash_page
        assert roundtripped.band_selection == original.band_selection
        assert roundtripped.min_bitrate == original.min_bitrate
        assert roundtripped.per_client_bandwidth_limit_up == original.per_client_bandwidth_limit_up
        assert roundtripped.per_client_bandwidth_limit_down == original.per_client_bandwidth_limit_down
        assert roundtripped.per_ssid_bandwidth_limit_up == original.per_ssid_bandwidth_limit_up
        assert roundtripped.per_ssid_bandwidth_limit_down == original.per_ssid_bandwidth_limit_down
        assert roundtripped.visible == original.visible
        assert roundtripped.available_on_all_aps == original.available_on_all_aps
        assert roundtripped.availability_tags == original.availability_tags


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = ssid_api.APISsid_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = ssid_api.APISsid_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

