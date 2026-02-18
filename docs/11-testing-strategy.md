# Testing Strategy

This document defines the testing architecture for an OpenAPI-driven resource module collection (e.g. NovaCom `example_namespace.novacom_rm`). It covers the mock server, the Molecule test runner, unit tests, and the three-layer validation model that ensures every module is spec-compliant, behaviorally correct, and idempotent.

**Audience**: Framework developers, feature developers, AI agents

**Related Documents**:
- [06-foundation-components.md](06-foundation-components.md) — What is being tested (core components)
- [07-adding-resources.md](07-adding-resources.md) — Step 7: testing a new resource module
- [08-code-generators.md](08-code-generators.md) — Generated code that needs testing
- [09-agent-collaboration.md](09-agent-collaboration.md) — Agent testing workflow

---

## Table of Contents

1. [Testing Philosophy](#section-1-testing-philosophy)
2. [Mock Server Architecture](#section-2-mock-server-architecture)
3. [Molecule Collection Testing](#section-3-molecule-collection-testing)
4. [Test Anatomy — Per-Module Scenarios](#section-4-test-anatomy--per-module-scenarios)
5. [Unit Tests — Colocated `*_test.py` Files](#section-5-unit-tests--colocated-_testpy-files)
6. [Adding Tests for a New Module](#section-6-adding-tests-for-a-new-module)
7. [Running Tests](#section-7-running-tests)
8. [What Each Layer Catches](#section-8-what-each-layer-catches)

---

## SECTION 1: Testing Philosophy

### Three-Layer Validation

Every test run validates three layers simultaneously. Each layer catches a different category of bug. No single layer is sufficient on its own.

```
┌─────────────────────────────────────────────────────────────────┐
│ Layer 1: Spec Compliance                                        │
│ "Does the module speak the API's language correctly?"           │
│                                                                  │
│ openapi-core middleware in the mock server validates every       │
│ HTTP request and response against the OpenAPI spec. If the module     │
│ sends a malformed payload or expects an invalid response        │
│ shape, the mock returns 400 and the test fails.                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 2: Module Behavior                                        │
│ "Does the module do what the user asked?"                       │
│                                                                  │
│ Molecule converge/verify/cleanup playbooks test the full CRUD   │
│ lifecycle: create a resource, gather it back, assert fields     │
│ match, update it, gather again, delete it, verify removal.      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 3: Idempotence and Round-Trip Contract                    │
│ "Is the module safe to re-run? Does output match input format?" │
│                                                                  │
│ Molecule's idempotence step re-runs converge and asserts        │
│ changed: false. Verify playbooks assert that gathered output    │
│ uses the same schema as merged input (snake_case, names not     │
│ IDs, same field structure). This is the convergence contract.   │
└─────────────────────────────────────────────────────────────────┘
```

### Why Three Layers

- **Spec compliance alone** does not prove the module creates the right resource or handles state correctly. A module could send a valid HTTP request that creates the wrong thing.
- **Behavior tests alone** do not prove the module talks to the API correctly. A mock that ignores invalid payloads would pass behavior tests even if the module sends garbage.
- **Idempotence alone** does not prove correctness. A module that always returns `changed: false` without doing anything would pass idempotence.

All three together give confidence: the module speaks the API correctly (Layer 1), does what the user asked (Layer 2), and is safe to re-run with a consistent data contract (Layer 3).

### Test Pyramid

```
                    ┌──────────┐
                    │ Molecule │  Integration: full CRUD lifecycle
                    │ Scenarios│  per module, against mock server
                    ├──────────┤  (~45 scenarios, slower ~30s startup)
                    │          │
               ┌────┴──────────┴────┐
               │  Colocated Unit    │  Sibling *_test.py files in
               │  Tests (pytest)    │  plugin_utils/ — transform
               │                    │  roundtrips, spec drift, types
               └────────────────────┘  (sub-second, no server needed)
```

**Unit tests must run first.** Pure-Python data bugs — wrong field names, scope param leaks, broken transforms, missing dataclass fields — should fail in sub-second `pytest` runs, not after a ~30s Molecule startup cycle. Molecule integration tests verify the full CRUD lifecycle against the mock server, but they are the **second** line of defense, not the first.

Unit tests run in milliseconds and catch transform logic bugs. Molecule scenarios run in seconds per module and catch integration bugs (wrong endpoint, broken state logic, non-idempotent behavior). Both are needed, but unit tests gate integration.

---

## SECTION 2: Mock Server Architecture

### Purpose

A stateful Flask + openapi-core mock server that enforces the platform's OpenAPI spec. It serves as:

1. The integration test backend for the collection
2. A documented reference pattern for any future OpenAPI-driven collection

### Location

```
tools/mock_server/
├── __init__.py
├── server.py              # Flask app factory, auto-route generation
├── state_store.py         # In-memory stateful CRUD store
├── spec_loader.py         # OpenAPI spec loading + path matching
├── response_generator.py  # Generate spec-compliant responses from schemas
└── README.md              # Reference pattern documentation
```

### How It Works

```
openapi_spec.json (platform OpenAPI spec)
    │
    ▼
spec_loader.py ────────► Parses all paths, methods, inline schemas
    │                     Builds path → schema lookup table
    │                     Extracts primary keys from path parameters
    ▼
server.py ─────────────► Registers Flask routes for every path in spec
    │                     Adds openapi-core middleware:
    │                       - Validates request params, headers, body
    │                       - Validates response body before returning
    │                     Routes delegate to state_store for CRUD
    ▼
state_store.py ────────► In-memory dict-of-dicts
    │                     Key: (resource_type, primary_key_values)
    │                     POST   → creates entry, returns 201
    │                     GET    → retrieves entry or list, returns 200
    │                     PUT    → updates entry, returns 200
    │                     DELETE → removes entry, returns 204
    ▼
response_generator.py ─► Generates spec-compliant response bodies
                          Fills required fields with type-appropriate defaults
                          Merges state_store data with schema defaults
                          Ensures every response passes spec validation
```

### Key Design Decisions

**Auto-route generation.** The mock server reads all paths from the OpenAPI spec and registers Flask routes dynamically. Zero manual route definitions. When the spec changes, the mock server automatically covers new endpoints.

**openapi-core middleware.** Every request is validated against the spec: path parameters, query parameters, headers, and request body. Every response is validated before returning. This catches bugs at the HTTP boundary — wrong field names, missing required fields, invalid types — before the Ansible module even processes the response.

**Stateful CRUD.** In-memory `state_store` maintains resource state across requests within a test session. This enables convergence testing:

1. `POST /networks/{id}/appliance/vlans` — creates VLAN, stored in state
2. `GET /networks/{id}/appliance/vlans/{vlanId}` — retrieves it from state
3. `PUT /networks/{id}/appliance/vlans/{vlanId}` — updates it in state
4. `DELETE /networks/{id}/appliance/vlans/{vlanId}` — removes from state
5. `GET /networks/{id}/appliance/vlans/{vlanId}` — returns 404

Without statefulness, you cannot test the convergence loop (gather → diff → act → verify).

**Primary key inference.** The mock extracts primary keys from path parameters. For `/networks/{networkId}/appliance/vlans/{vlanId}`, the primary key is `(networkId, vlanId)`. This happens automatically from the spec — no manual key configuration.

**Schema-driven responses.** When a resource is created or updated, the mock merges the user-provided data with defaults generated from the response schema. This ensures responses always conform to the spec, even for fields the user did not provide.

### Standalone Mode

The mock server can be run directly for manual testing and exploration:

```bash
python -m tools.mock_server.server --spec openapi_spec.json --port 29443
```

This is useful for:
- Exploring the API surface during development
- Manual `curl` testing of endpoint behavior
- Debugging module interactions outside of Molecule

### Dependencies

- `flask` — HTTP server framework
- `openapi-core>=0.19` — Request/response validation against OpenAPI 3.0
- `pyyaml` — Spec parsing

### Reference Pattern: Adapting for Another Spec

To reuse this mock server for a different OpenAPI-driven collection:

1. Replace the spec for the target platform with the new OpenAPI spec file
2. Adjust primary key inference if the new API uses non-standard path parameter naming
3. Add any custom behavior (e.g., rate limiting simulation, pagination)
4. The auto-routing, spec validation, and state store work unchanged

See `tools/mock_server/README.md` for detailed adaptation instructions.

---

## SECTION 3: Molecule Collection Testing

### Why Molecule

Molecule is the standard Ansible testing framework and was [rewritten to support shared testing resources](https://docs.ansible.com/projects/molecule/getting-started-collections/) (e.g. a single mock server). For this collection, it provides:

- **Ansible-native execution** — tests are playbooks, not custom scripts. The same `state: merged` / `state: gathered` / `state: deleted` that users write in production playbooks is what tests exercise.
- **Collection-aware** — discovers scenarios via `extensions/molecule/**/molecule.yml`, supporting nested `{module}/{state}/` layouts.
- **Idempotence built-in** — the `idempotence` step re-runs converge and asserts `changed: false`. This is the single most important test for a resource module.
- **Shared state** — with `shared_state: true`, the **default scenario is the lifecycle manager**. Molecule runs **default create** first and **default destroy** last — even when targeting a single scenario with `-s`. Component scenarios (appliance_vlans, wireless_ssid, etc.) **skip create/destroy** and only run their own test sequence. The mock server is started once and stopped once; all module scenarios use that shared server. See [Collection Testing — Shared State](https://docs.ansible.com/projects/molecule/getting-started-collections/#shared-state-vs-per-scenario-resources).
- **Config inheritance** — base `config.yml` defines the component test sequence and shared_state; `default/molecule.yml` overrides to just `create`/`destroy`; per-module `molecule.yml` files inherit and are typically empty.

### Directory Layout

```
extensions/molecule/
├── config.yml                         # Shared base: test_sequence, shared_state: true
├── inventory.yml                      # Shared inventory (platform_api_url → mock server)
├── default/                           # Lifecycle manager (runs first and last)
│   ├── molecule.yml                   # test_sequence: [create, destroy] only
│   ├── create.yml                     # Start mock server
│   └── destroy.yml                    # Stop mock server
├── appliance_vlans/                   # Module group directory
│   ├── merged/                        # Per-state scenario: molecule test -s appliance_vlans/merged
│   │   ├── molecule.yml              # Minimal (inherits config.yml)
│   │   ├── vars.yml                  # expected_config — shared data source
│   │   ├── converge.yml             # vars_files + module call — documentation source
│   │   ├── verify.yml               # vars_files + gather + path_contained_in
│   │   └── cleanup.yml              # Delete test resources
│   ├── replaced/
│   │   ├── molecule.yml
│   │   ├── vars.yml                  # Replacement config data
│   │   ├── prepare.yml              # Seed prerequisite state (merged)
│   │   ├── converge.yml
│   │   ├── verify.yml
│   │   └── cleanup.yml
│   ├── overridden/                   # prepare seeds 2 resources, converge overrides to 1
│   │   └── ...
│   ├── deleted/                      # prepare seeds resource, converge deletes it
│   │   └── ...
│   └── gathered/
│       └── ...
├── wireless_ssid/
│   ├── merged/
│   ├── replaced/
│   └── gathered/                     # No delete (singleton)
├── facts/
│   └── gathered/
└── ... (48 module groups, ~186 per-state scenarios total)
```

### Converge as Source of Truth

Each scenario's `converge.yml` + `vars.yml` pair is the **single source of truth** for both documentation and integration tests. The vars file holds the expected data, and the converge contains only the module call — the clean example a user would write:

```yaml
---
# vars.yml — shared data
expected_config:
  vlan_id: "100"
  name: Test-Config
  subnet: 192.168.128.0/24
  appliance_ip: 192.168.128.1

---
# converge.yml — module call only
- name: "Converge — appliance_vlans (merged)"
  hosts: localhost
  gather_facts: false
  vars_files:
    - vars.yml
  tasks:
    - name: Create appliance_vlans with merged state
      cisco.meraki_rm.meraki_appliance_vlans:
        network_id: "N_123456789012345678"
        state: merged
        config:
          - "{{ expected_config }}"
      register: merge_result
```

Assertions live in `verify.yml`, not in the converge. This separation means:

1. **Documentation examples are clean** — A pre-commit hook (`tools/inject_examples.py`) reads `vars.yml` + `converge.yml`, renders the vars as a `set_fact` task, and injects the combined result into the `EXAMPLES` block of `plugins/modules/{prefix}_*.py`. No assertion noise.

2. **Converge survives idempotence** — With no assertions in converge, Molecule's idempotence replay runs cleanly; `verify.yml` independently validates state after each converge using the same shared data.

3. **Verify validates actual data** — `verify.yml` loads `vars.yml` and uses `path_contained_in` to check that every expected field is present and correct in the gathered state. No more "something exists" — full field-level validation.

```
extensions/molecule/appliance_vlans/merged/vars.yml + converge.yml
        │
        ├──► tools/inject_examples.py ──► plugins/modules/{prefix}_{resource}.py (EXAMPLES)
        │     (renders vars as set_fact      └── ansible-doc reads EXAMPLES
        │      + converge tasks)
        │
        ├──► Molecule runs converge directly as integration test
        │
        └──► verify.yml loads same vars.yml for field-level assertions
```

### Shared Config (`config.yml`)

```yaml
---
ansible:
  executor:
    args:
      ansible_playbook:
        - --inventory=${MOLECULE_PROJECT_DIRECTORY}/extensions/molecule/inventory.yml
  env:
    ANSIBLE_FORCE_COLOR: "true"
    ANSIBLE_HOST_KEY_CHECKING: "false"
    ANSIBLE_DEPRECATION_WARNINGS: "false"
    ANSIBLE_SYSTEM_WARNINGS: "false"
    ANSIBLE_COMMAND_WARNINGS: "false"

scenario:
  test_sequence:
    - prepare
    - converge
    - verify
    - idempotence
    - verify
    - cleanup

shared_state: true

verifier:
  name: ansible
```

Key points:

- **Depth-independent inventory path** — Uses `MOLECULE_PROJECT_DIRECTORY` (collection root) rather than `MOLECULE_SCENARIO_DIRECTORY` to resolve `inventory.yml`. This works regardless of how deeply a scenario is nested (`default/` at depth 1, `appliance_vlans/merged/` at depth 2, etc.).
- **No create/destroy in component sequence** — Component scenarios run only prepare / converge / verify / idempotence / verify / cleanup. With `shared_state: true`, Molecule delegates lifecycle to the default scenario.
- **Default scenario** — Has its own `molecule.yml` with `test_sequence: [create, destroy]`. Molecule runs **default create** first, then all component scenarios, then **default destroy** last. This happens for both `molecule test --all` and `molecule test -s appliance_vlans/merged`. One mock server for the whole run. See [Testing resource management playbooks (default scenario)](https://docs.ansible.com/projects/molecule/getting-started-collections/#testing-resource-management-playbooks-default-scenario).
- **Manager `.survive` flag** — `default/create.yml` touches a `.survive` flag file in the runtime directory. A watchdog thread inside the manager watches this file: while it exists the manager stays alive across playbooks. When `default/destroy.yml` removes the flag, the watchdog shuts the manager down gracefully. In production (no flag), the watchdog instead monitors the parent `ansible-playbook` PID and shuts down when it exits. See Lesson 25.
- **Idempotence in sequence** — Converge runs twice; second time must produce `changed: false`.
- **Double verify** — Verify runs after converge and again after idempotence, catching state drift.

### Shared Inventory (`inventory.yml`)

```yaml
---
all:
  hosts:
    localhost:
      ansible_connection: local
      platform_api_url: "http://127.0.0.1:{{ mock_server_port | default('29443') }}"
      platform_api_key: "test-mock-api-key-for-molecule"
  vars:
    mock_server_port: 29443
    mock_server_spec: "{{ lookup('env', 'MOLECULE_PROJECT_DIRECTORY') }}/openapi_spec.json"
```

All module scenarios inherit this inventory. The `platform_api_url` points at the mock server started by the default scenario.

### Execution Flow

With `molecule test --all` or `molecule test -s appliance_vlans/merged`:

```
1.  default                        → create     Start mock server
2.  appliance_vlans/merged         → converge   Module call (spawns Platform Manager)
3.  appliance_vlans/merged         → verify     Independent gather + assert (reconnects to manager)
4.  appliance_vlans/merged         → idempotence  Replay converge → changed: false (reconnects)
5.  appliance_vlans/merged         → verify     Re-verify (reconnects)
6.  appliance_vlans/merged         → cleanup    Delete test resources (reconnects)
7.  appliance_vlans/replaced       → prepare    Seed via merged (reconnects to same manager)
8.  appliance_vlans/replaced       → converge   Module call (replaced)
9.  appliance_vlans/replaced       → verify/idempotence/verify/cleanup
10. appliance_vlans/overridden     → prepare/converge/.../cleanup
11. appliance_vlans/deleted        → prepare/converge/.../cleanup
12. wireless_ssid/merged           → prepare/converge/.../cleanup
...                                → (all per-state scenarios, only with --all)
N.  default                        → destroy    Stop mock server + kill Platform Manager
```

Mock server and Platform Manager both run once. The manager is spawned on the first
module task and reused across all Molecule phases via socket + keyfile reconnection
(enabled by the `.survive` flag file created in `default/create.yml`). Within a single
playbook, tasks reuse the manager via `ansible_facts` (zero I/O). `default/destroy.yml`
removes the `.survive` flag — the manager's watchdog detects this and shuts down
gracefully. The mock server is killed directly.

---

## SECTION 4: Test Anatomy — Per-State Scenarios

### Per-State Scenario Pattern

Each resource module is tested with **one Molecule scenario per state** in a nested `{module}/{state}/` directory. This gives every state its own idempotence check — Molecule replays only the converge for that scenario, so there is no oscillation between competing configs.

```
extensions/molecule/appliance_vlans/
├── merged/       # molecule test -s appliance_vlans/merged
├── replaced/     # molecule test -s appliance_vlans/replaced
├── overridden/   # molecule test -s appliance_vlans/overridden
├── deleted/      # molecule test -s appliance_vlans/deleted
└── gathered/     # molecule test -s appliance_vlans/gathered
```

The pattern for each per-state scenario:

| Step | `merged` | `replaced` | `overridden` | `deleted` | `gathered` |
|------|----------|------------|--------------|-----------|------------|
| prepare | — | Seed via merged | Seed 2+ resources | Seed via merged | Seed via merged |
| converge | set_fact + module call | set_fact + module call | set_fact + module call | set_fact + module call | module call (gather) |
| verify | Gather + assert exists | Gather + assert exists | Gather + assert count=1 | Gather + assert empty | Assert non-empty |
| idempotence | Replay → `ok` | Replay → `ok` | Replay → `ok` | Replay → `ok` | Replay → `ok` |
| cleanup | Delete resources | Delete resources | Delete resources | No-op | Delete resources |

### Return Values: `before` / `after`

All mutating states (merged, replaced, overridden, deleted) return `before` and `after` lists following the Ansible network resource module convention:

```
{
    "before": [ ... ],   # resource config before this run
    "after":  [ ... ],   # resource config after this run
    "changed": bool,     # derived from before != after
    "gathered": [ ... ], # only for state=gathered
}
```

Idempotency falls out naturally: if `before == after`, `changed = false`.

### Shared Vars — Single Source of Test Data

Each scenario has a `vars.yml` containing the `expected_config`. Both `converge.yml` and `verify.yml` load it via `vars_files`, eliminating data duplication.

```yaml
---
# extensions/molecule/appliance_vlans/merged/vars.yml
expected_config:
  vlan_id: "100"
  name: Test-Config
  subnet: 192.168.128.0/24
  appliance_ip: 192.168.128.1
  group_policy_id: example
  template_vlan_type: same
  cidr: 192.168.128.0/24
  mask: 24
```

### Converge — Clean Documentation Example

Each `converge.yml` loads `vars.yml` and contains only the module call — the exact code a user would write. No assertions, no debug output. This is the documentation source.

```yaml
---
# extensions/molecule/appliance_vlans/merged/converge.yml
- name: "Converge — appliance_vlans (merged)"
  hosts: localhost
  gather_facts: false
  vars_files:
    - vars.yml
  tasks:
    - name: Create appliance_vlans with merged state
      cisco.meraki_rm.meraki_appliance_vlans:
        network_id: "N_123456789012345678"
        state: merged
        config:
          - "{{ expected_config }}"
      register: merge_result
```

Because each converge tests a single state, the idempotence replay is guaranteed not to oscillate. With no assertions in the converge, the replay runs cleanly regardless of `changed` status.

For documentation injection, `inject_examples.py` reads `vars.yml` and renders it as a `set_fact` task prepended to the converge tasks — producing a complete, copy-pasteable example for `ansible-doc`.

### Verify — Full Data Validation via Shared Vars

Each `verify.yml` loads the same `vars.yml`, independently gathers the current state, and validates that every expected field is present and correct using the `path_contained_in` filter.

```yaml
---
# extensions/molecule/appliance_vlans/merged/verify.yml
- name: "Verify — appliance_vlans (merged)"
  hosts: localhost
  gather_facts: false
  vars_files:
    - vars.yml
  tasks:
    - name: Gather current configuration
      cisco.meraki_rm.meraki_appliance_vlans:
        network_id: "N_123456789012345678"
        state: gathered
      register: gathered

    - name: Assert configuration exists after merged
      ansible.builtin.assert:
        that:
          - gathered.gathered is defined
          - gathered.gathered | length > 0
        fail_msg: Expected at least one resource after merged

    - name: Compare expected paths to gathered state (subset check)
      ansible.builtin.set_fact:
        path_check: "{{ expected_paths | cisco.meraki_rm.path_contained_in(result_paths) }}"
      vars:
        expected_paths: "{{ expected_config | ansible.utils.to_paths }}"
        result_paths: "{{ gathered.gathered[0] | ansible.utils.to_paths }}"

    - name: Assert all expected fields are present and match
      ansible.builtin.assert:
        that: path_check.contained | bool
        success_msg: "{{ success_msg }}"
        fail_msg: "{{ fail_msg }}"
      vars:
        success_msg: "All expected fields match. Extras: {{ path_check.extras }}"
        fail_msg: "Missing or mismatch: {{ path_check.missing }}. Extras: {{ path_check.extras }}"
```

State-specific verify behavior:
- **merged/replaced/overridden**: `vars_files` + `path_contained_in` against `gathered.gathered[0]`
- **overridden**: same, plus `gathered.gathered | length == 1`
- **deleted**: no vars_files needed — asserts `gathered.gathered | length == 0`
- **gathered**: asserts `gathered.gathered | length > 0`

Verify runs twice in the test sequence (after converge and after idempotence), catching state drift.

### prepare.yml — Seeds Prerequisite State

States that require an existing resource to test against (replaced, overridden, deleted, gathered) use `prepare.yml` to seed it:

```yaml
---
# extensions/molecule/appliance_vlans/replaced/prepare.yml
- name: "Prepare — appliance_vlans (replaced)"
  hosts: localhost
  gather_facts: false
  tasks:
  - name: Seed resource via merged (prerequisite for replaced)
    cisco.meraki_rm.meraki_appliance_vlans:
      network_id: "N_123456789012345678"
      state: merged
      config:
        - vlan_id: "100"
          name: Test-Config
          subnet: 192.168.128.0/24
          appliance_ip: 192.168.128.1
```

For `overridden`, the prepare seeds *multiple* resources so the test can verify that extras get deleted. For `merged`, no prepare is needed — the converge itself creates the resource.

### cleanup.yml — Removes Test Resources

For modules that support delete:

```yaml
---
# extensions/molecule/appliance_vlans/merged/cleanup.yml
- name: "Cleanup — appliance_vlans (merged)"
  hosts: localhost
  gather_facts: false
  tasks:
  - name: Remove test resources
    cisco.meraki_rm.meraki_appliance_vlans:
      network_id: "N_123456789012345678"
      state: deleted
      config:
        - vlan_id: "100"
    ignore_errors: true
```

For singletons without delete support, cleanup is a no-op debug message.
For `deleted` scenarios, cleanup is a no-op since the converge already removed the resource.

### Idempotence — Automatic, Per-State

Molecule handles this. After converge completes, Molecule re-runs converge.yml and checks that **every task returns `changed: false`**. If any task returns `changed: true`, the idempotence step fails.

This is the most important test for a resource module. It validates:
- The module correctly detects existing state (gather `before`)
- The diff logic works (`before == after` → no spurious changes)
- The module does not call the API unnecessarily

Because each scenario converges a single state, the replay against an
already-converged system naturally produces `changed: false`. The `before`/`after`
pattern makes this automatic: `changed = (before != after)`.

### Supported States per Module

Not all modules support all five states. The table below shows which states produce example files:

| Module Archetype | merged | replaced | overridden | gathered | deleted |
|---|---|---|---|---|---|
| Full CRUD (e.g. appliance_vlans) | Yes | Yes | Yes | Yes | Yes |
| Singleton (e.g. appliance_firewall) | Yes | Yes | — | Yes | — |
| Org CRUD (e.g. organization_admins) | Yes | — | — | Yes | Yes |
| Facts ({prefix}_facts) | — | — | — | Yes | — |

---

## SECTION 5: Unit Tests — Colocated `*_test.py` Files

### Purpose

Fast, sub-second feedback on pure-Python data logic: field mappings, bidirectional transforms, dataclass construction, and spec drift. These tests catch the class of bugs that historically were only discovered after a ~30s Molecule startup cycle — wrong field names, scope param leaks, broken transforms, missing dataclass fields.

### Design Principle: Colocated Sibling Files

Each source file in `plugin_utils/` has a sibling `*_test.py` file right next to it. This convention:

- Makes it obvious which tests cover which code
- Eliminates `sys.path` hacks (tests use relative imports from their own package)
- Is discovered by pytest via `pyproject.toml` configuration

### pytest Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests", "plugins"]
python_files = ["test_*.py", "*_test.py"]
```

This tells pytest to discover both the existing `tests/` tree and colocated `*_test.py` files under `plugins/`.

### File Layout

```
plugins/plugin_utils/
  user_models/
    vlan.py
    vlan_test.py              # Tier 1: forward transform, scope exclusion
    admin.py
    admin_test.py
    ...                       # ~47 pairs (auto-generated)
  api/v1/
    vlan.py
    vlan_test.py              # Tier 2: reverse transform, roundtrip, endpoints
    admin.py
    admin_test.py
    ...                       # ~47 pairs (auto-generated)
    generated/
      vlan.py
      vlan_test.py            # Tier 3: drift detection (field inventory + spec cross-ref)
      admin.py
      admin_test.py
      ...                     # ~47 pairs (auto-generated)
  platform/
    base_transform.py
    base_transform_test.py    # Tier 4: core engine (hand-written)
    loader.py
    loader_test.py            # Tier 4: _detect_collection_prefix (hand-written)
    types.py
    types_test.py             # Tier 4: EndpointOperation, ModuleConfig (hand-written)
```

### Four-Tier Test Structure

**Tier 1: `user_models/{name}_test.py`** (~47 files, auto-generated)
- Dataclass instantiation — all fields default to `None`
- Forward transform: `UserX.to_api(ctx)` produces correct camelCase fields
- Scope params (e.g. `network_id`) do NOT appear in API output
- `None` fields are omitted in forward direction

**Tier 2: `api/v1/{name}_test.py`** (~47 files, auto-generated)
- Reverse transform: `APIX_v1.to_ansible(ctx)` produces correct snake_case fields
- Roundtrip: User → API → User preserves every mapped field
- Endpoint operations: validate path, method, path_params are non-empty

**Tier 3: `api/v1/generated/{name}_test.py`** (~47 files, auto-generated)
- All expected fields exist on the dataclass (locked against current generation)
- All fields default to `None` (every field is `Optional`)
- Field count matches expected (catches silent additions or removals)
- **Spec drift detection**: field names cross-referenced against `spec3.json` response and request schemas — catches regeneration drift where fields are added, removed, or renamed

**Tier 4: `platform/*_test.py`** (3 files, hand-written)
- `base_transform_test.py`: forward/reverse mapping, field filtering for unknown keys, `_post_transform_hook`, scope param exclusion, roundtrip, edge cases
- `loader_test.py`: `_detect_collection_prefix()` for dev vs collection namespaces, `DynamicClassLoader` user class and API class loading
- `types_test.py`: `EndpointOperation`, `ResourceModuleStates`, `ModuleConfig` construction, defaults, field inventories

### Test Generator

Most colocated tests (Tiers 1–3) are auto-generated from dataclass introspection:

```bash
python tools/generate_model_tests.py          # write all *_test.py files
python tools/generate_model_tests.py --check   # dry-run, report what would change
```

The generator (`tools/generate_model_tests.py`) introspects each `user_models/*.py` and paired `api/v1/*.py`:

1. Reads `_field_mapping` dict from the user model
2. Reads dataclass fields from both user model and API model
3. Reads `get_endpoint_operations()` from the API mixin
4. For `generated/*.py`: parses "Source paths" from docstrings, extracts field names from `spec3.json` for cross-referencing

Regenerate after any of these change:
- Adding or modifying a user model or API model
- Regenerating `api/v1/generated/*.py` from the OpenAPI spec
- Changing `_field_mapping` in any model

### What Colocated Tests Catch (That Molecule Caught Late)

| Bug from development | Tier that catches it | Old detection method |
|---|---|---|
| `networkId` leaking through transform into API dataclass | Tier 1 scope exclusion | Molecule integration (30s startup) |
| `APIVlan_v1(**response_with_networkId)` constructor blows up | Tier 2 roundtrip / Tier 4 field filtering | Molecule integration |
| `quality_retention_profile_id` mapped to `qualityRetentionProfileId` instead of `id` | Tier 1 forward transform (AttributeError) | Molecule integration |
| `vlan_id` vs `id` field name in return data | Tier 2 reverse transform | Molecule integration |
| Generated dataclass missing field after spec regeneration | Tier 3 spec drift | Manual review |

### Mock Server Self-Tests

Separate from colocated tests, the mock server has its own tests in `tests/`:

- **state_store** — CRUD operations, primary key handling, 404 on missing resources
- **spec_loader** — path parsing, schema extraction, path parameter matching
- **response_generator** — schema-compliant response generation, default filling

---

## SECTION 6: Adding Tests for a New Module

When adding a new resource module (see [07-adding-resources.md](07-adding-resources.md)), follow this checklist to add tests.

### Step 1: Create Example Files

Create per-state YAML task files in `examples/{resource_name}/`:

```bash
mkdir -p examples/{resource_name}
```

Write one file per supported state:

- **`merged.yml`** — Create/update with realistic values, register result, assert `changed`
- **`replaced.yml`** — Full replacement with different values, assert `changed`
- **`gathered.yml`** — Read current state, register as `gathered`, display with `debug`
- **`deleted.yml`** — Remove by primary key, assert `changed`

Each file is a flat list of Ansible tasks (no play header — the Molecule wrapper provides that).

### Step 2: Inject into Module Documentation

```bash
python tools/inject_examples.py
```

This concatenates your per-state files and writes them into the `EXAMPLES` block of `plugins/modules/{prefix}_{resource_name}.py`. Verify with:

```bash
python tools/inject_examples.py --check  # exits 0 if in sync
```

### Step 3: Generate Molecule Scenario

```bash
python tools/generate_molecule_scenarios.py
```

This creates `extensions/molecule/{resource_name}/` with:
- `molecule.yml` — inherits shared config
- `converge.yml` — `include_tasks: examples/{resource_name}/merged.yml`
- `verify.yml` — `include_tasks: examples/{resource_name}/gathered.yml` + assertions
- `cleanup.yml` — `include_tasks: examples/{resource_name}/deleted.yml` (or no-op for singletons)

### Step 4: Generate Colocated Unit Tests

```bash
python tools/generate_model_tests.py
```

This generates sibling `*_test.py` files for the new model:
- `plugins/plugin_utils/user_models/{resource_name}_test.py` (Tier 1)
- `plugins/plugin_utils/api/v1/{resource_name}_test.py` (Tier 2)
- `plugins/plugin_utils/api/v1/generated/{resource_name}_test.py` (Tier 3)

### Step 5: Run Unit Tests First, Then Molecule

```bash
# Unit tests first (fast — catches transform bugs in sub-seconds)
pytest plugins/plugin_utils/ -v -k {resource_name}

# Only after unit tests pass: integration test (default scenario starts mock server)
molecule test -s {resource_name}

# During iteration
molecule converge -s {resource_name}
molecule verify -s {resource_name}
```

**Always run unit tests before Molecule.** If a transform mapping is wrong, a unit test catches it in under 2 seconds. Molecule would take 30+ seconds to reach the same failure.

### Pre-Commit Hook

The `.pre-commit-config.yaml` wires `inject_examples.py --check` as a hook. If you edit an example file and forget to re-inject, the hook fails on commit — keeping docs and tests in sync.

---

## SECTION 7: Running Tests

### How `shared_state` Works

With `shared_state: true`, Molecule uses the **default scenario as the lifecycle manager**. Even when targeting a single scenario with `-s`, Molecule runs **default create** first and **default destroy** last. Component scenarios skip create/destroy entirely — they only run their own test sequence (prepare / converge / verify / idempotence / verify / cleanup).

This means the mock server is always started and stopped for you. You never need to start it manually. The Platform Manager (multiprocessing RPC service) is spawned on the first module task and reused across all Molecule phases via socket + keyfile reconnection. See the [official Collection Testing guide](https://docs.ansible.com/projects/molecule/getting-started-collections/#shared-state-vs-per-scenario-resources).

### Single Module (All States)

```bash
# Wildcard: run all states for a module (merged, replaced, overridden, deleted, gathered)
MOLECULE_GLOB="extensions/molecule/**/molecule.yml" molecule test -s 'appliance_vlans/*'
```

### Single State

```bash
# Target a specific state
MOLECULE_GLOB="extensions/molecule/**/molecule.yml" molecule test -s appliance_vlans/merged
```

### Iteration

```bash
# converge/verify only (default scenario still manages server lifecycle)
MOLECULE_GLOB="extensions/molecule/**/molecule.yml" molecule converge -s appliance_vlans/merged
MOLECULE_GLOB="extensions/molecule/**/molecule.yml" molecule verify -s appliance_vlans/merged
```

### Full Integration Suite

```bash
# All module scenarios with shared mock server + platform manager
MOLECULE_GLOB="extensions/molecule/**/molecule.yml" molecule test --all --command-borders --report
```

This runs the complete flow:

```
DETAILS
default                      → create:      Start mock server
appliance_vlans/merged       → converge:    Module call (spawns Platform Manager)
appliance_vlans/merged       → verify/idempotence/verify/cleanup
appliance_vlans/replaced     → prepare/converge/verify/idempotence/verify/cleanup
appliance_vlans/overridden   → prepare/converge/.../cleanup
appliance_vlans/deleted      → prepare/converge/.../cleanup
appliance_vlans/gathered     → prepare/converge/.../cleanup
wireless_ssid/merged         → converge/.../cleanup
...                          → (all ~186 per-state scenarios)
default                      → destroy:     Stop mock server + kill Platform Manager

SCENARIO RECAP
default            : actions=2   successful=2
appliance_vlans    : actions=6   successful=6
wireless_ssid      : actions=6   successful=6
...
```

Use `--command-borders` for visual separation and `--report` for a summary table at the end.

### Unit Tests (Fast Feedback — Always Run First)

```bash
# All colocated unit tests (~700 tests, <2 seconds)
pytest plugins/ -v

# Specific module
pytest plugins/ -v -k vlan

# Platform engine tests only
pytest plugins/plugin_utils/platform/ -v

# Spec drift detection only
pytest plugins/plugin_utils/api/v1/generated/ -v

# Mock server self-tests (in tests/ tree)
pytest tests/ -v

# Everything
pytest -v
```

### CI/CD Integration

```yaml
# .github/workflows/test.yml (example)
name: Collection Tests

on: [push, pull_request]

jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements-dev.txt
      - run: pytest plugins/ tests/ -v --tb=short

  integration:
    runs-on: ubuntu-latest
    needs: unit
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements-dev.txt
      - run: pip install ansible-core
      - run: molecule test --all --report
```

Unit tests run first (fast gate — ~700 tests in <2s). Integration tests run only if unit tests pass. This prevents wasting CI minutes on Molecule runs that would fail due to a simple field mapping bug.

---

## SECTION 8: What Each Layer Catches

### Bug Category to Test Layer Matrix

| Bug Category | Colocated Unit (Tier) | Spec Validation (Mock) | Molecule Behavior | Molecule Idempotence |
|---|---|---|---|---|
| **Wrong camelCase field name** (e.g., `applianceIP` instead of `applianceIp`) | Tier 1 forward (AttributeError) | Catches (400 from mock) | — | — |
| **Wrong field mapping** (e.g., `id` vs `qualityRetentionProfileId`) | Tier 1 forward / Tier 2 reverse | Catches (wrong payload) | — | — |
| **Scope param leaks into API output** (`networkId` in body) | Tier 1 scope exclusion | Catches (extra field) | — | — |
| **Missing required field in request** | — | Catches (400 from mock) | — | — |
| **Invalid field type** (string where int expected) | — | Catches (400 from mock) | — | — |
| **Wrong API endpoint path** | Tier 2 endpoint ops | Catches (404 from mock) | — | — |
| **Broken forward transform** (User → API) | Tier 1 forward + Tier 2 roundtrip | Catches (invalid payload) | — | — |
| **Broken reverse transform** (API → User) | Tier 2 reverse + roundtrip | — | Catches (verify assertions fail) | — |
| **Generated dataclass field drift** (spec regeneration) | Tier 3 spec drift | — | — | — |
| **Extra/missing fields on generated dataclass** | Tier 3 field count + inventory | — | — | — |
| **BaseTransformMixin field filtering broken** | Tier 4 base_transform | — | Catches (constructor error) | — |
| **Module creates wrong resource** | — | — | Catches (verify finds wrong data) | — |
| **Module does not create resource** | — | — | Catches (verify finds nothing) | — |
| **Module does not update resource** | — | — | Catches (verify finds old data) | — |
| **Module does not delete resource** | — | — | Catches (cleanup + verify) | — |
| **Module not idempotent** (re-creates on re-run) | — | — | — | Catches (changed: true on re-run) |
| **Spurious diff** (unchanged field reported as changed) | — | — | — | Catches (changed: true on re-run) |
| **Gathered output does not match merged input format** | — | — | Catches (verify assertions fail) | — |
| **Read-only field leaks into write** | — | Catches (extra field in request) | — | — |
| **Name-to-ID transform broken** | Tier 2 roundtrip | — | Catches (wrong IDs in request) | — |
| **Multi-endpoint ordering wrong** | — | — | Catches (dependent operation fails) | — |

### Reading the Matrix

- **Colocated unit tests (Tiers 1–4)** catch pure-Python data bugs in sub-seconds. No server, no Ansible, no YAML. These are the **first line of defense** — run them before anything else. Most transform and field mapping bugs appear here.
- **Spec validation** catches HTTP contract bugs. The mock server enforces the spec so the module cannot lie about what it sends.
- **Molecule behavior** catches functional bugs. The module must actually do what the user asked.
- **Molecule idempotence** catches convergence bugs. The module must detect existing state and not act unnecessarily.

No single column covers all rows. All four are needed for confidence. But the leftmost column (unit tests) is the fastest and should be the first gate in CI and in the developer workflow.

---

## Summary

| Component | Location | Purpose |
|---|---|---|
| **Colocated Unit Tests** | `plugins/plugin_utils/**/*_test.py` | Transform roundtrips, spec drift, foundation (700+ tests) |
| **Test Generator** | `tools/generate_model_tests.py` | Auto-generates Tier 1–3 `*_test.py` files from dataclass introspection |
| **pytest Config** | `pyproject.toml` | Discovers `*_test.py` in both `tests/` and `plugins/` |
| **Examples** | `examples/{module}/{state}.yml` | Source of truth for docs + tests |
| **Injection Hook** | `tools/inject_examples.py` | Syncs examples into module `EXAMPLES` strings |
| **Pre-Commit** | `.pre-commit-config.yaml` | Fails commit if examples are out of sync |
| **Filter Plugin** | `plugins/filter/path_contained_in.py` | Subset comparison for round-trip assertions |
| **Mock Server** | `tools/mock_server/` | Stateful, spec-enforcing HTTP backend |
| **Molecule Config** | `extensions/molecule/config.yml` | Shared test settings (inventory, sequence, shared state) |
| **Default Scenario** | `extensions/molecule/default/` | Mock server lifecycle (create/destroy) |
| **Module Scenarios** | `extensions/molecule/{module}/` | Per-module CRUD + idempotence tests |

**Test commands (run in this order):**

| Command | Purpose | Speed |
|---|---|---|
| `pytest plugins/ -v` | Colocated unit tests (transforms, spec drift, foundation) | <2 seconds |
| `pytest -v` | All unit tests (colocated + tests/ tree) | <3 seconds |
| `molecule test -s {module}` | Single module integration test | ~30 seconds |
| `molecule test --all --report` | Full integration suite (~48 modules) | Minutes |

**Tooling commands:**

| Command | Purpose |
|---|---|
| `python tools/generate_model_tests.py` | (Re)generate colocated `*_test.py` files from dataclass introspection |
| `python tools/generate_model_tests.py --check` | Dry-run: report what would change without writing |
| `python tools/generate_examples.py` | (Re)generate per-state example files from DOCUMENTATION |
| `python tools/inject_examples.py` | Inject examples into module `EXAMPLES` strings |
| `python tools/inject_examples.py --check` | Verify all modules are in sync (pre-commit hook) |
| `python tools/generate_molecule_scenarios.py` | (Re)generate Molecule scenarios from examples |

---

## Related Documents

- [06-foundation-components.md](06-foundation-components.md) — Core components being tested
- [07-adding-resources.md](07-adding-resources.md) — Step 7 references this testing workflow
- [08-code-generators.md](08-code-generators.md) — Generated code that unit tests validate
- [09-agent-collaboration.md](09-agent-collaboration.md) — Agent testing workflow (Phase C)
- [10-case-study-novacom.md](10-case-study-novacom.md) — Module map drives the scenario list

*Document version: 1.2 | OpenAPI Resource Module SDK | Testing Strategy*
