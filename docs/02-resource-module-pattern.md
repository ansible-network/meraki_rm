# The Resource Module Pattern

This document explains what a resource module is, its states, the convergence contract, and the critical distinction between managing entities and calling endpoints. NovaCom Networks serves as the fictitious example throughout: a cloud-managed network infrastructure provider (wireless APs, switches, appliances, cameras) with a REST/OpenAPI Dashboard API and a hierarchy of Organizations > Sites > Networks > Devices.

---

## Section 1: What a Resource Module Is

### Manages a Configuration Entity, Not an API Endpoint

A resource module manages a **configuration entity** — a VLAN, an SSID, a switch port, an ACL. It does not manage an HTTP endpoint. The user thinks in terms of the thing they are configuring, not the API path that happens to implement it.

The module's job is **convergence**: you declare the desired state of a thing, and the module figures out what operations are needed to make reality match. The user never thinks about HTTP verbs, endpoint paths, or payload structure. They think about the entity and the state they want it in.

### Convergence: Declare Desired State, Module Makes Reality Match

Convergence is the defining behavior. Given a desired state declaration, the module:

1. Reads the current state from the device
2. Compares it to what the user declared
3. Computes the minimal set of changes needed
4. Applies only those changes (or skips if nothing differs)
5. Reports what changed

The user declares *what* they want. The module handles *how* to get there.

### User Never Thinks About HTTP Verbs, Endpoint Paths, or Payload Structure

A playbook author writing:

```yaml
- name: Ensure engineering VLAN exists
  novacom.dashboard.novacom_appliance_vlan:
    network_id: "N_12345"
    config:
      - vlan_id: 100
        name: Engineering
        subnet: 10.100.0.0/24
        appliance_ip: 10.100.0.1
        dhcp_handling: run_server
    state: merged
```

does not need to know that NovaCom uses `POST /networks/{id}/appliance/vlans` for creation and `PUT /networks/{id}/appliance/vlans/{vlanId}` for updates. They do not need to know the API expects `dhcpHandling` in camelCase or that the payload nests DHCP settings under a different key. The module abstracts all of that.

### Owns the Full Lifecycle of Its Entity

A resource module owns the **full lifecycle** of its entity. One module handles:

- **Create** — when the entity does not exist
- **Read** — gathering current state
- **Update** — merging or replacing configuration
- **Delete** — removing configuration

CRUD is not separate modules. They are **states within one module**. The same `novacom_appliance_vlan` module that creates VLAN 100 can later replace it, override all VLANs, or delete it — all via the `state` parameter.

---

## Section 2: The Seven States

Every resource module exposes a `state` parameter. Each state has precise semantics about what the module will do with the provided configuration relative to what exists on the device.

### Operational States (Modify the Device)

These states change the device configuration. They are additive, replacement, or removal operations.

#### `merged` (default)

**Additive merge.** If the entity does not exist: create it. If it exists: update only the specified fields, leave the rest untouched. If the config is already present: no change (`changed: false`). This is the safest state — it can never destroy anything the user did not explicitly touch.

**NovaCom VLAN example:**

```yaml
- name: Ensure engineering VLAN exists with this name
  novacom.dashboard.novacom_appliance_vlan:
    network_id: "N_12345"
    config:
      - vlan_id: 100
        name: Engineering
        subnet: 10.100.0.0/24
        appliance_ip: 10.100.0.1
        dhcp_handling: run_server
    state: merged
```

If VLAN 100 already exists with `name: Engineering` and a different DHCP configuration (e.g., `dhcp_handling: relay`), the DHCP config is left alone. Only the specified fields are touched. If VLAN 100 does not exist, it is created. If it already has exactly this config, `changed: false` is returned.

#### `replaced`

**Replace the configuration of the specified entity instances.** For each instance you provide, its entire config is replaced by what you declare. Instances you do not mention are left untouched. Fields you omit for a listed instance revert to defaults.

**NovaCom VLAN example (difference from merged):**

```yaml
- name: Replace VLAN 100 config entirely
  novacom.dashboard.novacom_appliance_vlan:
    network_id: "N_12345"
    config:
      - vlan_id: 100
        name: Engineering
        subnet: 10.100.0.0/24
        appliance_ip: 10.100.0.1
    state: replaced
```

VLAN 100 now has *exactly* the config listed above and nothing else. Any DHCP settings, DNS servers, or other attributes that were on VLAN 100 are reset to defaults. VLAN 200, 300, and any other VLANs are untouched. With `merged`, omitting `dhcp_handling` would leave the existing value; with `replaced`, it reverts to the default.

