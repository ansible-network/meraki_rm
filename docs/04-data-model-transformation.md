# Data Model Transformation

This document explains the three-tier data class transformation pattern used to bridge user-facing configuration and vendor-specific API schemas. NovaCom Networks serves as the fictitious example throughout: a cloud-managed network infrastructure provider (wireless APs, switches, appliances, cameras) with the NovaCom Dashboard API (REST/OpenAPI 3.0, camelCase naming, deep endpoint hierarchy).

---

## Section 1: The Three-Tier Data Flow

The pattern for modern collections involves a **three-tier data flow** ensuring the user-facing YAML remains clean while vendor-specific API complexities are isolated. Each tier has a distinct responsibility and crosses a well-defined boundary.

### The Three Tiers

| Tier | Name | Responsibility | Boundary |
|------|------|----------------|----------|
| **1** | User Model (Ansible Data Class) | Flat, human-readable model derived from the argspec. snake_case, normalized terminology. | Crosses the RPC boundary; stable interface for all presentation layers |
| **2** | Transformation Mixin | Logic that "hoists" or "sinks" data between formats. Field mapping, name translation, ID lookups. | Lives entirely within the manager; never exposed to callers |
| **3** | Device Model (API Data Class) | Strict mirror of the OpenAPI schema for serialization. camelCase, vendor naming, nested structures. | Internal to the manager; used only for API communication |

### Data Flow Overview

```
USER (Playbook / MCP Tool / CLI)
    │
    │  config: [{ vlan_id: 100, name: Engineering, dhcp_handling: run_server }]
    │  (User Model format — snake_case, flat, human-readable)
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER (Ansible action plugin / MCP tool handler)               │
│  Validates input, creates User Model dataclass, sends to manager via RPC     │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    │  RPC BOUNDARY — only User Model data crosses
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  MANAGER (Persistent process)                                                │
│                                                                             │
│  1. TRANSFORMATION MIXIN: Sink (User → Device)                               │
│     - Field mapping: vlan_id → id, dhcp_handling → dhcpHandling             │
│     - Name-to-ID lookups if needed                                           │
│     - Structure nesting (flat → nested)                                      │
│                                                                             │
│  2. DEVICE MODEL: API payload                                                │
│     { id: 100, name: "Engineering", dhcpHandling: "run_server", ... }        │
│                                                                             │
│  3. API CLIENT: HTTP calls                                                   │
│     PUT /networks/N_12345/appliance/vlans/100                                │
│                                                                             │
│  4. API RESPONSE: Device Model format                                        │
│     { id: 100, networkId: "N_12345", dhcpHandling: "run_server", ... }        │
│                                                                             │
│  5. TRANSFORMATION MIXIN: Hoist (Device → User)                              │
│     - Field mapping: id → vlan_id, dhcpHandling → dhcp_handling             │
│     - ID-to-name lookups if needed                                           │
│     - Structure flattening (nested → flat)                                    │
│                                                                             │
│  6. USER MODEL: Result returned to caller                                    │
│     { vlan_id: 100, name: Engineering, dhcp_handling: run_server }           │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    │  RPC BOUNDARY — only User Model data crosses
    ▼
USER receives gathered/after state in same format as input
```

### Why Three Tiers?

- **User Model** — The stable contract. Ansible playbooks, MCP tools, and CLI all speak this language. It does not change when the API version changes or when the vendor adds internal fields.
- **Transformation Mixin** — Where developer value lives. Encapsulates all vendor-specific knowledge: field names, nesting, lookups, multi-endpoint orchestration. One place to maintain when the API evolves.
- **Device Model** — Auto-generated from OpenAPI. Stays in sync with the API schema. Never exposed; callers never see camelCase or nested structures.

---

## Section 2: User Model

The User Model is the **stable interface** that crosses the RPC boundary. It is what the user writes in YAML and what they receive back from gather/after operations.

### Characteristics

