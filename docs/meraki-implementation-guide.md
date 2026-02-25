# Meraki Implementation Guide

This document maps the generic resource-module SDK pattern (documented using NovaCom as a fictitious example) to the **Cisco Meraki Dashboard API**. It covers namespace conventions, API-specific adaptations, the complete module map (~45 modules), schema extraction strategy for the Meraki OpenAPI spec, and implementation priority.

**Collection namespace**: `cisco.meraki_rm`

**OpenAPI spec**: `spec3.json` (Meraki Dashboard API v1.67.0, 594 paths)

**Audience**: Developers building the Meraki collection

---

## Table of Contents

1. [NovaCom-to-Meraki Mapping](#section-1-novacom-to-meraki-mapping)
2. [API Characteristics](#section-2-api-characteristics)
3. [Schema Extraction Strategy](#section-3-schema-extraction-strategy)
4. [Module Map](#section-4-module-map)
5. [Module Naming Conventions](#section-5-module-naming-conventions)
6. [Implementation Priority](#section-6-implementation-priority)
7. [Meraki-Specific Adaptations](#section-7-meraki-specific-adaptations)

---

## SECTION 1: NovaCom-to-Meraki Mapping

The design docs use NovaCom Networks as a fictitious stand-in. NovaCom's API structure, hierarchy, and patterns are modeled directly on Meraki. The following table maps every NovaCom concept to its Meraki equivalent.

### Namespace and Identity

| Concept | NovaCom (Docs) | Meraki (Implementation) |
|---|---|---|
| Collection namespace | `novacom.dashboard` | `cisco.meraki_rm` |
| Module prefix | `novacom_` | `meraki_` |
| Base URL | `https://api.novacom.io/v1/` | `https://api.meraki.com/api/v1` |
| Auth header | `X-NovaCom-API-Key` | `X-Cisco-Meraki-API-Key` |
| Auth type | API key in header | API key in header (+ bearer token) |
| Rate limit | 10 req/s/org | 10 req/s/org (with burst) |
| API version | v1, v2 (multi-version) | v1 only (single version) |

### Management Hierarchy

| NovaCom Term | Meraki Term | Notes |
|---|---|---|
| Organization | Organization | Top-level tenant. Identical concept. |
| Site | Network | Meraki uses "network" where NovaCom uses "site." A network is a logical grouping within an organization. |
| Network | (no separate concept) | In Meraki, a network encompasses what NovaCom splits into sites and networks. |
| Device | Device | Individual hardware (AP, switch, appliance, camera). Identified by serial number. |

### Key Variable Names

| NovaCom Variable | Meraki Variable | Used In |
|---|---|---|
| `novacom_url` | `meraki_dashboard_url` | Inventory / host vars |
| `novacom_api_key` | `meraki_api_key` | Inventory / host vars |
| `novacom_base_url` | `meraki_base_url` | PlatformService |
| `platform_manager_socket` | `platform_manager_socket` | Unchanged (internal) |
| `platform_manager_authkey` | `platform_manager_authkey` | Unchanged (internal) |

### Import Paths

| NovaCom Import | Meraki Import |
|---|---|
| `ansible_collections.novacom.dashboard.plugins.plugin_utils.platform.base_transform` | `plugins.plugin_utils.platform.base_transform` (flat layout, relative imports) |
| `ansible_collections.novacom.dashboard.plugins.plugin_utils.manager.platform_manager` | `plugins.plugin_utils.manager.platform_manager` |
| `ansible_collections.novacom.dashboard.plugins.plugin_utils.user_models.vlan` | `plugins.plugin_utils.user_models.vlan` |
| `ansible_collections.novacom.dashboard.plugins.action.base_action` | `plugins.action.base_action` |

Since we use a flat layout (workspace root = collection root), imports within the collection use relative paths rather than the full `ansible_collections.cisco.meraki_rm` prefix during development. The full prefix is needed when the collection is installed via `ansible-galaxy`.

---

## SECTION 2: API Characteristics

### Meraki Dashboard API Overview

- **OpenAPI version**: 3.0.1
- **API version**: v1.67.0 (February 2026)
- **Total paths**: 594
- **Methods**: 471 GET, 157 POST, 175 PUT, 63 DELETE
- **Configuration endpoints**: 337 (PUT/POST/DELETE)
- **Read-only endpoints**: 257 (GET only)
- **Authentication**: API key via `X-Cisco-Meraki-API-Key` header or bearer token
- **Base URL**: `https://api.meraki.com/api/v1`
- **Rate limiting**: 10 requests/second per organization, with `Retry-After` header on 429
- **Naming**: camelCase throughout (e.g., `applianceIp`, `dhcpHandling`, `vlanId`)

### Scope Hierarchy

All endpoints fall under one of four scopes:

| Scope | Path Prefix | Count | Primary Key |
|---|---|---|---|
| **Network** | `/networks/{networkId}/...` | 263 | `networkId` |
| **Organization** | `/organizations/{organizationId}/...` | 250 | `organizationId` |
| **Device** | `/devices/{serial}/...` | 71 | `serial` |
| **Administered** | `/administered/...` | 10 | (user identity) |

### Critical API Behaviors

**No shared schemas.** The Meraki OpenAPI spec has **no `components/schemas`**. All 594 endpoints use inline schemas only. This is the biggest deviation from the NovaCom pattern and requires a custom schema extraction approach (see Section 3).

**Action Batches.** Meraki supports atomic multi-operation transactions via `POST /organizations/{organizationId}/actionBatches`. This is critical for multi-endpoint resource modules (e.g., wireless SSID with 14 sub-endpoints).

**Pagination.** List endpoints return paginated results with `Link` headers for next/previous pages. The PlatformService must handle pagination transparently.

**Single API version.** Unlike the NovaCom docs which describe multi-version support (v1, v2), Meraki currently has only v1. The version registry and loader still work but will discover only `v1/`.

---

## SECTION 3: Schema Extraction Strategy

### The Problem

The standard approach from [08-code-generators.md](08-code-generators.md) uses `datamodel-code-generator` to generate Python dataclasses from `components/schemas` in the OpenAPI spec. Meraki's spec has **no shared schemas** — all schemas are inline within each operation's `requestBody` and `responses`.

This means `datamodel-code-generator` cannot generate useful models directly.

### The Solution: Custom Schema Extractor

Build `tools/generators/extract_meraki_schemas.py` that:

1. **Parses `spec3.json`** and iterates over all paths and operations
2. **Extracts inline schemas** from `requestBody.content.application/json.schema` and `responses.200.content.application/json.schema` for each operation
3. **Groups schemas by resource entity** using path pattern matching:
   - All paths matching `/networks/{networkId}/appliance/vlans*` → `vlan` entity
   - All paths matching `/networks/{networkId}/wireless/ssids*` → `ssid` entity
   - All paths matching `/organizations/{organizationId}/admins*` → `admin` entity
4. **Merges request + response schemas** per entity:
   - Request schema has the fields you can write
   - Response schema has the fields you get back (superset of request + read-only fields)
   - Union of both = complete entity schema
5. **Deduplicates fields** across operations (GET, POST, PUT for the same entity often share the same fields)
6. **Generates Python dataclasses** to `plugins/plugin_utils/api/v1/generated/{entity}.py`

### Path-to-Entity Mapping Rules

| Path Pattern | Entity Name | Module |
|---|---|---|
| `/networks/{id}/appliance/vlans*` | `vlan` | `meraki_appliance_vlans` |
| `/networks/{id}/appliance/firewall/*` | `firewall` | `meraki_appliance_firewall` |
| `/networks/{id}/wireless/ssids/{num}*` | `ssid` | `meraki_wireless_ssid` |
| `/networks/{id}/switch/accessPolicies*` | `switch_access_policy` | `meraki_switch_access_policies` |
| `/organizations/{id}/admins*` | `admin` | `meraki_organization_admins` |
| `/devices/{serial}/switch/ports*` | `switch_port` | `meraki_switch_ports` |

The extractor uses configurable path-to-entity rules so the mapping can be adjusted without changing code.

### Generated Output Example

For the VLAN entity, the extractor produces:

```python
# plugins/plugin_utils/api/v1/generated/vlan.py

"""Generated API dataclass for Meraki appliance VLAN.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY - regenerate using tools/generators/
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class Vlan:
    """Meraki appliance VLAN API schema."""
    id: Optional[int] = None
    networkId: Optional[str] = None
    name: Optional[str] = None
    applianceIp: Optional[str] = None
    subnet: Optional[str] = None
    groupPolicyId: Optional[str] = None
    templateVlanType: Optional[str] = None
    cidr: Optional[str] = None
    mask: Optional[int] = None
    dhcpHandling: Optional[str] = None
    dhcpLeaseTime: Optional[str] = None
    dhcpBootOptionsEnabled: Optional[bool] = None
    dhcpBootNextServer: Optional[str] = None
    dhcpBootFilename: Optional[str] = None
    dhcpOptions: Optional[List[Dict[str, Any]]] = None
    reservedIpRanges: Optional[List[Dict[str, Any]]] = None
    dnsNameservers: Optional[str] = None
    fixedIpAssignments: Optional[Dict[str, Any]] = None
    # ... additional fields from response schema
```

Note: API model fields use **camelCase** (matching the API). The transform mixin handles conversion to snake_case for the user model.

---

## SECTION 4: Module Map

### Summary

| Domain | Module Count | Key Resources |
|---|---|---|
| Appliance | 11 | VLANs, firewall, VPN, traffic shaping, static routes, ports, security |
| Wireless | 4 | SSIDs (complex), RF profiles, air marshal, ethernet ports |
| Switching | 10 | Switch ports, access policies, DHCP, QoS, routing, STP, ACLs, stacks |
| Network-General | 8 | Settings, group policies, floor plans, firmware, webhooks, VLAN profiles |
| Camera/Sensor | 3 | Quality/retention profiles, wireless profiles, sensor alerts |
| Organization | 8 | Admins, SAML, policy objects, adaptive policy, config templates |
| Device | 3 | Device settings, management interface, switch routing |
| Cross-Cutting | 1 | Facts (gather-only) |
| **Total** | **~48** | |

### Appliance Domain (11 modules)

| Module | Aggregated Endpoints | Primary Key | Complexity |
|---|---|---|---|
| `meraki_appliance_vlans` | `GET/POST/PUT/DELETE .../appliance/vlans/{vlanId}`, `GET/PUT .../appliance/vlans/settings` | `vlan_id` | Medium (DHCP settings hoisted) |
| `meraki_appliance_firewall` | `GET/PUT .../appliance/firewall/l3FirewallRules`, `.../l7FirewallRules`, `.../inboundFirewallRules`, `.../cellularFirewallRules`, `.../firewalledServices/{service}`, `.../inboundCellularFirewallRules`, `.../settings` | (singleton per network) | High (7 sub-endpoints) |
| `meraki_appliance_vpn` | `GET/PUT .../appliance/vpn/siteToSiteVpn`, `GET/PUT .../appliance/vpn/bgp` | (singleton) | Medium |
| `meraki_appliance_traffic_shaping` | `GET/PUT .../appliance/trafficShaping`, `.../trafficShaping/rules`, `.../trafficShaping/uplinkBandwidth`, `POST/DELETE .../trafficShaping/customPerformanceClasses` | (singleton) | Medium |
| `meraki_appliance_static_routes` | `GET/POST/PUT/DELETE .../appliance/staticRoutes/{staticRouteId}` | `static_route_id` | Simple |
| `meraki_appliance_port` | `GET/PUT .../appliance/ports/{portId}` | `port_id` | Simple |
| `meraki_appliance_security` | `GET/PUT .../appliance/security/intrusion`, `GET/PUT .../appliance/security/malware` | (singleton) | Simple |
| `meraki_appliance_warm_spare` | `GET/PUT .../appliance/warmSpare`, `POST .../appliance/warmSpare/swap` | (singleton) | Simple |
| `meraki_appliance_ssid` | `GET/PUT .../appliance/ssids/{number}` | `number` | Simple |
| `meraki_appliance_prefixes` | `GET/POST/PUT/DELETE .../appliance/prefixes/delegated/statics/{staticDelegatedPrefixId}` | `static_delegated_prefix_id` | Simple |
| `meraki_appliance_rf_profiles` | `GET/POST/PUT/DELETE .../appliance/rfProfiles/{rfProfileId}` | `rf_profile_id` | Simple |

### Wireless Domain (4 modules)

| Module | Aggregated Endpoints | Primary Key | Complexity |
|---|---|---|---|
| `meraki_wireless_ssid` | `GET/PUT .../wireless/ssids/{number}`, `.../firewall/l3FirewallRules`, `.../firewall/l7FirewallRules`, `.../trafficShaping/rules`, `.../splash/settings`, `.../hotspot20`, `.../identityPsks/{identityPskId}`, `.../bonjour/forwarding`, `.../eapOverride`, `.../vpn`, `.../schedules`, `.../deviceTypeGroupPolicies` | `number` | **MOST COMPLEX** (14 sub-endpoints) |
| `meraki_wireless_rf_profiles` | `GET/POST/PUT/DELETE .../wireless/rfProfiles/{rfProfileId}` | `rf_profile_id` | Simple |
| `meraki_wireless_air_marshal_rules` | `POST/PUT/DELETE .../wireless/airMarshal/rules/{ruleId}`, `GET/PUT .../wireless/airMarshal/settings` | `rule_id` | Medium |
| `meraki_wireless_ethernet_port_profiles` | `GET/POST/PUT/DELETE .../wireless/ethernet/ports/profiles/{profileId}`, `POST .../assign`, `POST .../setDefault` | `profile_id` | Medium |

### Switching Domain (10 modules)

| Module | Aggregated Endpoints | Primary Key | Complexity |
|---|---|---|---|
| `meraki_switch_ports` | `GET/PUT /devices/{serial}/switch/ports/{portId}`, `POST .../ports/cycle` | `port_id` (device-scoped) | Medium |
| `meraki_switch_access_policies` | `GET/POST/PUT/DELETE .../switch/accessPolicies/{accessPolicyNumber}` | `access_policy_number` | Simple |
| `meraki_switch_dhcp_policy` | `GET/PUT .../switch/dhcpServerPolicy`, `GET/POST/PUT/DELETE .../arpInspection/trustedServers/{trustedServerId}` | (singleton + trusted servers) | Medium |
| `meraki_switch_qos_rules` | `GET/POST/PUT/DELETE .../switch/qosRules/{qosRuleId}`, `GET/PUT .../qosRules/order` | `qos_rule_id` | Simple |
| `meraki_switch_routing` | `GET/PUT .../switch/routing/multicast`, `GET/PUT .../routing/ospf`, `GET/POST/PUT/DELETE .../multicast/rendezvousPoints/{rendezvousPointId}` | (singleton + rendezvous points) | Medium |
| `meraki_switch_stp` | `GET/PUT .../switch/stp` | (singleton) | Simple |
| `meraki_switch_acl` | `GET/PUT .../switch/accessControlLists` | (singleton) | Simple |
| `meraki_switch_stacks` | `GET/POST/PUT/DELETE .../switch/stacks/{switchStackId}`, `.../routing/interfaces/{interfaceId}`, `.../routing/staticRoutes/{staticRouteId}` | `switch_stack_id` | High (stacking + routing) |
| `meraki_switch_link_aggregations` | `GET/POST/PUT/DELETE .../switch/linkAggregations/{linkAggregationId}` | `link_aggregation_id` | Simple |
| `meraki_switch_settings` | `GET/PUT .../switch/mtu`, `GET/PUT .../switch/stormControl`, `GET/PUT .../switch/dscpToCosMappings`, `GET/PUT .../switch/alternateManagementInterface`, `GET/PUT .../switch/settings` | (singleton, consolidated) | Medium |

### Network-General Domain (8 modules)

| Module | Aggregated Endpoints | Primary Key | Complexity |
|---|---|---|---|
| `meraki_network_settings` | `GET/PUT .../settings`, `GET/PUT .../alerts/settings`, `GET/PUT .../netflow`, `GET/PUT .../snmp`, `GET/PUT .../syslogServers`, `GET/PUT .../trafficAnalysis` | (singleton, consolidated) | Medium |
| `meraki_group_policies` | `GET/POST/PUT/DELETE .../groupPolicies/{groupPolicyId}` | `group_policy_id` | Simple |
| `meraki_floor_plans` | `GET/POST/PUT/DELETE .../floorPlans/{floorPlanId}` | `floor_plan_id` | Simple |
| `meraki_firmware_upgrade` | `GET/PUT .../firmwareUpgrades`, `POST .../firmwareUpgrades/rollbacks`, `GET/POST/PUT/DELETE .../firmwareUpgrades/staged/*` | (singleton + staged) | High |
| `meraki_webhooks` | `GET/POST/PUT/DELETE .../webhooks/httpServers/{httpServerId}`, `GET/POST/PUT/DELETE .../webhooks/payloadTemplates/{payloadTemplateId}` | `http_server_id` / `payload_template_id` | Medium |
| `meraki_vlan_profiles` | `GET/POST/PUT/DELETE .../vlanProfiles/{iname}`, `POST .../vlanProfiles/assignments/reassign` | `iname` | Medium |
| `meraki_auth_users` | `GET/POST/PUT/DELETE .../merakiAuthUsers/{merakiAuthUserId}` | `meraki_auth_users_id` | Simple |
| `meraki_mqtt_brokers` | `GET/POST/PUT/DELETE .../mqttBrokers/{mqttBrokerId}` | `mqtt_broker_id` | Simple |

### Camera/Sensor Domain (3 modules)

| Module | Aggregated Endpoints | Primary Key | Complexity |
|---|---|---|---|
| `meraki_camera_quality_retention_profiles` | `GET/POST/PUT/DELETE .../camera/qualityRetentionProfiles/{qualityRetentionProfileId}` | `quality_retention_profile_id` | Simple |
| `meraki_camera_wireless_profiles` | `GET/POST/PUT/DELETE .../camera/wirelessProfiles/{wirelessProfileId}` | `wireless_profile_id` | Simple |
| `meraki_sensor_alert_profiles` | `GET/POST/PUT/DELETE .../sensor/alerts/profiles/{id}` | `id` | Simple |

### Organization Domain (8 modules)

| Module | Aggregated Endpoints | Primary Key | Complexity |
|---|---|---|---|
| `meraki_organization_admins` | `GET/POST/PUT/DELETE .../admins/{adminId}` | `admin_id` | Medium (RBAC, networks, tags) |
| `meraki_organization_saml` | `GET/PUT .../saml`, `GET/POST/PUT/DELETE .../saml/idps/{idpId}`, `GET/POST/PUT/DELETE .../samlRoles/{samlRoleId}` | `idp_id` / `saml_role_id` | Medium |
| `meraki_organization_policy_objects` | `GET/POST/PUT/DELETE .../policyObjects/{policyObjectId}`, `GET/POST/PUT/DELETE .../policyObjects/groups/{policyObjectGroupId}` | `policy_object_id` / `policy_object_group_id` | Medium |
| `meraki_organization_adaptive_policy` | `GET/POST/PUT/DELETE .../adaptivePolicy/acls/{aclId}`, `.../groups/{id}`, `.../policies/{id}`, `GET/PUT .../adaptivePolicy/settings` | multiple | High |
| `meraki_organization_config_templates` | `GET/POST/PUT/DELETE .../configTemplates/{configTemplateId}`, `GET/PUT .../configTemplates/{id}/switch/profiles/ports/{portId}` | `config_template_id` | Medium |
| `meraki_organization_alert_profiles` | `GET/POST/PUT/DELETE .../alerts/profiles/{alertConfigId}` | `alert_config_id` | Simple |
| `meraki_organization_branding_policies` | `GET/POST/PUT/DELETE .../brandingPolicies/{brandingPolicyId}`, `GET/PUT .../brandingPolicies/priorities` | `branding_policy_id` | Simple |
| `meraki_organization_vpn` | `GET/PUT .../appliance/vpn/thirdPartyVPNPeers`, `GET/PUT .../appliance/vpn/vpnFirewallRules` | (singleton) | Medium |

### Device Domain (3 modules)

| Module | Aggregated Endpoints | Primary Key | Complexity |
|---|---|---|---|
| `meraki_device` | `GET/PUT /devices/{serial}` | `serial` | Simple |
| `meraki_device_management_interface` | `GET/PUT /devices/{serial}/managementInterface` | `serial` (singleton) | Simple |
| `meraki_device_switch_routes` | `GET/POST/PUT/DELETE /devices/{serial}/switch/routing/interfaces/{interfaceId}`, `.../routing/staticRoutes/{staticRouteId}` | `interface_id` / `static_route_id` | Medium |

### Cross-Cutting (1 module)

| Module | Purpose | Complexity |
|---|---|---|
| `meraki_facts` | Gather-only module: organizations, networks, devices, inventory. Uses `state: gathered` only. | Medium (many GET endpoints) |

---

## SECTION 5: Module Naming Conventions

### Pattern

```
meraki_{domain}_{entity}
```

| Component | Rule | Example |
|---|---|---|
| Prefix | Always `meraki_` | `meraki_` |
| Domain | Matches API path segment | `appliance`, `wireless`, `switch`, `organization`, `device` |
| Entity | Singular noun, describes the thing being managed | `vlan`, `ssid`, `port`, `admin` |

### Examples

| API Path | Module Name | Rationale |
|---|---|---|
| `/networks/{id}/appliance/vlans/{vlanId}` | `meraki_appliance_vlans` | Domain: appliance, Entity: vlan |
| `/networks/{id}/wireless/ssids/{number}` | `meraki_wireless_ssid` | Domain: wireless, Entity: ssid |
| `/devices/{serial}/switch/ports/{portId}` | `meraki_switch_ports` | Domain: switch, Entity: port |
| `/organizations/{id}/admins/{adminId}` | `meraki_organization_admins` | Domain: organization, Entity: admin |
| `/devices/{serial}` | `meraki_device` | No sub-domain, just device |

### What NOT to Do

| Bad Name | Why | Good Name |
|---|---|---|
| `meraki_networks_appliance_vlans` | Mirrors API path (endpoint-centric) | `meraki_appliance_vlans` |
| `meraki_appliance_vlanss` | Plural (Ansible convention is singular) | `meraki_appliance_vlans` |
| `meraki_vlan_create` | CRUD verb in name (lifecycle is via `state`) | `meraki_appliance_vlans` |
| `meraki_appliance_firewall_l3_rules` | Too granular (L3 rules are part of firewall entity) | `meraki_appliance_firewall` |

---

## SECTION 6: Implementation Priority

### Sprint 1: Foundation Proof (5 modules)

These modules prove the full pattern end-to-end: foundation, generators, transforms, action plugins, mock server, Molecule tests.

| Module | Why First | Complexity |
|---|---|---|
| `meraki_appliance_vlans` | Straightforward CRUD, high usage, good proving ground | Medium |
| `meraki_wireless_ssid` | Most complex (14 sub-endpoints), demonstrates full aggregation pattern | High |
| `meraki_switch_ports` | Per-device scoping, common use case | Medium |
| `meraki_organization_admins` | RBAC, demonstrates name-to-ID transforms (org name → org ID) | Medium |
| `meraki_facts` | Gather-only, immediately useful, validates reverse transform | Medium |

### Sprint 2: Appliance + Organization (17 modules)

| Domain | Modules |
|---|---|
| Appliance | `firewall`, `vpn`, `traffic_shaping`, `static_route`, `port`, `security`, `warm_spare`, `ssid`, `prefix`, `rf_profile` |
| Organization | `saml`, `policy_object`, `adaptive_policy`, `config_template`, `alert_profile`, `branding_policy`, `vpn` |

### Sprint 3: Switching + Wireless (13 modules)

| Domain | Modules |
|---|---|
| Switching | `access_policy`, `dhcp_policy`, `qos_rule`, `routing`, `stp`, `acl`, `stack`, `link_aggregation`, `settings` |
| Wireless | `rf_profile`, `air_marshal`, `ethernet_port_profile` |

### Sprint 4: Remaining (13 modules) — Complete

| Domain | Modules |
|---|---|
| Camera/Sensor | `camera_quality_retention_profile`, `camera_wireless_profile`, `sensor_alert_profile` |
| Network-General | `network_settings`, `group_policy`, `floor_plan`, `firmware_upgrade`, `webhook`, `vlan_profile`, `meraki_auth_users`, `mqtt_broker` |
| Device | `device`, `device_management_interface`, `device_switch_routing` |

### Efficiency Analysis

- **~80% simple/medium** — straightforward entity aggregation, 1:1 or rename field mappings, single or few endpoints. Agent-automatable.
- **~20% complex** — `wireless_ssid` (14 sub-endpoints), `appliance_firewall` (7 sub-endpoints), `switch_stack` (stacking + routing), `organization_adaptive_policy` (4 sub-resources). Require careful hoisting logic and domain knowledge.

---

## SECTION 7: Meraki-Specific Adaptations

### Rate Limit Handling

Meraki enforces 10 requests/second per organization. On rate limit, the API returns HTTP 429 with a `Retry-After` header.

PlatformService implements:

```python
def _handle_rate_limit(self, response):
    """Handle 429 rate limit response."""
    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 1))
        logger.warning(f"Rate limited. Retrying after {retry_after}s")
        time.sleep(retry_after)
        return True  # Signal retry
    return False
```

All API calls should use a retry loop with exponential backoff:

```python
def _api_call(self, method, url, **kwargs):
    """Make API call with rate limit retry."""
    max_retries = 5
    for attempt in range(max_retries):
        response = self.session.request(method, url, **kwargs)
        if not self._handle_rate_limit(response):
            return response
    raise RuntimeError(f"Rate limit exceeded after {max_retries} retries")
```

Implementation: `plugins/plugin_utils/manager/platform_manager.py` — methods `_handle_rate_limit()` and `_api_call()`.

### Action Batch Support

For multi-endpoint modules (e.g., `meraki_wireless_ssid`), use Action Batches when atomicity matters:

```
POST /organizations/{organizationId}/actionBatches
{
  "confirmed": true,
  "synchronous": true,
  "actions": [
    {"resource": "/networks/N_123/wireless/ssids/1", "operation": "update", "body": {...}},
    {"resource": "/networks/N_123/wireless/ssids/1/firewall/l3FirewallRules", "operation": "update", "body": {...}}
  ]
}
```

Add `batch_eligible: bool` to EndpointOperation:

```python
@dataclass
class EndpointOperation:
    path: str
    method: str
    fields: List[str]
    path_params: Optional[List[str]] = None
    required_for: Optional[str] = None
    depends_on: Optional[str] = None
    order: int = 0
    batch_eligible: bool = True  # NEW: can this operation be batched?
```

The PlatformService decides whether to use direct API calls or batch them based on the operation plan and the `state` parameter:

- `state: merged` with single endpoint → direct call
- `state: overridden` with multi-endpoint → Action Batch
- `state: replaced` with multi-instance → Action Batch

### Pagination

Meraki list endpoints paginate with `Link` headers:

```
Link: <https://api.meraki.com/api/v1/networks/N_123/appliance/vlans?startingAfter=100>; rel=next
```

PlatformService auto-paginates for `gather` operations:

```python
def _paginated_get(self, url, **kwargs):
    """GET with automatic pagination."""
    results = []
    while url:
        response = self._api_call('GET', url, **kwargs)
        response.raise_for_status()
        results.extend(response.json())
        # Parse Link header for next page
        url = self._parse_next_link(response.headers.get('Link'))
    return results
```

Implementation: `plugins/plugin_utils/manager/platform_manager.py` — methods `_paginated_get()` and `_parse_next_link()`.

### Version Detection

Meraki currently has only v1. Version detection is simple:

```python
def _detect_version(self) -> str:
    """Detect Meraki API version. Currently always v1."""
    return '1'
```

If Meraki introduces v2 in the future, the version registry and loader handle it automatically — add a `v2/` directory under `api/` and the registry discovers it.

### Authentication

PlatformService initializes the session with the Meraki API key:

```python
def __init__(self, base_url: str, api_key: str):
    self.base_url = base_url.rstrip('/')
    self.session = requests.Session()
    self.session.headers.update({
        'X-Cisco-Meraki-API-Key': api_key,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'cisco.meraki_rm Ansible Collection',
    })
```

### Data-Driven Action Plugins

Unlike the NovaCom reference (where each action plugin contains a full `run()` method),
the Meraki collection uses a **data-driven base class**.  Each resource action plugin
is pure configuration — no `run()` override needed:

```python
# plugins/action/meraki_appliance_vlans.py
from .base_action import BaseResourceActionPlugin

class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'vlan'
    USER_MODEL = 'plugins.plugin_utils.user_models.vlan.UserVlan'
```

`BaseResourceActionPlugin.run()` handles the full lifecycle automatically:

1. **Auto-discovers DOCUMENTATION** from the sibling `plugins/modules/` file
   using the action plugin filename (both are always `meraki_<name>.py`).
2. **Validates input** by parsing DOCUMENTATION into an Ansible ArgumentSpec.
3. **Resolves the User Model class** from the `USER_MODEL` dotted path via `importlib`.
4. **Extracts the scope value** (`network_id`, `organization_id`, or `serial`)
   from `SCOPE_PARAM`.
5. **Dispatches per state**: gathered → find, deleted → delete (if `SUPPORTS_DELETE`),
   overridden → gather + diff + delete extras + replace desired,
   merged/replaced → create or update (using `CANONICAL_KEY` to decide).
6. **Validates output** against the same argspec before returning — strips
   undocumented fields, enforcing the return data contract with the user.

#### Class Attributes

| Attribute | Type | Default | Description |
|---|---|---|---|
| `MODULE_NAME` | `str` | (required) | Resource identifier, e.g. `'vlan'` |
| `SCOPE_PARAM` | `str` | `'network_id'` | Which arg carries the resource scope |
| `USER_MODEL` | `str` | (required) | Dotted import path to the User Model class |
| `CANONICAL_KEY` | `str` | `None` | Human-facing field for matching (name, email, vlan_id) |
| `SYSTEM_KEY` | `str` | `None` | API-generated identity for URL routing (admin_id, etc.) |
| `SUPPORTS_DELETE` | `bool` | `True` | `False` for singletons (no delete endpoint) |

#### Archetypes

| Archetype | CANONICAL_KEY | SUPPORTS_DELETE | Modules |
|---|---|---|---|
| Full CRUD | set (e.g. `'admin_id'`) | `True` | admin, config_template, policy_object, ... |
| Update-only | `None` | `True` | vlan, static_route, webhook, ... |
| Singleton | `None` | `False` | firewall, vpn, network_settings, ... |

The only module with a custom `run()` is `meraki_facts`, which returns
`ansible_facts` instead of the standard `config` list.

### Examples as Source of Truth

The Meraki collection uses a **single-source-of-truth** pattern where the same YAML task
files serve as both `ansible-doc` examples and Molecule integration tests.

#### Layout

```
examples/
  appliance_vlans/
    merged.yml        # state: merged  — create/update
    replaced.yml      # state: replaced — full replacement
    overridden.yml    # state: overridden — declarative desired state
    gathered.yml      # state: gathered — read current config
    deleted.yml       # state: deleted  — remove resource
  wireless_ssid/
    merged.yml
    replaced.yml
    gathered.yml        # No deleted.yml (singleton, no overridden)
  facts/
    gathered.yml        # Facts module only supports gathered
```

Each file contains a flat list of Ansible tasks (no play header). Tasks include
`register:` and `assert:` steps so they function as tests when included by Molecule.

#### Documentation Injection

A pre-commit hook (`tools/inject_examples.py`) concatenates per-state files in
canonical order (merged → replaced → overridden → gathered → deleted) and writes
them into the `EXAMPLES` block of `plugins/modules/meraki_*.py`:

```bash
python tools/inject_examples.py           # inject all
python tools/inject_examples.py --check   # pre-commit mode: exit 1 if stale
```

#### Molecule Integration

Molecule scenarios use `include_tasks` to wire directly to the example files:

- `converge.yml` → includes `merged.yml` (and optionally `replaced.yml`)
- `verify.yml` → includes `gathered.yml` + additional assertions
- `cleanup.yml` → includes `deleted.yml` (or no-op for singletons)

Because `merged.yml` only creates/updates (never deletes), re-running converge
against an already-converged system produces `changed: false` — satisfying
Molecule's automatic idempotence check.

#### Supported States

| State | HTTP Method | Purpose | All modules? |
|---|---|---|---|
| `merged` | POST / PUT | Create or update | Yes |
| `replaced` | PUT | Full resource replacement | Most (not org-scoped) |
| `overridden` | GET + DELETE + PUT | Gather, diff, delete extras, replace desired | CRUD modules (replaced + deleted) |
| `gathered` | GET | Read current config | Yes |
| `deleted` | DELETE | Remove resource | CRUD modules only |

---

## SECTION 8: Lessons Learned

Mistakes, course corrections, and design decisions made during implementation.
These are captured so that future collections (or AI agents building from these
docs) do not repeat them.

### 1. `parsed` and `rendered` Are CLI Constructs

**Mistake**: The NovaCom reference includes `parsed` and `rendered` states.
These were initially carried into the Meraki collection.

**Fix**: Removed. These states exist for CLI-based network modules (IOS, NXOS)
that parse running-config text. API-driven collections only need:
`merged`, `replaced`, `overridden`, `gathered`, `deleted`.

**Rule**: If your collection talks to a REST API (not a CLI), drop `parsed`
and `rendered` from the valid states.

### 2. `DOCUMENTATION` Must Be Literal in Module Files

**Mistake**: Initially placed `DOCUMENTATION` strings in a shared
`plugins/plugin_utils/docs/` directory and imported them into module files.

**Fix**: Moved `DOCUMENTATION`, `EXAMPLES`, and `RETURN` strings directly
into `plugins/modules/meraki_*.py`. `ansible-doc` parses module files
statically using AST — it cannot follow imports, `importlib`, or any
runtime resolution.

**Rule**: `DOCUMENTATION`, `EXAMPLES`, and `RETURN` must be top-level
string literals in the module file. No imports. No indirection.

### 3. Data-Driven Action Plugins Eliminate Boilerplate

**Mistake**: Initially generated 48 action plugins each with a full `run()`
method containing ~80 lines of near-identical code.

**Fix**: Refactored to a data-driven `BaseResourceActionPlugin` where
subclasses declare 5 class attributes and inherit `run()`. 47 of 48 action
plugins are now ~8 lines of pure configuration. Only `meraki_facts` needs
a custom `run()`.

**Rule**: If your action plugins share 90%+ logic, push it into the base
class and make subclasses declarative. Use `importlib` for lazy model
resolution from a dotted path string.

### 4. Naming: Avoid Double Prefix

**Mistake**: The entity `merakiAuthUser` (from the API path
`/merakiAuthUsers/{id}`) was naively prefixed to produce
`meraki_meraki_auth_user` — a double `meraki_` prefix.

**Fix**: Renamed to `meraki_auth_users`. The extraction scripts must strip
any prefix that duplicates the collection's own module prefix.

**Rule**: When generating module names from API paths, check whether the
entity name already starts with the collection prefix.

### 5. Plural Names for List-Based Modules

**Mistake**: Initially used singular names (`meraki_appliance_vlan`) for
all modules, regardless of whether they manage a list or a singleton.

**Fix**: Adopt the Ansible network RM convention:
- **Plural** for list-based CRUD: `meraki_appliance_vlans`, `meraki_switch_ports`
- **Singular** for singletons: `meraki_appliance_firewall`, `meraki_network_settings`

This matches `cisco.ios.ios_vlans`, `arista.eos.eos_interfaces`, etc.

**Rule**: If `config:` takes a list of items and the module supports
`deleted`, the name should be plural. Singletons (one config per scope)
stay singular.

### 6. Examples as Source of Truth

**Mistake**: Initially maintained separate example stubs in module files and
hand-written Molecule converge playbooks. These diverged immediately.

**Fix**: Created `examples/{module}/{state}.yml` as the single source of
truth. A pre-commit hook (`tools/inject_examples.py`) injects them into
module `EXAMPLES` strings. Molecule `include_tasks` them directly.

**Rule**: Never maintain the same YAML tasks in two places. Use one source
and generate/include everywhere else.

### 7. Per-State Example Files Enable Idempotence Testing

**Mistake**: Initially generated one flat example file per module containing
all states (merged, gathered, deleted). This breaks Molecule's idempotence
check because re-running converge would re-create and re-delete.

**Fix**: Split into per-state files. Molecule converge includes only
`merged.yml` (idempotent on re-run). Verify includes `gathered.yml`.
Cleanup includes `deleted.yml`.

**Rule**: Structure examples so that converge can be re-run without side
effects. Keep create/update separate from delete.

### 8. `overridden` Is Free for CRUD Modules

**Mistake**: Initially omitted `overridden` from all modules because
"it seemed complex."

**Fix**: If a module already supports `replaced` (PUT per item) and
`deleted` (DELETE per item), then `overridden` is just their composition:
gather current set → diff against desired → delete extras → replace matches.

**Rule**: Add `overridden` to every module that has both `replaced` and
`deleted`. It costs nothing extra in implementation and gives users the
most declarative state.

### 9. Inline Schemas Require Custom Extraction

**Mistake**: Assumed `datamodel-code-generator` could generate models from
the Meraki OpenAPI spec.

**Fix**: Meraki's spec has **zero** `components/schemas` — all schemas are
inline. Built a custom `tools/generators/extract_meraki_schemas.py` that
parses paths, extracts inline schemas, groups by entity, merges
request+response fields, and generates Python dataclasses.

**Rule**: Check for `components/schemas` before choosing a code generator.
If the spec uses only inline schemas, you need a custom extractor.

### 10. `overridden` Needs Real Gather-Diff-Delete Logic

**Mistake**: Initially, `overridden` fell through to the same `else` branch
as `merged` and `replaced` in `run()`. It iterated the user's config list
and created/updated each item — but never gathered the current set, diffed,
or deleted extras. This made it identical to `merged`.

**Fix**: Implemented `_do_overridden()` as a distinct dispatch path:

1. **Gather** all current resources for the scope (`manager.execute('find', ...)`)
2. **Build** a set of desired primary keys from the user's `config` list
3. **Delete** any current item whose key is NOT in the desired set
4. **Replace** each item in the desired set (full PUT)

This is the correct semantics: "the set should look exactly like this."

**Rule**: `overridden` is not just "merged for each item." It requires a
gather-diff-delete-replace cycle. Test it with Molecule by asserting that
resources NOT in the desired set are actually removed.

### 11. Return Values Must Be Validated Against the Argspec

**Mistake**: The base `run()` method validated input args against the
DOCUMENTATION argspec, but returned results directly to the user without
any output validation. This meant reverse transform bugs (wrong field names,
extra API-side fields leaking through) were invisible until a user noticed.

**Fix**: Added `_validate_output()` that filters each item in the `config`
return list against the documented `config.suboptions`. Fields not in the
documented schema are stripped. This enforces the user contract: what we
return matches exactly what `ansible-doc` says we return.

```python
# In run(), after dispatch:
if argspec and results:
    results = self._validate_output(results, argspec)
```

**Rule**: Validate output, not just input. The argspec defines the contract
in both directions. If a field appears in the return data but not in
`config.suboptions`, it's a bug — either the field mapping is wrong or
the DOCUMENTATION is incomplete.

### 12. Use `to_paths` + Subset Filter for Round-Trip Assertions

**Mistake**: Initial examples only asserted `is changed` and `is not failed` —
confirming "something happened" but not "the right thing happened."

**Fix**: Flatten expected and result with `ansible.utils.to_paths`, then use a
**subset** check: expected path-dict is contained in result (all expected keys
present with same value). Use a collection filter so we get one assert and
clear reporting (missing vs extras).

The collection provides `path_contained_in(expected_paths, result_paths)` in
`plugins/filter/path_contained_in.py`. It returns `{ contained, missing, extras }`:
- **contained**: True if every expected key exists in result with same value (string-normalized).
- **missing**: Expected keys not in result or value mismatch (for fail_msg).
- **extras**: Keys in result not in expected (server-populated; log only).

```yaml
- name: Flatten expected and actual to paths
  ansible.builtin.set_fact:
    expected_paths: "{{ expected_config | ansible.utils.to_paths }}"
    result_paths: "{{ result.config[0] | ansible.utils.to_paths }}"

- name: Compare expected paths to result (subset: expected contained in result)
  ansible.builtin.set_fact:
    path_check: "{{ expected_paths | path_contained_in(result_paths) }}"

- name: Assert all expected fields are present and match
  ansible.builtin.assert:
    that: path_check.contained | bool
    fail_msg: "Expected paths missing or mismatch: {{ path_check.missing }}"

- name: Log server-populated fields not in expected
  ansible.builtin.debug:
    msg: "Extra fields: {{ path_check.extras }}"
```

No loop: one assert on `path_check.contained`; failures show `path_check.missing`;
extras are logged. Requires `ansible.utils` and the collection filter.

### 13. Pre-Commit Hooks Prevent Doc Drift

**Observation**: Without automated enforcement, examples and module
documentation will inevitably diverge. A `--check` flag on the injection
script, wired as a pre-commit hook, catches drift before it reaches the
repository.

**Rule**: Any generated-from-source artifact (EXAMPLES strings, Molecule
scenarios) should have a `--check` mode and a pre-commit hook.

### 14. Tight Tasks, vars, and Filter Plugins Over Loops

**Observation**: Playbooks stay readable when tasks are tight and
complex expressions live in vars or in filter plugins.

- **vars**: Use task-scoped `vars:` for intermediate values (e.g. path
  dicts) and for long strings (e.g. `success_msg`, `fail_msg`) so the
  task body stays short and line length stays low.
- **Filter plugins vs loops**: A single filter (e.g. `path_contained_in`)
  that returns a structured result (`contained`, `missing`, `extras`)
  replaces a multi-step “flatten → set_fact → loop assert → debug”
  with one set_fact and one assert. Fewer tasks, clearer intent, right
  tool for the job.
- **Complex Jinja/pipes**: Long or tricky `rejectattr`, `dict2items`,
  `selectattr`, `items2dict` chains in playbooks are hard to read and
  debug. Move that logic into a collection filter plugin; the playbook
  calls the filter and asserts on the result. Easier to test and
  maintain.

**Rule**: Prefer a small filter plugin over a long Jinja/Ansible pipe or
a loop over items. Use vars to keep task blocks and line length under
control.

### 15. Colocated Unit Tests Before Molecule — Catch Data Bugs in Sub-Seconds

**Mistake**: Pure-Python data bugs — wrong field names in `_field_mapping`,
scope params leaking through transforms, generated dataclass constructor
blowups — were only caught after a ~30s Molecule startup cycle (mock server
init with openapi-core, Ansible bootstrap, etc.). This made the debug loop
painfully slow.

**Fix**: Adopted **colocated `*_test.py` files** as sibling files next to
every source file in `plugin_utils/`. A generator script
(`tools/generate_model_tests.py`) introspects dataclass fields and
`_field_mapping` dicts to emit tests covering forward transforms, reverse
transforms, roundtrips, scope param exclusion, endpoint operations, and
spec drift detection. All ~700 tests run in under 2 seconds with plain
`pytest plugins/`.

**Concrete bug caught**: `camera_quality_retention_profile` had
`quality_retention_profile_id` mapped to `qualityRetentionProfileId` in
the user model, but the generated API class uses `id`. The colocated
Tier 1 forward transform test caught this instantly with an
`AttributeError` — no Molecule startup, no mock server, no YAML.

**Rule**: Always run `pytest plugins/` before `molecule test`. If a field
mapping is wrong, a unit test catches it in under 2 seconds. Molecule is
the second line of defense for integration behavior, not the first line
for data correctness.

### 16. `shared_state` Means the Default Scenario Is the Lifecycle Manager

**Mistake**: Initially assumed `shared_state: true` only applied to
`molecule test --all`, and that single-scenario runs (`molecule test -s
appliance_vlans`) would need the mock server started manually or via
`provisioner.playbooks.create/destroy` delegation.

**Fix**: With `shared_state: true`, Molecule runs the **default scenario**
(create first, destroy last) even for a single-scenario run. The default
scenario's `create.yml` starts the mock server, and its `destroy.yml`
stops it. Component scenarios skip create/destroy entirely.

No `provisioner.playbooks` delegation is needed. The shared config
(`config.yml`) defines only the component test sequence (prepare through
cleanup) plus `shared_state: true`. The default scenario's `molecule.yml`
overrides the sequence to just `[create, destroy]`.

See [Collection Testing — Shared State](https://docs.ansible.com/projects/molecule/getting-started-collections/#shared-state-vs-per-scenario-resources).

**Rule**: If your collection tests use a shared resource (mock server,
database, container), put its lifecycle in `default/create.yml` and
`default/destroy.yml`. Set `shared_state: true` in `config.yml`. Done.

### 17. `before`/`after` Return Values — The Standard Network RM Contract

**Mistake**: The initial action plugin returned `{changed: bool, config: list}`.
`changed` was set to `bool(config)` — always `true` if any config items existed,
regardless of whether anything actually changed. Idempotence naturally failed.

**Fix**: Refactored `BaseResourceActionPlugin.run()` to follow the standard
Ansible network resource module pattern used by `cisco.ios`, `cisco.nxos`, etc.:

1. Gather current state → `before`
2. Apply desired mutations
3. Gather resulting state → `after`
4. `changed = (before != after)`

This makes idempotency automatic: if the resource already matches desired state,
the gather-before and gather-after are identical, so `changed = false`. No
per-state `changed` tracking needed.

**Rule**: Never hardcode `changed: true`. Always derive it from `before != after`.
The gather steps aren't "extra overhead" — they're the module's contract with the user.

### 18. Per-State Molecule Scenarios — No Oscillation

**Mistake**: Initially used one Molecule scenario per module with converge running
both merged and replaced sequentially. Idempotence always failed because the
replay oscillated: merged(config-A) → replaced(config-B) → replay merged(sees B,
changes to A) → `changed: true`.

**Fix**: Split into per-state scenarios in a nested `{module}/{state}/` directory
hierarchy: `appliance_vlans/merged/`, `appliance_vlans/replaced/`, etc. Each converges
a single state. States requiring prerequisite resources (replaced, overridden, deleted)
use `prepare.yml` to seed state before converge.

Benefits:
- Every state gets its own idempotence check
- No scenario oscillation — converge always converges to the same state
- `molecule test --all` runs all per-state scenarios with shared mock server
- `molecule test -s appliance_vlans/merged` targets one state
- Module states grouped in filesystem — easy navigation for 48+ modules

**Rule**: One Molecule scenario per (module × state). Use `prepare.yml` to seed
prerequisites. Never combine competing states in a single converge.

### 19. Empty List Falsiness in `_find_resource`

**Mistake**: `_find_resource()` used `if main_result:` to check for a valid response.
When the API returned an empty list `[]` (e.g., after deleting all VLANs), this was
treated as falsy — `_find_resource` returned `{}` instead of `{'config': []}`.
The caller then appended `{}` as a result item, making `after = [{}]` instead of `[]`.
The delete scenario's assertion `after | length == 0` failed.

**Fix**: Changed to explicit `isinstance(main_result, list)` check first, which
correctly handles empty lists. `[]` now returns `{'config': []}`.

**Rule**: Never use truthiness to distinguish "no result" from "empty result" in
Python. An empty list is a valid result — use `is None` or `isinstance()`.

### 20. Example Assertions Must Survive Idempotence Replay

**Mistake**: Example files used `merge_result is changed` in assertions. These
examples are also the Molecule converge content. During idempotence replay,
`changed: false` is the correct behavior, but the assertion expects `true` and fails.

**Fix**: Changed assertions to `merge_result is not failed` — validates the operation
succeeded without assuming whether the result changed. Molecule's built-in idempotence
checker detects `changed` tasks separately.

**Rule**: Example assertions should validate correctness (`is not failed`,
`after | length > 0`, `path_check.contained`), never assume `is changed`.

### 21. Nested Molecule Directories — Converge/Verify Split

**Decision**: Restructured from flat `appliance_vlans_merged/` scenarios to nested
`appliance_vlans/merged/` hierarchy. Split example content into two files:
- `converge.yml` — set_fact + module call only (documentation source)
- `verify.yml` — independent gather + assertions (no cross-playbook variable deps)

**Why split**: converge.yml doubles as the documentation example source (injected
into `EXAMPLES` via pre-commit hook). Assertions pollute documentation. Verify runs
as a separate playbook anyway, so it cannot reference `register` variables from
converge — it must independently gather state.

**Why nest**: 48 modules × 5 states = ~186 scenarios. Flat layout is unnavigable.
Nested `{module}/{state}/` groups related scenarios and scales naturally. The
`config.yml` inventory path uses `MOLECULE_PROJECT_DIRECTORY` (depth-independent)
instead of `MOLECULE_SCENARIO_DIRECTORY/../` (breaks at depth 2+).

**Generator**: `tools/restructure_molecule.py` parses example files, splits
tasks into converge (set_fact + module call) and verify (assertions), and generates
the complete nested directory structure with prepare/cleanup files.

**Rule**: converge.yml is the documentation source — keep it clean. Assertions live
in verify.yml. Use `MOLECULE_PROJECT_DIRECTORY` for paths that must work at any depth.

### 22. Shared `vars.yml` for Converge/Verify Data

**Mistake**: After splitting examples into `converge.yml` (module calls) and `verify.yml`
(assertions), the verify could no longer access `expected_config` defined via `set_fact`
in converge — they run as separate Ansible playbooks. The verify regressed to only
checking "something exists" rather than validating actual field values.

**Fix**: Extracted `expected_config` into a `vars.yml` file per scenario. Both
`converge.yml` and `verify.yml` load it via `vars_files`. The verify now uses
`path_contained_in` against the gathered state, restoring full field-level validation.

```
extensions/molecule/appliance_vlans/merged/
├── vars.yml          # expected_config — single source of data
├── converge.yml      # vars_files: vars.yml + module call
├── verify.yml        # vars_files: vars.yml + gather + path_contained_in
```

For documentation injection, `inject_examples.py` reads `vars.yml` and renders it
as a `set_fact` task prepended to the converge tasks — producing a complete example.

**Rule**: When splitting playbooks, extract shared data into a vars file. Never
duplicate data between converge and verify. `vars_files` is the Ansible-native way
to share data across separate playbook files.

### 23. Molecule Nested Scenario Discovery — Upstream Proposal

**Challenge**: Molecule's `-s` flag uses `str.replace("*", scenario_name)` on the
glob pattern, which breaks with multi-level wildcards. A nested scenario at
`appliance_vlans/merged/molecule.yml` cannot be targeted with the default glob.

**Proposed upstream fix**: If `-s` value contains `/`, treat it as a path relative
to the scenarios root instead of glob substitution. This is unambiguous (no filesystem
path can contain `/` in a directory name) and backward compatible (no `/` in existing
scenario names). For display names in `molecule list`, use relative-path naming when
scenarios are discovered at multiple depths. Both changes are gated behind collection
mode only — standalone role testing is untouched.

See `NESTED_SCENARIOS.md` in the Molecule repo for the full proposal.

**Rule**: When contributing to upstream tools, prefer detection-based behavior changes
(slash in name, mixed depths) over flags. Make the default behavior smarter rather than
adding opt-in complexity.

### 24. Singleton Idempotence — Skip Check for Keyless Resources

**Mistake**: Modules without `CANONICAL_KEY` (singletons like `network_settings`,
`appliance_security`) always sent the API update on every run because the
`_apply_merged_or_replaced` skip-if-matching check was gated behind
`if self._match_key`. The before/after comparison then detected changes introduced
by the mock server's response (extra fields, type coercion) and reported `changed: true`
on idempotence replay.

**Fix**: Added a `_config_matches(item, before[0])` check in the `else` branch
(no CANONICAL_KEY). Singletons now compare the desired config against the existing state
and skip the API call when all user-supplied fields already match.

**Rule**: Every code path through `_apply_merged_or_replaced` must have a no-op
short-circuit. Test idempotence for both keyed (list) and keyless (singleton) resources.

### 25. Platform Manager Lifecycle — Surviving the Ansible Fork Model

**Problem**: The multiprocessing manager died after every task. The call chain is
`ansible-playbook → fork worker → manager.start() → server child`. Three independent
Python mechanisms conspire to kill the server child when the fork worker exits:

1. `multiprocessing.process._children` — atexit handler joins/terminates active children
2. `BaseManager._finalize_manager` — a `Finalize` callback sends a shutdown RPC to
   the server via the socket
3. Process-group signals — `SIGTERM`/`SIGHUP` sent to the worker's PGID propagate to
   same-group children

This is unlike the classic "weather station" `BaseManager` pattern where the manager
IS the main process and nothing kills it.

**Fix**: Always detach, with lifecycle controlled by a `.survive` flag file.

The manager is **always** detached from Python's cleanup (three-part detach below) so
it survives Ansible fork-worker exits.  This gives task-to-task reuse within a
playbook and cross-playbook reuse.

```python
# 1. Remove from _children so atexit won't join/terminate
multiprocessing.process._children.discard(manager._process)

# 2. Cancel the Finalize callback so atexit won't send shutdown RPC
fin = manager.shutdown
del _finalizer_registry[fin._key]

# 3. os.setsid() in PlatformManager._run_server (server-side)
#    — own session, immune to parent's PGID signals
```

**Lifecycle — unified watchdog, two strategies:**

A daemon watchdog thread always runs inside the server child process.  At startup it
checks for a `.survive` flag file next to its socket and picks a strategy:

- **No flag file (production)**: Watch `os.getppid()`.  When the parent
  `ansible-playbook` process exits, the watchdog sends `SIGTERM` to itself — clean
  shutdown, no orphans.
- **Flag file present (Molecule)**: Watch the flag file.  When `destroy.yml` removes
  it, the watchdog sends `SIGTERM` to itself — clean shutdown, no PID-file parsing or
  `kill` needed.

`default/create.yml` touches the flag; `default/destroy.yml` removes it and waits for
the socket to disappear.  No environment variables — the `.survive` file is the only
interface.

**Reconnection tiers:**

| Tier | Scope | Mechanism |
|------|-------|-----------|
| 1 | Task-to-task (same playbook) | `ansible_facts` with socket + authkey |
| 2 | Task/playbook-to-playbook | Socket + keyfile on disk |

Runtime files (`.sock`, `.key`, `.pid`) are always written so both tiers work in
all modes.

**Runtime directory**: `$XDG_RUNTIME_DIR/meraki_rm/` (per-user tmpfs, 0700).
Falls back to `/tmp/meraki_rm_<uid>/` if `XDG_RUNTIME_DIR` is unset.

```
$XDG_RUNTIME_DIR/meraki_rm/
├── manager_localhost.sock     # Unix domain socket
├── manager_localhost.pid      # PID (informational / fallback)
├── manager_localhost.key      # 32-byte authkey (0600)
└── manager_localhost.survive  # optional: watchdog watches file not ppid
```

**Rule**: `BaseManager` is designed for client-server use where the server is the main
process. When spawning as a child inside Ansible's fork model, you must always detach
from all three cleanup mechanisms (`_children`, `_finalizer_registry`, PGID signals).
Use a flag file — not an env var — for lifecycle control since the server child process
reads it after fork, and env vars don't propagate reliably through Ansible's process
tree.

### 26. Molecule Wildcard Scenario Selection

**Problem**: Running `molecule test -s 'appliance_vlans/*'` failed because the
`Scenarios._verify()` method compared the literal `appliance_vlans/*` against
resolved config names (`appliance_vlans/merged`, etc.) and rejected the mismatch.

**Fix**: After `get_configs()` resolves the glob to actual configs, replace
`scenario_names` with the discovered config names. This lets the verify pass
naturally for wildcard expansions. Combined with the collection-mode path-based
`_resolve_scenario_glob`, users can target all states for a module with a single
`-s 'module/*'` flag.

**Rule**: When glob-based discovery happens before name validation, the validation
must accept the expanded names, not the original glob pattern.

---

## Related Documents

- [01-overview.md](01-overview.md) — Architecture context and vision
- [06-foundation-components.md](06-foundation-components.md) — Core component specs (adapt for Meraki)
- [07-adding-resources.md](07-adding-resources.md) — Step-by-step workflow for each module
- [08-code-generators.md](08-code-generators.md) — Code generation (schema extractor replaces `generate_api_models.sh`)
- [10-case-study-novacom.md](10-case-study-novacom.md) — NovaCom module map (Meraki equivalent)
- [11-testing-strategy.md](11-testing-strategy.md) — Mock server, Molecule, testing workflow

*Document version: 1.7 | Meraki Dashboard (`cisco.meraki_rm`) | Implementation Guide*
