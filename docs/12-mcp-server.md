# MCP Server Reference

Auto-generated from User Model introspection.  Do not edit manually — regenerate with `python tools/generate_mcp_docs.py`.

---

## Overview

The Meraki RM MCP server exposes **48 tools**, one per resource module.  Tools are generated at startup by introspecting User Model dataclasses.

### Running the Server

```bash
# Task mode (default) — returns Ansible YAML snippets
meraki-mcp-server --mode=task

# Live mode — executes against the Meraki Dashboard API
export MERAKI_API_KEY=your_key_here
meraki-mcp-server --mode=live
```

### Installation

```bash
pip install 'plugins/plugin_utils/[mcp]'
```

---

## Tool Summary

| Tool | Scope | Canonical Key | Category | States |
|------|-------|---------------|----------|--------|
| `meraki_adaptive_policy` | `organization_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_admin` | `organization_id` | `email` | B | deleted, gathered, merged, overridden, replaced |
| `meraki_air_marshal` | `network_id` | — | C | deleted, merged, replaced |
| `meraki_appliance_rf_profile` | `network_id` | `name` | B | deleted, gathered, merged, overridden, replaced |
| `meraki_appliance_ssid` | `network_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_branding_policy` | `organization_id` | `name` | B | deleted, gathered, merged, overridden, replaced |
| `meraki_camera_quality_retention_profile` | `network_id` | `name` | B | deleted, gathered, merged, overridden, replaced |
| `meraki_camera_wireless_profile` | `network_id` | `name` | B | deleted, gathered, merged, overridden, replaced |
| `meraki_config_template` | `organization_id` | `name` | B | deleted, gathered, merged, overridden, replaced |
| `meraki_device` | `serial` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_device_management_interface` | `serial` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_device_switch_routing` | `serial` | `name` | B | deleted, gathered, merged, overridden, replaced |
| `meraki_ethernet_port_profile` | `network_id` | `name` | B | deleted, gathered, merged, overridden, replaced |
| `meraki_facts` | `network_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_firewall` | `network_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_firmware_upgrade` | `network_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_floor_plan` | `network_id` | `name` | B | deleted, gathered, merged, overridden, replaced |
| `meraki_group_policy` | `network_id` | `name` | B | deleted, gathered, merged, overridden, replaced |
| `meraki_meraki_auth_user` | `network_id` | `email` | B | deleted, gathered, merged, overridden, replaced |
| `meraki_mqtt_broker` | `network_id` | `name` | B | deleted, gathered, merged, overridden, replaced |
| `meraki_network_settings` | `network_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_org_alert_profile` | `organization_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_org_vpn` | `organization_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_policy_object` | `organization_id` | `name` | B | deleted, gathered, merged, overridden, replaced |
| `meraki_port` | `network_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_prefix` | `network_id` | `prefix` | B | deleted, gathered, merged, overridden, replaced |
| `meraki_saml` | `organization_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_security` | `network_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_sensor_alert_profile` | `network_id` | `name` | B | deleted, gathered, merged, overridden, replaced |
| `meraki_ssid` | `network_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_static_route` | `network_id` | `name` | B | deleted, gathered, merged, overridden, replaced |
| `meraki_switch_access_policy` | `network_id` | `access_policy_number` | A | deleted, gathered, merged, overridden, replaced |
| `meraki_switch_acl` | `network_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_switch_dhcp_policy` | `network_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_switch_link_aggregation` | `network_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_switch_port` | `serial` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_switch_qos_rule` | `network_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_switch_routing` | `network_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_switch_settings` | `network_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_switch_stack` | `network_id` | `name` | B | deleted, gathered, merged |
| `meraki_switch_stp` | `network_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_traffic_shaping` | `network_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_vlan` | `network_id` | `vlan_id` | A | deleted, gathered, merged, overridden, replaced |
| `meraki_vlan_profile` | `network_id` | `iname` | A | deleted, gathered, merged, overridden, replaced |
| `meraki_vpn` | `network_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_warm_spare` | `network_id` | — | C | deleted, gathered, merged, overridden, replaced |
| `meraki_webhook` | `network_id` | `name` | B | deleted, gathered, merged, overridden, replaced |
| `meraki_wireless_rf_profile` | `network_id` | `name` | B | deleted, gathered, merged, overridden, replaced |

---

## Tool Reference

### `meraki_adaptive_policy`

Manage Meraki adaptive policy resources. Scope: organization_id

**Metadata**

- **Scope**: `organization_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `organization_id` | string | yes | Target organization id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `enabled_networks` | array[string] |  | List of network IDs with adaptive policy enabled. |
| `last_entry_rule` | string |  | Rule to apply when no matching ACL is found. |

---

### `meraki_admin`

Manage Meraki admin resources. Canonical key: email System key: admin_id Scope: organization_id

**Metadata**

