# CLI Reference

Auto-generated from User Model introspection.  Do not edit manually — regenerate with `python tools/generate_cli_docs.py`.

---

## Overview

The `meraki-cli` tool provides **48 commands**, one per resource module.  Commands are generated dynamically by introspecting User Model dataclasses.

### Installation

```bash
pip install 'plugins/plugin_utils/[cli]'
```

### Quick Start

```bash
# List all available resource commands
meraki-cli --list

# Gather VLANs from a network
export MERAKI_API_KEY=your_key_here
meraki-cli vlan gathered --network-id "L_123456789012345678"

# Create/update a VLAN
meraki-cli vlan merged --network-id L_123 --vlan-id 100 --name Engineering

# Use mock server for testing
meraki-cli --mock vlan gathered --network-id N_test

# Output as JSON
meraki-cli --json admin gathered --organization-id ORG_1

# Output as YAML
meraki-cli --yaml webhook gathered --network-id N_123
```

### Global Flags

| Flag | Description |
|------|-------------|
| `--mock` | Auto-start mock server and execute against it |
| `--json` | Output results as JSON |
| `--yaml` | Output results as YAML |
| `--list` | List available resource commands and exit |

### Complex Arguments

Fields with complex types (Dict, List[Dict]) accept either inline JSON strings or file references:

```bash
# Inline JSON
meraki-cli group-policy merged --network-id N_123 --bandwidth-limits '{"limitUp": 1000, "limitDown": 2000}'

# File reference
meraki-cli group-policy merged --network-id N_123 --bandwidth-limits @limits.json
```

---

## Command Summary

| Command | Scope | States |
|---------|-------|--------|
| `adaptive-policy` | `organization_id` | deleted, gathered, merged, overridden, replaced |
| `admin` | `organization_id` | deleted, gathered, merged, overridden, replaced |
| `air-marshal` | `network_id` | deleted, merged, replaced |
| `appliance-rf-profile` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `appliance-ssid` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `branding-policy` | `organization_id` | deleted, gathered, merged, overridden, replaced |
| `camera-quality-retention-profile` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `camera-wireless-profile` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `config-template` | `organization_id` | deleted, gathered, merged, overridden, replaced |
| `device` | `serial` | deleted, gathered, merged, overridden, replaced |
| `device-management-interface` | `serial` | deleted, gathered, merged, overridden, replaced |
| `device-switch-routing` | `serial` | deleted, gathered, merged, overridden, replaced |
| `ethernet-port-profile` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `facts` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `firewall` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `firmware-upgrade` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `floor-plan` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `group-policy` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `meraki-auth-user` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `mqtt-broker` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `network-settings` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `org-alert-profile` | `organization_id` | deleted, gathered, merged, overridden, replaced |
| `org-vpn` | `organization_id` | deleted, gathered, merged, overridden, replaced |
| `policy-object` | `organization_id` | deleted, gathered, merged, overridden, replaced |
| `port` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `prefix` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `saml` | `organization_id` | deleted, gathered, merged, overridden, replaced |
| `security` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `sensor-alert-profile` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `ssid` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `static-route` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `switch-access-policy` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `switch-acl` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `switch-dhcp-policy` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `switch-link-aggregation` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `switch-port` | `serial` | deleted, gathered, merged, overridden, replaced |
| `switch-qos-rule` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `switch-routing` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `switch-settings` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `switch-stack` | `network_id` | deleted, gathered, merged |
| `switch-stp` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `traffic-shaping` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `vlan` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `vlan-profile` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `vpn` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `warm-spare` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `webhook` | `network_id` | deleted, gathered, merged, overridden, replaced |
| `wireless-rf-profile` | `network_id` | deleted, gathered, merged, overridden, replaced |

---

## Command Reference

### `meraki-cli adaptive-policy`

Manage Meraki adaptive policy resources. Scope: organization_id

**Usage**

```bash
meraki-cli adaptive-policy <state> --organization-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--organization-id` (required) | string | Target organization id |
| `--enabled-networks` | string[] | List of network IDs with adaptive policy enabled. |
| `--last-entry-rule` | string | Rule to apply when no matching ACL is found. |

---

### `meraki-cli admin`

Manage Meraki admin resources. Canonical key: email System key: admin_id Scope: organization_id

**Usage**

```bash
meraki-cli admin <state> --organization-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `email`
**System key**: `admin_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--organization-id` (required) | string | Target organization id |
| `--admin-id` | string | Server-assigned ID, resolved automatically by matching on C(email). Provide only to disambiguate when duplicate emails exist. |
| `--name` | string | Admin name. |
| `--email` | string | Admin email. |
| `--org-access` | string | Admin's level of access to the organization. |
| `--tags` | JSON | List of tag-based access controls. (accepts JSON string or @file.json) |
| `--networks` | JSON | List of network-based access controls. (accepts JSON string or @file.json) |
| `--authentication-method` | string | Admin's authentication method. |
| `--account-status` | string | Status of the admin's account. |
| `--two-factor-auth-enabled / --no-two-factor-auth-enabled` | boolean | Indicates whether two-factor authentication is enabled. |
| `--has-api-key / --no-has-api-key` | boolean | Indicates whether the admin has an API key. |
| `--last-active` | string | Time when the admin was last active. |

---

### `meraki-cli air-marshal`

Manage Meraki air marshal resources. System key: rule_id Scope: network_id

**Usage**

```bash
meraki-cli air-marshal <state> --network-id <value> [options]
```

**States**: `deleted`, `merged`, `replaced`

**System key**: `rule_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--rule-id` | string | Server-assigned rule ID. Discover via C(state=gathered). |
| `--type` | string | Rule type (allow, block, or alert). |
| `--match` | JSON | Rule specification/match criteria. (accepts JSON string or @file.json) |
| `--default-policy` | string | Default policy for rogue networks. |
| `--ssid` | string | SSID name for the rule. |
| `--bssids` | JSON | BSSIDs broadcasting the SSID. (accepts JSON string or @file.json) |
| `--channels` | JSON | Channels where SSID was observed. (accepts JSON string or @file.json) |
| `--first-seen` | integer |  |
| `--last-seen` | integer |  |
| `--created-at` | string |  |
| `--updated-at` | string |  |

---

### `meraki-cli appliance-rf-profile`

Manage Meraki appliance rf profile resources. Canonical key: name System key: rf_profile_id Scope: network_id

**Usage**

```bash
meraki-cli appliance-rf-profile <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `name`
**System key**: `rf_profile_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--rf-profile-id` | string | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `--name` | string | Name of the profile. Required for create. |
| `--two-four-ghz-settings` | JSON | Settings for 2.4GHz band. (accepts JSON string or @file.json) |
| `--five-ghz-settings` | JSON | Settings for 5GHz band. (accepts JSON string or @file.json) |
| `--per-ssid-settings` | JSON | Per-SSID radio settings by number. (accepts JSON string or @file.json) |
| `--assigned` | JSON | Assigned RF profiles. (accepts JSON string or @file.json) |