#### `overridden`

**Replace ALL instances of the resource type.** Nuclear option. What you list is what exists. Instances not in your list are deleted. This is the **compliance state** — it enforces "the device should look exactly like this."

**NovaCom VLAN example:**

```yaml
- name: Only these VLANs should exist
  novacom.dashboard.novacom_appliance_vlan:
    network_id: "N_12345"
    config:
      - vlan_id: 100
        name: Engineering
        subnet: 10.100.0.0/24
        appliance_ip: 10.100.0.1
        dhcp_handling: run_server
      - vlan_id: 200
        name: Guest
        subnet: 10.200.0.0/24
        appliance_ip: 10.200.0.1
        dhcp_handling: relay
    state: overridden
```

If VLANs 100, 200, and 300 existed on the device, VLAN 300 is **deleted**. VLANs 100 and 200 are replaced with exactly the config above. The result is a device with precisely two VLANs — no more, no less. This is how you enforce compliance: run the playbook, and any unauthorized VLANs are removed.

#### `deleted`

**Remove configuration.** Two modes depending on what you provide:

- **With config specified:** Delete the listed instances only.
- **Without config (or empty config):** Delete all instances of the resource type.

**NovaCom VLAN examples — both modes:**

```yaml
# Delete specific VLAN(s)
- name: Remove VLAN 100
  novacom.dashboard.novacom_appliance_vlan:
    network_id: "N_12345"
    config:
      - vlan_id: 100
    state: deleted

# Delete all VLANs
- name: Remove all VLANs
  novacom.dashboard.novacom_appliance_vlan:
    network_id: "N_12345"
    state: deleted
```

In the first case, only VLAN 100 is removed; VLANs 200 and 300 remain. In the second case, every VLAN on the network is removed.

### Read-Only States (Do Not Modify the Device)

These states read or transform data without contacting the device or making changes.

#### `gathered`

**Read current config from the device and return it as structured data** using the same schema as the `config` parameter. No changes are made. This is step 1 of the convergence loop exposed to the user.

```yaml
- name: Get current VLAN configuration
  novacom.dashboard.novacom_appliance_vlan:
    network_id: "N_12345"
    state: gathered
  register: vlan_facts
```

The returned data uses the module's argspec — human-readable field names, snake_case, no vendor internals. The output schema matches the input schema so you can diff, compare, or feed it into another task. This is how you read state using the same vocabulary you use to write state.

#### `rendered`

**Generate device-native config (API payloads) from provided structured data** without contacting the device. Offline operation. Useful for review, audit, or generating what *would* be sent.

```yaml
- name: Render VLAN config to API payloads
  novacom.dashboard.novacom_appliance_vlan:
    network_id: "N_12345"
    config:
      - vlan_id: 100
        name: Engineering
        subnet: 10.100.0.0/24
    state: rendered
  register: rendered_output
```

The output shows the exact JSON payloads that would be sent to the NovaCom API. No API call is made. Useful for debugging, documentation, or pre-flight validation.

#### `parsed`

**Parse device-native config (API responses) into the module's structured data format** without contacting the device. Offline operation. Useful for importing existing configs.

```yaml
- name: Parse API response into module format
  novacom.dashboard.novacom_appliance_vlan:
    network_id: "N_12345"
    running_config: "{{ api_response_json }}"
    state: parsed
  register: parsed_output
```

Given raw API response data, the module converts it to the same structured format used by `config` and `gathered`. Useful for migrating from manual API usage or importing configs from another source.

### Why These States: Set Theory as the Foundation

The five operational states are not arbitrary design choices — they are the natural set operations on a keyed collection of configuration records. Understanding this makes the state model self-evident rather than something to memorize.

**The model.** A resource module manages a collection **S** of configuration records, each identified by a primary key (e.g., `vlan_id`, `admin_id`, `number`). The user provides a desired set **D**. The device holds a current set **C**. Each state defines a set operation that produces the next state **C′**.

#### Formal Definitions