| Characteristic | Description |
|----------------|-------------|
| **Flat** | No deep nesting. Fields are at the top level of each entity instance. |
| **Human-readable** | Names that make sense to a network engineer, not a JSON schema. |
| **Ansible-idiomatic** | Follows Ansible conventions: snake_case, normalized terminology. |
| **snake_case** | All field names use snake_case (`dhcp_handling`, not `dhcpHandling`). |
| **Normalized terminology** | Industry-standard or intuitive names: `auth_mode` not `authMode`, `bandwidth_limit_up` not `perClientBandwidthLimitUp`. |
| **Names over IDs** | Where possible, use human-readable names (organization names) instead of opaque IDs. |
| **Read-only fields** | Fields like `id`, `created_at` are marked read-only; returned from API but not accepted as input. |
| **Write-only fields** | Fields like `password`, `api_key` are accepted on create/update but never returned (security). |
| **Generated from DOCUMENTATION** | The argspec and User Model structure derive from the same schema/DOCUMENTATION strings. |

### NovaCom VLAN User Model Example

```python
from dataclasses import dataclass
from typing import Optional, List

from library.transforms.base_transform import BaseTransformMixin


@dataclass
class UserVlan(BaseTransformMixin):
    """User-facing VLAN model. Flat, snake_case, Ansible-idiomatic."""

    vlan_id: int
    name: Optional[str] = None
    subnet: Optional[str] = None
    appliance_ip: Optional[str] = None
    dhcp_handling: Optional[str] = None  # "run_server", "relay", "none"
    dhcp_relay_servers: Optional[List[str]] = None
    dns_nameservers: Optional[str] = None
    id: Optional[int] = None  # read-only; returned after creation

    # Additional fields for full coverage (abbreviated for clarity):
    # reserved_ip_ranges, dhcp_boot_filename, etc.
```

### Field Semantics

- **`vlan_id`** — The logical identifier (1–4094). User provides this; it maps to the API's `id` for existing VLANs or is used on create.
- **`name`** — Human-readable VLAN name. Maps 1:1 to API `name` (with case conversion).
- **`dhcp_handling`** — Normalized: `run_server`, `relay`, `none`. API may use `runServer`, `relay`, `none`; the mixin translates.
- **`dhcp_relay_servers`** — List of IPs. API uses `dhcpRelayServerIps`; mixin maps.
- **`id`** — Read-only. The API returns an internal ID after creation; we expose it for reference but do not accept it as input.

### Round-Trip Contract

The User Model defines both input and output. What the user provides in `config` is the same structure they receive in `gathered` and `after`. No separate RETURN schema. This enables:

- Diff comparison (desired vs actual) using identical field names
- Idempotency checks (compare before/after)
- Re-use of gathered data as input to another task

---

## Section 3: Device Model

The Device Model is a **strict mirror** of the OpenAPI schema. It exists solely for serialization to and from the API.

### Characteristics

| Characteristic | Description |
|----------------|-------------|
| **Mirrors API schema** | Field names, types, and structure match the API payload exactly. |
| **camelCase** | Or whatever the API uses (NovaCom uses camelCase throughout). |
| **Nested structures** | Matches API payload shape; may have nested objects, arrays of objects. |
| **Generated** | Produced from OpenAPI spec using `datamodel-code-generator` or equivalent. |
| **Complete** | Contains all API fields including internal ones the user never sees. |
| **Not exposed** | Never crosses the RPC boundary; callers never receive Device Model instances. |

### NovaCom VLAN Device Model Example

```python
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Vlan:
    """Device-facing VLAN model. Matches NovaCom API schema exactly."""

    id: Optional[int] = None
    networkId: Optional[str] = None
    applianceIp: Optional[str] = None
    cidr: Optional[str] = None
    dhcpBootFilename: Optional[str] = None
    dhcpHandling: Optional[str] = None
    dhcpRelayServerIps: Optional[List[str]] = None
    dnsNameservers: Optional[str] = None
    name: Optional[str] = None
    subnet: Optional[str] = None
    reservedIpRanges: Optional[List[str]] = None
    vlanTag: Optional[int] = None
    # ... many more API-specific fields
```

