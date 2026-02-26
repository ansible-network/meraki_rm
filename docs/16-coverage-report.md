# API Coverage Report

Auto-generated from `spec3.json` and User Model introspection.  Regenerate with `python tools/generate_coverage_report.py`.

---

## Summary

| Metric | Value |
|--------|-------|
| OpenAPI spec version | v1.67.0 |
| Total API paths | 594 |
| Total operations (GET/POST/PUT/DELETE) | 866 (471 GET, 157 POST, 175 PUT, 63 DELETE) |
| Paths mapped to a module entity | 187 |
| Paths not mapped (uncovered) | 407 |
| Path coverage | 187/594 (31%) |
| Resource entities (modules) | 48 |
| Entities with mapped paths | 47 |

---

## Presentation Layer Feature Matrix

All three presentation layers (Ansible, MCP server, CLI) share the same 
User Model introspection and PlatformService, so resource coverage is identical.

| Capability | Ansible | MCP Server | CLI |
|------------|---------|------------|-----|
| Resource modules/tools/commands | 48 | 48 | 48 |
| Full CRUD resources | 26 | 26 | 26 |
| Singleton resources | 22 | 22 | 22 |
| State: merged | All | All | All |
| State: gathered | All | All | All |
| State: replaced | 47 | 47 | 47 |
| State: overridden | 46 | 46 | 46 |
| State: deleted | 48 | 48 | 48 |
| Check mode | Yes | N/A | N/A |
| Diff mode | Yes | N/A | N/A |
| Output: JSON | Via callback | Response | `--json` |
| Output: YAML | Native | Response | `--yaml` |
| Output: Table | N/A | N/A | Default |
| Mock server | Molecule | `--mock` | `--mock` |
| Authentication | Inventory vars | Env vars | Env vars |

---

## Per-Domain Coverage

### Appliance

**11 entities, 40 paths covered**

| Entity | Module | Paths | Methods | Category |
|--------|--------|-------|---------|----------|
| `appliance_rf_profile` | `meraki_appliance_rf_profile` | 2 | DELETE, GET, POST, PUT | B |
| `appliance_ssid` | `meraki_appliance_ssid` | 2 | GET, PUT | Singleton |
| `firewall` | `meraki_firewall` | 13 | GET, PUT | Singleton |
| `port` | `meraki_port` | 2 | GET, PUT | Singleton |
| `prefix` | `meraki_prefix` | 2 | DELETE, GET, POST, PUT | B |
| `security` | `meraki_security` | 3 | GET, PUT | Singleton |
| `static_route` | `meraki_static_route` | 2 | DELETE, GET, POST, PUT | B |
| `traffic_shaping` | `meraki_traffic_shaping` | 7 | DELETE, GET, POST, PUT | Singleton |
| `vlan` | `meraki_vlan` | 3 | DELETE, GET, POST, PUT | A |
| `vpn` | `meraki_vpn` | 2 | GET, PUT | Singleton |
| `warm_spare` | `meraki_warm_spare` | 2 | GET, POST, PUT | Singleton |

### Camera/Sensor

**3 entities, 6 paths covered**

| Entity | Module | Paths | Methods | Category |
|--------|--------|-------|---------|----------|
| `camera_quality_retention_profile` | `meraki_camera_quality_retention_profile` | 2 | DELETE, GET, POST, PUT | B |
| `camera_wireless_profile` | `meraki_camera_wireless_profile` | 2 | DELETE, GET, POST, PUT | B |
| `sensor_alert_profile` | `meraki_sensor_alert_profile` | 2 | DELETE, GET, POST, PUT | B |

### Device

**4 entities, 13 paths covered**

| Entity | Module | Paths | Methods | Category |
|--------|--------|-------|---------|----------|
| `device` | `meraki_device` | 2 | GET, PUT | Singleton |
| `device_management_interface` | `meraki_device_management_interface` | 1 | GET, PUT | Singleton |
| `device_switch_routing` | `meraki_device_switch_routing` | 5 | DELETE, GET, POST, PUT | B |
| `switch_port` | `meraki_switch_port` | 5 | GET, POST, PUT | Singleton |

### Network

**8 entities, 38 paths covered**

| Entity | Module | Paths | Methods | Category |
|--------|--------|-------|---------|----------|
| `firmware_upgrade` | `meraki_firmware_upgrade` | 8 | DELETE, GET, POST, PUT | Singleton |
| `floor_plan` | `meraki_floor_plan` | 7 | DELETE, GET, POST, PUT | B |
| `group_policy` | `meraki_group_policy` | 2 | DELETE, GET, POST, PUT | B |
| `meraki_auth_user` | `meraki_meraki_auth_user` | 2 | DELETE, GET, POST, PUT | B |
| `mqtt_broker` | `meraki_mqtt_broker` | 2 | DELETE, GET, POST, PUT | B |
| `network_settings` | `meraki_network_settings` | 7 | GET, PUT | Singleton |
| `vlan_profile` | `meraki_vlan_profile` | 4 | DELETE, GET, POST, PUT | A |
| `webhook` | `meraki_webhook` | 6 | DELETE, GET, POST, PUT | B |

### Organization

**8 entities, 34 paths covered**

| Entity | Module | Paths | Methods | Category |
|--------|--------|-------|---------|----------|
| `adaptive_policy` | `meraki_adaptive_policy` | 8 | DELETE, GET, POST, PUT | Singleton |
| `admin` | `meraki_admin` | 2 | DELETE, GET, POST, PUT | B |
| `branding_policy` | `meraki_branding_policy` | 3 | DELETE, GET, POST, PUT | B |
| `config_template` | `meraki_config_template` | 5 | DELETE, GET, POST, PUT | B |
| `org_alert_profile` | `meraki_org_alert_profile` | 2 | DELETE, GET, POST, PUT | C |
| `org_vpn` | `meraki_org_vpn` | 5 | GET, PUT | Singleton |
| `policy_object` | `meraki_policy_object` | 4 | DELETE, GET, POST, PUT | B |
| `saml` | `meraki_saml` | 5 | DELETE, GET, POST, PUT | Singleton |