---

### `meraki-cli appliance-ssid`

Manage Meraki appliance ssid resources. Scope: network_id

**Usage**

```bash
meraki-cli appliance-ssid <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--number` | integer | SSID number (0-4). Required for merged, replaced. |
| `--name` | string | Name of the SSID. |
| `--enabled / --no-enabled` | boolean | Whether the SSID is enabled. |
| `--auth-mode` | string | Association control method. |
| `--encryption-mode` | string | PSK encryption mode. |
| `--psk` | string | Passkey (auth_mode is psk). |
| `--default-vlan-id` | integer | VLAN ID associated with this SSID. |
| `--visible / --no-visible` | boolean | Whether to advertise or hide this SSID. |
| `--wpa-encryption-mode` | string | WPA encryption mode. |
| `--radius-servers` | JSON | RADIUS 802.1x servers for authentication. (accepts JSON string or @file.json) |

---

### `meraki-cli branding-policy`

Manage Meraki branding policy resources. Canonical key: name System key: branding_policy_id Scope: organization_id

**Usage**

```bash
meraki-cli branding-policy <state> --organization-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `name`
**System key**: `branding_policy_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--organization-id` (required) | string | Target organization id |
| `--branding-policy-id` | string | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `--name` | string | Name of the branding policy. |
| `--enabled / --no-enabled` | boolean | Whether the policy is enabled. |
| `--admin-settings` | JSON | Settings for which kinds of admins this policy applies to. (accepts JSON string or @file.json) |
| `--help-settings` | JSON | Modifications to Help page features. (accepts JSON string or @file.json) |
| `--custom-logo` | JSON | Custom logo properties. (accepts JSON string or @file.json) |

---

### `meraki-cli camera-quality-retention-profile`

Manage Meraki camera quality retention profile resources. Canonical key: name System key: quality_retention_profile_id Scope: network_id

**Usage**

```bash
meraki-cli camera-quality-retention-profile <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `name`
**System key**: `quality_retention_profile_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--quality-retention-profile-id` | string | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `--name` | string | Name of the quality retention profile. |
| `--max-retention-days` | integer | Maximum retention days for recordings. |
| `--motion-based-retention-enabled / --no-motion-based-retention-enabled` | boolean | Enable motion-based retention. |
| `--restricted-bandwidth-mode-enabled / --no-restricted-bandwidth-mode-enabled` | boolean | Enable restricted bandwidth mode. |
| `--audio-recording-enabled / --no-audio-recording-enabled` | boolean | Enable audio recording. |
| `--cloud-archive-enabled / --no-cloud-archive-enabled` | boolean | Enable cloud archive. |
| `--schedule-id` | string | Schedule ID for recording. |
| `--video-settings` | JSON | Video quality and resolution settings per camera model. (accepts JSON string or @file.json) |
| `--smart-retention` | JSON | Smart retention settings. (accepts JSON string or @file.json) |

---

### `meraki-cli camera-wireless-profile`

Manage Meraki camera wireless profile resources. Canonical key: name System key: wireless_profile_id Scope: network_id

**Usage**

```bash
meraki-cli camera-wireless-profile <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `name`
**System key**: `wireless_profile_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--wireless-profile-id` | string | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `--name` | string | Name of the camera wireless profile. |
| `--identity` | JSON | Identity of the wireless profile (required for create). (accepts JSON string or @file.json) |
| `--ssid` | JSON | SSID configuration details. (accepts JSON string or @file.json) |

---

### `meraki-cli config-template`

Manage Meraki config template resources. Canonical key: name System key: config_template_id Scope: organization_id

**Usage**

```bash
meraki-cli config-template <state> --organization-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `name`
**System key**: `config_template_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--organization-id` (required) | string | Target organization id |
| `--config-template-id` | string | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `--name` | string | Name of the configuration template. |
| `--product-types` | string[] | Product types (e.g. wireless, switch, appliance). |
| `--time-zone` | string | Timezone of the configuration template. |
| `--copy-from-network-id` | string | Network or template ID to copy configuration from. |

---

### `meraki-cli device`

Manage Meraki device resources. Scope: serial

**Usage**