### Why a Separate Device Model?

- **Type safety** — Serialization/deserialization is explicit. No ad-hoc dict manipulation.
- **API evolution** — When NovaCom adds a field, regenerate the Device Model; the User Model and transform logic can remain unchanged if the new field is internal.
- **Validation** — The Device Model can enforce API constraints (e.g., `dhcpHandling` enum values) before sending.
- **Tooling** — Code generators produce the Device Model from OpenAPI; no manual maintenance of API field names.

---

## Section 4: Transformation Mixin — The Bridge

The Transformation Mixin is **where the developer adds value**. It defines how data moves between User Model and Device Model.

### Responsibilities

1. **Field mapping** — How fields map between user and device models (including name translation).
2. **Custom transformations** — Functions for complex conversions (names → IDs, value normalization).
3. **Endpoint operations** — Which API endpoints to call and in what order (critical for multi-endpoint entities like SSIDs).

### Hoisting (Device → User)

**Hoisting** extracts deeply nested API data into flat, user-friendly fields.

**Example:** NovaCom's wireless SSID API returns firewall rules under a nested path:

```
GET /networks/{id}/wireless/ssids/{num}
Response includes: (or from sub-endpoint)
  firewall: {
    l3FirewallRules: {
      rules: [ { policy: "deny", protocol: "tcp", ... } ]
    }
  }
```

The User Model has a flat field:

```python
l3_firewall_rules: Optional[List[dict]] = None
```

The mixin **hoists** `firewall.l3FirewallRules.rules` → `l3_firewall_rules`. The user sees a simple list; they never see the nested `firewall` object.

### Sinking (User → Device)

**Sinking** takes flat user-friendly fields and rebuilds nested API structures. It is the reverse of hoisting.

**Example:** The user provides:

```yaml
l3_firewall_rules:
  - policy: deny
    protocol: tcp
    dest_port: "80"
    dest_cidr: "0.0.0.0/0"
```

The mixin **sinks** this into the structure required by:

```
PUT /networks/{id}/wireless/ssids/{num}/firewall/l3FirewallRules
Body: { "rules": [ { "policy": "deny", "protocol": "tcp", "destPort": "80", "destCidr": "0.0.0.0/0" } ] }
```

The user never constructs the nested payload or knows the endpoint path.

### NovaCom VLAN Transform Mixin Example

```python
from library.transforms.base_transform import BaseTransformMixin
from library.models.user_model import UserVlan
from library.models.device_model import Vlan


class VlanTransformMixin_v1(BaseTransformMixin):
    """Transform between UserVlan and NovaCom API Vlan schema."""

    _field_mapping = {
        # User model field (snake_case) -> Device model field (camelCase)
        'vlan_id': 'id',
        'name': 'name',
        'subnet': 'subnet',
        'appliance_ip': 'applianceIp',
        'dhcp_handling': 'dhcpHandling',
        'dhcp_relay_servers': 'dhcpRelayServerIps',
        'dns_nameservers': 'dnsNameservers',
        'reserved_ip_ranges': 'reservedIpRanges',
    }

    _transform_registry = {
        # Custom transforms: e.g., name-to-ID lookups
        # 'organization': ('organizationId', org_name_to_id, org_id_to_name),
    }

    # Endpoint operations for this entity
    _create_endpoint = "/networks/{network_id}/appliance/vlans"
    _get_endpoint = "/networks/{network_id}/appliance/vlans/{vlan_id}"
    _update_endpoint = "/networks/{network_id}/appliance/vlans/{vlan_id}"
    _delete_endpoint = "/networks/{network_id}/appliance/vlans/{vlan_id}"
    _list_endpoint = "/networks/{network_id}/appliance/vlans"
```

### How BaseTransformMixin Uses the Mapping

