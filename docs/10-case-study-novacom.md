# Case Study: NovaCom Networks

## Company Overview

NovaCom Networks is a cloud-managed network infrastructure provider. Their platform manages wireless access points, managed switches, security appliances, and cameras/sensors through a unified cloud dashboard.

**Products:**
- Wireless access points (enterprise Wi-Fi)
- Managed switches (L2/L3)
- Security appliances (firewalls, VPN concentrators)
- Cameras and environmental sensors

**Management hierarchy:**
- **Organizations** -- top-level tenant (a company or business unit)
- **Sites** -- physical locations within an organization
- **Networks** -- logical network segments within a site
- **Devices** -- individual hardware (APs, switches, appliances, cameras)

**API:** NovaCom Dashboard API
- RESTful, OpenAPI 3.0 specification
- Base URL: `https://api.novacom.io/v1/`
- Authentication: API key in header (`X-NovaCom-API-Key`)
- Rate limiting: 10 requests/second per organization
- camelCase parameter naming throughout
- Deep endpoint hierarchy (paths up to 7 segments)
- Mix of configuration and monitoring endpoints (~500 total)
- Action Batch support for atomic multi-operation transactions

---

## Current State: The Endpoint Explosion

The existing `novacom.dashboard` Ansible collection contains **~500 modules**, the direct result of a 1:1 mapping between NovaCom Dashboard API endpoints and Ansible plugins.

### The Symptoms

**Fragmentation:** Configuring a single SSID requires interacting with multiple modules:
- `novacom.dashboard.networks_wireless_ssids` -- basic settings
- `novacom.dashboard.networks_wireless_ssids_psk` -- PSK configuration
- `novacom.dashboard.networks_wireless_ssids_firewall_l3_rules` -- L3 firewall rules
- `novacom.dashboard.networks_wireless_ssids_firewall_l7_rules` -- L7 firewall rules
- `novacom.dashboard.networks_wireless_ssids_traffic_shaping` -- QoS/shaping
- `novacom.dashboard.networks_wireless_ssids_splash_settings` -- captive portal

**State poverty:** Most modules only support `present` and `absent`. They lack the `overridden` and `replaced` states critical for network compliance. There is no way to say "only these SSIDs should exist."

**Chatty transactions:** Updating an SSID's name and its firewall rules requires two separate, sequential API calls, increasing the risk of rate-limiting and partial failures.

**API naming leakage:** Argument names mirror the API's camelCase and internal terminology rather than Ansible's snake_case and industry-standard naming:
- `authMode` instead of `auth_mode`
- `splashPage` instead of `splash_page`
- `bandSelection` instead of `band_selection`
- `perClientBandwidthLimitUp` instead of `per_client_bandwidth_limit_up`

### Real-World Example: SSID Management

**Current "endpoint" approach** -- setting up a secure guest Wi-Fi:

```yaml
- name: Configure SSID basic settings
  novacom.dashboard.networks_wireless_ssids:
    networkId: "N_12345"
    number: 1
    name: "Guest-Wi-Fi"
    enabled: true

- name: Configure SSID PSK
  novacom.dashboard.networks_wireless_ssids_psk:
    networkId: "N_12345"
    number: 1
    psk: "secret123"

- name: Configure L3 firewall rules
  novacom.dashboard.networks_wireless_ssids_firewall_l3_rules:
    networkId: "N_12345"
    number: 1
    rules:
      - policy: deny
        protocol: tcp
        destPort: "80"
        destCidr: "0.0.0.0/0"
```

Three tasks. Three modules. Three API calls. camelCase parameters. No convergence. No state comparison. If the SSID already has the right name, the module calls PUT anyway.

**Proposed "resource module" approach:**

```yaml
- name: Manage guest SSID
  novacom.dashboard.novacom_wireless_ssid:
    network_id: "N_12345"
    config:
      - number: 1
        name: "Guest-Wi-Fi"
        enabled: true
        auth_mode: "psk"
        psk: "secret123"
        l3_firewall_rules:
          - policy: deny
            protocol: tcp
            dest_port: "80"
            dest_cidr: "0.0.0.0/0"
    state: overridden
```

One task. One module. One entity. Full state management. snake_case. The module gathers current state, diffs against desired, and only makes the API calls needed. `state: overridden` means any unlisted SSIDs are removed -- compliance enforcement in a single declaration.

---

## Coverage Analysis

### Target Module Count

| Metric | Current | Target |
|--------|---------|--------|
| Total modules | ~500 | 42-50 |
| Modules per entity | ~10 (avg) | 1 |
| Configuration coverage | ~35% of endpoints | ~98% of configurable surface |
| Monitoring endpoints | Wrapped as modules | Excluded (use `novacom_facts` or direct API) |

The target is **42-50 resource modules** covering ~98% of the configurable surface area. The remaining ~65% of current modules wrap monitoring, analytics, and one-shot action endpoints that do not represent persistent configuration state and should not be resource modules.