- **Scope**: `organization_id`
- **Canonical key**: `email`
- **System key**: `admin_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `organization_id` | string | yes | Target organization id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `account_status` | string |  | Status of the admin's account. |
| `admin_id` | string |  | Server-assigned ID, resolved automatically by matching on C(email). Provide only to disambiguate when duplicate emails exist. |
| `authentication_method` | string |  | Admin's authentication method. |
| `email` | string |  | Admin email. |
| `has_api_key` | boolean |  | Indicates whether the admin has an API key. |
| `last_active` | string |  | Time when the admin was last active. |
| `name` | string |  | Admin name. |
| `networks` | array[object] |  | List of network-based access controls. |
| `org_access` | string |  | Admin's level of access to the organization. |
| `tags` | array[object] |  | List of tag-based access controls. |
| `two_factor_auth_enabled` | boolean |  | Indicates whether two-factor authentication is enabled. |

---

### `meraki_air_marshal`

Manage Meraki air marshal resources. System key: rule_id Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `rule_id`
- **Supports delete**: True
- **Valid states**: deleted, merged, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `bssids` | array[object] |  | BSSIDs broadcasting the SSID. |
| `channels` | array[integer] |  | Channels where SSID was observed. |
| `created_at` | string |  |  |
| `default_policy` | string |  | Default policy for rogue networks. |
| `first_seen` | integer |  |  |
| `last_seen` | integer |  |  |
| `match` | object |  | Rule specification/match criteria. |
| `rule_id` | string |  | Server-assigned rule ID. Discover via C(state=gathered). |
| `ssid` | string |  | SSID name for the rule. |
| `type` | string |  | Rule type (allow, block, or alert). |
| `updated_at` | string |  |  |

---

### `meraki_appliance_rf_profile`

Manage Meraki appliance rf profile resources. Canonical key: name System key: rf_profile_id Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `name`
- **System key**: `rf_profile_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `assigned` | array[object] |  | Assigned RF profiles. |
| `five_ghz_settings` | object |  | Settings for 5GHz band. |
| `name` | string |  | Name of the profile. Required for create. |
| `per_ssid_settings` | object |  | Per-SSID radio settings by number. |
| `rf_profile_id` | string |  | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `two_four_ghz_settings` | object |  | Settings for 2.4GHz band. |

---

### `meraki_appliance_ssid`

Manage Meraki appliance ssid resources. Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `auth_mode` | string |  | Association control method. |
| `default_vlan_id` | integer |  | VLAN ID associated with this SSID. |
| `enabled` | boolean |  | Whether the SSID is enabled. |
| `encryption_mode` | string |  | PSK encryption mode. |
| `name` | string |  | Name of the SSID. |
| `number` | integer |  | SSID number (0-4). Required for merged, replaced. |
| `psk` | string |  | Passkey (auth_mode is psk). |
| `radius_servers` | array[object] |  | RADIUS 802.1x servers for authentication. |
| `visible` | boolean |  | Whether to advertise or hide this SSID. |
| `wpa_encryption_mode` | string |  | WPA encryption mode. |

---

### `meraki_branding_policy`

Manage Meraki branding policy resources. Canonical key: name System key: branding_policy_id Scope: organization_id

**Metadata**

- **Scope**: `organization_id`
- **Canonical key**: `name`
- **System key**: `branding_policy_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `organization_id` | string | yes | Target organization id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `admin_settings` | object |  | Settings for which kinds of admins this policy applies to. |
| `branding_policy_id` | string |  | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `custom_logo` | object |  | Custom logo properties. |
| `enabled` | boolean |  | Whether the policy is enabled. |
| `help_settings` | object |  | Modifications to Help page features. |
| `name` | string |  | Name of the branding policy. |

---

### `meraki_camera_quality_retention_profile`

Manage Meraki camera quality retention profile resources. Canonical key: name System key: quality_retention_profile_id Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `name`
- **System key**: `quality_retention_profile_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `audio_recording_enabled` | boolean |  | Enable audio recording. |
| `cloud_archive_enabled` | boolean |  | Enable cloud archive. |
| `max_retention_days` | integer |  | Maximum retention days for recordings. |
| `motion_based_retention_enabled` | boolean |  | Enable motion-based retention. |
| `name` | string |  | Name of the quality retention profile. |
| `quality_retention_profile_id` | string |  | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `restricted_bandwidth_mode_enabled` | boolean |  | Enable restricted bandwidth mode. |
| `schedule_id` | string |  | Schedule ID for recording. |
| `smart_retention` | object |  | Smart retention settings. |
| `video_settings` | object |  | Video quality and resolution settings per camera model. |

---

### `meraki_camera_wireless_profile`