| State | Set Operation | Description |
|-------|---------------|-------------|
| **`gathered`** | **C** (read only) | Return the current set. No mutation. |
| **`merged`** | **C′ = C ∪ D** | Union. Items in **D** are added or updated in **C**. Items in **C** not mentioned in **D** are untouched. Additive only — nothing is ever removed. |
| **`replaced`** | **C′ = (C \ K(D)) ∪ D** | For each key **k** in **D**, remove the old record for **k** from **C** and insert the new one from **D**. Items in **C** whose keys are not in **D** are untouched. This is item-level replacement: omitted fields revert to defaults. |
| **`overridden`** | **C′ = D** | Set equality. The result is exactly **D** — no more, no less. Items in **C \ D** (by key) are deleted. Items in **D \ C** are created. Items in **D ∩ C** are replaced. |
| **`deleted`** | **C′ = C \ D** | Set difference. Remove items whose keys appear in **D**. If **D** is empty, **C′ = ∅** (delete all). |

Where **K(D)** denotes the set of primary keys present in **D**.

#### The Lattice of Destructiveness

The states form a natural ordering from least to most destructive:

```
gathered  →  merged  →  replaced  →  overridden  →  deleted
(read)      (additive)  (item-level)  (set-level)    (removal)
             never       resets        deletes         deletes
             removes     fields to     unlisted        listed
             anything    defaults      items           items
```

- **`merged`** is the safest mutating state. It can only add or update. It never removes a field or a record.
- **`replaced`** is more aggressive per-item: it resets omitted fields to defaults. But it only touches items you name.
- **`overridden`** is the most aggressive: it enforces **set equality**. Anything not in your declaration is deleted. This is why it is the compliance state — it guarantees the device matches the playbook exactly.
- **`deleted`** is explicit removal. You name what goes away.

#### Why This is Exactly Five States

These five operations exhaust the useful set-theoretic operations on a keyed collection:

1. **Read** the set → `gathered`
2. **Add to / update within** the set → `merged` (union)
3. **Replace specific items** in the set → `replaced` (keyed replacement)
4. **Make the set exactly this** → `overridden` (set equality / assignment)
5. **Remove from** the set → `deleted` (set difference)

There is no sixth operation. Any desired behavior can be composed from these five. This is why the resource module pattern has exactly these states — not because of convention, but because set theory has exactly these operations on keyed collections.

#### Why the Base Class Implements Them Generically

Because these operations are defined purely in terms of sets and keys, the implementation is **module-agnostic**. The base action plugin needs only three things from a subclass:

1. **A primary key** — to identify records across sets (e.g., `vlan_id`, `admin_id`)
2. **CRUD endpoints** — `create`, `find`/`find_all`, `update`, `delete`
3. **`SUPPORTS_DELETE`** — whether the resource type permits removal (physical ports cannot be deleted, only reconfigured)

Given these, the base class implements all five states as generic set operations. No module-specific logic is required for state handling. The `_apply_merged_or_replaced()` method handles both `merged` and `replaced` because they differ only in whether omitted fields are preserved (merge) or reset (replace). The `_apply_overridden()` method computes **C \ D** for deletions, then applies replacements — pure set arithmetic.

This is why adding `replaced` and `overridden` support to a module that already has `merged` and `deleted` is a one-line argspec change, not a feature implementation. The set theory is already in the base class.

---

## Section 3: Entities vs. Endpoints

The fundamental design distinction that separates a resource module from an API wrapper.

### The Endpoint-Centric Model (Anti-Pattern)

Map every API endpoint to a module. This is what automated code generators produce when pointed at an OpenAPI spec with no architectural guidance.

**Characteristics:**

- **One module per HTTP endpoint path** — each API route becomes its own module
- **Parameters mirror the API payload verbatim** — camelCase, vendor-internal names like `authMode`, `splashPage`, `bandSelection`
- **No state management** — `present`/`absent` at best, which collapses full state semantics into a boolean
- **Configuring a logical entity requires chaining multiple modules** — an SSID spans 6 endpoints, so 6 modules, 6 tasks
- **No convergence** — the module calls the endpoint whether or not anything needs to change
- **Idempotency is the caller's problem** — the user must add `when` conditions, `changed_when`, or retry logic

**Result for NovaCom:** ~500 modules for ~50 logical entities = **~10 modules per entity**. The user is doing the API's job: manually orchestrating endpoint calls in the correct order, handling dependencies, and hoping the API's camelCase parameter names are obvious enough to get right.

### The Entity-Centric Model (Resource Module)

Map every **configurable entity** to a module. The module owns the entity's full lifecycle.

**Characteristics:**

