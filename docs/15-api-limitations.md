# API Limitations and Their Influence on Module Design

This document explains how Meraki Dashboard API design decisions directly drive which modules support which states, how resources are identified, and where the collection must work around API constraints.

---

## 1. Three Identity Categories

Every resource in the Meraki API falls into one of three identity categories based on how the API identifies individual items. This classification determines how the collection matches user-provided desired state against existing resources.

### Category A — User Key Is the API Key

The user-meaningful identifier (e.g., `vlan_id`, `iname`) is the same value used in the API URL path. No system-generated ID exists. Matching is straightforward: the user provides the key, and it maps directly to the API.

| Module | Canonical Key | Scope | Notes |
|--------|--------------|-------|-------|
| `vlan` | `vlan_id` | network_id | VLAN ID (1-4094) is the API path parameter |
| `vlan_profile` | `iname` | network_id | Internal name is the path parameter |
| `switch_access_policy` | `access_policy_number` | network_id | Policy number is the path parameter |

**Implication**: Full state support. `replaced` and `overridden` work reliably because matching is deterministic.

### Category B — User Key + System-Generated ID

The resource has a user-meaningful field (name, email) and a separate system-generated ID used in API URLs. The collection must first gather existing resources, match by the canonical key, then use the system key for API operations.

| Module | Canonical Key | System Key | Scope |
|--------|--------------|------------|-------|
| `admin` | `email` | `admin_id` | organization_id |
| `appliance_rf_profile` | `name` | `rf_profile_id` | network_id |
| `branding_policy` | `name` | `branding_policy_id` | organization_id |
| `camera_quality_retention_profile` | `name` | `quality_retention_profile_id` | network_id |
| `camera_wireless_profile` | `name` | `wireless_profile_id` | network_id |
| `config_template` | `name` | `config_template_id` | organization_id |
| `device_switch_routing` | `name` | `interface_id` | serial |
| `ethernet_port_profile` | `name` | `profile_id` | network_id |
| `floor_plan` | `name` | `floor_plan_id` | network_id |
| `group_policy` | `name` | `group_policy_id` | network_id |
| `meraki_auth_user` | `email` | `meraki_auth_user_id` | network_id |
| `mqtt_broker` | `name` | `mqtt_broker_id` | network_id |
| `policy_object` | `name` | `policy_object_id` | organization_id |
| `prefix` | `prefix` | `static_delegated_prefix_id` | network_id |
| `sensor_alert_profile` | `name` | `id` | network_id |
| `static_route` | `name` | `static_route_id` | network_id |
| `switch_stack` | `name` | `switch_stack_id` | network_id |
| `webhook` | `name` | `http_server_id` | network_id |
| `wireless_rf_profile` | `name` | `rf_profile_id` | network_id |

**Implication**: The collection must perform a gather-first lookup to resolve the canonical key to the system key before any create/update/delete operation. If two resources share the same canonical key value (e.g., two webhooks named "alerts"), the match is ambiguous.

### Category C — System Key Only (No User-Meaningful Key)

The API provides only a system-generated ID. There is no user-meaningful field guaranteed to be unique. The collection must use content-based matching or positional fallback.

| Module | System Key | Scope | Matching Strategy |
|--------|-----------|-------|-------------------|
| `air_marshal` | `rule_id` | network_id | Content match on rule fields; restricted to `merged`, `replaced`, `deleted` |
| `org_alert_profile` | `alert_config_id` | organization_id | Content match on alert type + filters |
| `switch_link_aggregation` | `link_aggregation_id` | network_id | Content match on port members |
| `switch_qos_rule` | `qos_rule_id` | network_id | Content match on rule fields; positional fallback |

**Implication**: `overridden` state is unreliable for Category C because content-based matching cannot guarantee correct identification when multiple similar items exist. Some Category C modules restrict their valid states. For `replaced`, the collection falls back to positional matching (Nth desired item maps to Nth existing item) when content match fails.

---

## 2. State Restrictions by Archetype

### Full CRUD Resources (27 modules)

These have `SUPPORTS_DELETE = True` and support all five states. They have either a canonical key (Category A/B) or a system key (Category C) for item identification.

**Supported states**: `merged`, `replaced`, `overridden`, `gathered`, `deleted`

Modules: `admin`, `appliance_rf_profile`, `branding_policy`, `camera_quality_retention_profile`, `camera_wireless_profile`, `config_template`, `device_switch_routing`, `ethernet_port_profile`, `floor_plan`, `group_policy`, `meraki_auth_user`, `mqtt_broker`, `org_alert_profile`, `policy_object`, `prefix`, `sensor_alert_profile`, `static_route`, `switch_access_policy`, `switch_link_aggregation`, `switch_qos_rule`, `vlan`, `vlan_profile`, `webhook`, `wireless_rf_profile`