Manage Meraki camera wireless profile resources. Canonical key: name System key: wireless_profile_id Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `name`
- **System key**: `wireless_profile_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `identity` | object |  | Identity of the wireless profile (required for create). |
| `name` | string |  | Name of the camera wireless profile. |
| `ssid` | object |  | SSID configuration details. |
| `wireless_profile_id` | string |  | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |

---

### `meraki_config_template`

Manage Meraki config template resources. Canonical key: name System key: config_template_id Scope: organization_id

**Metadata**

- **Scope**: `organization_id`
- **Canonical key**: `name`
- **System key**: `config_template_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `organization_id` | string | yes | Target organization id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config_template_id` | string |  | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `copy_from_network_id` | string |  | Network or template ID to copy configuration from. |
| `name` | string |  | Name of the configuration template. |
| `product_types` | array[string] |  | Product types (e.g. wireless, switch, appliance). |
| `time_zone` | string |  | Timezone of the configuration template. |

---

### `meraki_device`

Manage Meraki device resources. Scope: serial

**Metadata**

- **Scope**: `serial`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `serial` | string | yes | Target serial. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `address` | string |  | Physical address of the device. |
| `floor_plan_id` | string |  | Floor plan to associate with the device. |
| `lat` | number |  | Latitude of the device. |
| `lng` | number |  | Longitude of the device. |
| `move_map_marker` | boolean |  | Set lat/lng from address. |
| `name` | string |  | Name of the device. |
| `notes` | string |  | Notes for the device (max 255 chars). |
| `switch_profile_id` | string |  | Switch template ID to bind to the device. |
| `tags` | array[string] |  | List of tags for the device. |

---

### `meraki_device_management_interface`

Manage Meraki device management interface resources. Scope: serial

**Metadata**

- **Scope**: `serial`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `serial` | string | yes | Target serial. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ddns_hostnames` | object |  | Dynamic DNS hostnames. |
| `wan1` | object |  | WAN 1 settings. |
| `wan2` | object |  | WAN 2 settings (MX devices only). |

---

### `meraki_device_switch_routing`

Manage Meraki device switch routing resources. Canonical key: name System key: interface_id Scope: serial

**Metadata**

- **Scope**: `serial`
- **Canonical key**: `name`
- **System key**: `interface_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `serial` | string | yes | Target serial. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `default_gateway` | string |  | IPv4 default gateway. |
| `dhcp_mode` | string |  | DHCP mode for the interface. |
| `dhcp_relay_server_ips` | array[string] |  | DHCP relay server IPs. |
| `interface_id` | string |  | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `interface_ip` | string |  | IPv4 address. |
| `multicast_routing` | string |  | Multicast routing status. |
| `name` | string |  | Interface name. |
| `ospf_settings` | object |  | IPv4 OSPF settings. |
| `subnet` | string |  | IPv4 subnet. |
| `vlan_id` | integer |  | VLAN ID. |

---

### `meraki_ethernet_port_profile`

Manage Meraki ethernet port profile resources. Canonical key: name System key: profile_id Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `name`
- **System key**: `profile_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `is_default` | boolean |  | Whether this is the default profile. |
| `name` | string |  | AP port profile name. |
| `ports` | array[object] |  | Ports configuration. |
| `profile_id` | string |  | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `serials` | array[string] |  | List of AP serials to assign. |
| `usb_ports` | array[object] |  | USB ports configuration. |

---

### `meraki_facts`

Manage Meraki facts resources. Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `gather_subset` | array[string] |  |  |
| `organization_id` | string |  |  |

---

### `meraki_firewall`

Manage Meraki firewall resources. Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `access` | string |  | Rule for which IPs are allowed to access. |
| `allowed_ips` | array[string] |  | Array of allowed CIDRs. |
| `application_categories` | array[object] |  | L7 application categories and applications. |
| `rules` | array[object] |  | Ordered array of L3 firewall rules. |
| `service` | string |  | Appliance service name. |
| `spoofing_protection` | object |  | Spoofing protection settings. |
| `syslog_default_rule` | boolean |  | Log the special default rule. |

---

### `meraki_firmware_upgrade`

Manage Meraki firmware upgrade resources. Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `products` | object |  | Product-specific upgrade settings (wireless, appliance, switch, camera). |
| `timezone` | string |  | Timezone for the network. |
| `upgrade_window` | object |  | Upgrade window (dayOfWeek, hourOfDay). |

---

### `meraki_floor_plan`