```bash
meraki-cli device <state> --serial <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--serial` (required) | string | Target serial |
| `--name` | string | Name of the device. |
| `--tags` | string[] | List of tags for the device. |
| `--lat` | number | Latitude of the device. |
| `--lng` | number | Longitude of the device. |
| `--address` | string | Physical address of the device. |
| `--notes` | string | Notes for the device (max 255 chars). |
| `--move-map-marker / --no-move-map-marker` | boolean | Set lat/lng from address. |
| `--floor-plan-id` | string | Floor plan to associate with the device. |
| `--switch-profile-id` | string | Switch template ID to bind to the device. |

---

### `meraki-cli device-management-interface`

Manage Meraki device management interface resources. Scope: serial

**Usage**

```bash
meraki-cli device-management-interface <state> --serial <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--serial` (required) | string | Target serial |
| `--wan1` | JSON | WAN 1 settings. (accepts JSON string or @file.json) |
| `--wan2` | JSON | WAN 2 settings (MX devices only). (accepts JSON string or @file.json) |
| `--ddns-hostnames` | JSON | Dynamic DNS hostnames. (accepts JSON string or @file.json) |

---

### `meraki-cli device-switch-routing`

Manage Meraki device switch routing resources. Canonical key: name System key: interface_id Scope: serial

**Usage**

```bash
meraki-cli device-switch-routing <state> --serial <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `name`
**System key**: `interface_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--serial` (required) | string | Target serial |
| `--interface-id` | string | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `--name` | string | Interface name. |
| `--subnet` | string | IPv4 subnet. |
| `--interface-ip` | string | IPv4 address. |
| `--default-gateway` | string | IPv4 default gateway. |
| `--vlan-id` | integer | VLAN ID. |
| `--multicast-routing` | string | Multicast routing status. |
| `--ospf-settings` | JSON | IPv4 OSPF settings. (accepts JSON string or @file.json) |
| `--dhcp-mode` | string | DHCP mode for the interface. |
| `--dhcp-relay-server-ips` | string[] | DHCP relay server IPs. |

---

### `meraki-cli ethernet-port-profile`

Manage Meraki ethernet port profile resources. Canonical key: name System key: profile_id Scope: network_id

**Usage**

```bash
meraki-cli ethernet-port-profile <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `name`
**System key**: `profile_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--profile-id` | string | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `--name` | string | AP port profile name. |
| `--ports` | JSON | Ports configuration. (accepts JSON string or @file.json) |
| `--usb-ports` | JSON | USB ports configuration. (accepts JSON string or @file.json) |
| `--is-default / --no-is-default` | boolean | Whether this is the default profile. |
| `--serials` | string[] | List of AP serials to assign. |

---

### `meraki-cli facts`

Manage Meraki facts resources. Scope: network_id

**Usage**

```bash
meraki-cli facts <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--gather-subset` | string[] |  |
| `--organization-id` | string |  |

---

### `meraki-cli firewall`

Manage Meraki firewall resources. Scope: network_id

**Usage**

```bash
meraki-cli firewall <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--rules` | JSON | Ordered array of L3 firewall rules. (accepts JSON string or @file.json) |
| `--syslog-default-rule / --no-syslog-default-rule` | boolean | Log the special default rule. |
| `--spoofing-protection` | JSON | Spoofing protection settings. (accepts JSON string or @file.json) |
| `--application-categories` | JSON | L7 application categories and applications. (accepts JSON string or @file.json) |
| `--access` | string | Rule for which IPs are allowed to access. |
| `--allowed-ips` | string[] | Array of allowed CIDRs. |
| `--service` | string | Appliance service name. |

---

### `meraki-cli firmware-upgrade`

Manage Meraki firmware upgrade resources. Scope: network_id

**Usage**

```bash
meraki-cli firmware-upgrade <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--upgrade-window` | JSON | Upgrade window (dayOfWeek, hourOfDay). (accepts JSON string or @file.json) |
| `--timezone` | string | Timezone for the network. |
| `--products` | JSON | Product-specific upgrade settings (wireless, appliance, switch, camera). (accepts JSON string or @file.json) |

---

### `meraki-cli floor-plan`

Manage Meraki floor plan resources. Canonical key: name System key: floor_plan_id Scope: network_id

**Usage**

```bash
meraki-cli floor-plan <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `name`
**System key**: `floor_plan_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--floor-plan-id` | string | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `--name` | string | Name of the floor plan. |
| `--center` | JSON | Center coordinates (lat/lng) of the floor plan. (accepts JSON string or @file.json) |
| `--bottom-left-corner` | JSON | Bottom left corner coordinates. (accepts JSON string or @file.json) |
| `--bottom-right-corner` | JSON | Bottom right corner coordinates. (accepts JSON string or @file.json) |
| `--top-left-corner` | JSON | Top left corner coordinates. (accepts JSON string or @file.json) |
| `--top-right-corner` | JSON | Top right corner coordinates. (accepts JSON string or @file.json) |
| `--width` | number | Width of the floor plan. |
| `--height` | number | Height of the floor plan. |
| `--floor-number` | number | Floor number within the building. |
| `--image-contents` | string | Base64 encoded floor plan image. |
| `--image-extension` | string | Image format (e.g., png, jpg). |

---

### `meraki-cli group-policy`

Manage Meraki group policy resources. Canonical key: name System key: group_policy_id Scope: network_id

**Usage**

```bash
meraki-cli group-policy <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `name`
**System key**: `group_policy_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--group-policy-id` | string | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `--name` | string | Name of the group policy. Required for create. |
| `--bandwidth` | JSON | Bandwidth settings for clients. (accepts JSON string or @file.json) |
| `--bonjour-forwarding` | JSON | Bonjour forwarding settings. (accepts JSON string or @file.json) |
| `--content-filtering` | JSON | Content filtering settings. (accepts JSON string or @file.json) |
| `--firewall-and-traffic-shaping` | JSON | Firewall and traffic shaping rules. (accepts JSON string or @file.json) |
| `--scheduling` | JSON | Schedule for the group policy. (accepts JSON string or @file.json) |
| `--splash-auth-settings` | string | Splash authorization bypass setting. |
| `--vlan-tagging` | JSON | VLAN tagging settings. (accepts JSON string or @file.json) |