### Switching

**9 entities, 31 paths covered**

| Entity | Module | Paths | Methods | Category |
|--------|--------|-------|---------|----------|
| `switch_access_policy` | `meraki_switch_access_policy` | 2 | DELETE, GET, POST, PUT | A |
| `switch_acl` | `meraki_switch_acl` | 1 | GET, PUT | Singleton |
| `switch_dhcp_policy` | `meraki_switch_dhcp_policy` | 4 | DELETE, GET, POST, PUT | Singleton |
| `switch_link_aggregation` | `meraki_switch_link_aggregation` | 2 | DELETE, GET, POST, PUT | C |
| `switch_qos_rule` | `meraki_switch_qos_rule` | 3 | DELETE, GET, POST, PUT | C |
| `switch_routing` | `meraki_switch_routing` | 4 | DELETE, GET, POST, PUT | Singleton |
| `switch_settings` | `meraki_switch_settings` | 5 | GET, PUT | Singleton |
| `switch_stack` | `meraki_switch_stack` | 9 | DELETE, GET, POST, PUT | B |
| `switch_stp` | `meraki_switch_stp` | 1 | GET, PUT | Singleton |

### Wireless

**4 entities, 25 paths covered**

| Entity | Module | Paths | Methods | Category |
|--------|--------|-------|---------|----------|
| `air_marshal` | `meraki_air_marshal` | 4 | DELETE, GET, POST, PUT | C |
| `ethernet_port_profile` | `meraki_ethernet_port_profile` | 4 | DELETE, GET, POST, PUT | B |
| `ssid` | `meraki_ssid` | 15 | DELETE, GET, POST, PUT | Singleton |
| `wireless_rf_profile` | `meraki_wireless_rf_profile` | 2 | DELETE, GET, POST, PUT | B |

---

## Uncovered API Paths

**407 paths** in the OpenAPI spec are not mapped to any module. These are grouped by reason for exclusion.

### API request logs — read-only

3 paths

- `/organizations/{organizationId}/apiRequests` [GET]
- `/organizations/{organizationId}/apiRequests/overview` [GET]
- `/organizations/{organizationId}/apiRequests/overview/responseCodes/byInterval` [GET]

### Administered endpoints (user-identity-scoped)

10 paths

- `/administered/identities/me` [GET]
- `/administered/identities/me/api/keys` [GET]
- `/administered/identities/me/api/keys/generate` [POST]
- `/administered/identities/me/api/keys/{suffix}/revoke` [POST]
- `/administered/licensing/subscription/entitlements` [GET]
- `/administered/licensing/subscription/subscriptions` [GET]
- `/administered/licensing/subscription/subscriptions/claim` [POST]
- `/administered/licensing/subscription/subscriptions/claimKey/validate` [POST]
- `/administered/licensing/subscription/subscriptions/compliance/statuses` [GET]
- `/administered/licensing/subscription/subscriptions/{subscriptionId}/bind` [POST]

### Assurance — monitoring/analytics

9 paths

- `/organizations/{organizationId}/assurance/alerts` [GET]
- `/organizations/{organizationId}/assurance/alerts/overview` [GET]
- `/organizations/{organizationId}/assurance/alerts/overview/byNetwork` [GET]
- `/organizations/{organizationId}/assurance/alerts/overview/byType` [GET]
- `/organizations/{organizationId}/assurance/alerts/overview/historical` [GET]
- `/organizations/{organizationId}/assurance/alerts/restore` [POST]
- `/organizations/{organizationId}/assurance/alerts/taxonomy/categories` [GET]
- `/organizations/{organizationId}/assurance/alerts/taxonomy/types` [GET]
- `/organizations/{organizationId}/assurance/alerts/{id}` [GET]

### Bluetooth client data — read-only

2 paths

- `/networks/{networkId}/bluetoothClients` [GET]
- `/networks/{networkId}/bluetoothClients/{bluetoothClientId}` [GET]

### Change log — read-only

1 paths

- `/organizations/{organizationId}/configurationChanges` [GET]

### Client analytics — read-only monitoring data

27 paths

- `/devices/{serial}/clients` [GET]
- `/networks/{networkId}/appliance/clients/{clientId}/security/events` [GET]
- `/networks/{networkId}/clients` [GET]
- `/networks/{networkId}/clients/applicationUsage` [GET]
- `/networks/{networkId}/clients/bandwidthUsageHistory` [GET]
- `/networks/{networkId}/clients/overview` [GET]
- `/networks/{networkId}/clients/provision` [POST]
- `/networks/{networkId}/clients/usageHistories` [GET]
- `/networks/{networkId}/clients/{clientId}` [GET]
- `/networks/{networkId}/clients/{clientId}/policy` [GET, PUT]
- `/networks/{networkId}/clients/{clientId}/splashAuthorizationStatus` [GET, PUT]
- `/networks/{networkId}/clients/{clientId}/trafficHistory` [GET]
- `/networks/{networkId}/clients/{clientId}/usageHistory` [GET]
- `/networks/{networkId}/wireless/clients/connectionStats` [GET]
- `/networks/{networkId}/wireless/clients/latencyStats` [GET]
- `/networks/{networkId}/wireless/clients/{clientId}/connectionStats` [GET]
- `/networks/{networkId}/wireless/clients/{clientId}/connectivityEvents` [GET]
- `/networks/{networkId}/wireless/clients/{clientId}/latencyHistory` [GET]
- `/networks/{networkId}/wireless/clients/{clientId}/latencyStats` [GET]
- `/organizations/{organizationId}/clients/bandwidthUsageHistory` [GET]
- `/organizations/{organizationId}/clients/overview` [GET]
- `/organizations/{organizationId}/clients/search` [GET]
- `/organizations/{organizationId}/summary/top/clients/byUsage` [GET]
- `/organizations/{organizationId}/summary/top/clients/manufacturers/byUsage` [GET]
- `/organizations/{organizationId}/switch/ports/clients/overview/byDevice` [GET]
- `/organizations/{organizationId}/wireless/clients/overview/byDevice` [GET]
- `/organizations/{organizationId}/wirelessController/clients/overview/history/byDevice/byInterval` [GET]