Manage Meraki floor plan resources. Canonical key: name System key: floor_plan_id Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `name`
- **System key**: `floor_plan_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `bottom_left_corner` | object |  | Bottom left corner coordinates. |
| `bottom_right_corner` | object |  | Bottom right corner coordinates. |
| `center` | object |  | Center coordinates (lat/lng) of the floor plan. |
| `floor_number` | number |  | Floor number within the building. |
| `floor_plan_id` | string |  | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `height` | number |  | Height of the floor plan. |
| `image_contents` | string |  | Base64 encoded floor plan image. |
| `image_extension` | string |  | Image format (e.g., png, jpg). |
| `name` | string |  | Name of the floor plan. |
| `top_left_corner` | object |  | Top left corner coordinates. |
| `top_right_corner` | object |  | Top right corner coordinates. |
| `width` | number |  | Width of the floor plan. |

---

### `meraki_group_policy`

Manage Meraki group policy resources. Canonical key: name System key: group_policy_id Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `name`
- **System key**: `group_policy_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `bandwidth` | object |  | Bandwidth settings for clients. |
| `bonjour_forwarding` | object |  | Bonjour forwarding settings. |
| `content_filtering` | object |  | Content filtering settings. |
| `firewall_and_traffic_shaping` | object |  | Firewall and traffic shaping rules. |
| `group_policy_id` | string |  | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `name` | string |  | Name of the group policy. Required for create. |
| `scheduling` | object |  | Schedule for the group policy. |
| `splash_auth_settings` | string |  | Splash authorization bypass setting. |
| `vlan_tagging` | object |  | VLAN tagging settings. |

---

### `meraki_meraki_auth_user`

Manage Meraki meraki auth user resources. Canonical key: email System key: meraki_auth_user_id Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `email`
- **System key**: `meraki_auth_user_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `account_type` | string |  | Authorization type for user. |
| `authorizations` | array[object] |  | User authorization info. |
| `email` | string |  | Email address of the user. |
| `email_password_to_user` | boolean |  | Whether Meraki should email the password to user. |
| `is_admin` | boolean |  | Whether the user is a Dashboard administrator. |
| `meraki_auth_user_id` | string |  | Server-assigned ID, resolved automatically by matching on C(email). Provide only to disambiguate when duplicate emails exist. |
| `name` | string |  | Name of the user. |
| `password` | string |  | Password for the user account. |

---

### `meraki_mqtt_broker`

Manage Meraki mqtt broker resources. Canonical key: name System key: mqtt_broker_id Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `name`
- **System key**: `mqtt_broker_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `authentication` | object |  | Authentication settings. |
| `host` | string |  | Host name or IP address of the MQTT broker. |
| `mqtt_broker_id` | string |  | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `name` | string |  | Name of the MQTT broker. |
| `port` | integer |  | Port for the MQTT broker. |
| `security` | object |  | Security settings. |

---

### `meraki_network_settings`

Manage Meraki network settings resources. Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `custom_pie_chart_items` | array[object] |  | Custom pie chart items for traffic reporting. |
| `fips` | object |  | FIPS options for the network. |
| `local_status_page` | object |  | Local status page authentication options. |
| `local_status_page_enabled` | boolean |  | Enable local device status pages. |
| `mode` | string |  | Traffic analysis mode. |
| `named_vlans` | object |  | Named VLANs options. |
| `remote_status_page_enabled` | boolean |  | Enable access to device status page via LAN IP. |
| `reporting_enabled` | boolean |  | Enable NetFlow traffic reporting. |
| `secure_port` | object |  | SecureConnect options. |

---

### `meraki_org_alert_profile`

Manage Meraki org alert profile resources. System key: alert_config_id Scope: organization_id

**Metadata**

- **Scope**: `organization_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `alert_config_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `organization_id` | string | yes | Target organization id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `alert_condition` | object |  | Conditions that determine if the alert triggers. |
| `alert_config_id` | string |  | Server-assigned config ID. Discover via C(state=gathered). |
| `description` | string |  | User-supplied description of the alert. |
| `enabled` | boolean |  | Whether the alert is enabled. |
| `network_tags` | array[string] |  | Network tags to monitor for the alert. |
| `recipients` | object |  | Recipients that receive the alert. |
| `type` | string |  | The alert type. |

---

### `meraki_org_vpn`

Manage Meraki org vpn resources. Scope: organization_id

**Metadata**

- **Scope**: `organization_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `organization_id` | string | yes | Target organization id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `peers` | array[object] |  | List of third-party VPN peers. |
| `third_party_vpn_peers` | array[object] |  |  |

---

### `meraki_policy_object`

Manage Meraki policy object resources. Canonical key: name System key: policy_object_id Scope: organization_id

**Metadata**

- **Scope**: `organization_id`
- **Canonical key**: `name`
- **System key**: `policy_object_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `organization_id` | string | yes | Target organization id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `category` | string |  | Category of policy object. |
| `cidr` | string |  | CIDR value (for cidr type). |
| `fqdn` | string |  | Fully qualified domain name (for fqdn type). |
| `group_ids` | array[string] |  | IDs of policy object groups this object belongs to. |
| `ip` | string |  | IP address (for ipAndMask type). |
| `mask` | string |  | Subnet mask (for ipAndMask type). |
| `name` | string |  | Name of the policy object. |
| `network_ids` | array[string] |  |  |
| `object_ids` | array[integer] |  |  |
| `policy_object_id` | string |  | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `type` | string |  | Type of policy object. |

