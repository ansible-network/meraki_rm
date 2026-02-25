# Design Principles: Architectural Guardrails, Validation Strategy, and Quality Gates

This document defines the architectural guardrails, validation strategy, and quality gates for OpenAPI-driven Ansible module generation. All examples use **NovaCom Networks** as the fictitious reference—a cloud-managed network infrastructure platform with the NovaCom Dashboard API.

---

## SECTION 1: Principle 1 — Entity Aggregation

### Core Rule

**Do NOT create a module for every endpoint.** Instead, identify the **Root Resource** and group sub-resources into a single config dictionary.

### The Anti-Pattern

When an agent naively maps one endpoint to one module, it produces fragmentation:

```
novacom_vlan           # GET/PUT/DELETE /vlans/{vlan_id}
novacom_vlan_ports     # GET/PUT /vlans/{vlan_id}/ports
novacom_vlan_dhcp      # GET/PUT /vlans/{vlan_id}/dhcp
```

This forces users to run three separate tasks for a single logical entity (a VLAN). It violates idempotency, complicates playbooks, and creates race conditions when multiple tasks touch the same underlying resource.

### The Resource Way

Group all sub-resources that share the same **Primary Key** into a single module:

```yaml
# novacom_appliance_vlan — ONE module, ONE config
- name: Configure VLAN 10 with ports and DHCP
  novacom_appliance_vlan:
    vlan_id: 10
    name: "Engineering"
    ports:
      - port_id: "1"
        tagged: true
      - port_id: "2"
        tagged: false
    dhcp_settings:
      enabled: true
      lease_time: 86400
      dns_servers:
        - 8.8.8.8
    state: merged
```

The argspec handles `vlan_id`, `ports`, and `dhcp_settings` as nested keys. One task, one logical entity.

### Logic: Primary Key as the Aggregation Criterion

**If three endpoints share the same Primary Key (e.g., `vlan_id`), they belong in the same module.**

| Endpoint | Primary Key | Conclusion |
|----------|-------------|------------|
| `GET /vlans/{vlan_id}` | `vlan_id` | Same resource |
| `GET /vlans/{vlan_id}/ports` | `vlan_id` | Same resource |
| `GET /vlans/{vlan_id}/dhcp` | `vlan_id` | Same resource |

All three are facets of the same entity. One module: `novacom_appliance_vlan`.

### NovaCom Example: SSID Endpoints

The NovaCom Dashboard API exposes six distinct endpoints for wireless SSIDs:

| Endpoint | Purpose |
|----------|---------|
| `GET/PUT /networks/{netId}/wireless/ssids/{num}` | Core SSID config (name, auth, band) |
| `GET/PUT /networks/{netId}/wireless/ssids/{num}/firewall/l3Rules` | L3 firewall rules |
| `GET/PUT /networks/{netId}/wireless/ssids/{num}/firewall/l7Rules` | L7 firewall rules |
| `GET/PUT /networks/{netId}/wireless/ssids/{num}/splash` | Splash page settings |
| `GET/PUT /networks/{netId}/wireless/ssids/{num}/trafficShaping` | Traffic shaping |
| `GET/PUT /networks/{netId}/wireless/ssids/{num}/vpn` | VPN passthrough |

All six share the same Primary Key: `(network_id, ssid_number)`.

**Result:** Six endpoints → **one module** (`novacom_wireless_ssid`). The config dictionary includes nested keys for `firewall`, `splash`, `traffic_shaping`, and `vpn`.

---

## SECTION 2: Principle 2 — Canonical Key Identity

### Core Rule

**Every resource module must identify resources by a Canonical Key — a human-meaningful, user-controlled field — not by an opaque, API-generated System Key.**

The framework distinguishes two kinds of identity:

- **Canonical Key**: The field a human uses to identify a resource. Stable, user-specified, meaningful. Examples: `name`, `email`, `vlan_id`, `prefix`, `iname`.
- **System Key**: The field the API generates internally for URL routing (PUT/DELETE paths). Opaque, server-assigned, never required from users in the normal workflow. Examples: `admin_id`, `rf_profile_id`, `static_delegated_prefix_id`.