- **One module per logical thing** — VLAN, SSID, switch port, ACL
- **Parameters use human-readable, Ansible-idiomatic names** — snake_case, normalized terminology (`auth_mode`, `splash_page`, `band_selection`)
- **Full state semantics** — `merged`, `replaced`, `overridden`, `deleted`, `gathered`
- **Module aggregates whatever API calls are needed internally** — one task, many endpoints
- **Convergence built in** — compare desired vs actual, only act on differences
- **Idempotency is the module's responsibility** — `changed: true` only when something actually changed

**Result for NovaCom:** ~45 modules for ~45 entities = **1 module per entity**. The user declares what they want. The module does the rest.

### Where Complexity Lives (Comparison Table)

| Concern | Endpoint Model | Resource Model |
|---------|----------------|----------------|
| **API path knowledge** | User (playbook) — must know which modules map to which paths | Module internals — user never sees paths |
| **Call ordering** | User (playbook) — must sequence tasks correctly | Module internals — transform mixin enforces order |
| **Payload construction** | User (task params) — must match API structure exactly | Transform mixin — user provides flat, normalized config |
| **Idempotency** | User (when/changed_when) — caller's responsibility | Module — diff desired vs actual, skip if no diff |
| **Rate limiting** | User (throttle/retries) — high risk with many tasks | Module — batching, action batches, fewer calls |
| **Field naming** | API's terms (camelCase, vendor jargon) | Ansible-normalized terms (snake_case, industry standard) |
| **State comparison** | Not available — no gathered state | Built-in — gathered vs desired, like-with-like diff |

In the endpoint model, complexity is pushed to the playbook author. In the resource model, it is absorbed by the module.

---

## Section 4: How an Entity Maps to Endpoints

A single resource module may aggregate multiple API endpoints behind one `config` schema. The user never sees the seams.

### NovaCom Wireless SSID: One Entity, Six Endpoints

The `novacom_wireless_ssid` resource module manages one logical entity (an SSID) but internally touches **six endpoints**:

| Sub-Resource | Endpoint | User-Facing Fields |
|--------------|----------|--------------------|
| Basic settings | `PUT /networks/{id}/wireless/ssids/{number}` | `name`, `enabled`, `band_selection`, etc. |
| PSK config | Same endpoint (`auth_mode`, `psk` fields) | `auth_mode`, `psk` |
| L3 firewall | `PUT /networks/{id}/wireless/ssids/{number}/firewall/l3FirewallRules` | `l3_firewall_rules` |
| L7 firewall | `PUT /networks/{id}/wireless/ssids/{number}/firewall/l7FirewallRules` | `l7_firewall_rules` |
| Traffic shaping | `PUT /networks/{id}/wireless/ssids/{number}/trafficShaping/rules` | `traffic_shaping_rules` |
| Splash settings | `PUT /networks/{id}/wireless/ssids/{number}/splash/settings` | `splash_settings` |

**Six endpoints. One entity. One module. One task in the playbook.**

```yaml
- name: Manage guest SSID
  novacom.dashboard.novacom_wireless_ssid:
    network_id: "N_12345"
    config:
      - number: 1
        name: "Guest-Wi-Fi"
        enabled: true
        auth_mode: psk
        psk: "secret123"
        l3_firewall_rules:
          - policy: deny
            protocol: tcp
            dest_port: "80"
            dest_cidr: "0.0.0.0/0"
        traffic_shaping_rules:
          - per_client_bandwidth_limit_up: 1024
            per_client_bandwidth_limit_down: 5120
    state: merged
```

The user provides a flat, structured config. The **transform mixin** knows how to:

1. **Split** the user's flat config into the right payloads for each endpoint
2. **Call** them in the correct order (basic settings before firewall, etc.)
3. **Reassemble** the responses into a unified gathered result that uses the same schema the user writes in

The user never thinks about the six endpoints. They think about one SSID.

---

## Section 5: The Convergence Contract

The defining behavior of a resource module is **convergence**: given a desired state declaration, the module computes the minimal set of changes to make reality match, applies them, and reports what changed.

### The Convergence Loop

```
1. GATHER:  Read current config from device (same schema as user input)
2. COMPARE: Diff desired config against current config
3. PLAN:    Compute operations needed (create, update, delete)
4. EXECUTE: Apply operations via API (or skip if no diff)
5. REPORT:  Return changed=true/false, before/after state, commands issued
```

### Why `gathered` Exists as a State

`gathered` is step 1 exposed to the user. It allows the playbook author to:

- Inspect current state before making changes
- Feed gathered data into conditional logic
- Build custom convergence logic if needed
- Debug what the device actually has