---

### `meraki_port`

Manage Meraki port resources. Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `access_policy` | string |  | Access policy name (access ports only). |
| `allowed_vlans` | string |  | Allowed VLANs (comma-delimited or 'all'). |
| `drop_untagged_traffic` | boolean |  | Drop untagged traffic (trunk ports). |
| `enabled` | boolean |  | Whether the port is enabled. |
| `port_id` | string |  | Port ID (e.g., 1, 2, 3, 4). Required for merged, replaced. |
| `type` | string |  | Port type (access or trunk). |
| `vlan` | integer |  | Native VLAN (trunk) or access VLAN. |

---

### `meraki_prefix`

Manage Meraki prefix resources. Canonical key: prefix System key: static_delegated_prefix_id Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `prefix`
- **System key**: `static_delegated_prefix_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | string |  | Identifying description for the prefix. |
| `origin` | object |  | WAN1/WAN2/Independent prefix configuration. |
| `prefix` | string |  | IPv6 prefix/prefix length. |
| `static_delegated_prefix_id` | string |  | Server-assigned ID, resolved automatically by matching on C(prefix). Provide only to disambiguate when duplicate prefixes exist. |

---

### `meraki_saml`

Manage Meraki saml resources. Scope: organization_id

**Metadata**

- **Scope**: `organization_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `organization_id` | string | yes | Target organization id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `consumer_url` | string |  | URL consuming SAML Identity Provider (IdP). |
| `enabled` | boolean |  | Whether SAML SSO is enabled. |
| `slo_logout_url` | string |  | URL for redirect on sign out. |
| `sp_initiated` | object |  | SP-Initiated SSO settings. |
| `sso_login_url` | string |  | URL for redirect to log in again when session expires. |
| `vision_consumer_url` | string |  | URL consuming SAML IdP for Meraki Vision Portal. |
| `x509cert_sha1_fingerprint` | string |  | SHA1 fingerprint of the SAML certificate from IdP. |

---

### `meraki_security`

Manage Meraki security resources. Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `allowed_files` | array[object] |  | Sha256 digests of files permitted by malware engine. |
| `allowed_urls` | array[object] |  | URLs permitted by malware detection engine. |
| `ids_rulesets` | string |  | Intrusion detection ruleset. |
| `mode` | string |  | Intrusion detection mode. |
| `protected_networks` | object |  | Networks included/excluded from detection. |

---

### `meraki_sensor_alert_profile`

Manage Meraki sensor alert profile resources. Canonical key: name System key: id Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `name`
- **System key**: `id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `conditions` | array[object] |  | List of conditions that trigger alerts. |
| `id` | string |  | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `include_sensor_url` | boolean |  | Include dashboard link to sensor in messages. |
| `message` | string |  | Custom message for email and text alerts. |
| `name` | string |  | Name of the sensor alert profile. |
| `recipients` | object |  | Recipients that receive alerts. |
| `schedule` | object |  | Sensor schedule for the alert profile. |
| `serials` | array[string] |  | Device serials assigned to this profile. |

---

### `meraki_ssid`

Manage Meraki ssid resources. Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `auth_mode` | string |  | Authentication mode. |
| `availability_tags` | array[string] |  | AP tags for SSID availability (when available_on_all_aps is false). |
| `available_on_all_aps` | boolean |  | Whether the SSID is broadcast on all APs. |
| `band_selection` | string |  | Band selection for the SSID. |
| `default_vlan_id` | integer |  | Default VLAN ID for all other APs. |
| `enabled` | boolean |  | Whether the SSID is enabled. |
| `encryption_mode` | string |  | Encryption mode for the SSID. |
| `ip_assignment_mode` | string |  | Client IP assignment mode. |
| `min_bitrate` | number |  | Minimum bitrate in Mbps. |
| `name` | string |  | SSID name. |
| `number` | integer |  | SSID number (0-14). Required for merged and replaced. |
| `per_client_bandwidth_limit_down` | integer |  | Per-client download bandwidth limit in Kbps (0 = no limit). |
| `per_client_bandwidth_limit_up` | integer |  | Per-client upload bandwidth limit in Kbps (0 = no limit). |
| `per_ssid_bandwidth_limit_down` | integer |  | Per-SSID download bandwidth limit in Kbps (0 = no limit). |
| `per_ssid_bandwidth_limit_up` | integer |  | Per-SSID upload bandwidth limit in Kbps (0 = no limit). |
| `psk` | string |  | Pre-shared key (for PSK auth). Write-only; not returned by API. |
| `splash_page` | string |  | Splash page type. |
| `use_vlan_tagging` | boolean |  | Whether to use VLAN tagging. |
| `visible` | boolean |  | Whether the SSID is advertised (visible) or hidden. |
| `vlan_id` | integer |  | VLAN ID for VLAN tagging. |
| `wpa_encryption_mode` | string |  | WPA encryption mode. |

---

### `meraki_static_route`

Manage Meraki static route resources. Canonical key: name System key: static_route_id Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `name`
- **System key**: `static_route_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `enabled` | boolean |  | Whether the route is enabled. |
| `fixed_ip_assignments` | object |  | Fixed DHCP IP assignments on the route. |
| `gateway_ip` | string |  | Gateway IP address (next hop). |
| `gateway_vlan_id` | integer |  | Gateway VLAN ID. |
| `ip_version` | integer |  | IP protocol version (4 or 6). |
| `name` | string |  | Name of the route. |
| `reserved_ip_ranges` | array[object] |  | DHCP reserved IP ranges. |
| `static_route_id` | string |  | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `subnet` | string |  | Subnet of the route (e.g., 192.168.1.0/24). |