---

### `meraki-cli meraki-auth-user`

Manage Meraki meraki auth user resources. Canonical key: email System key: meraki_auth_user_id Scope: network_id

**Usage**

```bash
meraki-cli meraki-auth-user <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `email`
**System key**: `meraki_auth_user_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--meraki-auth-user-id` | string | Server-assigned ID, resolved automatically by matching on C(email). Provide only to disambiguate when duplicate emails exist. |
| `--name` | string | Name of the user. |
| `--email` | string | Email address of the user. |
| `--password` | string | Password for the user account. |
| `--account-type` | string | Authorization type for user. |
| `--authorizations` | JSON | User authorization info. (accepts JSON string or @file.json) |
| `--is-admin / --no-is-admin` | boolean | Whether the user is a Dashboard administrator. |
| `--email-password-to-user / --no-email-password-to-user` | boolean | Whether Meraki should email the password to user. |

---

### `meraki-cli mqtt-broker`

Manage Meraki mqtt broker resources. Canonical key: name System key: mqtt_broker_id Scope: network_id

**Usage**

```bash
meraki-cli mqtt-broker <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `name`
**System key**: `mqtt_broker_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--mqtt-broker-id` | string | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `--name` | string | Name of the MQTT broker. |
| `--host` | string | Host name or IP address of the MQTT broker. |
| `--port` | integer | Port for the MQTT broker. |
| `--authentication` | JSON | Authentication settings. (accepts JSON string or @file.json) |
| `--security` | JSON | Security settings. (accepts JSON string or @file.json) |

---

### `meraki-cli network-settings`

Manage Meraki network settings resources. Scope: network_id

**Usage**

```bash
meraki-cli network-settings <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--local-status-page-enabled / --no-local-status-page-enabled` | boolean | Enable local device status pages. |
| `--remote-status-page-enabled / --no-remote-status-page-enabled` | boolean | Enable access to device status page via LAN IP. |
| `--local-status-page` | JSON | Local status page authentication options. (accepts JSON string or @file.json) |
| `--fips` | JSON | FIPS options for the network. (accepts JSON string or @file.json) |
| `--named-vlans` | JSON | Named VLANs options. (accepts JSON string or @file.json) |
| `--secure-port` | JSON | SecureConnect options. (accepts JSON string or @file.json) |
| `--reporting-enabled / --no-reporting-enabled` | boolean | Enable NetFlow traffic reporting. |
| `--mode` | string | Traffic analysis mode. |
| `--custom-pie-chart-items` | JSON | Custom pie chart items for traffic reporting. (accepts JSON string or @file.json) |

---

### `meraki-cli org-alert-profile`

Manage Meraki org alert profile resources. System key: alert_config_id Scope: organization_id

**Usage**

```bash
meraki-cli org-alert-profile <state> --organization-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**System key**: `alert_config_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--organization-id` (required) | string | Target organization id |
| `--alert-config-id` | string | Server-assigned config ID. Discover via C(state=gathered). |
| `--type` | string | The alert type. |
| `--enabled / --no-enabled` | boolean | Whether the alert is enabled. |
| `--alert-condition` | JSON | Conditions that determine if the alert triggers. (accepts JSON string or @file.json) |
| `--recipients` | JSON | Recipients that receive the alert. (accepts JSON string or @file.json) |
| `--network-tags` | string[] | Network tags to monitor for the alert. |
| `--description` | string | User-supplied description of the alert. |

---

### `meraki-cli org-vpn`

Manage Meraki org vpn resources. Scope: organization_id

**Usage**

```bash
meraki-cli org-vpn <state> --organization-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--organization-id` (required) | string | Target organization id |
| `--peers` | JSON | List of third-party VPN peers. (accepts JSON string or @file.json) |
| `--third-party-vpn-peers` | JSON |  (accepts JSON string or @file.json) |

---

### `meraki-cli policy-object`

Manage Meraki policy object resources. Canonical key: name System key: policy_object_id Scope: organization_id

**Usage**

```bash
meraki-cli policy-object <state> --organization-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `name`
**System key**: `policy_object_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--organization-id` (required) | string | Target organization id |
| `--policy-object-id` | string | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `--name` | string | Name of the policy object. |
| `--category` | string | Category of policy object. |
| `--type` | string | Type of policy object. |
| `--cidr` | string | CIDR value (for cidr type). |
| `--fqdn` | string | Fully qualified domain name (for fqdn type). |
| `--ip` | string | IP address (for ipAndMask type). |
| `--mask` | string | Subnet mask (for ipAndMask type). |
| `--group-ids` | string[] | IDs of policy object groups this object belongs to. |
| `--network-ids` | string[] |  |
| `--object-ids` | JSON |  (accepts JSON string or @file.json) |

---

### `meraki-cli port`

Manage Meraki port resources. Scope: network_id

**Usage**

```bash
meraki-cli port <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--port-id` | string | Port ID (e.g., 1, 2, 3, 4). Required for merged, replaced. |
| `--enabled / --no-enabled` | boolean | Whether the port is enabled. |
| `--type` | string | Port type (access or trunk). |
| `--vlan` | integer | Native VLAN (trunk) or access VLAN. |
| `--allowed-vlans` | string | Allowed VLANs (comma-delimited or 'all'). |
| `--access-policy` | string | Access policy name (access ports only). |
| `--drop-untagged-traffic / --no-drop-untagged-traffic` | boolean | Drop untagged traffic (trunk ports). |