### Event log — read-only

3 paths

- `/networks/{networkId}/events` [GET]
- `/networks/{networkId}/events/eventTypes` [GET]
- `/organizations/{organizationId}/appliance/security/events` [GET]

### Health data — read-only

1 paths

- `/networks/{networkId}/health/alerts` [GET]

### Insight — monitoring/analytics, not configuration

4 paths

- `/networks/{networkId}/insight/applications/{applicationId}/healthByTime` [GET]
- `/organizations/{organizationId}/insight/applications` [GET]
- `/organizations/{organizationId}/insight/monitoredMediaServers` [GET, POST]
- `/organizations/{organizationId}/insight/monitoredMediaServers/{monitoredMediaServerId}` [DELETE, GET, PUT]

### Live Tools — real-time diagnostics, not state management

18 paths

- `/devices/{serial}/liveTools/arpTable` [POST]
- `/devices/{serial}/liveTools/arpTable/{arpTableId}` [GET]
- `/devices/{serial}/liveTools/cableTest` [POST]
- `/devices/{serial}/liveTools/cableTest/{id}` [GET]
- `/devices/{serial}/liveTools/leds/blink` [POST]
- `/devices/{serial}/liveTools/leds/blink/{ledsBlinkId}` [GET]
- `/devices/{serial}/liveTools/macTable` [POST]
- `/devices/{serial}/liveTools/macTable/{macTableId}` [GET]
- `/devices/{serial}/liveTools/multicastRouting` [POST]
- `/devices/{serial}/liveTools/multicastRouting/{multicastRoutingId}` [GET]
- `/devices/{serial}/liveTools/ping` [POST]
- `/devices/{serial}/liveTools/ping/{id}` [GET]
- `/devices/{serial}/liveTools/pingDevice` [POST]
- `/devices/{serial}/liveTools/pingDevice/{id}` [GET]
- `/devices/{serial}/liveTools/throughputTest` [POST]
- `/devices/{serial}/liveTools/throughputTest/{throughputTestId}` [GET]
- `/devices/{serial}/liveTools/wakeOnLan` [POST]
- `/devices/{serial}/liveTools/wakeOnLan/{wakeOnLanId}` [GET]

### Network health — read-only

1 paths

- `/networks/{networkId}/networkHealth/channelUtilization` [GET]

### Network topology — read-only

2 paths

- `/networks/{networkId}/topology/linkLayer` [GET]
- `/organizations/{organizationId}/switch/ports/topology/discovery/byDevice` [GET]

### OpenAPI spec endpoint — meta/tooling

1 paths

- `/organizations/{organizationId}/openapiSpec` [GET]

### Spaces — emerging feature

2 paths

- `/organizations/{organizationId}/spaces/integrate/status` [GET]
- `/organizations/{organizationId}/spaces/integration/remove` [POST]

### Splash login data — read-only

1 paths

- `/networks/{networkId}/splashLoginAttempts` [GET]

### Summary — read-only aggregate reports

9 paths

- `/organizations/{organizationId}/summary/switch/power/history` [GET]
- `/organizations/{organizationId}/summary/top/appliances/byUtilization` [GET]
- `/organizations/{organizationId}/summary/top/applications/byUsage` [GET]
- `/organizations/{organizationId}/summary/top/applications/categories/byUsage` [GET]
- `/organizations/{organizationId}/summary/top/devices/byUsage` [GET]
- `/organizations/{organizationId}/summary/top/devices/models/byUsage` [GET]
- `/organizations/{organizationId}/summary/top/networks/byStatus` [GET]
- `/organizations/{organizationId}/summary/top/ssids/byUsage` [GET]
- `/organizations/{organizationId}/summary/top/switches/byEnergyUsage` [GET]

### Systems Manager (MDM) — different management paradigm

46 paths