### Why Gathered Output Uses the Same Schema as Input

So the diff in step 2 compares **like with like**. If the user declares:

```yaml
config:
  - vlan_id: 100
    name: Engineering
    subnet: 10.100.0.0/24
```

and the gathered output returns:

```yaml
gathered:
  - vlan_id: 100
    name: Engineering
    subnet: 10.100.0.0/24
    appliance_ip: 10.100.0.1
    dhcp_handling: run_server
```

the module can perform a proper diff. Same field names, same structure, same vocabulary. The comparison is straightforward. If the API returned camelCase and nested structures, the diff logic would need to normalize both sides — and the user would get inconsistent output when reading vs writing.

### The Contract

A module that cannot do this loop is not a resource module. It is an API client with YAML syntax. The convergence contract is what separates infrastructure automation from imperative scripting.

### Check Mode: The Convergence Loop Without Side Effects

Ansible's `--check` flag asks modules to predict what *would* change without actually changing anything. Because resource modules are built on set theory, check mode is not a simulation — it is a **computation**.

The convergence loop becomes:

```
1. GATHER:  Read current config from device → before
2. PREDICT: Compute after from set theory (no API calls)
3. REPORT:  Return changed=(before != after), before/after state
```

Step 2 does not contact the device. The set operations are pure functions:

- **`merged`**: predict `after` by merging desired fields onto `before`
- **`replaced`**: predict `after` by replacing matched items entirely
- **`overridden`**: predict `after = desired` (by definition — C' = D)
- **`deleted`**: predict `after` by removing items whose keys match

This is why `overridden` with `--check` is the **compliance audit**: "run the playbook in check mode. If `changed: true`, the device has drifted from the declared state." No changes are made. The report tells you exactly what would be brought into compliance.

```yaml
- name: Audit VLAN compliance
  novacom.dashboard.novacom_appliance_vlan:
    network_id: "N_12345"
    config:
      - vlan_id: 100
        name: Engineering
        subnet: 10.100.0.0/24
      - vlan_id: 200
        name: Guest
        subnet: 10.200.0.0/24
    state: overridden
  check_mode: true
  register: audit

- name: Report drift
  ansible.builtin.debug:
    msg: "Drift detected — {{ audit.before | length }} current vs {{ audit.after | length }} desired"
  when: audit is changed
```

### Diff Mode: Seeing What Changed

Ansible's `--diff` flag asks modules to show what changed (or what would change in check mode). Resource modules return structured `before`/`after` state, which Ansible renders as a unified diff.

Because `gathered` output uses the same schema as `config` input, the diff compares **like with like** — snake_case field names, normalized values, human-readable structure. No vendor-internal camelCase or nested API payloads.

```
TASK [Ensure engineering VLAN exists] ****
--- before
+++ after
@@ -1,3 +1,3 @@
 - name: Engineering
-  subnet: 10.100.0.0/24
+  subnet: 10.100.0.0/16
   vlan_id: '100'
```

Check mode and diff mode compose naturally: `--check --diff` shows what *would* change without changing anything. This is the standard pre-deployment review workflow for production infrastructure.

---

## Section 6: Why This Matters for NovaCom

### Summary: Endpoint Model vs. Resource Model

| Metric | Endpoint Model | Resource Model |
|--------|----------------|----------------|
| **Module count** | ~500 | 42-50 |
| **Tasks to configure SSID** | 3-6 | 1 |
| **Compliance enforcement** | Manual (not possible) | Built-in (`state: overridden`) |
| **API rate limit risk** | High (one call per task) | Low (batched, action batches) |
| **User must know API structure** | Yes | No |
| **Playbook readability** | Low (endpoint soup) | High (entity declarations) |

### The Transformation

The entity-centric model turns Ansible playbooks from **imperative API scripts** into **declarative infrastructure definitions**. Instead of "call this endpoint, then that one, then the other," the user writes "these VLANs should exist, these SSIDs should look like this, only these firewall rules apply." The module handles the rest.

For NovaCom specifically: with ~500 endpoints, a naive 1:1 mapping produces an unmaintainable collection. The resource module approach collapses that to ~45 modules, one per logical entity. Configuring a guest SSID goes from six tasks across six modules to one task. Compliance enforcement — "only these VLANs should exist" — becomes a single `state: overridden` declaration instead of manual diff-and-delete logic. The API rate limit (10 requests/second per organization) is less of a concern when the module batches operations and only calls the API when changes are needed.

That is the entire point of the resource module pattern.