### Singleton Resources (18 modules)

These manage configuration that always exists and cannot be created or deleted — only read and updated. The API exposes GET and PUT but no POST or DELETE.

**Supported states**: `merged`, `replaced`, `overridden`, `gathered` (no `deleted`)

| Module | What It Manages |
|--------|----------------|
| `adaptive_policy` | Adaptive policy ACLs, groups, policies, settings |
| `appliance_ssid` | Appliance SSID settings (fixed number of SSIDs) |
| `device` | Device name, address, tags, notes |
| `device_management_interface` | Management interface IP configuration |
| `facts` | Organization, network, device, inventory data (gathered only) |
| `firewall` | L3/L7/inbound/cellular firewall rules |
| `firmware_upgrade` | Firmware upgrade schedule and staged rollout |
| `network_settings` | Network-level settings (alerts, netflow, SNMP, syslog) |
| `org_vpn` | Organization VPN peers and firewall rules |
| `port` | Appliance port configuration |
| `saml` | SAML/SSO configuration, IdPs, roles |
| `security` | Intrusion detection and malware settings |
| `ssid` | Wireless SSID configuration (14 sub-endpoints) |
| `switch_acl` | Switch access control lists |
| `switch_dhcp_policy` | DHCP server policy and ARP inspection |
| `switch_port` | Switch port configuration |
| `switch_routing` | Multicast, OSPF, rendezvous points |
| `switch_settings` | MTU, storm control, DSCP, alt management |
| `switch_stp` | Spanning tree protocol settings |
| `traffic_shaping` | Traffic shaping rules and uplink bandwidth |
| `vpn` | Site-to-site VPN and BGP configuration |
| `warm_spare` | High availability warm spare settings |

**Why no `deleted`**: The API has no DELETE endpoint for these resources. The configuration always exists; you can modify it but not remove it. A "reset to defaults" operation would require knowing the default values for each resource, which the API does not expose.

### Restricted-State Resources (3 modules)

These have custom state restrictions due to API behavior:

| Module | Valid States | Why Restricted |
|--------|-------------|----------------|
| `switch_stack` | `merged`, `deleted`, `gathered` | Stack membership changes are destructive; `replaced`/`overridden` could cause network outages by removing devices from stacks |
| `air_marshal` | `merged`, `replaced`, `deleted` | No `gathered` as a list endpoint; no `overridden` due to Category C identity issues |

---

## 3. No Shared Schemas

### The Limitation

The Meraki OpenAPI spec (`spec3.json`, v1.67.0, 594 paths) has **no `components/schemas`** section. Every endpoint defines its request and response schemas inline. This is the largest deviation from typical OpenAPI specs.

### Impact on Development

| Area | Impact |
|------|--------|
| **Code generation** | Standard tooling (`datamodel-code-generator`) cannot generate shared models. A custom schema extractor is required to parse inline schemas, group them by entity, and merge request + response fields. |
| **Field discovery** | Each endpoint's fields must be discovered individually. The same logical field (e.g., `name`) may appear in GET, POST, and PUT schemas with slightly different descriptions or constraints. |
| **Response-only fields** | Fields like `id`, `networkId`, `createdAt` appear in response schemas but not request schemas. The collection must identify these to avoid sending read-only fields in PUT/POST requests. |
| **Type inconsistency** | The same field may have different types across endpoints (e.g., `vlanId` as integer in one endpoint and string in another). Transform mixins must normalize these. |

### Workaround

The collection uses a custom extraction pipeline:

1. Parse `spec3.json` and iterate over all paths and operations
2. Group endpoints by resource entity using path-pattern matching rules
3. Extract and merge inline schemas per entity (request union response)
4. Generate User Model dataclass fields from the merged schema
5. Use `tools/generate_model_descriptions.py` to sync field descriptions from module `DOCUMENTATION` into the dataclass metadata

---

## 4. Singleton Consolidation

### The Pattern

Several modules consolidate multiple related API endpoints into a single entity. This is intentional — it provides a unified configuration surface for resources that are logically one thing.

### Examples

| Module | Sub-Endpoints | Consolidation Rationale |
|--------|--------------|------------------------|
| `firewall` | 7 (L3 rules, L7 rules, inbound rules, cellular rules, firewalled services, settings, inbound cellular) | All are aspects of the network's firewall configuration |
| `ssid` | 14 (settings, L3/L7 firewall, traffic shaping, splash, hotspot 2.0, identity PSKs, bonjour, EAP, VPN, schedules, device type policies) | All configure a single SSID's behavior |
| `network_settings` | 6 (settings, alerts, netflow, SNMP, syslog, traffic analysis) | All are network-level configuration |
| `switch_settings` | 5 (MTU, storm control, DSCP, alt management, settings) | All are network-level switch configuration |