- `/networks/{networkId}/pii/smDevicesForKey` [GET]
- `/networks/{networkId}/pii/smOwnersForKey` [GET]
- `/networks/{networkId}/sm/bypassActivationLockAttempts` [POST]
- `/networks/{networkId}/sm/bypassActivationLockAttempts/{attemptId}` [GET]
- `/networks/{networkId}/sm/devices` [GET]
- `/networks/{networkId}/sm/devices/checkin` [POST]
- `/networks/{networkId}/sm/devices/fields` [PUT]
- `/networks/{networkId}/sm/devices/lock` [POST]
- `/networks/{networkId}/sm/devices/modifyTags` [POST]
- `/networks/{networkId}/sm/devices/move` [POST]
- `/networks/{networkId}/sm/devices/reboot` [POST]
- `/networks/{networkId}/sm/devices/shutdown` [POST]
- `/networks/{networkId}/sm/devices/wipe` [POST]
- `/networks/{networkId}/sm/devices/{deviceId}/cellularUsageHistory` [GET]
- `/networks/{networkId}/sm/devices/{deviceId}/certs` [GET]
- `/networks/{networkId}/sm/devices/{deviceId}/connectivity` [GET]
- `/networks/{networkId}/sm/devices/{deviceId}/desktopLogs` [GET]
- `/networks/{networkId}/sm/devices/{deviceId}/deviceCommandLogs` [GET]
- `/networks/{networkId}/sm/devices/{deviceId}/deviceProfiles` [GET]
- `/networks/{networkId}/sm/devices/{deviceId}/installApps` [POST]
- `/networks/{networkId}/sm/devices/{deviceId}/networkAdapters` [GET]
- `/networks/{networkId}/sm/devices/{deviceId}/performanceHistory` [GET]
- `/networks/{networkId}/sm/devices/{deviceId}/refreshDetails` [POST]
- `/networks/{networkId}/sm/devices/{deviceId}/restrictions` [GET]
- `/networks/{networkId}/sm/devices/{deviceId}/securityCenters` [GET]
- `/networks/{networkId}/sm/devices/{deviceId}/softwares` [GET]
- `/networks/{networkId}/sm/devices/{deviceId}/unenroll` [POST]
- `/networks/{networkId}/sm/devices/{deviceId}/uninstallApps` [POST]
- `/networks/{networkId}/sm/devices/{deviceId}/wlanLists` [GET]
- `/networks/{networkId}/sm/profiles` [GET]
- `/networks/{networkId}/sm/targetGroups` [GET, POST]
- `/networks/{networkId}/sm/targetGroups/{targetGroupId}` [DELETE, GET, PUT]
- `/networks/{networkId}/sm/trustedAccessConfigs` [GET]
- `/networks/{networkId}/sm/userAccessDevices` [GET]
- `/networks/{networkId}/sm/userAccessDevices/{userAccessDeviceId}` [DELETE]
- `/networks/{networkId}/sm/users` [GET]
- `/networks/{networkId}/sm/users/{userId}/deviceProfiles` [GET]
- `/networks/{networkId}/sm/users/{userId}/softwares` [GET]
- `/organizations/{organizationId}/assurance/alerts/dismiss` [POST]
- `/organizations/{organizationId}/sm/admins/roles` [GET, POST]
- `/organizations/{organizationId}/sm/admins/roles/{roleId}` [DELETE, GET, PUT]
- `/organizations/{organizationId}/sm/apnsCert` [GET]
- `/organizations/{organizationId}/sm/sentry/policies/assignments` [PUT]
- `/organizations/{organizationId}/sm/sentry/policies/assignments/byNetwork` [GET]
- `/organizations/{organizationId}/sm/vppAccounts` [GET]
- `/organizations/{organizationId}/sm/vppAccounts/{vppAccountId}` [GET]

### Traffic data — read-only

4 paths

- `/networks/{networkId}/traffic` [GET]
- `/networks/{networkId}/trafficShaping/applicationCategories` [GET]
- `/networks/{networkId}/trafficShaping/dscpTaggingOptions` [GET]
- `/organizations/{organizationId}/appliance/trafficShaping/vpnExclusions/byNetwork` [GET]

### Uplink status — read-only monitoring

8 paths

- `/devices/{serial}/appliance/uplinks/settings` [GET, PUT]
- `/networks/{networkId}/appliance/uplinks/usageHistory` [GET]
- `/organizations/{organizationId}/appliance/uplinks/statuses/overview` [GET]
- `/organizations/{organizationId}/appliance/uplinks/usage/byNetwork` [GET]
- `/organizations/{organizationId}/campusGateway/devices/uplinks/localOverrides/byDevice` [GET]
- `/organizations/{organizationId}/devices/uplinks/addresses/byDevice` [GET]
- `/organizations/{organizationId}/devices/uplinksLossAndLatency` [GET]
- `/organizations/{organizationId}/uplinks/statuses` [GET]

### Wireless controller — read-only monitoring

15 paths

- `/organizations/{organizationId}/wireless/devices/wirelessControllers/byDevice` [GET]
- `/organizations/{organizationId}/wirelessController/availabilities/changeHistory` [GET]
- `/organizations/{organizationId}/wirelessController/connections` [GET]
- `/organizations/{organizationId}/wirelessController/devices/interfaces/l2/byDevice` [GET]
- `/organizations/{organizationId}/wirelessController/devices/interfaces/l2/statuses/changeHistory/byDevice` [GET]
- `/organizations/{organizationId}/wirelessController/devices/interfaces/l2/usage/history/byInterval` [GET]
- `/organizations/{organizationId}/wirelessController/devices/interfaces/l3/byDevice` [GET]
- `/organizations/{organizationId}/wirelessController/devices/interfaces/l3/statuses/changeHistory/byDevice` [GET]
- `/organizations/{organizationId}/wirelessController/devices/interfaces/l3/usage/history/byInterval` [GET]
- `/organizations/{organizationId}/wirelessController/devices/interfaces/packets/overview/byDevice` [GET]
- `/organizations/{organizationId}/wirelessController/devices/interfaces/usage/history/byInterval` [GET]
- `/organizations/{organizationId}/wirelessController/devices/redundancy/failover/history` [GET]
- `/organizations/{organizationId}/wirelessController/devices/redundancy/statuses` [GET]
- `/organizations/{organizationId}/wirelessController/devices/system/utilization/history/byInterval` [GET]
- `/organizations/{organizationId}/wirelessController/overview/byDevice` [GET]

### Other Uncovered Paths

240 paths not mapped to any module or exclusion category. These may be candidates for future modules.