---

### `meraki_switch_access_policy`

Manage Meraki switch access policy resources. Canonical key: access_policy_number Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `access_policy_number`
- **System key**: `(same as canonical)`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `access_policy_number` | string |  | Access policy number (identifier). |
| `access_policy_type` | string |  | Access type of the policy. |
| `dot1x` | object |  | 802.1X settings. |
| `guest_vlan_id` | integer |  | Guest VLAN ID for unauthorized devices. |
| `host_mode` | string |  | Host mode for the access policy. |
| `name` | string |  | Name of the access policy. |
| `radius_accounting_enabled` | boolean |  | Enable RADIUS accounting. |
| `radius_accounting_servers` | array[object] |  | List of RADIUS accounting servers. |
| `radius_coa_support_enabled` | boolean |  | Enable RADIUS CoA support. |
| `radius_group_attribute` | string |  |  |
| `radius_servers` | array[object] |  | List of RADIUS servers for authentication. |
| `url_redirect_walled_garden_enabled` | boolean |  |  |
| `url_redirect_walled_garden_ranges` | array[string] |  |  |
| `voice_vlan_clients` | boolean |  |  |

---

### `meraki_switch_acl`

Manage Meraki switch acl resources. Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `rules` | array[object] |  | Ordered array of access control list rules. |

---

### `meraki_switch_dhcp_policy`

Manage Meraki switch dhcp policy resources. Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `alerts` | object |  | Email alert settings for DHCP servers. |
| `allowed_servers` | array[string] |  | MAC addresses of DHCP servers to permit. |
| `always_allowed_servers` | array[string] |  | MAC addresses always allowed on the network. |
| `arp_inspection` | object |  | Dynamic ARP Inspection settings. |
| `blocked_servers` | array[string] |  | MAC addresses of DHCP servers to block. |
| `default_policy` | string |  | Default policy for new DHCP servers (allow or block). |

---

### `meraki_switch_link_aggregation`

Manage Meraki switch link aggregation resources. System key: link_aggregation_id Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `link_aggregation_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `link_aggregation_id` | string |  | Server-assigned aggregation ID. Discover via C(state=gathered). |
| `switch_ports` | array[object] |  | Array of switch ports for the aggregation. |
| `switch_profile_ports` | array[object] |  | Array of switch profile ports for creating aggregation. |

---

### `meraki_switch_port`

Manage Meraki switch port resources. Scope: serial

**Metadata**

- **Scope**: `serial`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `serial` | string | yes | Target serial. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `access_policy_number` | integer |  | Access policy number. |
| `access_policy_type` | string |  | Access policy type. |
| `adaptive_policy_group_id` | string |  | Adaptive policy group ID. |
| `allowed_vlans` | string |  | Allowed VLANs (for trunk ports). |
| `dai_trusted` | boolean |  | DAI trusted. |
| `enabled` | boolean |  | Whether the port is enabled. |
| `flexible_stacking_enabled` | boolean |  | Flexible stacking enabled. |
| `isolation_enabled` | boolean |  | Port isolation enabled. |
| `link_negotiation` | string |  | Link speed negotiation. |
| `name` | string |  | Port name. |
| `peer_sgt_capable` | boolean |  | Peer SGT capable. |
| `poe_enabled` | boolean |  | Power over Ethernet enabled. |
| `port_id` | string |  | Port number/ID. |
| `port_schedule_id` | string |  | Port schedule ID. |
| `profile` | object |  | Port profile. |
| `rstp_enabled` | boolean |  | RSTP enabled. |
| `sticky_mac_allow_list` | array[string] |  | Sticky MAC allow list. |
| `sticky_mac_allow_list_limit` | integer |  | Sticky MAC allow list limit. |
| `storm_control_enabled` | boolean |  | Storm control enabled. |
| `stp_guard` | string |  | STP guard setting. |
| `tags` | array[string] |  | Tags for the port. |
| `type` | string |  | Port type. |
| `udld` | string |  | Unidirectional Link Detection action. |
| `vlan` | integer |  | VLAN number. |
| `voice_vlan` | integer |  | Voice VLAN number. |

---

### `meraki_switch_qos_rule`

Manage Meraki switch qos rule resources. System key: qos_rule_id Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `qos_rule_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `dscp` | integer |  | DSCP tag for incoming packet (-1 to trust incoming DSCP). |
| `dst_port` | integer |  | Destination port (TCP/UDP only). |
| `dst_port_range` | string |  | Destination port range (TCP/UDP only). |
| `protocol` | string |  | Protocol (ANY, TCP, or UDP). |
| `qos_rule_id` | string |  | Server-assigned rule ID. Discover via C(state=gathered). |
| `src_port` | integer |  | Source port (TCP/UDP only). |
| `src_port_range` | string |  | Source port range (TCP/UDP only). |
| `vlan` | integer |  | VLAN of incoming packet (null matches any VLAN). |

