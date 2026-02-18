"""Colocated tests for APISaml_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import saml as saml_api
from ...user_models import saml as saml_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = saml_api.APISaml_v1(
            enabled=True,
            consumerUrl='consumerUrl_val',
            sloLogoutUrl='sloLogoutUrl_val',
            ssoLoginUrl='ssoLoginUrl_val',
            x509certSha1Fingerprint='x509certSha1Fingerprint_val',
            visionConsumerUrl='visionConsumerUrl_val',
            spInitiated={'enabled': True},
        )
        user = api.to_ansible(_ctx())

        assert user.enabled == api.enabled
        assert user.consumer_url == api.consumerUrl
        assert user.slo_logout_url == api.sloLogoutUrl
        assert user.sso_login_url == api.ssoLoginUrl
        assert user.x509cert_sha1_fingerprint == api.x509certSha1Fingerprint
        assert user.vision_consumer_url == api.visionConsumerUrl
        assert user.sp_initiated == api.spInitiated


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = saml_user.UserSaml(
            enabled=True,
            consumer_url='consumer_url_val',
            slo_logout_url='slo_logout_url_val',
            sso_login_url='sso_login_url_val',
            x509cert_sha1_fingerprint='x509cert_sha1_fingerprint_val',
            vision_consumer_url='vision_consumer_url_val',
            sp_initiated={'enabled': True},
        )
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.enabled == original.enabled
        assert roundtripped.consumer_url == original.consumer_url
        assert roundtripped.slo_logout_url == original.slo_logout_url
        assert roundtripped.sso_login_url == original.sso_login_url
        assert roundtripped.x509cert_sha1_fingerprint == original.x509cert_sha1_fingerprint
        assert roundtripped.vision_consumer_url == original.vision_consumer_url
        assert roundtripped.sp_initiated == original.sp_initiated


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = saml_api.APISaml_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = saml_api.APISaml_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