The module resolves the system key behind the scenes by gathering current state and matching on the canonical key. The user never needs to know the UUID.

```
User writes:                    Framework resolves:
  name: "Engineering"     --->    rf_profile_id: "5a8f3b2c"
  email: "bob@corp.com"   --->    admin_id: "a1b2c3d4"
  vlan_id: 100            --->    (same — vlan_id is both)
```

### The Anti-Pattern

Exposing system-generated IDs as the primary identity:

```yaml
# BAD: User must know the API-generated UUID
- novacom_organization_admins:
    admin_id: "5a8f3b2c-d1e2-4f3a-b5c6-7d8e9f0a1b2c"
    name: "Bob Smith"
    state: merged
```

The user has no way to know `admin_id` without first gathering. If they created the admin weeks ago, the ID is lost. Every playbook becomes a two-step "gather then act" workflow.

### The Resource Way

Match by canonical key, resolve system key internally:

```yaml
# GOOD: User identifies by what they know
- novacom_organization_admins:
    email: "bob@corp.com"
    name: "Bob Smith"
    org_access: full
    state: merged
```

The module internally gathers all admins, finds the one with `email: "bob@corp.com"`, resolves `admin_id: "5a8f3b2c..."` from the gathered state, and uses it for the API call. The user never sees the UUID.

### Three Categories of Identity

**Category A — Canonical key IS the system key.** The user picks the value and the API uses it directly for routing. `CANONICAL_KEY` is set, `SYSTEM_KEY` is not needed.

| NovaCom Example | Canonical Key | System Key | Notes |
|---|---|---|---|
| `novacom_appliance_vlan` | `vlan_id` | (same) | User picks VLAN 10, API routes by `/vlans/10` |
| `novacom_vlan_profiles` | `iname` | (same) | User-defined identifier |
| `novacom_switch_access_policies` | `access_policy_number` | (same) | User-assigned number |

**Category B — Canonical key differs from system key.** The module matches by canonical key and resolves the system key behind the scenes. Both `CANONICAL_KEY` and `SYSTEM_KEY` are set.

| NovaCom Example | Canonical Key | System Key | Notes |
|---|---|---|---|
| `novacom_organization_admins` | `email` | `admin_id` | Email is unique per org |
| `novacom_wireless_rf_profiles` | `name` | `rf_profile_id` | Name is human-meaningful |
| `novacom_appliance_prefixes` | `prefix` | `static_delegated_prefix_id` | Subnet string is the identity |
| `novacom_webhooks` | `name` | `http_server_id` | Name chosen by user |

**Category C — No canonical key exists.** The resource has no human-meaningful unique field. `CANONICAL_KEY` is `None`, only `SYSTEM_KEY` is set. The framework resolves system keys automatically so the user does not need to discover or provide them:

- **`merged` / `deleted`**: The framework uses *content-based matching* — it compares all user-supplied fields against existing resources to find the correct target, then injects the system key for the API call.
- **`replaced` / `overridden`**: Content-based matching cannot work because the desired values intentionally differ from the current state. The framework falls back to *positional matching* — the Nth desired item maps to the Nth existing item.
- **`overridden` with new items**: After deleting extras, any desired item that has no existing match is created via a `POST` (no system key needed).

Users *may* still provide the system key explicitly as an escape hatch (see below), but it is not required for normal operation.

| NovaCom Example | Canonical Key | System Key | Notes |
|---|---|---|---|
| `novacom_switch_qos_rules` | (none) | `qos_rule_id` | Rules defined by dscp/vlan/protocol — no name |
| `novacom_switch_link_aggregations` | (none) | `link_aggregation_id` | Only port lists, no name |

### Duplicate Canonical Key Handling

The framework assumes canonical keys are unique within scope. If duplicates are detected during gather:

1. The module **fails immediately** with a clear error: *"Multiple resources with name='Engineering' found. Provide 'rf_profile_id' to disambiguate."*
2. The user adds the system key to their config as a tiebreaker.
3. When the system key is provided explicitly, it takes precedence over canonical key matching.

This is a safety net, not a silent heuristic. The module never guesses which duplicate the user meant.

### System Key as Escape Hatch

For **any** category, if the user provides the system key in their config, it overrides canonical key matching:

```yaml
# Explicit system key — used when duplicates exist or for Category C
- novacom_wireless_rf_profiles:
    rf_profile_id: "abc-123"    # system key takes precedence
    name: "Engineering"
    state: merged
```

### Module Documentation Requirement

Every module's DOCUMENTATION must identify:

- The canonical key field (or state that none exists)
- The system key field (when different from canonical key)
- For Category C: a note that the resource has no canonical key and the framework matches by content or position

### Decision Criteria for Choosing the Canonical Key

When generating a new module, evaluate candidate fields in this order:

1. **`name`** — most common; human-meaningful, typically unique per scope
2. **`email`** — for user/admin resources
3. **Domain-specific identifier** — `prefix` (subnet string), `iname` (profile identifier), `url`
4. **Numeric user-assigned key** — `vlan_id`, `access_policy_number`, `ssid_number`
5. **No candidate** — Category C; halt and document as gather-first resource

### Stop Condition

If the agent cannot identify a canonical key candidate for a resource:

- **Halt.** Do not default to the system key as canonical.
- **Ask:** "No canonical key found for this resource. Confirm this is a Category C (gather-first) resource, or identify the canonical key field."

---

## SECTION 3: Principle 3 — CRUD Consolidation

### Core Rule

A single resource module **must** handle the entire lifecycle of an object. The agent is **FORBIDDEN** from creating separate modules for `get_info`, `update`, and `delete`.

### The Anti-Pattern

```
novacom_vlans_get_info    # GET /vlans
novacom_vlans_update      # PUT /vlans/{vlan_id}
novacom_vlans_delete      # DELETE /vlans/{vlan_id}
```

Users must remember which module does what. State management becomes fragmented. Idempotency is impossible to guarantee across three plugins.

### The Resource Way

**One module, full lifecycle.** If the spec has GET, PUT, and DELETE for `/vlans`, the agent must implement **one** `novacom_appliance_vlan` module (or `novacom_appliance_vlans` for the collection), not three separate plugins.

### State Parameter Requirement

Every module **MUST** support the `state` parameter with at least:

| State | Behavior |
|-------|----------|
| `merged` | Create or update. Idempotent merge of user config with existing. |
| `deleted` | Remove the resource. Idempotent (no-op if already absent). |
| `gathered` | Read-only. Fetch current state and return as structured data. |

Optional states (when supported by the API):

| State | Behavior |
|-------|----------|
| `replaced` | Replace entire config. Use when API supports full replacement. |
| `overridden` | Replace all instances of a collection (e.g., all VLANs). |

### NovaCom Example

For `/vlans` with GET, PUT, DELETE:

```yaml
# Create/update
- novacom_appliance_vlan:
    vlan_id: 10
    name: "Engineering"
    state: merged

# Delete
- novacom_appliance_vlan:
    vlan_id: 10
    state: deleted

# Gather (no changes)
- novacom_appliance_vlan:
    state: gathered
  register: vlans
```

One module, one interface, full lifecycle.

---

## SECTION 4: Principle 4 — Namespace Hoisting Threshold

### Core Rule

Autogenerated "goop" often mirrors the API path. Use a **Path Depth** threshold to force consolidation.

**The Rule:** Any path deeper than **3 segments** (excluding base URL) should be evaluated for "sinking" into a parent resource.

### Path Depth Calculation

Count path segments after the base. For NovaCom:

```
/organizations/{orgId}/sites/{siteId}/networks/{netId}/wireless/ssids/{num}/firewall/l3Rules
```