---

### `meraki_switch_routing`

Manage Meraki switch routing resources. Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `areas` | array[object] |  | OSPF areas. |
| `dead_timer_in_seconds` | integer |  | OSPF dead timer in seconds. |
| `default_settings` | object |  | Default multicast settings for the network. |
| `enabled` | boolean |  | Enable OSPF routing. |
| `hello_timer_in_seconds` | integer |  | OSPF hello timer in seconds. |
| `md5_authentication_enabled` | boolean |  | Enable MD5 authentication for OSPF. |
| `md5_authentication_key` | object |  | MD5 authentication credentials. |
| `overrides` | array[object] |  | Multicast overrides per switch/stack/profile. |
| `v3` | object |  |  |

---

### `meraki_switch_settings`

Manage Meraki switch settings resources. Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `broadcast_threshold` | integer |  | Broadcast storm control threshold. |
| `default_mtu_size` | integer |  | MTU size for the entire network. |
| `enabled` | boolean |  |  |
| `mappings` | array[object] |  | DSCP to CoS mappings. |
| `multicast_threshold` | integer |  | Multicast storm control threshold. |
| `overrides` | array[object] |  | Override MTU for individual switches. |
| `power_exceptions` | array[object] |  | Per-switch power exceptions. |
| `protocols` | array[string] |  |  |
| `switches` | array[object] |  |  |
| `unknown_unicast_threshold` | integer |  | Unknown unicast storm control threshold. |
| `use_combined_power` | boolean |  | Use combined power for secondary power supplies. |
| `vlan_id` | integer |  |  |

---

### `meraki_switch_stack`

