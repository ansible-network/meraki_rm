"""Drift-detection tests for generated Ssid dataclass."""

from dataclasses import fields as dc_fields, is_dataclass
from . import ssid


class TestSchema:
    """Ssid field inventory — catches regeneration drift."""

    def test_is_dataclass(self):
        assert is_dataclass(ssid.Ssid)

    def test_expected_fields_exist(self):
        field_names = {f.name for f in dc_fields(ssid.Ssid())}
        expected = {'groupPolicyId', 'expiresAt', 'deviceTypePolicies', 'perClientBandwidthLimitDown', 'venue', 'enterpriseAdminAccess', 'rules', 'radiusRadsec', 'id', 'radiusFallbackEnabled', 'dnsRewrite', 'ldap', 'radiusGuestVlanEnabled', 'failover', 'namedVlans', 'billing', 'radiusAuthenticationNasId', 'welcomeMessage', 'splashTimeout', 'vlanId', 'allowLanAccess', 'radiusAccountingStartDelay', 'gre', 'naiRealms', 'identity', 'secondaryConcentratorNetworkId', 'radiusProxyEnabled', 'adminSplashUrl', 'dot11w', 'wifiPersonalNetworkId', 'activeDirectory', 'enabled', 'concentrator', 'mccMncs', 'controllerDisconnectionBehavior', 'networkAccessType', 'localRadius', 'perSsidBandwidthLimitUp', 'roamConsortOis', 'splashUrl', 'splitTunnel', 'trafficShapingEnabled', 'dot11r', 'radiusAttributeForGroupPolicies', 'splashLogo', 'radiusAccountingEnabled', 'walledGardenRanges', 'radiusServerAttemptsLimit', 'number', 'availableOnAllAps', 'rangesInSeconds', 'splashPage', 'defaultRulesEnabled', 'visible', 'encryptionMode', 'splashPrepaidFront', 'radiusEnabled', 'bandSelection', 'adultContentFilteringEnabled', 'ipAssignmentMode', 'radiusAccountingServers', 'guestSponsorship', 'apTagsAndVlanIds', 'speedBurst', 'authMode', 'email', 'radiusCoaEnabled', 'radiusFailoverPolicy', 'splashGuestSponsorDomains', 'name', 'eapolKey', 'radiusGuestVlanId', 'timeout', 'passphrase', 'radiusServers', 'radiusLoadBalancingPolicy', 'wpaEncryptionMode', 'ssidNumber', 'tenantId', 'psk', 'useSplashUrl', 'useRedirectUrl', 'ranges', 'perSsidBandwidthLimitDown', 'availabilityTags', 'disassociateClientsOnVpnFailover', 'domains', 'sentryEnrollment', 'splashImage', 'themeId', 'minBitrate', 'blockAllTrafficBeforeSignOn', 'exception', 'walledGardenEnabled', 'adaptivePolicyGroupId', 'radiusServerTimeout', 'useVlanTagging', 'localAuthFallback', 'lanIsolationEnabled', 'defaultVlanId', 'operator', 'ssidAdminAccessible', 'redirectUrl', 'radiusAccountingInterimInterval', 'localAuth', 'radiusOverride', 'selfRegistration', 'concentratorNetworkId', 'oauth', 'perClientBandwidthLimitUp', 'allowSimultaneousLogins', 'maxRetries', 'mandatoryDhcpEnabled', 'radiusCalledStationId', 'radiusTestingEnabled'}
        assert expected.issubset(field_names), f'Missing fields: {expected - field_names}'

    def test_all_fields_optional(self):
        """Every generated field should default to None (all Optional)."""
        obj = ssid.Ssid()
        for f in dc_fields(obj):
            assert getattr(obj, f.name) is None, f'{f.name} is not None by default'

    def test_field_count(self):
        """Guard against silent field additions or removals."""
        assert len(dc_fields(ssid.Ssid())) == 115