Segments: `organizations` → `sites` → `networks` → `wireless` → `ssids` → `firewall` → `l3Rules` = **7 segments**.

### The Anti-Pattern

```
novacom_ssid_firewall_l3_rules   # /.../ssids/{num}/firewall/l3Rules
novacom_ssid_firewall_l7_rules   # /.../ssids/{num}/firewall/l7Rules
novacom_ssid_splash             # /.../ssids/{num}/splash
novacom_ssid_traffic_shaping    # /.../ssids/{num}/trafficShaping
```

Five modules for one SSID. Users must orchestrate five tasks to configure a single wireless network.

### The Resource Way

**Sink** deep sub-resources into the parent. Instead of `novacom_ssid_firewall_l3_rules`, the L3 firewall rules become an **attribute** of `novacom_wireless_ssid`:

```yaml
- novacom_wireless_ssid:
    network_id: "N_abc123"
    number: 0
    name: "Corporate"
    auth_mode: psk
    firewall:
      l3_rules:
        - policy: allow
          protocol: tcp
          dest_port: "443"
      l7_rules:
        - policy: block
          type: "malware"
    splash:
      enabled: false
    state: merged
```

The module internally calls multiple endpoints, but the user sees one logical resource.

### Evaluation Criteria

When path depth > 3:

1. **Does the sub-resource have a lifecycle independent of the parent?** If no → sink.
2. **Is the sub-resource ever queried or managed alone?** If rarely → sink.
3. **Does sinking create an unwieldy argspec?** If yes → consider a separate module, but document the rationale.

For NovaCom SSID firewall rules: they are never managed without the SSID. Sink them.

---

## SECTION 5: Principle 5 — Data Normalization over API Mirroring

### Core Rule

The agent must **NOT** simply copy-paste OpenAPI `components/schemas` into user-facing field names.

If an API attribute name is a vendor-leaked internal term (e.g., `perClientBandwidthLimitUp`), the agent must flag it for human renaming to a standard Ansible term (e.g., `per_client_bandwidth_limit_up` or `bandwidth_limit_upload`).

**Human-readable names are mandatory.** If the agent cannot find a standard name, it must stop and ask.

### The Anti-Pattern

```yaml
# BAD: API schema leaked to user
- novacom_wireless_ssid:
    authMode: psk              # camelCase
    splashPage: "click"       # vendor term
    bandSelection: "auto"     # camelCase
    perClientBandwidthLimitUp: 1000   # internal naming
```

Users expect `snake_case`, descriptive names, and consistency with Ansible conventions.

### NovaCom Normalization Examples

| API Attribute | Normalized User-Facing Name |
|---------------|-----------------------------|
| `authMode` | `auth_mode` |
| `splashPage` | `splash_page` |
| `bandSelection` | `band_selection` |
| `perClientBandwidthLimitUp` | `per_client_bandwidth_limit_up` |
| `perClientBandwidthLimitDown` | `per_client_bandwidth_limit_down` |
| `ipV6` | `ipv6` (or `ip_v6` if context requires) |
| `radiusServers` | `radius_servers` |
| `minBitrate` | `min_bitrate` |
| `maxBitrate` | `max_bitrate` |
| `visible` | `visible` (already OK) |
| `encryptionMode` | `encryption_mode` |

### Normalization Rules