Manage Meraki switch stack resources. Canonical key: name System key: switch_stack_id Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `name`
- **System key**: `switch_stack_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `is_monitor_only` | boolean |  | Whether stack is monitor only. |
| `members` | array[object] |  | Members of the stack. |
| `name` | string |  | Name of the switch stack. |
| `serials` | array[string] |  | Serials of switches in the stack. |
| `switch_stack_id` | string |  | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `virtual_mac` | string |  | Virtual MAC address of the switch stack. |

---

### `meraki_switch_stp`

Manage Meraki switch stp resources. Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `rstp_enabled` | boolean |  | Enable RSTP (Rapid Spanning Tree Protocol). |
| `stp_bridge_priority` | array[object] |  | STP bridge priority for switches/stacks or templates. |

---

### `meraki_traffic_shaping`

Manage Meraki traffic shaping resources. Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `active_active_auto_vpn_enabled` | boolean |  | Whether active-active AutoVPN is enabled. |
| `bandwidth_limits` | object |  | Uplink bandwidth limits by interface. |
| `default_rules_enabled` | boolean |  | Whether default traffic shaping rules are enabled. |
| `default_uplink` | string |  | The default uplink (e.g., wan1, wan2). |
| `failover_and_failback` | object |  | WAN failover and failback settings. |
| `global_bandwidth_limits` | object |  | Global per-client bandwidth limit. |
| `load_balancing_enabled` | boolean |  | Whether load balancing is enabled. |
| `rules` | array[object] |  | Array of traffic shaping rules. |
| `vpn_traffic_uplink_preferences` | array[object] |  | Uplink preference rules for VPN traffic. |
| `wan_traffic_uplink_preferences` | array[object] |  | Uplink preference rules for WAN traffic. |

---

### `meraki_vlan`

Manage Meraki vlan resources. Canonical key: vlan_id Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `vlan_id`
- **System key**: `(same as canonical)`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `appliance_ip` | string |  | Appliance IP on the VLAN. |
| `cidr` | string |  | CIDR for template networks. |
| `dhcp_boot_filename` | string |  | DHCP boot filename. |
| `dhcp_boot_next_server` | string |  | DHCP boot next server. |
| `dhcp_boot_options_enabled` | boolean |  | Use DHCP boot options. |
| `dhcp_handling` | string |  | How the appliance handles DHCP requests on this VLAN. |
| `dhcp_lease_time` | string |  | DHCP lease term. |
| `dhcp_options` | array[object] |  | DHCP options for responses. |
| `dhcp_relay_server_ips` | array[string] |  | IPs of DHCP servers to relay requests to. |
| `dns_nameservers` | string |  | DNS nameservers for DHCP responses. |
| `fixed_ip_assignments` | object |  | Fixed IP assignments. |
| `group_policy_id` | string |  | Group policy ID. |
| `ipv6` | object |  | IPv6 configuration. |
| `mandatory_dhcp` | object |  | Mandatory DHCP configuration. |
| `mask` | integer |  | Mask for template networks. |
| `name` | string |  | VLAN name. |
| `reserved_ip_ranges` | array[object] |  | Reserved IP ranges on the VLAN. |
| `subnet` | string |  | Subnet (e.g., '192.168.1.0/24'). |
| `template_vlan_type` | string |  | Type of subnetting for template networks. |
| `vlan_id` | string |  | VLAN ID (1-4094). Required for merged and deleted. |

---

### `meraki_vlan_profile`

Manage Meraki vlan profile resources. Canonical key: iname Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `iname`
- **System key**: `(same as canonical)`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `iname` | string |  | VLAN profile iname (primary key). Required for merged, replaced, deleted. |
| `is_default` | boolean |  | Whether this is the default VLAN profile. |
| `name` | string |  | Name of the profile (1-255 chars). |
| `vlan_groups` | array[object] |  | Array of named VLAN groups. |
| `vlan_names` | array[object] |  | Array of named VLANs. |
| `vlan_profile` | object |  | VLAN profile configuration. |

---

### `meraki_vpn`

Manage Meraki vpn resources. Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `as_number` | integer |  | BGP autonomous system number. |
| `enabled` | boolean |  | Whether VPN is enabled. |
| `hubs` | array[object] |  | List of VPN hubs, in order of preference. |
| `ibgp_hold_timer` | integer |  | iBGP hold time in seconds. |
| `mode` | string |  | Site-to-site VPN mode. |
| `neighbors` | array[object] |  | List of eBGP neighbor configurations. |
| `subnet` | object |  | Configuration of subnet features. |
| `subnets` | array[object] |  | List of subnets and their VPN presence. |

---

### `meraki_warm_spare`

Manage Meraki warm spare resources. Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `(none — Category C)`
- **System key**: `(same as canonical)`
- **Supports delete**: False
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `enabled` | boolean |  | Whether warm spare is enabled. |
| `primary_serial` | string |  | Serial number of the primary appliance. |
| `spare_serial` | string |  | Serial number of the warm spare appliance. |
| `uplink_mode` | string |  | Uplink mode (virtual or public). |
| `virtual_ip1` | string |  | WAN 1 shared IP. |
| `virtual_ip2` | string |  | WAN 2 shared IP. |
| `wan1` | object |  | WAN 1 IP and subnet. |
| `wan2` | object |  | WAN 2 IP and subnet. |

---

### `meraki_webhook`

Manage Meraki webhook resources. Canonical key: name System key: http_server_id Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `name`
- **System key**: `http_server_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `http_server_id` | string |  | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `name` | string |  | Name for easy reference to the HTTP server. |
| `payload_template` | object |  | Payload template for POSTs to the HTTP server. |
| `shared_secret` | string |  | Shared secret included in POSTs to the server. |
| `url` | string |  | URL of the HTTP server. |

---

### `meraki_wireless_rf_profile`

Manage Meraki wireless rf profile resources. Canonical key: name System key: rf_profile_id Scope: network_id

**Metadata**

- **Scope**: `network_id`
- **Canonical key**: `name`
- **System key**: `rf_profile_id`
- **Supports delete**: True
- **Valid states**: deleted, gathered, merged, overridden, replaced

**Top-level input schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `config` | array[object] |  | List of resource configurations. |
| `network_id` | string | yes | Target network id. |
| `state` | string |  | Resource module state. |

**Config item fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ap_band_settings` | object |  |  |
| `band_selection_type` | string |  | Band selection (ssid or ap). |
| `client_balancing_enabled` | boolean |  | Steer clients to best available AP. |
| `five_ghz_settings` | object |  | 5 GHz band settings. |
| `is_indoor_default` | boolean |  | Set as default indoor profile. |
| `is_outdoor_default` | boolean |  | Set as default outdoor profile. |
| `min_bitrate_type` | string |  |  |
| `name` | string |  | Name of the RF profile. Must be unique. |
| `per_ssid_settings` | object |  |  |
| `rf_profile_id` | string |  | Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist. |
| `six_ghz_settings` | object |  | 6 GHz band settings. |
| `transmission` | object |  | Radio transmission settings. |
| `two_four_ghz_settings` | object |  | 2.4 GHz band settings. |

---

---

*Generated by `tools/generate_mcp_docs.py` from User Model introspection.*