The `BaseTransformMixin` provides generic methods:

- **`to_device(user_instance)`** — Applies `_field_mapping` in the forward direction (User → Device). For each user field, looks up the device field name, converts value if a transform is registered, and sets it on the Device Model.
- **`to_user(device_instance)`** — Applies `_field_mapping` in the reverse direction (Device → User). For each device field, finds the corresponding user field, applies reverse transform if any, and sets it on the User Model.

The same `_field_mapping` drives both directions; the mixin applies it bidirectionally.

---

## Section 5: Case Study — Clean Fit: NovaCom Organizations API

NovaCom's Organizations API is **API-first** with flat structures. The JSON returned by GET is nearly identical to what PUT expects. Transformation is trivial.

### API Structure

**GET /organizations/{orgId}** returns:

```json
{
  "id": 12345,
  "name": "Acme Corp",
  "api": {
    "enabled": true
  },
  "licensing": {
    "model": "per-device"
  }
}
```

**PUT /organizations/{orgId}** expects the same shape. No deep nesting of configurable fields; no asymmetric GET/PUT.

### User Model vs Device Model

| User Model (snake_case) | Device Model (camelCase) | Mapping |
|-------------------------|--------------------------|---------|
| `org_id` | `id` | 1:1 (name differs) |
| `name` | `name` | 1:1 |
| `api_enabled` | `api.enabled` | Nested (dot notation) |
| `licensing_model` | `licensing.model` | Nested (dot notation) |

### Transformation Complexity: Minimal

- Almost all fields map 1:1 with just camelCase → snake_case conversion.
- A few fields use dot notation for shallow nesting (`api.enabled` → `api_enabled`).
- No hoisting/sinking of deeply nested structures.
- No custom transforms (no name-to-ID lookups for Organizations themselves).
- **Agent/automation can generate the entire module with ~95% accuracy.**

### Before (API) and After (User Model)

**API response (Device Model):**

```json
{
  "id": 12345,
  "name": "Acme Corp",
  "api": { "enabled": true },
  "licensing": { "model": "per-device" }
}
```

**User Model (after hoisting):**

```python
UserOrganization(
    org_id=12345,
    name="Acme Corp",
    api_enabled=True,
    licensing_model="per-device"
)
```

**User Model (user input, before sinking):**

```yaml
config:
  - name: Acme Corp
    api_enabled: true
    licensing_model: per-device
```

**Device Model (after sinking, sent to API):**

```json
{
  "name": "Acme Corp",
  "api": { "enabled": true },
  "licensing": { "model": "per-device" }
}
```

The transformation is mechanical. A code generator can produce the mixin from the OpenAPI spec with minimal human intervention.

---

## Section 6: Case Study — Messy Fit: NovaCom Wireless SSID API

NovaCom's SSID API is a **legacy-wrapper** with significant complexity. It requires full hoisting and sinking.

### API Characteristics

| Characteristic | Description |
|----------------|-------------|
| **Deep nesting** | Firewall rules, traffic shaping, splash settings live under sub-paths. |
| **Multiple endpoints per entity** | Six endpoints for one SSID. |
| **Asymmetric GET/PUT** | GET may return a full tree; PUT expects specific branches to specific endpoints. |
| **Implicit defaults** | Some settings are invisible until explicitly configured. |

### The Six Endpoints

| Sub-Resource | Endpoint | User-Facing Field |
|--------------|----------|-------------------|
| Basic settings | `PUT /networks/{id}/wireless/ssids/{num}` | `name`, `enabled`, `auth_mode`, `band_selection`, etc. |
| PSK | Same endpoint (fields in body) | `psk` |
| L3 firewall | `PUT .../ssids/{num}/firewall/l3FirewallRules` | `l3_firewall_rules` |
| L7 firewall | `PUT .../ssids/{num}/firewall/l7FirewallRules` | `l7_firewall_rules` |
| Traffic shaping | `PUT .../ssids/{num}/trafficShaping/rules` | `traffic_shaping_rules` |
| Splash settings | `PUT .../ssids/{num}/splash/settings` | `splash_settings` |