- `/devices/{serial}/appliance/dhcp/subnets` [GET]
- `/devices/{serial}/appliance/performance` [GET]
- `/devices/{serial}/appliance/prefixes/delegated` [GET]
- `/devices/{serial}/appliance/prefixes/delegated/vlanAssignments` [GET]
- `/devices/{serial}/appliance/radio/settings` [GET, PUT]
- `/devices/{serial}/appliance/vmx/authenticationToken` [POST]
- `/devices/{serial}/blinkLeds` [POST]
- `/devices/{serial}/camera/analytics/live` [GET]
- `/devices/{serial}/camera/analytics/overview` [GET]
- `/devices/{serial}/camera/analytics/recent` [GET]
- `/devices/{serial}/camera/analytics/zones` [GET]
- `/devices/{serial}/camera/analytics/zones/{zoneId}/history` [GET]
- `/devices/{serial}/camera/customAnalytics` [GET, PUT]
- `/devices/{serial}/camera/generateSnapshot` [POST]
- `/devices/{serial}/camera/qualityAndRetention` [GET, PUT]
- `/devices/{serial}/camera/sense` [GET, PUT]
- `/devices/{serial}/camera/sense/objectDetectionModels` [GET]
- `/devices/{serial}/camera/video/settings` [GET, PUT]
- `/devices/{serial}/camera/videoLink` [GET]
- `/devices/{serial}/camera/wirelessProfiles` [GET, PUT]
- `/devices/{serial}/cellular/sims` [GET, PUT]
- `/devices/{serial}/cellularGateway/lan` [GET, PUT]
- `/devices/{serial}/cellularGateway/portForwardingRules` [GET, PUT]
- `/devices/{serial}/lldpCdp` [GET]
- `/devices/{serial}/lossAndLatencyHistory` [GET]
- `/devices/{serial}/reboot` [POST]
- `/devices/{serial}/sensor/commands` [GET, POST]
- `/devices/{serial}/sensor/commands/{commandId}` [GET]
- `/devices/{serial}/sensor/relationships` [GET, PUT]
- `/devices/{serial}/switch/warmSpare` [GET, PUT]
- `/devices/{serial}/wireless/alternateManagementInterface/ipv6` [PUT]
- `/devices/{serial}/wireless/bluetooth/settings` [GET, PUT]
- `/devices/{serial}/wireless/connectionStats` [GET]
- `/devices/{serial}/wireless/electronicShelfLabel` [GET, PUT]
- `/devices/{serial}/wireless/latencyStats` [GET]
- `/devices/{serial}/wireless/radio/settings` [GET, PUT]
- `/devices/{serial}/wireless/status` [GET]
- `/devices/{serial}/wireless/zigbee/enrollments` [POST]
- `/devices/{serial}/wireless/zigbee/enrollments/{enrollmentId}` [GET]
- `/networks/{networkId}` [DELETE, GET, PUT]
- `/networks/{networkId}/appliance/connectivityMonitoringDestinations` [GET, PUT]
- `/networks/{networkId}/appliance/contentFiltering` [GET, PUT]
- `/networks/{networkId}/appliance/contentFiltering/categories` [GET]
- `/networks/{networkId}/appliance/sdwan/internetPolicies` [PUT]
- `/networks/{networkId}/appliance/settings` [GET, PUT]
- `/networks/{networkId}/appliance/singleLan` [GET, PUT]
- `/networks/{networkId}/bind` [POST]
- `/networks/{networkId}/camera/schedules` [GET]
- `/networks/{networkId}/campusGateway/clusters` [POST]
- `/networks/{networkId}/campusGateway/clusters/{clusterId}` [PUT]
- `/networks/{networkId}/cellularGateway/connectivityMonitoringDestinations` [GET, PUT]
- `/networks/{networkId}/cellularGateway/dhcp` [GET, PUT]
- `/networks/{networkId}/cellularGateway/subnetPool` [GET, PUT]
- `/networks/{networkId}/cellularGateway/uplink` [GET, PUT]
- `/networks/{networkId}/devices` [GET]
- `/networks/{networkId}/devices/claim` [POST]
- `/networks/{networkId}/devices/claim/vmx` [POST]
- `/networks/{networkId}/devices/remove` [POST]
- `/networks/{networkId}/pii/piiKeys` [GET]
- `/networks/{networkId}/pii/requests` [GET, POST]
- `/networks/{networkId}/pii/requests/{requestId}` [DELETE, GET]
- `/networks/{networkId}/policies/byClient` [GET]
- `/networks/{networkId}/sensor/alerts/current/overview/byMetric` [GET]
- `/networks/{networkId}/sensor/alerts/overview/byMetric` [GET]
- `/networks/{networkId}/sensor/mqttBrokers` [GET]
- `/networks/{networkId}/sensor/mqttBrokers/{mqttBrokerId}` [GET, PUT]
- `/networks/{networkId}/sensor/relationships` [GET]
- `/networks/{networkId}/split` [POST]
- `/networks/{networkId}/switch/dhcp/v4/servers/seen` [GET]
- `/networks/{networkId}/switch/portSchedules` [GET, POST]
- `/networks/{networkId}/switch/portSchedules/{portScheduleId}` [DELETE, PUT]
- `/networks/{networkId}/unbind` [POST]
- `/networks/{networkId}/wireless/alternateManagementInterface` [GET, PUT]
- `/networks/{networkId}/wireless/billing` [GET, PUT]
- `/networks/{networkId}/wireless/bluetooth/settings` [GET, PUT]
- `/networks/{networkId}/wireless/channelUtilizationHistory` [GET]
- `/networks/{networkId}/wireless/clientCountHistory` [GET]
- `/networks/{networkId}/wireless/connectionStats` [GET]
- `/networks/{networkId}/wireless/dataRateHistory` [GET]
- `/networks/{networkId}/wireless/devices/connectionStats` [GET]
- `/networks/{networkId}/wireless/devices/latencyStats` [GET]
- `/networks/{networkId}/wireless/electronicShelfLabel` [GET, PUT]
- `/networks/{networkId}/wireless/electronicShelfLabel/configuredDevices` [GET]
- `/networks/{networkId}/wireless/failedConnections` [GET]
- `/networks/{networkId}/wireless/latencyHistory` [GET]
- `/networks/{networkId}/wireless/latencyStats` [GET]
- `/networks/{networkId}/wireless/location/scanning` [PUT]
- `/networks/{networkId}/wireless/meshStatuses` [GET]
- `/networks/{networkId}/wireless/radio/rrm` [PUT]
- `/networks/{networkId}/wireless/settings` [GET, PUT]
- `/networks/{networkId}/wireless/signalQualityHistory` [GET]
- `/networks/{networkId}/wireless/usageHistory` [GET]
- `/networks/{networkId}/wireless/zigbee` [PUT]
- `/organizations` [GET, POST]
- `/organizations/{organizationId}` [DELETE, GET, PUT]
- `/organizations/{organizationId}/actionBatches` [GET, POST]
- `/organizations/{organizationId}/actionBatches/{actionBatchId}` [DELETE, GET, PUT]
- `/organizations/{organizationId}/appliance/dns/local/profiles` [GET, POST]
- `/organizations/{organizationId}/appliance/dns/local/profiles/assignments` [GET]
- `/organizations/{organizationId}/appliance/dns/local/profiles/assignments/bulkCreate` [POST]
- `/organizations/{organizationId}/appliance/dns/local/profiles/assignments/bulkDelete` [POST]
- `/organizations/{organizationId}/appliance/dns/local/profiles/{profileId}` [DELETE, PUT]
- `/organizations/{organizationId}/appliance/dns/local/records` [GET, POST]
- `/organizations/{organizationId}/appliance/dns/local/records/{recordId}` [DELETE, PUT]
- `/organizations/{organizationId}/appliance/dns/split/profiles` [GET, POST]
- `/organizations/{organizationId}/appliance/dns/split/profiles/assignments` [GET]
- `/organizations/{organizationId}/appliance/dns/split/profiles/assignments/bulkCreate` [POST]
- `/organizations/{organizationId}/appliance/dns/split/profiles/assignments/bulkDelete` [POST]
- `/organizations/{organizationId}/appliance/dns/split/profiles/{profileId}` [DELETE, PUT]
- `/organizations/{organizationId}/appliance/firewall/multicastForwarding/byNetwork` [GET]
- `/organizations/{organizationId}/appliance/security/intrusion` [GET, PUT]
- `/organizations/{organizationId}/appliance/uplink/statuses` [GET]
- `/organizations/{organizationId}/camera/boundaries/areas/byDevice` [GET]
- `/organizations/{organizationId}/camera/boundaries/lines/byDevice` [GET]
- `/organizations/{organizationId}/camera/customAnalytics/artifacts` [GET, POST]
- `/organizations/{organizationId}/camera/customAnalytics/artifacts/{artifactId}` [DELETE, GET]
- `/organizations/{organizationId}/camera/detections/history/byBoundary/byInterval` [GET]
- `/organizations/{organizationId}/camera/onboarding/statuses` [GET, PUT]
- `/organizations/{organizationId}/camera/permissions` [GET]
- `/organizations/{organizationId}/camera/permissions/{permissionScopeId}` [GET]
- `/organizations/{organizationId}/camera/roles` [GET, POST]
- `/organizations/{organizationId}/camera/roles/{roleId}` [DELETE, GET, PUT]
- `/organizations/{organizationId}/campusGateway/clusters` [GET]
- `/organizations/{organizationId}/cellularGateway/esims/inventory` [GET]
- `/organizations/{organizationId}/cellularGateway/esims/inventory/{id}` [PUT]
- `/organizations/{organizationId}/cellularGateway/esims/serviceProviders` [GET]
- `/organizations/{organizationId}/cellularGateway/esims/serviceProviders/accounts` [GET, POST]
- `/organizations/{organizationId}/cellularGateway/esims/serviceProviders/accounts/communicationPlans` [GET]
- `/organizations/{organizationId}/cellularGateway/esims/serviceProviders/accounts/ratePlans` [GET]
- `/organizations/{organizationId}/cellularGateway/esims/serviceProviders/accounts/{accountId}` [DELETE, PUT]
- `/organizations/{organizationId}/cellularGateway/esims/swap` [POST]
- `/organizations/{organizationId}/cellularGateway/esims/swap/{id}` [PUT]
- `/organizations/{organizationId}/cellularGateway/uplink/statuses` [GET]
- `/organizations/{organizationId}/claim` [POST]
- `/organizations/{organizationId}/clone` [POST]
- `/organizations/{organizationId}/devices` [GET]
- `/organizations/{organizationId}/devices/availabilities` [GET]
- `/organizations/{organizationId}/devices/availabilities/changeHistory` [GET]
- `/organizations/{organizationId}/devices/controller/migrations` [GET, POST]
- `/organizations/{organizationId}/devices/details/bulkUpdate` [POST]
- `/organizations/{organizationId}/devices/overview/byModel` [GET]
- `/organizations/{organizationId}/devices/packetCapture/captures` [GET, POST]
- `/organizations/{organizationId}/devices/packetCapture/captures/bulkCreate` [POST]
- `/organizations/{organizationId}/devices/packetCapture/captures/bulkDelete` [POST]
- `/organizations/{organizationId}/devices/packetCapture/captures/{captureId}` [DELETE]
- `/organizations/{organizationId}/devices/packetCapture/captures/{captureId}/downloadUrl/generate` [POST]
- `/organizations/{organizationId}/devices/packetCapture/captures/{captureId}/stop` [POST]
- `/organizations/{organizationId}/devices/packetCapture/schedules` [GET, POST]
- `/organizations/{organizationId}/devices/packetCapture/schedules/reorder` [POST]
- `/organizations/{organizationId}/devices/packetCapture/schedules/{scheduleId}` [DELETE, PUT]
- `/organizations/{organizationId}/devices/powerModules/statuses/byDevice` [GET]
- `/organizations/{organizationId}/devices/provisioning/statuses` [GET]
- `/organizations/{organizationId}/devices/statuses` [GET]
- `/organizations/{organizationId}/devices/statuses/overview` [GET]
- `/organizations/{organizationId}/devices/system/memory/usage/history/byInterval` [GET]
- `/organizations/{organizationId}/earlyAccess/features` [GET]
- `/organizations/{organizationId}/earlyAccess/features/optIns` [GET, POST]
- `/organizations/{organizationId}/earlyAccess/features/optIns/{optInId}` [DELETE, GET, PUT]
- `/organizations/{organizationId}/firmware/upgrades` [GET]
- `/organizations/{organizationId}/firmware/upgrades/byDevice` [GET]
- `/organizations/{organizationId}/floorPlans/autoLocate/devices` [GET]
- `/organizations/{organizationId}/floorPlans/autoLocate/statuses` [GET]
- `/organizations/{organizationId}/integrations/xdr/networks` [GET]
- `/organizations/{organizationId}/integrations/xdr/networks/disable` [POST]
- `/organizations/{organizationId}/integrations/xdr/networks/enable` [POST]
- `/organizations/{organizationId}/inventory/claim` [POST]
- `/organizations/{organizationId}/inventory/devices` [GET]
- `/organizations/{organizationId}/inventory/devices/eox/overview` [GET]
- `/organizations/{organizationId}/inventory/devices/swaps/bulk` [POST]
- `/organizations/{organizationId}/inventory/devices/swaps/bulk/{id}` [GET]
- `/organizations/{organizationId}/inventory/onboarding/cloudMonitoring/exportEvents` [POST]
- `/organizations/{organizationId}/inventory/onboarding/cloudMonitoring/imports` [GET, POST]
- `/organizations/{organizationId}/inventory/onboarding/cloudMonitoring/networks` [GET]
- `/organizations/{organizationId}/inventory/onboarding/cloudMonitoring/prepare` [POST]
- `/organizations/{organizationId}/inventory/orders/claim` [POST]
- `/organizations/{organizationId}/inventory/orders/preview` [POST]
- `/organizations/{organizationId}/inventory/release` [POST]
- `/organizations/{organizationId}/licenses` [GET]
- `/organizations/{organizationId}/licenses/assignSeats` [POST]
- `/organizations/{organizationId}/licenses/move` [POST]
- `/organizations/{organizationId}/licenses/moveSeats` [POST]
- `/organizations/{organizationId}/licenses/overview` [GET]
- `/organizations/{organizationId}/licenses/renewSeats` [POST]
- `/organizations/{organizationId}/licenses/{licenseId}` [GET, PUT]
- `/organizations/{organizationId}/licensing/coterm/licenses` [GET]
- `/organizations/{organizationId}/licensing/coterm/licenses/move` [POST]
- `/organizations/{organizationId}/loginSecurity` [GET, PUT]
- `/organizations/{organizationId}/networks` [GET, POST]
- `/organizations/{organizationId}/networks/combine` [POST]
- `/organizations/{organizationId}/networks/moves` [GET, POST]
- `/organizations/{organizationId}/policies/assignments/byClient` [GET]
- `/organizations/{organizationId}/sensor/gateways/connections/latest` [GET]
- `/organizations/{organizationId}/sensor/readings/history` [GET]
- `/organizations/{organizationId}/sensor/readings/latest` [GET]
- `/organizations/{organizationId}/snmp` [GET, PUT]
- `/organizations/{organizationId}/splash/assets/{id}` [DELETE, GET]
- `/organizations/{organizationId}/splash/themes` [GET, POST]
- `/organizations/{organizationId}/splash/themes/{id}` [DELETE]
- `/organizations/{organizationId}/splash/themes/{themeIdentifier}/assets` [POST]
- `/organizations/{organizationId}/switch/devices/clone` [POST]
- `/organizations/{organizationId}/switch/ports/bySwitch` [GET]
- `/organizations/{organizationId}/switch/ports/overview` [GET]
- `/organizations/{organizationId}/switch/ports/statuses/bySwitch` [GET]
- `/organizations/{organizationId}/switch/ports/usage/history/byDevice/byInterval` [GET]
- `/organizations/{organizationId}/webhooks/alertTypes` [GET]
- `/organizations/{organizationId}/webhooks/callbacks/statuses/{callbackId}` [GET]
- `/organizations/{organizationId}/webhooks/logs` [GET]
- `/organizations/{organizationId}/wireless/airMarshal/rules` [GET]
- `/organizations/{organizationId}/wireless/airMarshal/settings/byNetwork` [GET]
- `/organizations/{organizationId}/wireless/devices/channelUtilization/byDevice` [GET]
- `/organizations/{organizationId}/wireless/devices/channelUtilization/byNetwork` [GET]
- `/organizations/{organizationId}/wireless/devices/channelUtilization/history/byDevice/byInterval` [GET]
- `/organizations/{organizationId}/wireless/devices/channelUtilization/history/byNetwork/byInterval` [GET]
- `/organizations/{organizationId}/wireless/devices/ethernet/statuses` [GET]
- `/organizations/{organizationId}/wireless/devices/packetLoss/byClient` [GET]
- `/organizations/{organizationId}/wireless/devices/packetLoss/byDevice` [GET]
- `/organizations/{organizationId}/wireless/devices/packetLoss/byNetwork` [GET]
- `/organizations/{organizationId}/wireless/devices/power/mode/history` [GET]
- `/organizations/{organizationId}/wireless/devices/radsec/certificates/authorities` [GET, POST, PUT]
- `/organizations/{organizationId}/wireless/devices/radsec/certificates/authorities/crls` [GET]
- `/organizations/{organizationId}/wireless/devices/radsec/certificates/authorities/crls/deltas` [GET]
- `/organizations/{organizationId}/wireless/devices/system/cpu/load/history` [GET]
- `/organizations/{organizationId}/wireless/location/scanning/byNetwork` [GET]
- `/organizations/{organizationId}/wireless/location/scanning/receivers` [GET, POST]
- `/organizations/{organizationId}/wireless/location/scanning/receivers/{receiverId}` [DELETE, PUT]
- `/organizations/{organizationId}/wireless/mqtt/settings` [GET, PUT]
- `/organizations/{organizationId}/wireless/radio/autoRf/channels/recalculate` [POST]
- `/organizations/{organizationId}/wireless/radio/rrm/byNetwork` [GET]
- `/organizations/{organizationId}/wireless/rfProfiles/assignments/byDevice` [GET]
- `/organizations/{organizationId}/wireless/ssids/firewall/isolation/allowlist/entries` [GET, POST]
- `/organizations/{organizationId}/wireless/ssids/firewall/isolation/allowlist/entries/{entryId}` [DELETE, PUT]
- `/organizations/{organizationId}/wireless/ssids/openRoaming/byNetwork` [GET]
- `/organizations/{organizationId}/wireless/ssids/statuses/byDevice` [GET]
- `/organizations/{organizationId}/wireless/zigbee/byNetwork` [GET]
- `/organizations/{organizationId}/wireless/zigbee/devices` [GET]
- `/organizations/{organizationId}/wireless/zigbee/devices/{id}` [PUT]
- `/organizations/{organizationId}/wireless/zigbee/disenrollments` [POST]
- `/organizations/{organizationId}/wireless/zigbee/disenrollments/{disenrollmentId}` [GET]
- `/organizations/{organizationId}/wireless/zigbee/doorLocks` [GET]
- `/organizations/{organizationId}/wireless/zigbee/doorLocks/{doorLockId}` [PUT]