---

### `meraki-cli prefix`

Manage Meraki prefix resources. Canonical key: prefix System key: static_delegated_prefix_id Scope: network_id

**Usage**

```bash
meraki-cli prefix <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `prefix`
**System key**: `static_delegated_prefix_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--static-delegated-prefix-id` | string | Server-assigned ID, resolved automatically by matching on C(prefix). Provide only to disambiguate when duplicate prefixes exist. |
| `--prefix` | string | IPv6 prefix/prefix length. |
| `--description` | string | Identifying description for the prefix. |
| `--origin` | JSON | WAN1/WAN2/Independent prefix configuration. (accepts JSON string or @file.json) |

---

### `meraki-cli saml`

Manage Meraki saml resources. Scope: organization_id

**Usage**

```bash
meraki-cli saml <state> --organization-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--organization-id` (required) | string | Target organization id |
| `--enabled / --no-enabled` | boolean | Whether SAML SSO is enabled. |
| `--consumer-url` | string | URL consuming SAML Identity Provider (IdP). |
| `--slo-logout-url` | string | URL for redirect on sign out. |
| `--sso-login-url` | string | URL for redirect to log in again when session expires. |
| `--x509cert-sha1-fingerprint` | string | SHA1 fingerprint of the SAML certificate from IdP. |
| `--vision-consumer-url` | string | URL consuming SAML IdP for Meraki Vision Portal. |
| `--sp-initiated` | JSON | SP-Initiated SSO settings. (accepts JSON string or @file.json) |

---

### `meraki-cli security`

Manage Meraki security resources. Scope: network_id

**Usage**

```bash
meraki-cli security <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--mode` | string | Intrusion detection mode. |
| `--ids-rulesets` | string | Intrusion detection ruleset. |
| `--protected-networks` | JSON | Networks included/excluded from detection. (accepts JSON string or @file.json) |
| `--allowed-files` | JSON | Sha256 digests of files permitted by malware engine. (accepts JSON string or @file.json) |
| `--allowed-urls` | JSON | URLs permitted by malware detection engine. (accepts JSON string or @file.json) |

---

### `meraki-cli sensor-alert-profile`

Manage Meraki sensor alert profile resources. Canonical key: name System key: id Scope: network_id

**Usage**

```bash
meraki-cli sensor-alert-profile <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `name`
**System key**: `id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--id` | string | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `--name` | string | Name of the sensor alert profile. |
| `--conditions` | JSON | List of conditions that trigger alerts. (accepts JSON string or @file.json) |
| `--schedule` | JSON | Sensor schedule for the alert profile. (accepts JSON string or @file.json) |
| `--recipients` | JSON | Recipients that receive alerts. (accepts JSON string or @file.json) |
| `--message` | string | Custom message for email and text alerts. |
| `--include-sensor-url / --no-include-sensor-url` | boolean | Include dashboard link to sensor in messages. |
| `--serials` | string[] | Device serials assigned to this profile. |

---

### `meraki-cli ssid`

Manage Meraki ssid resources. Scope: network_id

**Usage**

```bash
meraki-cli ssid <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--number` | integer | SSID number (0-14). Required for merged and replaced. |
| `--name` | string | SSID name. |
| `--enabled / --no-enabled` | boolean | Whether the SSID is enabled. |
| `--auth-mode` | string | Authentication mode. |
| `--encryption-mode` | string | Encryption mode for the SSID. |
| `--psk` | string | Pre-shared key (for PSK auth). Write-only; not returned by API. |
| `--wpa-encryption-mode` | string | WPA encryption mode. |
| `--ip-assignment-mode` | string | Client IP assignment mode. |
| `--use-vlan-tagging / --no-use-vlan-tagging` | boolean | Whether to use VLAN tagging. |
| `--default-vlan-id` | integer | Default VLAN ID for all other APs. |
| `--vlan-id` | integer | VLAN ID for VLAN tagging. |
| `--splash-page` | string | Splash page type. |
| `--band-selection` | string | Band selection for the SSID. |
| `--min-bitrate` | number | Minimum bitrate in Mbps. |
| `--per-client-bandwidth-limit-up` | integer | Per-client upload bandwidth limit in Kbps (0 = no limit). |
| `--per-client-bandwidth-limit-down` | integer | Per-client download bandwidth limit in Kbps (0 = no limit). |
| `--per-ssid-bandwidth-limit-up` | integer | Per-SSID upload bandwidth limit in Kbps (0 = no limit). |
| `--per-ssid-bandwidth-limit-down` | integer | Per-SSID download bandwidth limit in Kbps (0 = no limit). |
| `--visible / --no-visible` | boolean | Whether the SSID is advertised (visible) or hidden. |
| `--available-on-all-aps / --no-available-on-all-aps` | boolean | Whether the SSID is broadcast on all APs. |
| `--availability-tags` | string[] | AP tags for SSID availability (when available_on_all_aps is false). |

---

### `meraki-cli static-route`

Manage Meraki static route resources. Canonical key: name System key: static_route_id Scope: network_id

**Usage**