### Impact on States

Consolidation creates complexity for `replaced` and `overridden` states:

- **`replaced`**: Must PUT all sub-endpoints for the entity, not just the ones the user specified. Unspecified sub-endpoints must be reset or preserved depending on the resource.
- **`overridden`**: Must gather all sub-endpoints, diff against desired, and potentially reset sub-endpoints that the user did not include in their desired state.
- **API call count**: A single `overridden` operation on `firewall` may require 7 GETs + up to 7 PUTs = 14 API calls minimum. At 10 req/s, this takes ~1.5 seconds before rate limiting.

### Action Batch Mitigation

For multi-endpoint modules, Action Batches (`POST /organizations/{id}/actionBatches`) can execute multiple PUTs atomically:

- Reduces the window of inconsistent state
- Guarantees all-or-nothing for `overridden` operations
- Not all endpoints are batch-eligible (check Meraki documentation per endpoint)

---

## 5. camelCase / snake_case Boundary

### The Boundary

The Meraki API uses camelCase for all field names (`applianceIp`, `dhcpHandling`, `vlanId`). The Ansible collection uses snake_case (`appliance_ip`, `dhcp_handling`, `vlan_id`) to follow Python and Ansible conventions.

### Where Conversion Happens

```
User (snake_case) → Transform Mixin → API (camelCase) → Transform Mixin → User (snake_case)
```

The `_field_mapping` dict on each User Model's transform mixin defines the mapping. Most are simple rename transforms (snake_case ↔ camelCase). Some require structural transforms:

| Transform Type | Example | Complexity |
|----------------|---------|------------|
| Simple rename | `appliance_ip` ↔ `applianceIp` | Auto-generated |
| Nested rename | `dhcp_options[].code` ↔ `dhcpOptions[].code` | Manual mapping |
| Structural | `organizations` (names) ↔ `organizationIds` (IDs) | Custom transform function |
| Type coercion | `vlan_id` (str) ↔ `vlanId` (int) | Field-level coercion |

### Impact

- Every new resource requires a field mapping review
- Complex transforms (names ↔ IDs) require lookup functions in the transform mixin
- Type coercion issues are a common source of bugs (the API may accept both string and integer for the same field but return only one type)

---

## 6. Rate Limiting

### The Constraint

Meraki enforces **10 requests per second per organization**. Exceeding this returns HTTP 429 with a `Retry-After` header.

### Impact by State

| State | Typical API Calls | At 10 req/s |
|-------|-------------------|-------------|
| `gathered` | 1 GET (+ pagination) | < 1s |
| `merged` (single item) | 1 GET + 1 PUT/POST | < 1s |
| `merged` (10 items) | 1 GET + 10 PUT/POST | ~1s |
| `replaced` (singleton, 7 sub-endpoints) | 7 PUT | ~1s |
| `overridden` (10 items, 5 extras) | 1 GET + 5 DELETE + 10 PUT | ~2s |
| `overridden` (firewall, 7 sub-endpoints) | 7 GET + 7 PUT | ~1.5s |

### Mitigation

The `PlatformService` implements:

1. **Retry with backoff**: On 429, sleep for `Retry-After` seconds, then retry (up to 5 attempts)
2. **Action Batches**: Group multiple operations into a single API call where possible
3. **Pagination handling**: Transparently follow `Link` headers for list endpoints

---

## 7. Pagination

### The Mechanism

List endpoints return paginated results. The response includes a `Link` header with the URL for the next page:

```
Link: <https://api.meraki.com/api/v1/networks/N_123/appliance/vlans?startingAfter=100>; rel=next
```

### Impact

- The `gathered` state must auto-paginate to collect all items
- Large networks with hundreds of resources (e.g., switch ports across many switches) may require many paginated requests
- Each page counts against the rate limit
- The collection handles pagination transparently in `PlatformService._paginated_get()`

---

## 8. Summary: Limitation → Design Decision Map

| API Limitation | Design Decision |
|----------------|----------------|
| No shared schemas in OpenAPI spec | Custom schema extraction pipeline; manual field mapping |
| No user key for some resources (Category C) | Content-based matching with positional fallback |
| No DELETE for singletons | `SUPPORTS_DELETE = False`; no `deleted` state |
| camelCase field names | Transform mixins with `_field_mapping` dict |
| 10 req/s rate limit | Retry with backoff; Action Batch support |
| Paginated list responses | Transparent auto-pagination in `gathered` |
| Multiple sub-endpoints per logical resource | Singleton consolidation into single module |
| System-generated IDs (Category B) | Gather-first lookup to resolve canonical → system key |
| No PATCH semantics | Full PUT required; `merged` must send complete object |
| API returns superset of request fields | Response-only field filtering in output validation |