### Hoisting Example

**API GET** (or multiple GETs to sub-endpoints) returns:

```json
{
  "number": 1,
  "name": "Guest-Wi-Fi",
  "enabled": true,
  "authMode": "psk"
}
```

From `GET .../firewall/l3FirewallRules`:

```json
{
  "rules": [
    {
      "policy": "deny",
      "protocol": "tcp",
      "destPort": "80",
      "destCidr": "0.0.0.0/0"
    }
  ]
}
```

The mixin **hoists** these into a single User Model:

```python
UserSsid(
    number=1,
    name="Guest-Wi-Fi",
    enabled=True,
    auth_mode="psk",
    l3_firewall_rules=[
        {"policy": "deny", "protocol": "tcp", "dest_port": "80", "dest_cidr": "0.0.0.0/0"}
    ]
)
```

### Sinking Example

The user provides flat config. The mixin must:

1. Split into payloads for each endpoint.
2. Call endpoints in the correct order (basic settings before firewall, etc.).
3. Handle conditional fields (e.g., `psk` only when `auth_mode: psk`).

### SSID Transform Mixin (Simplified)

```python
class SsidTransformMixin_v1(BaseTransformMixin):
    """Transform for NovaCom Wireless SSID. Multi-endpoint aggregation."""

    _field_mapping = {
        'number': 'number',
        'name': 'name',
        'enabled': 'enabled',
        'auth_mode': 'authMode',
        'psk': 'psk',
        'band_selection': 'bandSelection',
        'splash_page': 'splashPage',
        # ... basic fields
    }

    # Sub-resource mappings (hoisted fields -> endpoint + payload path)
    _sub_resource_mapping = {
        'l3_firewall_rules': {
            'endpoint': '/networks/{network_id}/wireless/ssids/{number}/firewall/l3FirewallRules',
            'payload_key': 'rules',
            'method': 'PUT',
        },
        'l7_firewall_rules': {
            'endpoint': '/networks/{network_id}/wireless/ssids/{number}/firewall/l7FirewallRules',
            'payload_key': 'rules',
            'method': 'PUT',
        },
        'traffic_shaping_rules': {
            'endpoint': '/networks/{network_id}/wireless/ssids/{number}/trafficShaping/rules',
            'payload_key': 'rules',
            'method': 'PUT',
        },
        'splash_settings': {
            'endpoint': '/networks/{network_id}/wireless/ssids/{number}/splash/settings',
            'payload_key': None,  # entire body
            'method': 'PUT',
        },
    }

    def gather(self, context):
        """Gather requires multiple GET calls, then merge into User Model."""
        # 1. GET basic SSID settings
        basic = self._api.get(f"/networks/{context['network_id']}/wireless/ssids/{number}")
        user_data = self.to_user(basic)

        # 2. GET each sub-resource, hoist into user_data
        for field, config in self._sub_resource_mapping.items():
            resp = self._api.get(config['endpoint'].format(**context, number=number))
            if config['payload_key']:
                user_data[field] = self._normalize_rules(resp.get(config['payload_key'], []))
            else:
                user_data[field] = self._normalize_splash(resp)
        return user_data

    def apply(self, user_instance, context):
        """Apply requires multiple PUT calls in correct order."""
        # 1. PUT basic settings first (required before sub-resources)
        basic_payload = self.to_device(user_instance)
        self._api.put(f"/networks/{context['network_id']}/wireless/ssids/{user_instance.number}", basic_payload)

        # 2. PUT each sub-resource if present in user config
        for field, config in self._sub_resource_mapping.items():
            value = getattr(user_instance, field, None)
            if value is not None:
                payload = {config['payload_key']: value} if config['payload_key'] else value
                self._api.put(config['endpoint'].format(**context, number=user_instance.number), payload)
```

### Complexity Difference from Organizations