```bash
meraki-cli static-route <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `name`
**System key**: `static_route_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--static-route-id` | string | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `--name` | string | Name of the route. |
| `--subnet` | string | Subnet of the route (e.g., 192.168.1.0/24). |
| `--gateway-ip` | string | Gateway IP address (next hop). |
| `--gateway-vlan-id` | integer | Gateway VLAN ID. |
| `--enabled / --no-enabled` | boolean | Whether the route is enabled. |
| `--fixed-ip-assignments` | JSON | Fixed DHCP IP assignments on the route. (accepts JSON string or @file.json) |
| `--reserved-ip-ranges` | JSON | DHCP reserved IP ranges. (accepts JSON string or @file.json) |
| `--ip-version` | integer | IP protocol version (4 or 6). |

---

### `meraki-cli switch-access-policy`

Manage Meraki switch access policy resources. Canonical key: access_policy_number Scope: network_id

**Usage**

```bash
meraki-cli switch-access-policy <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `access_policy_number`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--access-policy-number` | string | Access policy number (identifier). |
| `--name` | string | Name of the access policy. |
| `--access-policy-type` | string | Access type of the policy. |
| `--host-mode` | string | Host mode for the access policy. |
| `--radius-servers` | JSON | List of RADIUS servers for authentication. (accepts JSON string or @file.json) |
| `--radius-accounting-servers` | JSON | List of RADIUS accounting servers. (accepts JSON string or @file.json) |
| `--radius-accounting-enabled / --no-radius-accounting-enabled` | boolean | Enable RADIUS accounting. |
| `--radius-coa-support-enabled / --no-radius-coa-support-enabled` | boolean | Enable RADIUS CoA support. |
| `--guest-vlan-id` | integer | Guest VLAN ID for unauthorized devices. |
| `--dot1x` | JSON | 802.1X settings. (accepts JSON string or @file.json) |
| `--radius-group-attribute` | string |  |
| `--url-redirect-walled-garden-enabled / --no-url-redirect-walled-garden-enabled` | boolean |  |
| `--url-redirect-walled-garden-ranges` | string[] |  |
| `--voice-vlan-clients / --no-voice-vlan-clients` | boolean |  |

---

### `meraki-cli switch-acl`

Manage Meraki switch acl resources. Scope: network_id

**Usage**

```bash
meraki-cli switch-acl <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--rules` | JSON | Ordered array of access control list rules. (accepts JSON string or @file.json) |

---

### `meraki-cli switch-dhcp-policy`

Manage Meraki switch dhcp policy resources. Scope: network_id

**Usage**

```bash
meraki-cli switch-dhcp-policy <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--default-policy` | string | Default policy for new DHCP servers (allow or block). |
| `--allowed-servers` | string[] | MAC addresses of DHCP servers to permit. |
| `--blocked-servers` | string[] | MAC addresses of DHCP servers to block. |
| `--always-allowed-servers` | string[] | MAC addresses always allowed on the network. |
| `--arp-inspection` | JSON | Dynamic ARP Inspection settings. (accepts JSON string or @file.json) |
| `--alerts` | JSON | Email alert settings for DHCP servers. (accepts JSON string or @file.json) |

---

### `meraki-cli switch-link-aggregation`

Manage Meraki switch link aggregation resources. System key: link_aggregation_id Scope: network_id

**Usage**

```bash
meraki-cli switch-link-aggregation <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**System key**: `link_aggregation_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--link-aggregation-id` | string | Server-assigned aggregation ID. Discover via C(state=gathered). |
| `--switch-ports` | JSON | Array of switch ports for the aggregation. (accepts JSON string or @file.json) |
| `--switch-profile-ports` | JSON | Array of switch profile ports for creating aggregation. (accepts JSON string or @file.json) |

---

### `meraki-cli switch-port`

Manage Meraki switch port resources. Scope: serial

**Usage**

```bash
meraki-cli switch-port <state> --serial <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--serial` (required) | string | Target serial |
| `--port-id` | string | Port number/ID. |
| `--name` | string | Port name. |
| `--tags` | string[] | Tags for the port. |
| `--enabled / --no-enabled` | boolean | Whether the port is enabled. |
| `--type` | string | Port type. |
| `--vlan` | integer | VLAN number. |
| `--voice-vlan` | integer | Voice VLAN number. |
| `--allowed-vlans` | string | Allowed VLANs (for trunk ports). |
| `--poe-enabled / --no-poe-enabled` | boolean | Power over Ethernet enabled. |
| `--isolation-enabled / --no-isolation-enabled` | boolean | Port isolation enabled. |
| `--rstp-enabled / --no-rstp-enabled` | boolean | RSTP enabled. |
| `--stp-guard` | string | STP guard setting. |
| `--link-negotiation` | string | Link speed negotiation. |
| `--port-schedule-id` | string | Port schedule ID. |
| `--udld` | string | Unidirectional Link Detection action. |
| `--access-policy-type` | string | Access policy type. |
| `--access-policy-number` | integer | Access policy number. |
| `--sticky-mac-allow-list` | string[] | Sticky MAC allow list. |
| `--sticky-mac-allow-list-limit` | integer | Sticky MAC allow list limit. |
| `--storm-control-enabled / --no-storm-control-enabled` | boolean | Storm control enabled. |
| `--adaptive-policy-group-id` | string | Adaptive policy group ID. |
| `--peer-sgt-capable / --no-peer-sgt-capable` | boolean | Peer SGT capable. |
| `--flexible-stacking-enabled / --no-flexible-stacking-enabled` | boolean | Flexible stacking enabled. |
| `--dai-trusted / --no-dai-trusted` | boolean | DAI trusted. |
| `--profile` | JSON | Port profile. (accepts JSON string or @file.json) |

---

### `meraki-cli switch-qos-rule`

Manage Meraki switch qos rule resources. System key: qos_rule_id Scope: network_id

**Usage**

