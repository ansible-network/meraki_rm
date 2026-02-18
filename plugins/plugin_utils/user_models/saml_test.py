"""Colocated tests for UserSaml — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import saml


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserSaml can be constructed with all fields."""

    def test_defaults(self):
        obj = saml.UserSaml()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserSaml -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = saml.UserSaml(
            enabled=True,
            consumer_url='consumer_url_val',
            slo_logout_url='slo_logout_url_val',
            sso_login_url='sso_login_url_val',
            x509cert_sha1_fingerprint='x509cert_sha1_fingerprint_val',
            vision_consumer_url='vision_consumer_url_val',
            sp_initiated={'enabled': True},
        )
        api = user.to_api(_ctx())

        assert api.enabled == user.enabled
        assert api.consumerUrl == user.consumer_url
        assert api.sloLogoutUrl == user.slo_logout_url
        assert api.ssoLoginUrl == user.sso_login_url
        assert api.x509certSha1Fingerprint == user.x509cert_sha1_fingerprint
        assert api.visionConsumerUrl == user.vision_consumer_url
        assert api.spInitiated == user.sp_initiated

    def test_none_fields_omitted(self):
        user = saml.UserSaml(enabled=True)
        api = user.to_api(_ctx())
        assert api.enabled == user.enabled
        assert getattr(api, 'consumerUrl', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = saml.UserSaml(organization_id='organization_id_val', enabled=True)
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'organization_id' not in api_field_names or getattr(api, 'organization_id', None) is None