1. **camelCase → snake_case:** Always.
2. **Vendor jargon → domain standard:** `splashPage` → `splash_page` (or `captive_portal` if that's the domain term).
3. **Internal IDs → descriptive:** `num` → `ssid_number` or `number` in context.
4. **Abbreviations:** Expand when unclear. `maxBw` → `max_bandwidth`. Keep common ones: `id`, `url`, `ip`, `dns`.
5. **Boolean prefixes:** Prefer `enabled`, `is_visible`, `has_splash` over ambiguous `visible`, `splash`.

### Agent Responsibility

- **Apply** standard transformations (camelCase → snake_case).
- **Flag** ambiguous terms for human review.
- **Stop** when no clear mapping exists. Do not guess.

---

## SECTION 6: Principle 6 — Single-Session Transactions

### Core Rule

Autogenerated modules often make **one API call per parameter**. This is forbidden.

The Transformer Mixin must generate a **Single Payload** for the Device Data Class. **One task = one API transaction.**

### The Anti-Pattern

```python
# BAD: Loop of API calls
for key, value in user_config.items():
    api.patch(f"/vlans/{vlan_id}", {key: value})
```

Result: N network round-trips, race conditions, partial state on failure, and poor performance.

### The Resource Way

1. **Build** the full payload from user input.
2. **Validate** the payload against the argspec.
3. **Send** one PUT or PATCH with the complete body.
4. **Return** the response (or gathered state).

```python
# GOOD: Single transaction
payload = transform_user_config_to_api_format(user_config)
response = api.put(f"/vlans/{vlan_id}", json=payload)
return transform_api_response_to_ansible(response)
```

### Exception: Multi-Endpoint Resources

For aggregated resources (e.g., SSID with 6 sub-endpoints), multiple API calls are unavoidable. They must be:

1. **Orchestrated** by the convergence engine as a **single logical transaction**.
2. **Ordered** correctly (e.g., create SSID before configuring firewall).
3. **Optionally batched** via Action Batches when the API supports it (e.g., NovaCom Batch API).

```python
# Multi-endpoint: still one logical transaction
def _converge_ssid(self, desired, current):
    batch = []
    if desired.core != current.core:
        batch.append(("PUT", f"/ssids/{num}", desired.core))
    if desired.firewall != current.firewall:
        batch.append(("PUT", f"/ssids/{num}/firewall/l3Rules", desired.firewall))
    # ...
    self._execute_batch(batch)  # One batch, one logical commit
```

From the user's perspective: one task, one transaction. Internally: one batch or ordered sequence.

### Rejection Criterion

If the agent produces logic that loops API calls for individual fields, the code is **rejected**.

---

## SECTION 7: Principle 7 — Symmetric Validation

### Core Rule

A **single ArgumentSpec** (derived from DOCUMENTATION) is used for **BOTH** input and output validation.

- **Client** validates user input before sending to manager.
- **Client** validates manager response before returning to user.
- **Same spec** ensures round-trip compliance.
- Catches transformation bugs early.
- Manager bugs fail fast with clear errors.

### Validation Flow

```
                    DOCUMENTATION (Single Source)
                                    |
                                    +--> Generate ArgumentSpec
                                    |
                            +-------+-------+
                            |               |
                            v               v
                    INPUT VALIDATE    OUTPUT VALIDATE
                            |               ^
                            v               |
                    Client                  Manager
                    Creates                 Transforms
                    Ansible                 (API hidden)
                    Dataclass               Returns
                                            Ansible
                                            Dataclass
```

### Flow Explanation

1. **DOCUMENTATION** is the single source of truth. It defines the schema for the resource (options, types, suboptions).
2. **ArgumentSpec** is generated from DOCUMENTATION. One spec, one contract.
3. **Input validation:** Before the manager runs, the client validates `user_args` against the argspec. Invalid input fails immediately with a clear error.
4. **Manager** transforms validated input to API format, calls the API, transforms response back to Ansible format.
5. **Output validation:** Before returning to the user, the manager's response is validated against the **same** argspec. If the manager returns a malformed structure (e.g., wrong type, missing required field), validation fails. This catches transformation bugs and API contract drift.

### Implementation Example

```python
# SINGLE ARGSPEC (from DOCUMENTATION)
argspec = build_argspec(DOCUMENTATION)

# Used for INPUT validation
validated_input = validate_data(user_args, argspec, direction='input')

# Used for OUTPUT validation (same spec!)
validated_output = validate_data(manager_response, argspec, direction='output')
```

### Direction Semantics

- **`direction='input'`:** Enforce required fields, reject unknown keys (if strict), coerce types. Filter write-only fields from validation (they may be absent in input).
- **`direction='output'`:** Enforce structure, coerce types. Filter read-only fields from write validation. Ensure gathered output matches merged input format.

### Benefits

| Benefit | Description |
|---------|-------------|
| Single source of truth | DOCUMENTATION drives both validation paths. No drift. |
| Symmetric contract | What you send is what you can receive. Round-trip guarantee. |
| Catches manager bugs | If the manager returns `authMode` instead of `auth_mode`, output validation fails. |
| Type safety at runtime | Python is dynamic; validation provides runtime type checking. |
| Clear error messages | "Field 'vlan_id' is required" vs. cryptic API 400. |
| No separate RETURN section | The argspec defines the return structure. RETURN can reference it. |

---

## SECTION 8: Stop Conditions for Code Generation

The agent **MUST** halt and escalate when it detects the following conditions.

### 1. Duplicate Schemas

**Condition:** Two different endpoints use the **exact same JSON schema** but different paths.

**Example:** NovaCom has `GET /networks/{id}/vlans` and `GET /appliances/{id}/vlans`. Both return the same `Vlan` schema.

**Interpretation:** This is a sign they should be a single "abstract" module (e.g., `novacom_vlan`) with a parameter to select context (network vs. appliance), or the agent must ask: "Are these the same logical resource?"

**Action:** Halt. Do not generate two modules. Ask human: "Unify into one module with context parameter, or keep separate with documented rationale?"

---

### 2. Circular References

**Condition:** The OpenAPI spec has **circular pointers** in schemas.

**Example:**
```yaml
Vlan:
  properties:
    ports:
      $ref: '#/components/schemas/Port'
Port:
  properties:
    vlan:
      $ref: '#/components/schemas/Vlan'
```

**Interpretation:** Naive dataclass generation produces infinite recursion. Python cannot represent this without forward references or breaking the cycle.

**Action:** Halt. Report: "Circular reference detected: Vlan ↔ Port. Human must define acyclic view (e.g., Port references vlan_id only, not full Vlan object)."

---

### 3. Missing Keys

**Condition:** An endpoint has **no unique identifier**—no `name`, `id`, or composite key field.

**Example:** NovaCom `GET /networks/{id}/events` returns a list of events with no stable `id` field, only `timestamp` and `message`.

**Interpretation:** The agent cannot maintain idempotency. It cannot answer "does this resource exist?" or "should I create or update?"

**Action:** Halt. Ask human: "Define a composite key for idempotency (e.g., timestamp + message_hash) or mark as gather-only (no merged/deleted)."

---

## SECTION 9: Quality Checklist

For **every** resource module, verify the following before merge.

### Argspec and User Model

- [ ] **Argspec is flat and human-readable** — No nested vendor namespaces in the user model. Prefer `firewall.l3_rules` over `firewallL3Rules` or `config.firewall.l3Rules`.
- [ ] **No vendor camelCase or internal terms** — All user-facing field names use snake_case and domain-standard terms.
- [ ] **All fields have descriptions in DOCUMENTATION** — Every option and suboption has a `description` for `ansible-doc` and UX.

### Round-Trip and State

- [ ] **Gathered state output matches merged state input format** — What you gather can be fed back into merged. Round-trip contract holds.
- [ ] **Read-only fields filtered from write operations** — `id`, `created_at`, `updated_at` appear in gathered but are not accepted in merged.
- [ ] **Write-only fields filtered from read operations** — `password`, `api_key`, `psk` appear in merged input but are never returned in gathered (or are masked).

### State Parameter

- [ ] **state parameter supports at minimum: merged, deleted, gathered** — Full lifecycle coverage.

### Naming and Idempotency

- [ ] **Module name follows entity naming** — `novacom_appliance_vlan`, not `novacom_networks_appliance_vlans` (endpoint mirroring).
- [ ] **Canonical key identified and documented** — Module DOCUMENTATION states the canonical key (or notes this is a Category C gather-first resource). See Principle 2.
- [ ] **System key documented when applicable** — If the canonical key differs from the API routing key, both are documented.
- [ ] **Duplicate canonical key detection** — Module fails with actionable error when duplicate canonical keys are found in existing resources.

### Multi-Endpoint Resources

- [ ] **Multi-endpoint resources use action batches or ordered operations** — No ad-hoc sequencing. Use batch API or documented order (e.g., create before configure).

---

## SECTION 10: Human-in-the-Loop Triggers

The agent **MUST** stop and ask a human when encountering the following. Do not guess or apply heuristics.

### 1. Semantic Unit Conversion

**Scenario:** API returns bandwidth in bytes per second, but users think in Mbps.

**Question:** Should the module convert? Which direction?

- **Input:** User specifies `bandwidth_limit: 100` (Mbps) → module converts to bytes for API?
- **Output:** API returns bytes → module converts to Mbps for gathered?
- **Both?** Round-trip in user units?

**Action:** Halt. Ask: "Bandwidth unit policy: user Mbps vs. API bytes. Convert on input, output, or both? Document in module."

---

### 2. Multi-Step State Transitions

**Scenario:** Changing `auth_mode` on an SSID from `open` to `psk` requires:
1. First setting the PSK (API may reject mode change without PSK).
2. Then changing the mode.

Order matters and is domain-specific.

**Action:** Halt. Ask: "State transition order for auth_mode change. Document in module. Implement ordered steps in convergence logic."

---

### 3. Conditional Dependencies

**Scenario:**
- `auth_mode: psk` requires `psk` field.
- `auth_mode: radius` requires `radius_servers`.
- `auth_mode: open` forbids `psk` and `radius_servers`.

These dependency chains need human validation. The agent cannot infer business rules from the schema alone.

**Action:** Halt. Ask: "Validate conditional requirements for auth_mode. Document in DOCUMENTATION. Add validation in argspec or custom validator."

---

### 4. Ambiguous Overridden Logic

**Scenario:** NovaCom has an "override all SSIDs" action. SSID 0 is the default and **cannot be deleted**. What does "override" mean for SSID 0?

- Include it in override (update in place)?
- Exclude it (never touch)?
- Fail if user tries to delete it?

**Action:** Halt. Ask: "Override semantics for non-deletable default SSID. Document and implement."

---

### 5. Entity Boundary Disputes

**Scenario:** NovaCom has:
- `GET/PUT /vpn/siteToSite` — Site-to-site VPN config.
- `GET/PUT /vpn/client` — Client VPN config.

Separate endpoints, but conceptually both are "VPN." Should they be:
- **One module** `novacom_vpn` with `type: site_to_site | client`?
- **Two modules** `novacom_vpn_site_to_site` and `novacom_vpn_client`?

The API structure suggests two. Domain logic might suggest one.

**Action:** Halt. Ask: "Entity boundary: one novacom_vpn module with type, or two separate modules? Consider UX, idempotency, and future API evolution."

---

## Summary

| Principle | One-Line Rule |
|-----------|---------------|
| 1. Entity Aggregation | Same primary key → one module. Group sub-resources. |
| 2. Canonical Key Identity | Match by human key (name, email). System key resolved internally. |
| 3. CRUD Consolidation | One module, full lifecycle. state: merged, deleted, gathered. |
| 4. Namespace Hoisting | Path depth > 3 → evaluate sinking into parent. |
| 5. Data Normalization | No API mirroring. snake_case, human-readable names. |
| 6. Single-Session Transactions | One task = one API transaction (or one batch). |
| 7. Symmetric Validation | Single argspec for input and output validation. |
| 8. Stop Conditions | Halt on duplicate schemas, circular refs, missing keys. |
| 9. Quality Checklist | Verify every item before merge. |
| 10. Human-in-the-Loop | Stop on unit conversion, state transitions, dependencies, ambiguity, entity disputes. |

---

*Document version: 1.1 | NovaCom Networks (fictitious) | OpenAPI Module Design Principles*