```bash
meraki-cli switch-qos-rule <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**System key**: `qos_rule_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--qos-rule-id` | string | Server-assigned rule ID. Discover via C(state=gathered). |
| `--dscp` | integer | DSCP tag for incoming packet (-1 to trust incoming DSCP). |
| `--vlan` | integer | VLAN of incoming packet (null matches any VLAN). |
| `--protocol` | string | Protocol (ANY, TCP, or UDP). |
| `--src-port` | integer | Source port (TCP/UDP only). |
| `--dst-port` | integer | Destination port (TCP/UDP only). |
| `--src-port-range` | string | Source port range (TCP/UDP only). |
| `--dst-port-range` | string | Destination port range (TCP/UDP only). |

---

### `meraki-cli switch-routing`

Manage Meraki switch routing resources. Scope: network_id

**Usage**

```bash
meraki-cli switch-routing <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--default-settings` | JSON | Default multicast settings for the network. (accepts JSON string or @file.json) |
| `--overrides` | JSON | Multicast overrides per switch/stack/profile. (accepts JSON string or @file.json) |
| `--enabled / --no-enabled` | boolean | Enable OSPF routing. |
| `--hello-timer-in-seconds` | integer | OSPF hello timer in seconds. |
| `--dead-timer-in-seconds` | integer | OSPF dead timer in seconds. |
| `--areas` | JSON | OSPF areas. (accepts JSON string or @file.json) |
| `--md5-authentication-enabled / --no-md5-authentication-enabled` | boolean | Enable MD5 authentication for OSPF. |
| `--md5-authentication-key` | JSON | MD5 authentication credentials. (accepts JSON string or @file.json) |
| `--v3` | JSON |  (accepts JSON string or @file.json) |

---

### `meraki-cli switch-settings`

Manage Meraki switch settings resources. Scope: network_id

**Usage**

```bash
meraki-cli switch-settings <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--default-mtu-size` | integer | MTU size for the entire network. |
| `--overrides` | JSON | Override MTU for individual switches. (accepts JSON string or @file.json) |
| `--broadcast-threshold` | integer | Broadcast storm control threshold. |
| `--multicast-threshold` | integer | Multicast storm control threshold. |
| `--unknown-unicast-threshold` | integer | Unknown unicast storm control threshold. |
| `--mappings` | JSON | DSCP to CoS mappings. (accepts JSON string or @file.json) |
| `--use-combined-power / --no-use-combined-power` | boolean | Use combined power for secondary power supplies. |
| `--power-exceptions` | JSON | Per-switch power exceptions. (accepts JSON string or @file.json) |
| `--enabled / --no-enabled` | boolean |  |
| `--vlan-id` | integer |  |
| `--switches` | JSON |  (accepts JSON string or @file.json) |
| `--protocols` | string[] |  |

---

### `meraki-cli switch-stack`

Manage Meraki switch stack resources. Canonical key: name System key: switch_stack_id Scope: network_id

**Usage**

```bash
meraki-cli switch-stack <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`

**Canonical key**: `name`
**System key**: `switch_stack_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--switch-stack-id` | string | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `--name` | string | Name of the switch stack. |
| `--serials` | string[] | Serials of switches in the stack. |
| `--members` | JSON | Members of the stack. (accepts JSON string or @file.json) |
| `--is-monitor-only / --no-is-monitor-only` | boolean | Whether stack is monitor only. |
| `--virtual-mac` | string | Virtual MAC address of the switch stack. |

---

### `meraki-cli switch-stp`

Manage Meraki switch stp resources. Scope: network_id

**Usage**

```bash
meraki-cli switch-stp <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--rstp-enabled / --no-rstp-enabled` | boolean | Enable RSTP (Rapid Spanning Tree Protocol). |
| `--stp-bridge-priority` | JSON | STP bridge priority for switches/stacks or templates. (accepts JSON string or @file.json) |

---

### `meraki-cli traffic-shaping`

Manage Meraki traffic shaping resources. Scope: network_id

**Usage**

```bash
meraki-cli traffic-shaping <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--default-rules-enabled / --no-default-rules-enabled` | boolean | Whether default traffic shaping rules are enabled. |
| `--default-uplink` | string | The default uplink (e.g., wan1, wan2). |
| `--rules` | JSON | Array of traffic shaping rules. (accepts JSON string or @file.json) |
| `--bandwidth-limits` | JSON | Uplink bandwidth limits by interface. (accepts JSON string or @file.json) |
| `--global-bandwidth-limits` | JSON | Global per-client bandwidth limit. (accepts JSON string or @file.json) |
| `--failover-and-failback` | JSON | WAN failover and failback settings. (accepts JSON string or @file.json) |
| `--load-balancing-enabled / --no-load-balancing-enabled` | boolean | Whether load balancing is enabled. |
| `--active-active-auto-vpn-enabled / --no-active-active-auto-vpn-enabled` | boolean | Whether active-active AutoVPN is enabled. |
| `--vpn-traffic-uplink-preferences` | JSON | Uplink preference rules for VPN traffic. (accepts JSON string or @file.json) |
| `--wan-traffic-uplink-preferences` | JSON | Uplink preference rules for WAN traffic. (accepts JSON string or @file.json) |

---

### `meraki-cli vlan`

Manage Meraki vlan resources. Canonical key: vlan_id Scope: network_id

**Usage**

```bash
meraki-cli vlan <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `vlan_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--vlan-id` | string | VLAN ID (1-4094). Required for merged and deleted. |
| `--name` | string | VLAN name. |
| `--subnet` | string | Subnet (e.g., '192.168.1.0/24'). |
| `--appliance-ip` | string | Appliance IP on the VLAN. |
| `--group-policy-id` | string | Group policy ID. |
| `--template-vlan-type` | string | Type of subnetting for template networks. |
| `--cidr` | string | CIDR for template networks. |
| `--mask` | integer | Mask for template networks. |
| `--dhcp-handling` | string | How the appliance handles DHCP requests on this VLAN. |
| `--dhcp-relay-server-ips` | string[] | IPs of DHCP servers to relay requests to. |
| `--dhcp-lease-time` | string | DHCP lease term. |
| `--dhcp-boot-options-enabled / --no-dhcp-boot-options-enabled` | boolean | Use DHCP boot options. |
| `--dhcp-boot-next-server` | string | DHCP boot next server. |
| `--dhcp-boot-filename` | string | DHCP boot filename. |
| `--dhcp-options` | JSON | DHCP options for responses. (accepts JSON string or @file.json) |
| `--dns-nameservers` | string | DNS nameservers for DHCP responses. |
| `--reserved-ip-ranges` | JSON | Reserved IP ranges on the VLAN. (accepts JSON string or @file.json) |
| `--fixed-ip-assignments` | JSON | Fixed IP assignments. (accepts JSON string or @file.json) |
| `--ipv6` | JSON | IPv6 configuration. (accepts JSON string or @file.json) |
| `--mandatory-dhcp` | JSON | Mandatory DHCP configuration. (accepts JSON string or @file.json) |