---

## Module State Summary

| Module | Scope | Canonical Key | System Key | Category | States |
|--------|-------|---------------|------------|----------|--------|
| `adaptive_policy` | `organization_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `admin` | `organization_id` | `email` | `admin_id` | B | deleted, gathered, merged, overridden, replaced |
| `air_marshal` | `network_id` | — | `rule_id` | C | deleted, merged, replaced |
| `appliance_rf_profile` | `network_id` | `name` | `rf_profile_id` | B | deleted, gathered, merged, overridden, replaced |
| `appliance_ssid` | `network_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `branding_policy` | `organization_id` | `name` | `branding_policy_id` | B | deleted, gathered, merged, overridden, replaced |
| `camera_quality_retention_profile` | `network_id` | `name` | `quality_retention_profile_id` | B | deleted, gathered, merged, overridden, replaced |
| `camera_wireless_profile` | `network_id` | `name` | `wireless_profile_id` | B | deleted, gathered, merged, overridden, replaced |
| `config_template` | `organization_id` | `name` | `config_template_id` | B | deleted, gathered, merged, overridden, replaced |
| `device` | `serial` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `device_management_interface` | `serial` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `device_switch_routing` | `serial` | `name` | `interface_id` | B | deleted, gathered, merged, overridden, replaced |
| `ethernet_port_profile` | `network_id` | `name` | `profile_id` | B | deleted, gathered, merged, overridden, replaced |
| `facts` | `network_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `firewall` | `network_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `firmware_upgrade` | `network_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `floor_plan` | `network_id` | `name` | `floor_plan_id` | B | deleted, gathered, merged, overridden, replaced |
| `group_policy` | `network_id` | `name` | `group_policy_id` | B | deleted, gathered, merged, overridden, replaced |
| `meraki_auth_user` | `network_id` | `email` | `meraki_auth_user_id` | B | deleted, gathered, merged, overridden, replaced |
| `mqtt_broker` | `network_id` | `name` | `mqtt_broker_id` | B | deleted, gathered, merged, overridden, replaced |
| `network_settings` | `network_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `org_alert_profile` | `organization_id` | — | `alert_config_id` | C | deleted, gathered, merged, overridden, replaced |
| `org_vpn` | `organization_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `policy_object` | `organization_id` | `name` | `policy_object_id` | B | deleted, gathered, merged, overridden, replaced |
| `port` | `network_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `prefix` | `network_id` | `prefix` | `static_delegated_prefix_id` | B | deleted, gathered, merged, overridden, replaced |
| `saml` | `organization_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `security` | `network_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `sensor_alert_profile` | `network_id` | `name` | `id` | B | deleted, gathered, merged, overridden, replaced |
| `ssid` | `network_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `static_route` | `network_id` | `name` | `static_route_id` | B | deleted, gathered, merged, overridden, replaced |
| `switch_access_policy` | `network_id` | `access_policy_number` | — | A | deleted, gathered, merged, overridden, replaced |
| `switch_acl` | `network_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `switch_dhcp_policy` | `network_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `switch_link_aggregation` | `network_id` | — | `link_aggregation_id` | C | deleted, gathered, merged, overridden, replaced |
| `switch_port` | `serial` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `switch_qos_rule` | `network_id` | — | `qos_rule_id` | C | deleted, gathered, merged, overridden, replaced |
| `switch_routing` | `network_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `switch_settings` | `network_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `switch_stack` | `network_id` | `name` | `switch_stack_id` | B | deleted, gathered, merged |
| `switch_stp` | `network_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `traffic_shaping` | `network_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `vlan` | `network_id` | `vlan_id` | — | A | deleted, gathered, merged, overridden, replaced |
| `vlan_profile` | `network_id` | `iname` | — | A | deleted, gathered, merged, overridden, replaced |
| `vpn` | `network_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `warm_spare` | `network_id` | — | — | Singleton | deleted, gathered, merged, overridden, replaced |
| `webhook` | `network_id` | `name` | `http_server_id` | B | deleted, gathered, merged, overridden, replaced |
| `wireless_rf_profile` | `network_id` | `name` | `rf_profile_id` | B | deleted, gathered, merged, overridden, replaced |

---

*Generated by `tools/generate_coverage_report.py` from `spec3.json` and User Model introspection.*