| Aspect | Organizations (Clean) | SSID (Messy) |
|--------|------------------------|--------------|
| Endpoints per entity | 1 | 6 |
| Hoisting | None (flat) | Full (4+ sub-resources) |
| Sinking | Simple 1:1 | Multi-step, ordered |
| Custom transforms | None | Possibly (e.g., rule normalization) |
| Call ordering | N/A | Critical (basic before firewall) |
| Agent automation | ~95% | ~60% (human must design aggregation) |

---

## Section 7: Bidirectional Transformation

Transformation works in both directions. The same field mapping definition drives both; only the direction of application changes.

### Forward: User Model → Device Model (Writing to API)

When the user provides desired state and the manager must call the API:

| Step | Operation | Example |
|------|------------|---------|
| 1 | Field name translation | `dhcp_handling` → `dhcpHandling` |
| 2 | Name-to-ID lookups | `organizations: ["Engineering"]` → `organizationIds: [1]` |
| 3 | Structure nesting | `api_enabled: true` → `api: { enabled: true }` |
| 4 | Value normalization | `dhcp_handling: "run_server"` → `dhcpHandling: "runServer"` (if API uses different enum) |

### Reverse: Device Model → User Model (Reading from API)

When the API returns data and the manager must produce user-facing output:

| Step | Operation | Example |
|------|------------|---------|
| 1 | Field name translation | `dhcpHandling` → `dhcp_handling` |
| 2 | ID-to-name lookups | `organizationIds: [1]` → `organizations: ["Engineering"]` |
| 3 | Structure flattening | `firewall: { l3FirewallRules: { rules: [...] } }` → `l3_firewall_rules: [...]` |
| 4 | Value normalization | `dhcpHandling: "runServer"` → `dhcp_handling: "run_server"` |

### Same Mapping, Opposite Direction

The `BaseTransformMixin` uses a single `_field_mapping` dictionary. For forward transform, it iterates user fields and sets device fields. For reverse, it iterates device fields and sets user fields. The mapping is symmetric:

```python
_field_mapping = {
    'vlan_id': 'id',           # User vlan_id <-> Device id
    'dhcp_handling': 'dhcpHandling',
    'dhcp_relay_servers': 'dhcpRelayServerIps',
}
```

Forward: `user.vlan_id` → `device.id`  
Reverse: `device.id` → `user.vlan_id`

Custom transforms in `_transform_registry` have both forward and reverse functions (e.g., `org_name_to_id` and `org_id_to_name`) so lookups work both ways.

---

## Section 8: Nested Field Support

APIs often nest fields. The User Model stays flat; the mixin handles nesting via **dot notation**.

### Dot Notation

A user field `address_city` can map to `address.city` in the Device Model. The `BaseTransformMixin` interprets dot-delimited paths:

- **Sinking:** Set `device.address.city = value` when user provides `address_city`.
- **Hoisting:** Set `user.address_city = device.address.city` when reading from API.

### NovaCom Example: Organization Address

**Device Model (API):**

```json
{
  "id": 12345,
  "name": "Acme Corp",
  "address": {
    "street": "123 Main St",
    "city": "San Francisco",
    "state": "CA",
    "zip": "94105"
  }
}
```

**User Model (flat):**

```python
@dataclass
class UserOrganization:
    org_id: Optional[int] = None
    name: Optional[str] = None
    address_street: Optional[str] = None
    address_city: Optional[str] = None
    address_state: Optional[str] = None
    address_zip: Optional[str] = None
```

**Field mapping:**

```python
_field_mapping = {
    'org_id': 'id',
    'name': 'name',
    'address_street': 'address.street',
    'address_city': 'address.city',
    'address_state': 'address.state',
    'address_zip': 'address.zip',
}
```

### Implementation in BaseTransformMixin

The mixin must support get/set on dotted paths:

```python
def _get_nested(obj, path: str):
    """Get value at dotted path, e.g., 'address.city'."""
    for key in path.split('.'):
        obj = getattr(obj, key, None) or (obj.get(key) if isinstance(obj, dict) else None)
        if obj is None:
            return None
    return obj

def _set_nested(obj, path: str, value):
    """Set value at dotted path, creating nested dicts/objects as needed."""
    keys = path.split('.')
    for key in keys[:-1]:
        obj = obj.setdefault(key, {}) if isinstance(obj, dict) else getattr(obj, key, None)
    if isinstance(obj, dict):
        obj[keys[-1]] = value
    else:
        setattr(obj, keys[-1], value)
```

---

## Section 9: Agent Automation Boundary

Not all transformation work can be automated. The following table clarifies what an agent can do easily versus what requires human judgment.

### What an Agent CAN Do Easily

| Task | Description |
|------|-------------|
| **Scaffold boilerplate** | Generate argspec, imports, class structure from schema. |
| **Map simple 1:1 fields** | camelCase ↔ snake_case conversion for fields that align. |
| **Generate unit test shells** | Test structure, fixtures for valid/invalid input. |
| **Create Device Model from OpenAPI** | Use `datamodel-code-generator` to produce API data classes. |
| **Mechanical multi-endpoint aggregation** | When endpoints are documented and mapping is obvious. |
| **Dot notation for shallow nesting** | `address.city` → `address_city` when structure is clear. |

### What a Human MUST Do

| Task | Description |
|------|-------------|
| **Semantic normalization** | `bandSelection` → `band_selection` vs `radio_band_preference`? The choice affects usability. |
| **State-machine logic** | SSID auth mode changes may require resetting dependent fields (e.g., switching from `psk` to `radius` clears `psk`). |
| **Conditional dependencies** | `auth_mode: psk` requires `psk` field; `auth_mode: radius` requires `radius_servers`. Validation and transform logic must encode this. |
| **Ambiguous override logic** | What happens to default SSID 0 when `state: overridden` is used? Can it be deleted? Does it get reset? |
| **Multi-step operation ordering** | Domain knowledge: basic SSID settings must be applied before firewall rules. |
| **Implicit default handling** | API may not return fields until they are set; gather must handle missing vs. default. |
| **Name-to-ID lookup paths** | Which API endpoint provides the lookup? What is the cache key? |

### Summary Table: Clean vs Messy Fit

| Characteristic | Clean Fit (e.g., Organizations) | Messy Fit (e.g., SSID) |
|----------------|----------------------------------|------------------------|
| **API structure** | Flat, symmetric GET/PUT | Nested, asymmetric |
| **Endpoints per entity** | 1 | 2–6+ |
| **Field mapping** | Mostly 1:1, case conversion | Many custom mappings, hoisting, sinking |
| **Custom transforms** | None or trivial | Name-to-ID, value normalization |
| **Call ordering** | N/A | Critical |
| **State machine logic** | None | Auth mode, conditional fields |
| **Override semantics** | Straightforward | Edge cases (default SSID, etc.) |
| **Agent automation** | ~95% | ~60% |
| **Human review** | Light (naming choices) | Heavy (aggregation design, edge cases) |

### Rule of Thumb

If the mapping is **mechanical** (field A in user model maps to field B in API, with predictable conversion), the agent handles it. If the mapping requires **domain knowledge** (what does this field mean, when is it valid, what are the side effects), a human must review and implement.

---

## Summary

The three-tier data flow — User Model, Transformation Mixin, Device Model — isolates vendor-specific complexity while presenting a stable, human-readable interface. NovaCom's Organizations API demonstrates a clean fit where transformation is mostly mechanical; the SSID API demonstrates a messy fit requiring full hoisting, sinking, and multi-endpoint orchestration. The `BaseTransformMixin` provides generic bidirectional transformation driven by field mappings; dot notation handles nested fields. Agents can automate the majority of clean-fit modules and scaffold messy-fit ones, but semantic decisions, state machines, and edge cases require human expertise.
