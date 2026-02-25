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
5a. [Contract Tests — `test_action_contracts.py`](#section-5a-contract-tests--testsunittest_action_contractspy)
5b. [Full-Flow Spec Validation — `test_spec_validation.py`](#section-5b-full-flow-spec-validation--testsunittest_spec_validationpy)
5c. [In-Process Integration Tests — `test_integration_flow.py`](#section-5c-in-process-integration-tests--testsunittest_integration_flowpy)
6. [Adding Tests for a New Module](#section-6-adding-tests-for-a-new-module)
7. [Running Tests](#section-7-running-tests)
8. [What Each Layer Catches](#section-8-what-each-layer-catches)
9. [Molecule Scenario Coverage](#section-9-molecule-scenario-coverage)

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
                    ├──────────┤  (~234 scenarios, slower ~30s startup)
                    │          │
               ┌────┴──────────┴────┐
               │  In-Process        │  PlatformService → Flask mock server
               │  Integration       │  CRUD + OpenAPI validation, no HTTP
               ├────────────────────┤  (~188 tests, ~10 seconds)
               │  Full-Flow Spec    │  Argspec → transform → validate()
               │  Validation        │  → jsonschema vs spec (tests/unit/)
               ├────────────────────┤  (~138 tests, <3 seconds)
               │  Contract Tests    │  Action plugin ↔ endpoint op wiring
               │                    │  (tests/unit/, ~414 tests, <2 seconds)
               ├────────────────────┤
               │  Colocated Unit    │  Sibling *_test.py files in
               │  Tests (pytest)    │  plugin_utils/ — transform
               │                    │  roundtrips, spec drift, types
               └────────────────────┘  (sub-second, no server needed)
```

**Unit tests must run first.** Pure-Python data bugs — wrong field names, scope param leaks, broken transforms, missing dataclass fields, invalid enum values, argspec mismatches — should fail in sub-second `pytest` runs, not after a ~30s Molecule startup cycle. Molecule integration tests verify the full CRUD lifecycle against the mock server, but they are the **second** line of defense, not the first.

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
│   ├── gathered/
│   │   └── ...
│   └── check/                        # check_mode + diff: predict without applying
│       ├── molecule.yml             # test_sequence: prepare, converge, verify, cleanup
│       ├── vars.yml                 # expected_config (+ prepare_config for singletons)
│       ├── prepare.yml              # No-op (collection) or seed baseline (singleton)
│       ├── converge.yml             # check_mode: true, diff: true + assertions
│       ├── verify.yml               # Gather + assert state unchanged
│       └── cleanup.yml              # Gather + delete (collection) or no-op (singleton)
├── wireless_ssid/
│   ├── merged/
│   ├── replaced/
│   ├── gathered/                     # No delete (singleton)
│   └── check/
├── facts/
│   └── gathered/
└── ... (48 module groups, 234 per-state scenarios total)
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

1. **Documentation examples are clean** — A pre-commit hook (`tools/inject_examples.py`) reads per-state task files from `examples/{module}/` (generated by `tools/generate_examples.py`), concatenates them, and injects the combined result into the `EXAMPLES` block of `plugins/modules/{prefix}_*.py`. No assertion noise.

2. **Converge survives idempotence** — With no assertions in converge, Molecule's idempotence replay runs cleanly; `verify.yml` independently validates state after each converge using the same shared data.

3. **Verify validates actual data** — `verify.yml` loads `vars.yml` and uses `path_contained_in` to check that every expected field is present and correct in the gathered state. No more "something exists" — full field-level validation.

```
examples/{module}/merged.yml, gathered.yml, etc.
        │
        └──► tools/inject_examples.py ──► plugins/modules/{prefix}_{resource}.py (EXAMPLES)
              (concatenates per-state files)    └── ansible-doc reads EXAMPLES

extensions/molecule/{module}/merged/vars.yml + converge.yml
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
├── gathered/     # molecule test -s appliance_vlans/gathered
└── check/        # molecule test -s appliance_vlans/check
```

The pattern for each per-state scenario:

| Step | `merged` | `replaced` | `overridden` | `deleted` | `gathered` | `check` |
|------|----------|------------|--------------|-----------|------------|---------|
| prepare | — | Seed via merged | Seed 2+ resources | Seed via merged | Seed via merged | — (collection) / Seed baseline (singleton) |
| converge | set_fact + module call | set_fact + module call | set_fact + module call | set_fact + module call | module call (gather) | `check_mode: true`, `diff: true` + assert prediction |
| verify | Gather + assert exists | Gather + assert exists | Gather + assert count=1 | Gather + assert empty | Assert non-empty | Gather + assert unchanged |
| idempotence | Replay → `ok` | Replay → `ok` | Replay → `ok` | Replay → `ok` | Replay → `ok` | — (skipped; check mode always predicts `changed`) |
| cleanup | Delete resources | Delete resources | Delete resources | No-op | Delete resources | Gather + delete (collection) / No-op (singleton) |

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

For documentation injection, `inject_examples.py` reads per-state YAML files from `examples/{module}/` and concatenates them into a complete, copy-pasteable example for `ansible-doc`.

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

### Check Mode Scenarios — `check/`

Every module with a `merged/` scenario also has a `check/` scenario, generated by `tools/generate_check_scenarios.py`. These validate Ansible's `--check` and `--diff` flags end-to-end:

1. **Converge** runs the module with `check_mode: true` and `diff: true`, then asserts:
   - `changed == true` (the prediction detects a difference)
   - `before` and `after` are populated
   - `diff.before` and `diff.after` contain YAML-formatted state
2. **Verify** independently gathers actual state and confirms nothing changed — check mode is purely predictive.

For **collection resources**, prepare is a no-op (empty baseline). Check mode predicts adding the resource; verify confirms nothing was created.

For **singleton resources**, prepare seeds a baseline from `gathered/vars.yml`. Converge runs check mode with the different `merged/vars.yml` config. Verify gathers and confirms the baseline is intact via `path_contained_in`.

The test sequence omits `idempotence` because check mode always predicts `changed: true` for the same input — it never applies changes, so Molecule's idempotence replay (which expects `changed: false` on the second run) would fail by design.

```bash
# Generate check scenarios for all modules
python tools/generate_check_scenarios.py

# Generate for a specific module
python tools/generate_check_scenarios.py --module appliance_vlans

# Dry-run (preview without writing)
python tools/generate_check_scenarios.py --dry-run
```

### Supported States per Module

Not all modules support all six states. The table below shows which states produce example files:

| Module Archetype | merged | replaced | overridden | gathered | deleted | check |
|---|---|---|---|---|---|---|
| Full CRUD (e.g. appliance_vlans) | Yes | Yes | Yes | Yes | Yes | Yes |
| Singleton (e.g. appliance_firewall) | Yes | Yes | — | Yes | — | Yes |
| Org CRUD (e.g. organization_admins) | Yes | Yes | Yes | Yes | Yes | Yes |
| Facts ({prefix}_facts) | — | — | — | Yes | — | — |

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

## SECTION 5a: Contract Tests — `tests/unit/test_action_contracts.py`

### Purpose

Validate the architectural wiring between action plugins, their transform mixins, and endpoint operations. These tests are parametrized over every `meraki_*.py` action plugin and run entirely in Python — no Ansible runtime, no mock server.

### Location

```
tests/unit/
├── conftest.py                  # Shared discovery helpers (parse_action_plugin, load_classes)
├── test_action_contracts.py     # Contract validation (~414 tests)
└── test_spec_validation.py      # Full-flow spec validation (Section 5b)
```

### What Contract Tests Validate

| Contract | Assertion |
|---|---|
| **State routing** | Every state in `VALID_STATES` maps to an existing endpoint operation (`merged` → `update` or `create`, `deleted` → `delete`, `gathered` → `find`) |
| **Identity fields** | `SCOPE_PARAM`, `CANONICAL_KEY`, and `SYSTEM_KEY` (when set) exist as fields on the User Model dataclass |
| **Field mapping keys** | Every key in `_field_mapping` is a real field on the User Model |
| **Field mapping values** | Every value in `_field_mapping` is a real field on the API class |
| **Endpoint fields** | Fields listed in `EndpointOperation.fields` exist on the API class |
| **Data roundtrip** | `UserModel → .to_api() → .to_ansible()` preserves all mapped field values |

### Discovery

Tests dynamically discover all action plugins by globbing `plugins/action/meraki_*.py`, parsing class attributes (`MODULE_NAME`, `SCOPE_PARAM`, `USER_MODEL`, `CANONICAL_KEY`, `SYSTEM_KEY`, `VALID_STATES`, `SUPPORTS_DELETE`) from source text without importing, then loading the corresponding classes.

### Why These Live in `tests/unit/` Not `plugins/`

Ansible's plugin loader scans `plugins/` directories. Test files placed there would be mistakenly loaded as plugins. The `tests/unit/` location avoids this, with `conftest.py` adding `plugins/` to `sys.path` for imports.

---

## SECTION 5b: Full-Flow Spec Validation — `tests/unit/test_spec_validation.py`

### Purpose

End-to-end validation of the data pipeline from Molecule fixture data through the transform layer to the OpenAPI spec — without running Ansible, Molecule, or the mock server. Uses the same `vars.yml` files that Molecule uses as fixtures.

### Three Stages

```
┌─────────────────────────────────────────────────────────────────┐
│ Stage 0: Argspec Validation                                     │
│ "Does the fixture data pass Ansible's own argument spec?"       │
│                                                                  │
│ Loads DOCUMENTATION from the module file, feeds vars.yml data   │
│ through Ansible's ArgumentSpecValidator — type coercion,        │
│ choices, required_if, mutually_exclusive, nested suboptions.    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 1: Outbound — Request Body Validation                     │
│ "Does the transformed API payload match the OpenAPI spec?"      │
│                                                                  │
│ vars.yml → UserModel(**config) → .to_api() → validate()        │
│ (checks _FIELD_CONSTRAINTS enums) → build request body          │
│ → jsonschema.validate() against spec's request schema           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 2: Inbound — Response Roundtrip Validation                │
│ "Does a spec-shaped response survive the reverse transform?"    │
│                                                                  │
│ Simulated response (request body + schema defaults + identity   │
│ fields) → _safe_construct(APIClass) → .to_ansible()             │
│ → assert every expected_config key matches                      │
└─────────────────────────────────────────────────────────────────┘
```

### `_FIELD_CONSTRAINTS` — Spec-Derived Validation on API Dataclasses

The code generator (`tools/generators/extract_meraki_schemas.py`) extracts enum constraints from the OpenAPI spec and emits them as `_FIELD_CONSTRAINTS` class variables on generated API dataclasses:

```python
@dataclass
class WirelessRfProfile:
    _FIELD_CONSTRAINTS: ClassVar[dict] = {
        'bandSelectionType': {'enum': ['ap', 'ssid']},
        'minBitrateType': {'enum': ['band', 'ssid']},
    }
    # ... fields ...
```

`BaseTransformMixin.validate()` checks these constraints and raises `ValueError` listing all violations. This fires in tests and can be called in the action plugin before building request bodies — catching bad values *before* the API call.

### Discovery

Fixtures are discovered by globbing `extensions/molecule/*/merged/vars.yml`. Each directory name maps to an action plugin file `plugins/action/meraki_{dir_name}.py`, and the corresponding module file `plugins/modules/meraki_{dir_name}.py` provides the argspec.

### Fixture Data as Single Source of Truth

The `vars.yml` files serve triple duty:

1. **Molecule integration tests** — converge/verify playbooks load them
2. **Full-flow spec validation** — this test suite uses them as fixtures
3. **Documentation** — `inject_examples.py` renders them into module `EXAMPLES`

When a `vars.yml` changes, all three consumers automatically pick up the change.

---

## SECTION 5c: In-Process Integration Tests — `tests/unit/test_integration_flow.py`

### Purpose

Exercises the full `PlatformService → Mock Server` flow — real CRUD, real OpenAPI validation, real state — without subprocesses or TCP. Uses `requests-flask-adapter` to mount the Flask mock server directly into `PlatformService`'s `requests.Session`, giving HTTP-level fidelity at unit-test speed.

This tier fills the gap between full-flow spec validation (Section 5b), which validates transforms without touching the server, and Molecule (Section 3), which adds Ansible subprocess and HTTP overhead:

- **Full-flow spec validation** validates `vars.yml → UserModel → APIModel → jsonschema` but never calls the server
- **In-process integration** sends real HTTP calls through PlatformService, hits the mock server's CRUD store, and validates OpenAPI compliance — all in-process (~10 seconds)
- **Molecule** does the same but through `ansible-playbook` subprocesses over TCP (~30s startup + seconds per module)

### How It Works

```
┌──────────────────────────────────────────────────────────┐
│  pytest process (single Python interpreter)              │
│                                                          │
│  ┌──────────────┐     requests-flask-adapter    ┌──────┐ │
│  │ Platform     │ ──── Session.get/put/post ──► │ Flask│ │
│  │ Service      │     (in-process, no TCP)      │ Mock │ │
│  │              │ ◄── response dict ─────────── │Server│ │
│  └──────────────┘                               └──────┘ │
│         │                                          │     │
│  UserModel ↔ APIModel                       StateStore   │
│  transforms + validate()                    + openapi-   │
│                                              core        │
└──────────────────────────────────────────────────────────┘
```

The `requests-flask-adapter` library replaces the TCP transport layer with a direct Python function call, so `session.get("http://mock/api/...")` routes to `app.test_client()` internally. The mock server's `openapi-core` middleware still validates every request and response against the OpenAPI spec.

### Location

```
tests/unit/
├── conftest.py                    # Shared discovery helpers
├── test_action_contracts.py       # Contract validation (Section 5a)
├── test_spec_validation.py        # Full-flow spec validation (Section 5b)
└── test_integration_flow.py       # In-process integration (this section)
```

### Dependencies

```
requests-flask-adapter>=0.1.0     # added to requirements-dev.txt
```

### Fixture Setup

A module-scoped `flask_app` fixture creates the mock server app once. A per-test `svc` fixture resets the `StateStore` and wires a fresh `PlatformService` via the adapter:

```python
@pytest.fixture(scope="module")
def flask_app():
    app = create_app(str(SPEC_PATH))
    FlaskSession.register("http://mock-meraki", app)
    yield app

@pytest.fixture()
def svc(flask_app):
    flask_app.config["STATE_STORE"].clear()
    return _make_service()
```

Each test gets a clean state store, preventing cross-test contamination while reusing the (expensive) app and spec parsing.

### Test Classes

**TestWriteThenFind** — Write a resource via PlatformService, then find it back. Asserts that all expected fields from `vars.yml` are present and correct in the returned data. For collection resources (POST create), server-assigned primary keys are excluded from comparison.

**TestIdempotence** — For singleton/update resources, writing the same data twice must produce identical state. Collection resources (POST create) are skipped since create is not idempotent by design.

**TestGatheredRoundTrip** — Write, then find. All expected keys (excluding scope and server-assigned PKs) must appear in the result, validating the full transform roundtrip through the server.

**TestDeleteRemovesResource** — For collection resources with delete endpoints: create a resource, capture the server-assigned ID, delete it, verify the store is empty.

### What This Tier Catches

- **PlatformService dispatch bugs** — wrong HTTP method, malformed URL, missing path parameters
- **Mock server CRUD bugs** — items not stored, not retrieved, or not deleted correctly
- **OpenAPI request validation failures** — request body rejected by openapi-core middleware (400)
- **OpenAPI response validation failures** — response shape doesn't match the spec
- **Transform + HTTP integration bugs** — field that survives transform but breaks at the wire level
- **Idempotence at the service level** — update produces different state on second call

### Skip Lists

Some modules are structurally inapplicable for certain tests. These are skipped via per-test-class skip lists in `test_integration_flow.py`:

- **`_WRITE_FIND_SKIP`** — modules with no find endpoint (e.g., `wireless_air_marshal_rules` has only create/update/delete ops, so write-then-find cannot run)
- **`_ROUNDTRIP_SKIP`** — modules where roundtrip validation is structurally inapplicable (e.g., no find endpoint, or spec response schema omits keys that the user model expects)
- **`_DELETE_SKIP`** — modules where the delete test is structurally inapplicable (beyond the built-in guards for `SUPPORTS_DELETE`, `has_delete`, and `is_collection`; e.g., singleton resources or modules with no delete endpoint). Currently empty.

### Coverage Comparison

| Validation Point | Full-Flow Spec | In-Process Integration | Molecule |
|---|---|---|---|
| Argspec validation | Yes | — | Yes (implicit) |
| Transform correctness | Yes | Yes (via PlatformService) | Yes |
| `_FIELD_CONSTRAINTS` / validate() | Yes | Yes (called by transforms) | Yes |
| jsonschema vs spec | Yes | Yes (openapi-core middleware) | Yes |
| HTTP dispatch (method, URL, params) | — | Yes | Yes |
| Stateful CRUD (create/read/update/delete) | — | Yes | Yes |
| Idempotence (service level) | — | Yes | Yes (Ansible level) |
| Ansible module execution | — | — | Yes |
| `changed` / `before` / `after` | — | — | Yes |
| Playbook-level assertions | — | — | Yes |

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

### Step 3: Generate Molecule Scenarios

```bash
python tools/restructure_molecule.py
python tools/generate_check_scenarios.py
```

`restructure_molecule.py` creates per-state `extensions/molecule/{resource_name}/{state}/` directories with `molecule.yml`, `vars.yml`, `converge.yml`, `verify.yml`, `prepare.yml`, and `cleanup.yml`.

`generate_check_scenarios.py` creates the `check/` scenario for check mode and diff mode testing.

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
# Wildcard: run all states for a module (merged, replaced, overridden, deleted, gathered, check)
molecule test -s 'appliance_vlans/*'
```

### Single State

```bash
# Target a specific state
molecule test -s appliance_vlans/merged
```

### Check Mode Only

```bash
# All check scenarios (46 modules)
molecule test -s '*/check' --report

# Single module check scenario
molecule test -s appliance_vlans/check
```

### Iteration

```bash
# converge/verify only (default scenario still manages server lifecycle)
molecule converge -s appliance_vlans/merged
molecule verify -s appliance_vlans/merged
```

### Full Integration Suite

```bash
# All module scenarios with shared mock server + platform manager
molecule test --all --command-borders --report
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
appliance_vlans/check        → prepare/converge/verify/cleanup (no idempotence)
wireless_ssid/merged         → converge/.../cleanup
...                          → (all 234 per-state scenarios)
default                      → destroy:     Stop mock server + kill Platform Manager

SCENARIO RECAP
default            : actions=2   successful=2
appliance_vlans    : actions=6   successful=6
wireless_ssid      : actions=6   successful=6
...
```

Use `--command-borders` for visual separation and `--report` for a summary table at the end.

### In-Process Integration Tests

```bash
# Full PlatformService → mock server flow (~188 tests, ~10 seconds)
pytest tests/unit/test_integration_flow.py -v
```

This runs the same CRUD lifecycle that Molecule tests but without Ansible or TCP. Each test gets a fresh `StateStore`, writes via PlatformService, and verifies the result. Ideal for rapid iteration on transform or mock server changes.

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

# Contract tests — action plugin ↔ endpoint wiring (~414 tests, <2 seconds)
pytest tests/unit/test_action_contracts.py -v

# Full-flow spec validation — argspec + transform + jsonschema (~138 tests, <3 seconds)
pytest tests/unit/test_spec_validation.py -v

# All tests/ tree (contract + spec validation + mock server self-tests)
pytest tests/ -v

# Everything (colocated + tests/ tree)
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

Unit tests run first (fast gate — ~1200+ tests in <5s across colocated, contract, and spec validation). In-process integration adds ~10 seconds of PlatformService → mock server CRUD testing. Molecule integration tests run only if both pass. This prevents wasting CI minutes on Molecule runs that would fail due to a simple field mapping bug, an invalid enum value, or an argspec mismatch.

---

## SECTION 8: What Each Layer Catches

### Bug Category to Test Layer Matrix

| Bug Category | Colocated Unit (Tier) | Contract Tests | Full-Flow Spec | In-Process Integration | Molecule Behavior | Molecule Idempotence |
|---|---|---|---|---|---|---|
| **Wrong camelCase field name** | Tier 1 forward (AttributeError) | — | — | Catches (400 from mock) | — | — |
| **Wrong field mapping** | Tier 1 forward / Tier 2 reverse | — | — | Catches (wrong payload) | — | — |
| **Scope param leaks into API output** | Tier 1 scope exclusion | — | — | Catches (extra field) | — | — |
| **Missing required field in request** | — | — | Catches (jsonschema) | Catches (400 from mock) | — | — |
| **Invalid enum value** (e.g., `"example"`) | — | — | Catches (validate() + jsonschema) | Catches (400 from mock) | — | — |
| **Invalid field type** (string where int) | — | — | Catches (argspec + jsonschema) | Catches (400 from mock) | — | — |
| **Argspec choices violation** | — | — | Catches (ArgumentSpecValidator) | — | — | — |
| **Wrong API endpoint path** | Tier 2 endpoint ops | — | — | Catches (404 from mock) | — | — |
| **State has no matching endpoint op** | — | Catches (state routing) | — | — | — | — |
| **CANONICAL_KEY missing from user model** | — | Catches (identity fields) | — | — | — | — |
| **Endpoint field not on API class** | — | Catches (endpoint fields) | — | — | — | — |
| **Broken forward transform** (User → API) | Tier 1 forward + Tier 2 roundtrip | — | Catches (jsonschema) | Catches (invalid payload) | — | — |
| **Broken reverse transform** (API → User) | Tier 2 reverse + roundtrip | — | Catches (roundtrip) | Catches (find mismatch) | Catches (verify) | — |
| **Generated dataclass field drift** | Tier 3 spec drift | — | — | — | — | — |
| **Extra/missing fields on generated dataclass** | Tier 3 field count + inventory | — | — | — | — | — |
| **BaseTransformMixin field filtering broken** | Tier 4 base_transform | — | — | Catches (constructor error) | Catches (constructor error) | — |
| **PlatformService dispatch bug** | — | — | — | Catches (wrong URL/method) | Catches (wrong URL/method) | — |
| **CRUD state not persisted** | — | — | — | Catches (find empty after write) | Catches (verify) | — |
| **Module creates wrong resource** | — | — | — | Catches (field mismatch) | Catches (verify) | — |
| **Module does not create resource** | — | — | — | Catches (find empty) | Catches (verify) | — |
| **Module does not update resource** | — | — | — | Catches (find stale) | Catches (verify) | — |
| **Module does not delete resource** | — | — | — | Catches (find non-empty) | Catches (cleanup) | — |
| **Service-level idempotence** | — | — | — | Catches (state diff) | — | — |
| **Module not idempotent (Ansible)** | — | — | — | — | — | Catches (changed: true) |
| **Spurious diff** | — | — | — | — | — | Catches (changed: true) |
| **Check mode leaks changes** | — | — | — | — | Catches (check/verify) | — |
| **Check mode prediction wrong** | — | — | — | — | Catches (check/converge) | — |
| **Diff output missing or malformed** | — | — | — | — | Catches (check/converge) | — |
| **Gathered output ≠ merged input format** | — | — | Catches (roundtrip) | Catches (key mismatch) | Catches (verify) | — |
| **Read-only field leaks into write** | — | — | — | Catches (extra field) | — | — |
| **Name-to-ID transform broken** | Tier 2 roundtrip | — | — | — | Catches (wrong IDs) | — |
| **Multi-endpoint ordering wrong** | — | — | — | — | Catches (dependent op fails) | — |
| **vars.yml fixture data invalid** | — | — | Catches (all 3 stages) | Catches (write fails) | — | — |

### Reading the Matrix

- **Colocated unit tests (Tiers 1–4)** catch pure-Python data bugs in sub-seconds. No server, no Ansible, no YAML. First line of defense.
- **Contract tests** catch architectural wiring bugs — state-to-operation mismatches, missing identity fields, broken field lists. Pure Python, ~1 second.
- **Full-flow spec validation** catches data-level bugs — invalid enums, type mismatches, argspec violations, request schema violations, response roundtrip drift. Uses the same vars.yml fixtures as Molecule but runs in ~2 seconds.
- **In-process integration** catches HTTP dispatch and CRUD state bugs by running PlatformService against the real mock server in-process — no TCP, no subprocesses. Validates OpenAPI compliance at the wire level with ~10 second runtime.
- **Molecule behavior** catches functional bugs at the Ansible level. The module must actually do what the user asked, including `changed`/`before`/`after` semantics.
- **Molecule idempotence** catches convergence bugs. The module must detect existing state and not act unnecessarily.

No single column covers all rows. All six are needed for confidence. The leftmost columns are the fastest and should be the first gate in CI.

---

## SECTION 9: Molecule Scenario Coverage

234 active Molecule scenarios across 48 modules. The table below shows which resource module states have Molecule scenario coverage and why certain states are absent.

### Coverage Legend

| Symbol | Meaning |
|--------|---------|
| :white_check_mark: | Scenario exists and passes |
| — | State not supported by this module |
| :x: _reason_ | State is valid but scenario is missing |

### Full Coverage (all valid states have scenarios)

These modules have a Molecule scenario for every state they support.

| Module | gathered | merged | replaced | deleted | overridden | check | Scope |
|--------|:--------:|:------:|:--------:|:-------:|:----------:|:-----:|-------|
| `appliance_prefixes` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `appliance_rf_profiles` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `appliance_static_routes` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `appliance_vlans` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `auth_users` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `camera_quality_retention_profiles` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `camera_wireless_profiles` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `device_switch_routes` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | serial |
| `floor_plans` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `group_policies` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `mqtt_brokers` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `sensor_alert_profiles` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `switch_access_policies` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `switch_link_aggregations` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `switch_qos_rules` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `vlan_profiles` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `webhooks` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `wireless_ethernet_port_profiles` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `wireless_rf_profiles` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `organization_admins` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | organization |
| `organization_alert_profiles` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | organization |
| `organization_branding_policies` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | organization |
| `organization_config_templates` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | organization |
| `organization_policy_objects` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | organization |

### Singleton Resources (no delete — `SUPPORTS_DELETE = False`)

These resources represent device/network configuration that always exists. They cannot be deleted, only reconfigured. Valid states: `gathered`, `merged`, `replaced`, `check`.

| Module | gathered | merged | replaced | check | Scope |
|--------|:--------:|:------:|:--------:|:-----:|-------|
| `appliance_firewall` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `appliance_port` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `appliance_security` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `appliance_ssid` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `appliance_traffic_shaping` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `appliance_vpn` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `appliance_warm_spare` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `device` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | serial |
| `device_management_interface` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | serial |
| `firmware_upgrade` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `network_settings` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `organization_adaptive_policy` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | organization |
| `organization_saml` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | organization |
| `organization_vpn` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | organization |
| `switch_acl` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `switch_dhcp_policy` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `switch_ports` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | serial |
| `switch_routing` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `switch_settings` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `switch_stp` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |
| `wireless_ssid` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | network |

### Special / Custom State Modules

| Module | gathered | merged | replaced | deleted | overridden | check | Notes |
|--------|:--------:|:------:|:--------:|:-------:|:----------:|:-----:|-------|
| `facts` | :white_check_mark: | — | — | — | — | — | Facts-only module; uses `gather_subset`, not resource states |
| `switch_stacks` | :white_check_mark: | :white_check_mark: | — | :white_check_mark: | — | :white_check_mark: | Custom `VALID_STATES`; API does not support `replaced` or `overridden` |
| `wireless_air_marshal_rules` | — | — | — | :white_check_mark: | — | — | No `merged` scenario; no network-level GET endpoint; `merged`/`replaced` create resources but cannot verify via `gathered` |

### Coverage Summary

| Category | Modules | Scenarios |
|----------|---------|-----------|
| Full coverage (all valid states) | 24 | 144 |
| Singleton (all valid states) | 21 | 84 |
| Special / custom states | 3 | 6 |
| **Total** | **48** | **234** |

---

## Summary

| Component | Location | Purpose |
|---|---|---|
| **Colocated Unit Tests** | `plugins/plugin_utils/**/*_test.py` | Transform roundtrips, spec drift, foundation (700+ tests) |
| **Contract Tests** | `tests/unit/test_action_contracts.py` | Action plugin ↔ endpoint wiring validation (414+ tests) |
| **Full-Flow Spec Validation** | `tests/unit/test_spec_validation.py` | Argspec + transform + jsonschema validation (138+ tests) |
| **In-Process Integration** | `tests/unit/test_integration_flow.py` | PlatformService → mock server CRUD + OpenAPI validation (188+ tests) |
| **Test Generator** | `tools/generate_model_tests.py` | Auto-generates Tier 1–3 `*_test.py` files from dataclass introspection |
| **Check Scenario Generator** | `tools/generate_check_scenarios.py` | Auto-generates check-mode Molecule scenarios (46 modules) |
| **Schema Generator** | `tools/generators/extract_meraki_schemas.py` | Generates API dataclasses with `_FIELD_CONSTRAINTS` from spec |
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
| `pytest tests/unit/test_action_contracts.py -v` | Contract tests (action plugin ↔ endpoint wiring) | <2 seconds |
| `pytest tests/unit/test_spec_validation.py -v` | Full-flow spec validation (argspec + transform + jsonschema) | <3 seconds |
| `pytest tests/unit/test_integration_flow.py -v` | In-process integration (PlatformService → mock server CRUD) | ~10 seconds |
| `pytest -v` | All unit tests (colocated + contract + spec + integration + mock server) | ~15 seconds |
| `molecule test -s {module}` | Single module integration test | ~30 seconds |
| `molecule test --all --report` | Full integration suite (48 modules, 234 scenarios) | Minutes |

**Tooling commands:**

| Command | Purpose |
|---|---|
| `python tools/generate_model_tests.py` | (Re)generate colocated `*_test.py` files from dataclass introspection |
| `python tools/generate_model_tests.py --check` | Dry-run: report what would change without writing |
| `python -m tools.generators.extract_meraki_schemas --spec spec3.json --output plugins/plugin_utils/api/v1/generated/` | (Re)generate API dataclasses with `_FIELD_CONSTRAINTS` from OpenAPI spec |
| `python tools/generate_examples.py` | (Re)generate per-state example files from DOCUMENTATION |
| `python tools/inject_examples.py` | Inject examples into module `EXAMPLES` strings |
| `python tools/inject_examples.py --check` | Verify all modules are in sync (pre-commit hook) |
| `python tools/restructure_molecule.py` | (Re)generate per-state Molecule scenarios from examples |
| `python tools/generate_check_scenarios.py` | (Re)generate check-mode Molecule scenarios for all modules |

---

## Related Documents

- [06-foundation-components.md](06-foundation-components.md) — Core components being tested
- [07-adding-resources.md](07-adding-resources.md) — Step 7 references this testing workflow
- [08-code-generators.md](08-code-generators.md) — Generated code that unit tests validate
- [09-agent-collaboration.md](09-agent-collaboration.md) — Agent testing workflow (Phase C)
- [10-case-study-novacom.md](10-case-study-novacom.md) — Module map drives the scenario list

*Document version: 1.7 | OpenAPI Resource Module SDK | Testing Strategy*