class TestSpecDrift:
    """Cross-reference dataclass fields against spec3.json response schemas."""

    SPEC_FIELDS = ['activeDirectory', 'adaptivePolicyGroupId', 'adminSplashUrl', 'adultContentFilteringEnabled', 'allowLanAccess', 'allowSimultaneousLogins', 'apTagsAndVlanIds', 'authMode', 'availabilityTags', 'availableOnAllAps', 'bandSelection', 'billing', 'blockAllTrafficBeforeSignOn', 'concentrator', 'concentratorNetworkId', 'controllerDisconnectionBehavior', 'defaultRulesEnabled', 'defaultVlanId', 'deviceTypePolicies', 'disassociateClientsOnVpnFailover', 'dnsRewrite', 'domains', 'dot11r', 'dot11w', 'eapolKey', 'email', 'enabled', 'encryptionMode', 'enterpriseAdminAccess', 'exception', 'expiresAt', 'failover', 'gre', 'groupPolicyId', 'guestSponsorship', 'id', 'identity', 'ipAssignmentMode', 'lanIsolationEnabled', 'ldap', 'localAuth', 'localAuthFallback', 'localRadius', 'mandatoryDhcpEnabled', 'maxRetries', 'mccMncs', 'minBitrate', 'naiRealms', 'name', 'namedVlans', 'networkAccessType', 'number', 'oauth', 'operator', 'passphrase', 'perClientBandwidthLimitDown', 'perClientBandwidthLimitUp', 'perSsidBandwidthLimitDown', 'perSsidBandwidthLimitUp', 'psk', 'radiusAccountingEnabled', 'radiusAccountingInterimInterval', 'radiusAccountingServers', 'radiusAccountingStartDelay', 'radiusAttributeForGroupPolicies', 'radiusAuthenticationNasId', 'radiusCalledStationId', 'radiusCoaEnabled', 'radiusEnabled', 'radiusFailoverPolicy', 'radiusFallbackEnabled', 'radiusGuestVlanEnabled', 'radiusGuestVlanId', 'radiusLoadBalancingPolicy', 'radiusOverride', 'radiusProxyEnabled', 'radiusRadsec', 'radiusServerAttemptsLimit', 'radiusServerTimeout', 'radiusServers', 'radiusTestingEnabled', 'ranges', 'rangesInSeconds', 'redirectUrl', 'roamConsortOis', 'rules', 'secondaryConcentratorNetworkId', 'selfRegistration', 'sentryEnrollment', 'speedBurst', 'splashGuestSponsorDomains', 'splashImage', 'splashLogo', 'splashPage', 'splashPrepaidFront', 'splashTimeout', 'splashUrl', 'splitTunnel', 'ssidAdminAccessible', 'ssidNumber', 'tenantId', 'themeId', 'timeout', 'trafficShapingEnabled', 'useRedirectUrl', 'useSplashUrl', 'useVlanTagging', 'venue', 'visible', 'vlanId', 'walledGardenEnabled', 'walledGardenRanges', 'welcomeMessage', 'wifiPersonalNetworkId', 'wpaEncryptionMode']

    def test_dataclass_covers_spec(self):
        """Every spec response property should have a dataclass field."""
        dc_names = {f.name for f in dc_fields(ssid.Ssid())}
        spec_set = set(self.SPEC_FIELDS)
        missing = spec_set - dc_names
        assert not missing, f'Spec fields missing from dataclass: {missing}'

    def test_dataclass_no_extra_fields(self):
        """Warn if the dataclass has fields not in the spec (may indicate stale fields)."""
        dc_names = {f.name for f in dc_fields(ssid.Ssid())}
        spec_set = set(self.SPEC_FIELDS)
        extras = dc_names - spec_set
        assert not extras, (
            f'Dataclass has fields not in spec responses: {extras}. '
            f'These may be stale or from request-only schemas.'
        )