---

### `meraki-cli vlan-profile`

Manage Meraki vlan profile resources. Canonical key: iname Scope: network_id

**Usage**

```bash
meraki-cli vlan-profile <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `iname`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--iname` | string | VLAN profile iname (primary key). Required for merged, replaced, deleted. |
| `--name` | string | Name of the profile (1-255 chars). |
| `--is-default / --no-is-default` | boolean | Whether this is the default VLAN profile. |
| `--vlan-names` | JSON | Array of named VLANs. (accepts JSON string or @file.json) |
| `--vlan-groups` | JSON | Array of named VLAN groups. (accepts JSON string or @file.json) |
| `--vlan-profile` | JSON | VLAN profile configuration. (accepts JSON string or @file.json) |

---

### `meraki-cli vpn`

Manage Meraki vpn resources. Scope: network_id

**Usage**

```bash
meraki-cli vpn <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--mode` | string | Site-to-site VPN mode. |
| `--hubs` | JSON | List of VPN hubs, in order of preference. (accepts JSON string or @file.json) |
| `--subnets` | JSON | List of subnets and their VPN presence. (accepts JSON string or @file.json) |
| `--subnet` | JSON | Configuration of subnet features. (accepts JSON string or @file.json) |
| `--enabled / --no-enabled` | boolean | Whether VPN is enabled. |
| `--as-number` | integer | BGP autonomous system number. |
| `--ibgp-hold-timer` | integer | iBGP hold time in seconds. |
| `--neighbors` | JSON | List of eBGP neighbor configurations. (accepts JSON string or @file.json) |

---

### `meraki-cli warm-spare`

Manage Meraki warm spare resources. Scope: network_id

**Usage**

```bash
meraki-cli warm-spare <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`


**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--enabled / --no-enabled` | boolean | Whether warm spare is enabled. |
| `--spare-serial` | string | Serial number of the warm spare appliance. |
| `--uplink-mode` | string | Uplink mode (virtual or public). |
| `--virtual-ip1` | string | WAN 1 shared IP. |
| `--virtual-ip2` | string | WAN 2 shared IP. |
| `--wan1` | JSON | WAN 1 IP and subnet. (accepts JSON string or @file.json) |
| `--wan2` | JSON | WAN 2 IP and subnet. (accepts JSON string or @file.json) |
| `--primary-serial` | string | Serial number of the primary appliance. |

---

### `meraki-cli webhook`

Manage Meraki webhook resources. Canonical key: name System key: http_server_id Scope: network_id

**Usage**

```bash
meraki-cli webhook <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `name`
**System key**: `http_server_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--http-server-id` | string | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `--name` | string | Name for easy reference to the HTTP server. |
| `--url` | string | URL of the HTTP server. |
| `--shared-secret` | string | Shared secret included in POSTs to the server. |
| `--payload-template` | JSON | Payload template for POSTs to the HTTP server. (accepts JSON string or @file.json) |

---

### `meraki-cli wireless-rf-profile`

Manage Meraki wireless rf profile resources. Canonical key: name System key: rf_profile_id Scope: network_id

**Usage**

```bash
meraki-cli wireless-rf-profile <state> --network-id <value> [options]
```

**States**: `deleted`, `gathered`, `merged`, `overridden`, `replaced`

**Canonical key**: `name`
**System key**: `rf_profile_id`

**Arguments**

| Flag | Type | Description |
|------|------|-------------|
| `--network-id` (required) | string | Target network id |
| `--rf-profile-id` | string | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `--name` | string | Name of the RF profile. Must be unique. |
| `--band-selection-type` | string | Band selection (ssid or ap). |
| `--client-balancing-enabled / --no-client-balancing-enabled` | boolean | Steer clients to best available AP. |
| `--two-four-ghz-settings` | JSON | 2.4 GHz band settings. (accepts JSON string or @file.json) |
| `--five-ghz-settings` | JSON | 5 GHz band settings. (accepts JSON string or @file.json) |
| `--six-ghz-settings` | JSON | 6 GHz band settings. (accepts JSON string or @file.json) |
| `--transmission` | JSON | Radio transmission settings. (accepts JSON string or @file.json) |
| `--is-indoor-default / --no-is-indoor-default` | boolean | Set as default indoor profile. |
| `--is-outdoor-default / --no-is-outdoor-default` | boolean | Set as default outdoor profile. |
| `--ap-band-settings` | JSON |  (accepts JSON string or @file.json) |
| `--per-ssid-settings` | JSON |  (accepts JSON string or @file.json) |
| `--min-bitrate-type` | string |  |

---

---

*Generated by `tools/generate_cli_docs.py` from User Model introspection.*