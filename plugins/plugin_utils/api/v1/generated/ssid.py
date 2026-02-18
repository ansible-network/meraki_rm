"""Generated API dataclass for Meraki wireless ssid.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/wireless/ssids
    /networks/{networkId}/wireless/ssids/{number}
    /networks/{networkId}/wireless/ssids/{number}/bonjourForwarding
    /networks/{networkId}/wireless/ssids/{number}/deviceTypeGroupPolicies
    /networks/{networkId}/wireless/ssids/{number}/eapOverride
    /networks/{networkId}/wireless/ssids/{number}/firewall/l3FirewallRules
    /networks/{networkId}/wireless/ssids/{number}/firewall/l7FirewallRules
    /networks/{networkId}/wireless/ssids/{number}/hotspot20
    /networks/{networkId}/wireless/ssids/{number}/identityPsks
    /networks/{networkId}/wireless/ssids/{number}/identityPsks/{identityPskId}
    /networks/{networkId}/wireless/ssids/{number}/openRoaming
    /networks/{networkId}/wireless/ssids/{number}/schedules
    /networks/{networkId}/wireless/ssids/{number}/splash/settings
    /networks/{networkId}/wireless/ssids/{number}/trafficShaping/rules
    /networks/{networkId}/wireless/ssids/{number}/vpn
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional


@dataclass
class Ssid:
    """Meraki wireless ssid API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    _FIELD_CONSTRAINTS: ClassVar[dict] = {
        'authMode': {'enum': ['8021x-entra', '8021x-google', '8021x-localradius', '8021x-meraki', '8021x-nac', '8021x-radius', 'ipsk-with-nac', 'ipsk-with-radius', 'ipsk-with-radius-easy-psk', 'ipsk-without-radius', 'open', 'open-enhanced', 'open-with-nac', 'open-with-radius', 'psk']},
        'bandSelection': {'enum': ['5 GHz band only', 'Dual band operation', 'Dual band operation with Band Steering']},
        'controllerDisconnectionBehavior': {'enum': ['default', 'open', 'restricted']},
        'encryptionMode': {'enum': ['wep', 'wpa']},
        'enterpriseAdminAccess': {'enum': ['access disabled', 'access enabled']},
        'ipAssignmentMode': {'enum': ['Bridge mode', 'Campus Gateway', 'Ethernet over GRE', 'Layer 3 roaming', 'Layer 3 roaming with a concentrator', 'NAT mode', 'VPN']},
        'networkAccessType': {'enum': ['Chargeable public network', 'Emergency services only network', 'Free public network', 'Personal device network', 'Private network', 'Private network with guest access', 'Test or experimental', 'Wildcard']},
        'radiusAttributeForGroupPolicies': {'enum': ['Airespace-ACL-Name', 'Aruba-User-Role', 'Filter-Id', 'Reply-Message']},
        'radiusFailoverPolicy': {'enum': ['Allow access', 'Deny access']},
        'radiusLoadBalancingPolicy': {'enum': ['Round robin', 'Strict priority order']},
        'splashPage': {'enum': ['Billing', 'Cisco ISE', 'Click-through splash page', 'Facebook Wi-Fi', 'Google Apps domain', 'Google OAuth', 'Microsoft Entra ID', 'None', 'Password-protected with Active Directory', 'Password-protected with LDAP', 'Password-protected with Meraki RADIUS', 'Password-protected with custom RADIUS', 'SMS authentication', 'Sponsored guest', 'Systems Manager Sentry']},
        'splashTimeout': {'enum': [30, 60, 120, 240, 480, 720, 1080, 1440, 2880, 5760, 7200, 10080, 20160, 43200, 86400, 129600]},
        'wpaEncryptionMode': {'enum': ['WPA1 and WPA2', 'WPA1 only', 'WPA2 only', 'WPA3 192-bit Security', 'WPA3 Transition Mode', 'WPA3 only']},
    }

    # The current setting for Active Directory. Only valid if splashPage is 'Pa...
    activeDirectory: Optional[Dict[str, Any]] = None
    # Adaptive policy group ID this SSID is assigned to.
    adaptivePolicyGroupId: Optional[str] = None
    # URL for the admin splash page
    adminSplashUrl: Optional[str] = None
    # Boolean indicating whether or not adult content will be blocked
    adultContentFilteringEnabled: Optional[bool] = None
    # Allows wireless client access to local LAN (boolean value - true allows a...
    allowLanAccess: Optional[bool] = None
    # Whether or not to allow simultaneous logins from different devices.
    allowSimultaneousLogins: Optional[bool] = None
    # The list of tags and VLAN IDs used for VLAN tagging. This param is only v...
    apTagsAndVlanIds: Optional[List[Dict[str, Any]]] = None
    # The association control method for the SSID
    authMode: Optional[str] = None
    # List of tags for this SSID. If availableOnAllAps is false, then the SSID ...
    availabilityTags: Optional[List[str]] = None
    # Whether all APs broadcast the SSID or if it's restricted to APs matching ...
    availableOnAllAps: Optional[bool] = None
    # The client-serving radio frequencies of this SSID in the default indoor R...
    bandSelection: Optional[str] = None
    # Details associated with billing splash
    billing: Optional[Dict[str, Any]] = None
    # How restricted allowing traffic should be. If true, all traffic types are...
    blockAllTrafficBeforeSignOn: Optional[bool] = None
    # The VPN concentrator settings for this SSID.
    concentrator: Optional[Dict[str, Any]] = None
    # The concentrator to use when the ipAssignmentMode is 'Layer 3 roaming wit...
    concentratorNetworkId: Optional[str] = None
    # How login attempts should be handled when the controller is unreachable.
    controllerDisconnectionBehavior: Optional[str] = None
    # Whether default traffic shaping rules are enabled (true) or disabled (fal...
    defaultRulesEnabled: Optional[bool] = None
    # The default VLAN ID used for 'all other APs'. This param is only valid wh...
    defaultVlanId: Optional[int] = None
    # List of device type policies.
    deviceTypePolicies: Optional[List[Dict[str, Any]]] = None
    # Disassociate clients when 'VPN' concentrator failover occurs in order to ...
    disassociateClientsOnVpnFailover: Optional[bool] = None
    # DNS servers rewrite settings
    dnsRewrite: Optional[Dict[str, Any]] = None
    # An array of domain names
    domains: Optional[List[str]] = None
    # The current setting for 802.11r
    dot11r: Optional[Dict[str, Any]] = None
    # The current setting for Protected Management Frames (802.11w).
    dot11w: Optional[Dict[str, Any]] = None
    # EAPOL Key settings.
    eapolKey: Optional[Dict[str, Any]] = None
    # The email associated with the System's Manager User
    email: Optional[str] = None
    # Whether or not the SSID is enabled
    enabled: Optional[bool] = None
    # The psk encryption mode for the SSID
    encryptionMode: Optional[str] = None
    # Whether or not an SSID is accessible by 'enterprise' administrators ('acc...
    enterpriseAdminAccess: Optional[str] = None
    # Bonjour forwarding exception
    exception: Optional[Dict[str, Any]] = None
    # Timestamp for when the Identity PSK expires, or 'null' to never expire
    expiresAt: Optional[str] = None
    # Secondary VPN concentrator settings. This is only used when two VPN conce...
    failover: Optional[Dict[str, Any]] = None
    # Ethernet over GRE settings
    gre: Optional[Dict[str, Any]] = None
    # The group policy to be applied to clients
    groupPolicyId: Optional[str] = None
    # Details associated with guest sponsored splash
    guestSponsorship: Optional[Dict[str, Any]] = None
    # The unique identifier of the Identity PSK
    id: Optional[str] = None
    # EAP settings for identity requests.
    identity: Optional[Dict[str, Any]] = None
    # The client IP assignment mode
    ipAssignmentMode: Optional[str] = None
    # Boolean indicating whether Layer 2 LAN isolation should be enabled or dis...
    lanIsolationEnabled: Optional[bool] = None
    # The current setting for LDAP. Only valid if splashPage is 'Password-prote...
    ldap: Optional[Dict[str, Any]] = None
    # Extended local auth flag for Enterprise NAC
    localAuth: Optional[bool] = None
    # The current configuration for Local Authentication Fallback. Enables the ...
    localAuthFallback: Optional[Dict[str, Any]] = None
    # The current setting for Local Authentication, a built-in RADIUS server on...
    localRadius: Optional[Dict[str, Any]] = None
    # Whether clients connecting to this SSID must use the IP address assigned ...
    mandatoryDhcpEnabled: Optional[bool] = None
    # Maximum number of general EAP retries.
    maxRetries: Optional[int] = None
    # An array of MCC/MNC pairs
    mccMncs: Optional[List[Dict[str, Any]]] = None
    # The minimum bitrate in Mbps of this SSID in the default indoor RF profile
    minBitrate: Optional[int] = None
    # An array of NAI realms
    naiRealms: Optional[List[Dict[str, Any]]] = None
    # The name of the SSID
    name: Optional[str] = None
    # Named VLAN settings.
    namedVlans: Optional[Dict[str, Any]] = None
    # The network type of this SSID
    networkAccessType: Optional[str] = None
    # Unique identifier of the SSID
    number: Optional[int] = None
    # The OAuth settings of this SSID. Only valid if splashPage is 'Google OAuth'.
    oauth: Optional[Dict[str, Any]] = None
    # Operator settings for this SSID
    operator: Optional[Dict[str, Any]] = None
    # The passphrase for client authentication
    passphrase: Optional[str] = None
    # The download bandwidth limit in Kbps. (0 represents no limit.)
    perClientBandwidthLimitDown: Optional[int] = None
    # The upload bandwidth limit in Kbps. (0 represents no limit.)
    perClientBandwidthLimitUp: Optional[int] = None
    # The total download bandwidth limit in Kbps (0 represents no limit)
    perSsidBandwidthLimitDown: Optional[int] = None
    # The total upload bandwidth limit in Kbps (0 represents no limit)
    perSsidBandwidthLimitUp: Optional[int] = None
    # The passkey for the SSID. This param is only valid if the authMode is 'psk'
    psk: Optional[str] = None
    # Whether or not RADIUS accounting is enabled
    radiusAccountingEnabled: Optional[bool] = None
    # The interval (in seconds) in which accounting information is updated and ...
    radiusAccountingInterimInterval: Optional[int] = None
    # List of RADIUS accounting 802.1X servers to be used for authentication
    radiusAccountingServers: Optional[List[Dict[str, Any]]] = None
    # The delay (in seconds) before sending the first RADIUS accounting start m...
    radiusAccountingStartDelay: Optional[int] = None
    # RADIUS attribute used to look up group policies
    radiusAttributeForGroupPolicies: Optional[str] = None
    # The template of the NAS identifier to be used for RADIUS authentication (...
    radiusAuthenticationNasId: Optional[str] = None
    # The template of the called station identifier to be used for RADIUS (ex. ...
    radiusCalledStationId: Optional[str] = None
    # If true, Meraki devices will act as a RADIUS Dynamic Authorization Server...
    radiusCoaEnabled: Optional[bool] = None
    # Whether RADIUS authentication is enabled
    radiusEnabled: Optional[bool] = None
    # Policy which determines how authentication requests should be handled in ...
    radiusFailoverPolicy: Optional[str] = None
    # Whether or not higher priority RADIUS servers should be retried after 60 ...
    radiusFallbackEnabled: Optional[bool] = None
    # Whether or not RADIUS Guest VLAN is enabled. This param is only valid if ...
    radiusGuestVlanEnabled: Optional[bool] = None
    # VLAN ID of the RADIUS Guest VLAN. This param is only valid if the authMod...
    radiusGuestVlanId: Optional[int] = None
    # Policy which determines which RADIUS server will be contacted first in an...
    radiusLoadBalancingPolicy: Optional[str] = None
    # If true, the RADIUS response can override VLAN tag. This is not valid whe...
    radiusOverride: Optional[bool] = None
    # If true, Meraki devices will proxy RADIUS messages through the Meraki clo...
    radiusProxyEnabled: Optional[bool] = None
    # The current settings for RADIUS RADSec
    radiusRadsec: Optional[Dict[str, Any]] = None
    # The maximum number of transmit attempts after which a RADIUS server is fa...
    radiusServerAttemptsLimit: Optional[int] = None
    # The amount of time for which a RADIUS client waits for a reply from the R...
    radiusServerTimeout: Optional[int] = None
    # List of RADIUS 802.1X servers to be used for authentication
    radiusServers: Optional[List[Dict[str, Any]]] = None
    # If true, Meraki devices will periodically send Access-Request messages to...
    radiusTestingEnabled: Optional[bool] = None
    # List of outage ranges. Has a start date and time, and end date and time. ...
    ranges: Optional[List[Dict[str, Any]]] = None
    # List of outage ranges in seconds since Sunday at Midnight. Has a start an...
    rangesInSeconds: Optional[List[Dict[str, Any]]] = None
    # The custom redirect URL where the users will go after the splash page.
    redirectUrl: Optional[str] = None
    # An array of roaming consortium OIs (hexadecimal number 3-5 octets in length)
    roamConsortOis: Optional[List[str]] = None
    # Bonjour forwarding rules
    rules: Optional[List[Dict[str, Any]]] = None
    # The secondary concentrator to use when the ipAssignmentMode is 'VPN'. If ...
    secondaryConcentratorNetworkId: Optional[str] = None
    # Self-registration for splash with Meraki authentication.
    selfRegistration: Optional[Dict[str, Any]] = None
    # Systems Manager sentry enrollment splash settings.
    sentryEnrollment: Optional[Dict[str, Any]] = None
    # The SpeedBurst setting for this SSID'
    speedBurst: Optional[Dict[str, Any]] = None
    # Array of valid sponsor email domains for sponsored guest splash type.
    splashGuestSponsorDomains: Optional[List[str]] = None
    # The image used in the splash page.
    splashImage: Optional[Dict[str, Any]] = None
    # The logo used in the splash page.
    splashLogo: Optional[Dict[str, Any]] = None
    # The type of splash page for the SSID
    splashPage: Optional[str] = None
    # The prepaid front image used in the splash page.
    splashPrepaidFront: Optional[Dict[str, Any]] = None
    # Splash page timeout
    splashTimeout: Optional[str] = None
    # The custom splash URL of the click-through splash page.
    splashUrl: Optional[str] = None
    # The VPN split tunnel settings for this SSID.
    splitTunnel: Optional[Dict[str, Any]] = None
    # SSID Administrator access status
    ssidAdminAccessible: Optional[bool] = None
    # SSID number
    ssidNumber: Optional[int] = None
    # The OpenRoaming DNA Spaces tenant ID.
    tenantId: Optional[str] = None
    # The id of the selected splash theme.
    themeId: Optional[str] = None
    # General EAP timeout in seconds.
    timeout: Optional[int] = None
    # Whether traffic shaping rules are applied to clients on your SSID.
    trafficShapingEnabled: Optional[bool] = None
    # The Boolean indicating whether the the user will be redirected to the cus...
    useRedirectUrl: Optional[bool] = None
    # Boolean indicating whether the users will be redirected to the custom spl...
    useSplashUrl: Optional[bool] = None
    # Whether or not traffic should be directed to use specific VLANs. This par...
    useVlanTagging: Optional[bool] = None
    # Venue settings for this SSID
    venue: Optional[Dict[str, Any]] = None
    # Whether the SSID is advertised or hidden by the AP
    visible: Optional[bool] = None
    # The VLAN ID used for VLAN tagging. This param is only valid when the ipAs...
    vlanId: Optional[int] = None
    # Allow users to access a configurable list of IP ranges prior to sign-on
    walledGardenEnabled: Optional[bool] = None
    # Domain names and IP address ranges available in Walled Garden mode
    walledGardenRanges: Optional[List[str]] = None
    # The welcome message for the users on the splash page.
    welcomeMessage: Optional[str] = None
    # The WiFi Personal Network unique identifier
    wifiPersonalNetworkId: Optional[str] = None
    # The types of WPA encryption
    wpaEncryptionMode: Optional[str] = None