### Configuration vs. Monitoring

Not every API endpoint belongs in a resource module. The distinction:

- **Configuration endpoints** (resource module territory): Manage persistent state. VLANs, SSIDs, firewall rules, port configurations, admin accounts. These have a lifecycle -- they are created, read, updated, and deleted. They benefit from convergence logic.

- **Monitoring endpoints** (not resource modules): Return point-in-time data. Client counts, traffic statistics, event logs, device status. These are read-only, have no lifecycle, and cannot be "converged." They belong in a `novacom_facts` module or are accessed via the API directly.

- **Action endpoints** (not resource modules): Trigger one-shot operations. Reboot device, blink LEDs, generate snapshot. These are imperative, not declarative. They may warrant simple action modules, but they are not resource modules.

### Domain Breakdown

| Domain | Current Modules | Target Modules | Key Resources |
|--------|----------------|----------------|---------------|
| **Organizations** | ~40 | 5-6 | Admin accounts, SAML, licenses, policy objects, alerts |
| **Sites** | ~30 | 4-5 | Site settings, firmware, group policies, floor plans |
| **Wireless** | ~60 | 3-4 | SSIDs, RF profiles, Bluetooth settings |
| **Appliance** | ~80 | 10-12 | VLANs, firewall rules, VPN, traffic shaping, static routes, content filtering, 1:1 NAT, port forwarding |
| **Switching** | ~50 | 6-8 | Switch ports, STP, ACLs, DHCP policies, stacking, routing interfaces |
| **Systems Manager** | ~40 | 5-6 | Profiles, device tags, geofencing |
| **Camera/Sensors** | ~30 | 3-4 | Quality/retention, schedules, wireless profiles, sensor alerts |
| **Common** | ~170 | 2-3 | Device settings, `novacom_facts`, management interface |

**Total: ~500 current modules --> 42-50 resource modules**

### Efficiency Analysis

- **~80% straightforward:** Simple entity aggregation. Group sub-endpoints by root resource, build the `config` argspec, implement state logic. Agent-automatable.
- **~20% complex:** SSIDs (6 sub-endpoints), switch ports (port-level + stack-level + routing), appliance VPN (site-to-site + client), content filtering (categories + URL lists). Require careful hoisting logic and domain knowledge.

---

## Module Map

### Wireless Domain

| Module | Aggregated Endpoints | Primary Key | Hoisted Fields |
|--------|---------------------|-------------|----------------|
| `novacom_wireless_ssid` | `PUT /networks/{id}/wireless/ssids/{num}`, `PUT .../firewall/l3FirewallRules`, `PUT .../firewall/l7FirewallRules`, `PUT .../trafficShaping/rules`, `PUT .../splash/settings`, `GET .../hotspot20` | `number` | `l3_firewall_rules`, `l7_firewall_rules`, `traffic_shaping_rules`, `splash_settings`, `hotspot20` |
| `novacom_wireless_rf_profile` | `POST/PUT/DELETE /networks/{id}/wireless/rfProfiles/{rfProfileId}` | `rf_profile_id` | -- |
| `novacom_wireless_bluetooth` | `PUT /networks/{id}/wireless/bluetooth/settings` | (singleton) | -- |

**25 endpoints --> 3 modules.** The SSID module is the most complex, aggregating 6 sub-endpoint paths into a single entity.

### Appliance Domain

| Module | Aggregated Endpoints | Primary Key | Notes |
|--------|---------------------|-------------|-------|
| `novacom_appliance_vlan` | `POST/PUT/DELETE /networks/{id}/appliance/vlans/{vlanId}` | `vlan_id` | DHCP settings hoisted in |
| `novacom_appliance_firewall` | `PUT .../firewall/l3FirewallRules`, `PUT .../firewall/l7FirewallRules` | (singleton per network) | L3 + L7 in one module |
| `novacom_appliance_vpn_s2s` | `PUT /networks/{id}/appliance/vpn/siteToSiteVpn` | (singleton) | Site-to-site VPN |
| `novacom_appliance_vpn_client` | `PUT /networks/{id}/appliance/vpn/clientVpn` | (singleton) | Client VPN |
| `novacom_appliance_traffic_shaping` | `PUT .../trafficShaping`, `PUT .../trafficShaping/rules`, `PUT .../trafficShaping/uplinkBandwidth` | (singleton) | Rules + bandwidth |
| `novacom_appliance_static_route` | `POST/PUT/DELETE .../staticRoutes/{staticRouteId}` | `route_id` | -- |
| `novacom_appliance_content_filtering` | `PUT .../contentFiltering` | (singleton) | Categories + URL lists |
| `novacom_appliance_nat` | `PUT .../firewall/oneToOneNatRules`, `PUT .../firewall/portForwardingRules` | (singleton) | 1:1 NAT + port forwarding |

**~40 endpoints --> 8 modules.**

### Switching Domain

| Module | Aggregated Endpoints | Primary Key | Notes |
|--------|---------------------|-------------|-------|
| `novacom_switch_port` | `PUT /devices/{serial}/switch/ports/{portId}` | `port_id` (per device) | Per-device port config |
| `novacom_switch_stp` | `PUT /networks/{id}/switch/stp` | (singleton) | STP settings |
| `novacom_switch_acl` | `PUT /networks/{id}/switch/accessControlLists` | (singleton) | ACL rules |
| `novacom_switch_dhcp_policy` | `PUT /networks/{id}/switch/dhcpServerPolicy` | (singleton) | DHCP server policy |
| `novacom_switch_stack` | `POST/PUT/DELETE .../switch/stacks/{stackId}`, `.../stacks/{stackId}/routing/interfaces` | `stack_id` | Stacking + routing |
| `novacom_switch_routing` | `POST/PUT/DELETE /devices/{serial}/switch/routing/interfaces/{interfaceId}` | `interface_id` | L3 interfaces |

**~50 endpoints --> 6 modules.**

### Organization and Site Domain

| Module | Scope | Notes |
|--------|-------|-------|
| `novacom_organization` | Organization CRUD | Name, licensing, API settings |
| `novacom_organization_admin` | Admin user management | CRUD + RBAC |
| `novacom_organization_saml` | SAML/SSO configuration | IdP settings, role mappings |
| `novacom_organization_policy_object` | Reusable policy objects | IP groups, FQDN groups |
| `novacom_site` | Site CRUD + settings | Timezone, firmware, group policies |
| `novacom_site_alert` | Alert settings | Alert types, recipients, thresholds |

### Common

| Module | Scope | Notes |
|--------|-------|-------|
| `novacom_device` | Per-device settings | Name, tags, address, notes |
| `novacom_facts` | Gather facts | Read-only: device inventory, network topology, org metadata |

---

## Implementation Roadmap

### Phase 1: Foundation (One-time)

Build the core SDK: BaseTransformMixin, convergence engine, API client, multiprocess manager, code generators. See [06-foundation-components.md](06-foundation-components.md).

**Estimated effort:** 8-12 hours

### Phase 2: High-Value Resources (Sprint 1)

Start with the modules that deliver the most impact:

1. `novacom_appliance_vlan` -- straightforward, high usage, good proving ground
2. `novacom_wireless_ssid` -- complex (6 sub-endpoints), demonstrates full pattern
3. `novacom_switch_port` -- per-device scoping, common use case
4. `novacom_organization_admin` -- RBAC, demonstrates name-to-ID transforms
5. `novacom_facts` -- read-only gathered state, useful immediately

**Estimated effort:** 2-4 hours per module (simple), 4-6 hours (complex)

### Phase 3: Broad Coverage (Sprint 2-3)

Remaining modules in domain order. Most are straightforward (80% category) and can be agent-assisted.

### Phase 4: Advanced Features

- Action Batch integration (atomic multi-endpoint transactions)
- Check mode / diff mode support
- Bulk operations
- Inventory plugin for device discovery

---

## Complexity Analysis for Agents

| Aspect | Agent Can Handle | Human Required |
|--------|-----------------|----------------|
| Schema extraction from OpenAPI | Yes | -- |
| User model argspec generation | Yes | Review naming choices |
| Simple 1:1 field mapping | Yes | -- |
| Multi-endpoint aggregation (mechanical) | Yes | Review entity boundaries |
| Name-to-ID transform boilerplate | Yes | Verify lookup API paths |
| Unit test scaffolding | Yes | -- |
| Semantic term normalization | No | `bandSelection` --> `band_selection` vs `radio_band`? |
| State machine logic (e.g., SSID auth modes) | No | Auth mode changes may require field resets |
| Conditional field dependencies | No | `auth_mode: psk` requires `psk` field, `auth_mode: radius` requires `radius_servers` |
| `overridden` state edge cases | No | What does "remove all SSIDs" mean for SSID 0 (default)? |

**Rule of thumb:** If the mapping is mechanical (field A in user model maps to field B in API), the agent handles it. If the mapping requires domain knowledge (what does this field *mean* and when is it valid), a human reviews.

---

## Action Batch Support

The NovaCom Dashboard API supports **Action Batches** -- atomic transactions that group multiple API calls into a single all-or-nothing operation.

```
POST /organizations/{orgId}/actionBatches
{
  "confirmed": true,
  "synchronous": true,
  "actions": [
    {"resource": "/networks/N_123/appliance/vlans", "operation": "create", "body": {...}},
    {"resource": "/networks/N_123/appliance/vlans/100/...", "operation": "update", "body": {...}}
  ]
}
```

Resource modules that aggregate multiple endpoints (like `novacom_wireless_ssid` with 6 sub-endpoints) should use Action Batches when:
- The `state` is `overridden` or `replaced` (multi-step updates)
- Multiple instances are being modified in a single task
- Atomicity matters (partial application would leave inconsistent state)

The convergence engine's `planner` component decides whether to use direct API calls or batch them based on the operation plan.
