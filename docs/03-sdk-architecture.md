# SDK Architecture

This document explains the SDK architecture: presentation-layer independence, how resource modules and MCP tools are the same thing, the library structure, and the SDK API boundary. NovaCom Networks serves as the fictitious example throughout: a cloud-managed network infrastructure provider (wireless APs, switches, appliances, cameras) with the NovaCom Dashboard API.

---

## Section 1: The Core Insight

A resource module and a well-scoped MCP tool are **the same thing**.

Both manage an entity. Both accept a declarative description of desired state. Both compare desired against actual, compute a minimal diff, execute necessary operations, and return structured results. The only difference is the wire format at the edges — YAML/argspec vs JSON/JSON Schema.

The valuable work — entity modeling, state convergence, API interaction, data transformation — does not belong to Ansible. It belongs to a **library**. An MCP server is another caller. We are building an SDK. Ansible is one presentation layer. MCP is another.

### What This Means in Practice

- **Entity modeling** — defining what a VLAN, SSID, or switch port *is* — is library work. The library knows the fields, constraints, and lifecycle.
- **State convergence** — gather current state, diff against desired, compute minimal operations, execute, report — is library work. The library owns the convergence loop.
- **API interaction** — HTTP calls, authentication, rate limiting, Action Batch support — is library work. The library talks to the NovaCom Dashboard API.
- **Data transformation** — user-facing snake_case ↔ API camelCase, organization names ↔ IDs — is library work. The library performs forward and reverse transforms.

None of this logic imports Ansible. None of it knows about MCP. It operates on Python data classes and dicts. An Ansible action plugin and an MCP tool handler both call the same `sdk.execute()` with the same parameters. The framing is different; the contract is identical.

---

## Section 2: The Parallel (Side-by-Side Comparison)

The following table compares Ansible Resource Module and MCP Tool across every dimension. The convergence contract is the same; only the wire format differs.

| Concern | Ansible Resource Module | MCP Tool |
|---------|-------------------------|----------|
| **Input schema** | `DOCUMENTATION` argspec (YAML docstring defining options, types, required, choices) | Tool `inputSchema` (JSON Schema defining properties, types, required, enum) |
| **Input data** | Task `args` dict (e.g., `config: [{vlan_id: 100, name: Engineering}]`, `state: merged`) | Tool `arguments` dict (e.g., `config: [{"vlan_id": 100, "name": "Engineering"}]`, `action: "merge"`) |
| **Caller** | Ansible playbook engine (executes tasks, passes vars) | LLM or MCP client (invokes tools, passes arguments from user/agent intent) |
| **Validation** | `ArgumentSpecValidator` (Ansible's built-in validator against argspec) | JSON Schema validation (standard validation against inputSchema) |
| **Entity identification** | Module name (e.g., `novacom.dashboard.novacom_appliance_vlan`) | Tool name (e.g., `novacom_appliance_vlan`) |
| **State declaration** | `state: merged` parameter (merged, replaced, overridden, deleted, gathered) | `action: merge` parameter (merge, replace, override, delete, gather) or equivalent |
| **Desired config** | `config:` block (list of dicts, user-model format) | Equivalent JSON structure (list of objects, same user-model format) |
| **Execution** | Action plugin calls library (`sdk.execute("vlan", "merge", desired, context)`) | Tool handler calls library (same `sdk.execute()` call) |
| **Output schema** | Same as input (round-trip contract; DOCUMENTATION defines both) | Structured `content` response (same fields as input; round-trip contract) |
| **Output** | `changed`, `diff`, `before`, `after`, `gathered`, `operations` | Same: `changed`, `diff`, `before`, `after`, `gathered`, `operations` |
| **Idempotency** | Module's responsibility (diff desired vs actual, skip if no change) | Tool's responsibility (same logic; tool must not call API blindly) |
| **Description** | `DOCUMENTATION` string (module purpose, options, examples) | Tool `description` field (tool purpose, parameters, usage) |

### The Convergence Contract Is Identical

Both a resource module and a well-scoped MCP tool execute the same loop:

```
1. Accept desired state declaration (user-model format)
2. Gather current state from device (via API)
3. Diff desired vs. current (structural diff)
4. Compute minimal operations (create, update, delete)
5. Execute (or dry-run)
6. Return structured result: changed, before, after, diff, operations
```

If an MCP tool does not do this, it is not well-scoped — it is an HTTP proxy. The same holds for Ansible: a module that wraps an endpoint instead of managing an entity is just an API client with YAML syntax.

### The Anti-Pattern Is the Same in Both Worlds

The endpoint-wrapping anti-pattern produces bad MCP tools for exactly the same reason it produces bad Ansible modules:

- **500 thin wrappers** instead of **45 entity tools** — one tool per API endpoint vs one tool per logical entity
- **LLM calling `novacom_put_networks_ssids_l3_firewall_rules`** has the same problems as a playbook author chaining `novacom.dashboard.networks_wireless_ssids_firewall_l3_rules`
- Both are forced to understand the API path structure, call ordering, and payload format
- Both lack convergence — no diff, no idempotency, no "only change what differs"
- Both push complexity to the caller instead of absorbing it in the tool/module

A well-scoped tool says: "Tell me what you want the SSID to look like. I'll handle the rest." A well-scoped resource module says the same thing. The library implements it once.

---

## Section 3: The SDK / Library Structure

The library is the product. It is presentation-layer agnostic. The following directory structure shows how responsibilities are organized.

```
library/
├── entities/                    # Entity definitions
│   ├── base.py                  # BaseEntity: lifecycle, convergence contract
│   ├── vlan.py                  # VLAN entity
│   ├── ssid.py                  # SSID entity
│   ├── switch_port.py           # Switch port entity
│   └── ...
├── models/                      # Data classes
│   ├── user_model.py            # User-facing model (flat, normalized names)
│   ├── device_model.py          # Device-facing model (matches API schema)
│   └── ...
├── transforms/                  # Data class transformation
│   ├── base_transform.py        # BaseTransformMixin
│   └── mixins/                  # Per-entity transform mixins
│       ├── vlan.py
│       ├── ssid.py
│       └── ...
├── convergence/                 # State engine
│   ├── engine.py                # Gather → Diff → Plan → Execute → Report
│   ├── diff.py                  # Structural diff
│   └── planner.py               # Operation planning
├── api/                         # API client layer
│   ├── client.py                # NovaCom Dashboard API client
│   ├── auth.py                  # Authentication
│   ├── batch.py                 # Action Batch support
│   └── rate_limit.py            # Rate limiting / retry
└── schema/                      # Schema definitions (shared source of truth)
    ├── vlan.py                  # VLAN schema
    ├── ssid.py                  # SSID schema
    └── ...
```

### What the Library Owns

| Responsibility | Location | Description |
|----------------|----------|-------------|
| **Entity definition** | `entities/` + `schema/` | What is a VLAN, SSID, switch port; what fields, constraints, lifecycle |
| **User-facing model** | `models/user_model.py` | Flat, snake_case, normalized names; what the user writes and reads |
| **Device-facing model** | `models/device_model.py` | Matches NovaCom API schema; camelCase, nested structure |
| **Transform** | `transforms/` | User model ↔ device model; forward and reverse; name-to-ID lookups |
| **Convergence** | `convergence/` | Gather, diff, plan, execute, report; the state engine |
| **API interaction** | `api/` | HTTP calls, auth, Action Batch, rate limiting, retry |
| **Schema** | `schema/` | Single source of truth for entity structure; drives argspec, JSON Schema, transforms |

### What the Library Does NOT Own

| Responsibility | Belongs To | Description |
|----------------|------------|-------------|
| YAML parsing | Ansible presentation layer | Parsing playbook task structure |
| Ansible argspec construction | Ansible presentation layer | Building ArgumentSpec from schema |
| Ansible return dict formatting | Ansible presentation layer | Formatting `changed`, `diff`, etc. for Ansible |
| MCP protocol handling | MCP presentation layer | Tool registration, JSON-RPC, stdio/SSE transport |
| JSON Schema emission | MCP presentation layer | Projecting schema to MCP tool inputSchema |
| CLI argument parsing | CLI presentation layer | Click, argparse, or similar |
| Any framework-specific plumbing | Respective presentation layers | Each layer handles its own conventions |

The library exposes a clean API. It does not import `ansible`, `mcp`, or `click`. It receives dicts and returns dicts (or dataclasses that serialize to dicts).

---

## Section 4: Presentation Layers

Each presentation layer is a **thin adapter** that translates between its framework's conventions and the library's API. The real logic lives in the library; the adapter is ~10 lines of real logic.

### Presentation Layer: Ansible

**Directory structure:**

```
ansible_collections/novacom/dashboard/
├── plugins/
│   ├── modules/
│   │   ├── novacom_appliance_vlan.py       # Module doc + argspec stub
│   │   ├── novacom_wireless_ssid.py
│   │   └── ...
│   ├── action/
│   │   ├── novacom_appliance_vlan.py       # Action plugin (thin)
│   │   ├── novacom_wireless_ssid.py
│   │   └── ...
│   └── module_utils/
│       └── sdk_bridge.py                   # Glue: Ansible args → library → Ansible return
```

**Action plugin code (~10 lines of real logic):**

```python
def run(self, tmp=None, task_vars=None):
    # 1. Translate Ansible args to library input
    entity_name = "vlan"
    desired = self._task.args.get("config", [])
    action = self._task.args.get("state", "merged")
    context = {
        "network_id": self._task.args["network_id"],
        "api_key": task_vars.get("novacom_api_key"),
    }

    # 2. Call sdk.execute() — the only real line
    result = sdk.execute(entity_name, action, desired, context)

    # 3. Translate library result to Ansible return dict
    return {
        "changed": result.changed,
        "diff": {"before": result.before, "after": result.after},
        "gathered": result.gathered,
    }
```

The action plugin validates input (via ArgumentSpec), creates the context, calls the library, and formats the return. All entity logic, convergence, and API interaction happen in the library.

### Presentation Layer: MCP Server

**Directory structure:**

```
mcp_server/
├── server.py                    # MCP server setup, tool registration
├── tools/
│   ├── novacom_appliance_vlan.py    # Tool definition (thin)
│   ├── novacom_wireless_ssid.py
│   └── ...
└── schema_bridge.py             # Glue: library schema → JSON Schema for MCP
```

**Tool handler code (~10 lines of real logic):**

```python
@server.tool()
async def novacom_appliance_vlan(
    network_id: str,
    config: list[dict] | None = None,
    action: str = "merge",    # merge, replace, override, delete, gather
) -> dict:
    """Manage NovaCom network appliance VLANs.

    Supports declarative state management: merge new config,
    replace specific VLANs, override all VLANs, delete, or
    gather current state. Uses NovaCom Dashboard API.
    """
    context = {"network_id": network_id, "api_key": get_api_key()}

    # Same library call
    result = sdk.execute("vlan", action, config or [], context)

    return {
        "changed": result.changed,
        "before": result.before,
        "after": result.after,
        "diff": result.diff,
    }
```

Same library call. Different wire format. The MCP server registers the tool with a description and inputSchema (derived from the library schema). The tool handler receives JSON arguments, builds context, calls `sdk.execute()`, and returns a structured response.

### Presentation Layer: CLI (Hypothetical)

**Click command code:**

```python
@click.command()
@click.argument("entity")
@click.option("--action", default="merge", type=click.Choice(["merge", "replace", "override", "delete", "gather"]))
@click.option("--config", type=click.Path(exists=True))
@click.option("--network-id", required=True)
def configure(entity, action, config, network_id):
    desired = yaml.safe_load(open(config)) if config else []
    context = {"network_id": network_id, "api_key": os.environ.get("NOVACOM_API_KEY")}
    result = sdk.execute(entity, action, desired, context)
    click.echo(f"Changed: {result.changed}")
    if result.diff:
        click.echo(json.dumps(result.diff, indent=2))
```

Different front door. Same library. The CLI parses arguments, loads config from a file, builds context from env vars, and calls `sdk.execute()`.

---

## Section 5: Schema as Single Source of Truth

Schema definitions in the library are the authoritative source for entity structure. Every presentation layer derives its input/output format from the same schema.

### Generation Flow

```
schema/vlan.py (library)
    │
    ├──→ Ansible DOCUMENTATION argspec (generated)
    ├──→ MCP tool inputSchema JSON Schema (generated)
    ├──→ CLI help text (generated)
    └──→ API documentation (generated)
```

One definition. Many projections.

### Example: EntitySchema Definition (NovaCom VLAN)

```python
VLAN_SCHEMA = EntitySchema(
    name="vlan",
    description="Manage NovaCom network appliance VLANs",
    identifier=["vlan_id"],
    fields=[
        Field("vlan_id", type=int, required=True,
              description="VLAN identifier (1-4094)"),
        Field("name", type=str,
              description="VLAN name"),
        Field("subnet", type=str,
              description="Subnet in CIDR notation"),
        Field("appliance_ip", type=str,
              description="Appliance IP address on this VLAN"),
        Field("dhcp_handling", type=str,
              choices=["run_server", "relay", "none"],
              description="DHCP handling mode"),
        Field("dhcp_relay_servers", type=list, element_type=str,
              description="DHCP relay server IPs (when dhcp_handling is relay)"),
        Field("dns_nameservers", type=list, element_type=str,
              description="DNS nameservers for this VLAN"),
        Field("reserved_ip_ranges", type=list, element_type=str,
              description="Reserved IP ranges (e.g., 10.100.0.1-10.100.0.50)"),
        Field("id", type=str, read_only=True,
              description="Internal VLAN ID (read-only, returned after creation)"),
    ],
    read_only=["id"],
    states=["merged", "replaced", "overridden", "deleted", "gathered"],
)
```

### What This Single Definition Enables

| Consumer | Use |
|----------|-----|
| **Ansible** | Generates `DOCUMENTATION` string and argspec; options, types, required, choices |
| **MCP** | Generates tool `description` and `inputSchema` JSON Schema |
| **Transforms** | Know which fields to map between user and device models; which fields need name-to-ID lookup |
| **Convergence** | Knows `vlan_id` is the identifier; which fields to diff; which are read-only |
| **Tests** | Know what valid and invalid inputs look like; fixtures for unit and integration tests |

One truth. Many projections. Adding a new field to the schema propagates to all presentation layers. Changing a type or constraint propagates everywhere.

---

## Section 6: How States Map Across Presentation Layers

State semantics are entity-level concepts. They belong to the library, not to any presentation layer. Each layer exposes them in its own idiom.

| Library Action | Ansible `state:` | MCP Tool Pattern | Semantics |
|----------------|------------------|------------------|-----------|
| `merge` | `merged` | `action: "merge"` or default | Additive. Create if missing; update only specified fields. Leave rest untouched. |
| `replace` | `replaced` | `action: "replace"` | Replace listed instances entirely. Omitted fields revert to defaults. |
| `override` | `overridden` | `action: "override"` | Nuclear. Only what you list should exist. Unlisted instances deleted. |
| `delete` | `deleted` | `action: "delete"` | Remove specified instances, or all if config empty/omitted. |
| `gather` | `gathered` | `action: "gather"` or separate read tool | Read-only. Return current state in user-model format. |

### MCP Tool Decomposition (Presentation-Layer Concern)

An MCP server could split into separate tools if that improves LLM tool selection:

| Tool | Maps To | Use Case |
|------|---------|----------|
| `novacom_vlan_configure` | `merge` / `replace` / `override` (with action param) | Configure VLANs |
| `novacom_vlan_delete` | `delete` | Remove VLANs |
| `novacom_vlan_get` | `gather` | Read current VLAN config |

Tool decomposition is a presentation-layer concern. The library receives an action, desired state, and context; it does not care whether the caller used one tool with an action parameter or three separate tools.

---

## Section 7: Manager-Side Transformation Architecture

All data transformations happen in the **persistent manager process**, not in the client action plugins. This follows the multiprocess manager pattern.

### Core Principle

- **Manager** performs forward transform (User Model → Device Model)
- **Manager** performs reverse transform (Device Model → User Model)
- **Client** never sees API format
- Only **user-model dataclasses** cross the RPC boundary

### Client Responsibilities (Thin)

| Step | Responsibility |
|------|----------------|
| 1 | Validate input (ArgumentSpec from DOCUMENTATION) |
| 2 | Create user-model dataclass |
| 3 | Send to manager via RPC |
| 4 | Receive user-model dataclass back |
| 5 | Validate output (same ArgumentSpec) |
| 6 | Format return dict for Ansible |

The client does **not** perform transformations. It does **not** know API field names or structure. It does **not** resolve names to IDs. It validates, serializes, sends, receives, validates again, and formats.

### Manager Responsibilities (Heavy)

| Step | Responsibility |
|------|----------------|
| 1 | Maintain persistent platform connection |
| 2 | Detect and cache API version |
| 3 | Load version-specific classes |
| 4 | Perform forward transform (User Model → Device Model) |
| 5 | Execute API calls (multi-endpoint support) |
| 6 | Perform reverse transform (Device Model → User Model) |
| 7 | Provide lookup helpers (names ↔ IDs) |
| 8 | Return user-model dataclass (not API response) |

The manager owns all API knowledge. It has the session, cache, and context needed for lookups. It transforms both ways so the client only ever sees user-model format.

### Round-Trip Data Contract

Output data uses the **same format and fields** as input data (defined in DOCUMENTATION). No separate RETURN section needed.

| Direction | Example |
|-----------|---------|
| **Input** | `organizations=['Engineering']` (names) |
| **Output** | `organizations=['Engineering']` (names, not IDs) |
| **API format** | `organization_ids=[1]` (internal to manager, never crosses RPC) |

The user provides names. The user receives names. The API uses IDs internally. The manager performs the lookups and reverse lookups; the client never sees IDs.

### Data Flow Diagram

```
ACTION PLUGIN (Client)               MANAGER (Server)
1. Validate input (ArgumentSpec)
2. Create UserModel dataclass
   organizations=['Engineering'] ->   3. Receive UserModel
                                      4. TRANSFORM: User -> Device
                                         organizations=['Engineering']
                                         -> (lookup names -> IDs)
                                         organization_ids=[1]
                                      5. Call Platform API
                                      6. Receive API response
                                      7. TRANSFORM: Device -> User
                                         organization_ids=[1]
                                         -> (lookup IDs -> names)
                                         organizations=['Engineering']
8. Receive UserModel result      <-   9. Return UserModel dataclass
9. Validate output (ArgumentSpec)
10. Format for Ansible return
```

The RPC boundary carries only user-model data. API format (`organization_ids`, camelCase, nested structure) stays inside the manager.

---

## Section 8: SDK API Boundary

The library exposes a clean, minimal surface. Every presentation layer calls `sdk.execute()` and projects `Result` into its own format.

### SDK Class

```python
class SDK:
    def execute(
        self,
        entity: str,           # "vlan", "ssid", "switch_port"
        action: str,           # "merge", "replace", "override", "delete", "gather"
        desired: list[dict],   # Desired state (user-model format)
        context: dict,         # Connection info, credentials, scope
    ) -> Result:
        """Execute a state action on an entity."""

    def get_schema(self, entity: str) -> EntitySchema:
        """Return the schema for an entity (for presentation layers to project)."""

    def list_entities(self) -> list[str]:
        """List available entity types."""


@dataclass
class Result:
    changed: bool
    before: list[dict]     # State before execution (user-model format)
    after: list[dict]      # State after execution (user-model format)
    diff: list[dict]       # Per-instance diffs
    gathered: list[dict]   # Current state (for gather action)
    operations: list[str]  # What was done (for logging/audit)
```

### Context Structure (NovaCom Example)

```python
context = {
    "network_id": "N_12345",
    "api_key": "...",
    "base_url": "https://api.novacom.io/v1/",
    # Optional: organization_id, site_id, device_serial for scoped entities
}
```

### Usage

The library is the product. The presentation layers are distribution channels. Ansible, MCP, CLI, and any future consumer all call the same `execute()` method. The library does not know or care who called it.

---

## Section 10: Meraki RM Implementation

The `cisco.meraki_rm` Ansible collection implements this architecture. The SDK lives inside `plugins/plugin_utils/` and is dual-packaged: it ships as part of the Ansible collection tarball *and* as a standalone Python package (`meraki-rm-sdk`) for non-Ansible consumers like the MCP server.

### Directory Layout

```
plugins/plugin_utils/               # SDK root
├── platform/
│   ├── base_transform.py           # BaseTransformMixin + resource metadata defaults
│   ├── types.py                    # EndpointOperation
│   ├── registry.py                 # APIVersionRegistry
│   └── loader.py                   # DynamicClassLoader
├── manager/
│   ├── platform_manager.py         # PlatformService + PlatformManager
│   └── rpc_client.py               # ManagerRPCClient
├── user_models/                    # 48 User Model dataclasses
│   ├── vlan.py                     # UserVlan (Category A)
│   ├── admin.py                    # UserAdmin (Category B)
│   ├── qos_rule.py                 # UserQosRule (Category C)
│   └── ...
├── mcp/                            # MCP server subpackage
│   ├── schema.py                   # dataclass → JSON Schema conversion
│   ├── introspect.py               # User Model discovery + tool definition generation
│   └── server.py                   # MCP server (task and live modes)
├── cli/                            # CLI subpackage
│   └── main.py                     # Dynamic argparse from User Model introspection
├── mock.py                         # Shared mock server lifecycle utilities
└── pyproject.toml                  # Standalone Python packaging (meraki-rm-sdk)
```

### User Models as Single Source of Truth

Each User Model dataclass carries both field definitions *and* resource metadata:

```python
@dataclass
class UserVlan(BaseTransformMixin):
    MODULE_NAME = 'vlan'
    CANONICAL_KEY = 'vlan_id'
    # SCOPE_PARAM, SYSTEM_KEY, SUPPORTS_DELETE, VALID_STATES
    # inherit defaults from BaseTransformMixin

    vlan_id: Optional[str] = field(
        default=None, metadata={"description": "VLAN ID (1-4094)."}
    )
    name: Optional[str] = field(
        default=None, metadata={"description": "VLAN name."}
    )
    # ...
```

This single class drives:

| Consumer | What It Reads |
|----------|---------------|
| **Ansible action plugin** | `MODULE_NAME`, `SCOPE_PARAM`, `CANONICAL_KEY`, `SYSTEM_KEY`, `VALID_STATES`, field types |
| **MCP server** | Same metadata + `field.metadata["description"]` for tool schemas |
| **CLI** | Same metadata + field types for argparse flag generation |
| **Code generators** | Field names, types, descriptions for docs and test scaffolding |

### Dual Packaging

The `pyproject.toml` in `plugins/plugin_utils/` defines the standalone SDK:

```toml
[project]
name = "meraki-rm-sdk"
version = "0.1.0"
dependencies = ["requests"]

[project.optional-dependencies]
mcp = ["mcp", "pyyaml"]
cli = ["pyyaml", "requests"]

[project.scripts]
meraki-mcp-server = "meraki_rm_sdk.mcp.server:main"
meraki-cli = "meraki_rm_sdk.cli.main:main"
```

Install modes:

| Mode | Command | Use Case |
|------|---------|----------|
| **Ansible collection** | `ansible-galaxy collection install cisco.meraki_rm` | Playbook authors |
| **SDK (non-editable)** | `pip install plugins/plugin_utils/` | Introspection tools |
| **SDK + MCP** | `pip install 'plugins/plugin_utils/[mcp]'` | Full MCP server with dependencies |
| **SDK + CLI** | `pip install 'plugins/plugin_utils/[cli]'` | Command-line interface |

The `galaxy.yml` `build_ignore` list excludes `pyproject.toml`, `mcp/`, `cli/`, `mock.py`, and Python packaging artifacts from the Ansible collection tarball.

### MCP Server

The MCP server dynamically generates 48 tools by introspecting User Model dataclasses at startup:

1. `introspect.py` scans `user_models/` via `pkgutil.iter_modules()`
2. For each `User*` dataclass, reads `MODULE_NAME`, `SCOPE_PARAM`, `CANONICAL_KEY`, `VALID_STATES`
3. `schema.py` converts field types and `metadata["description"]` to JSON Schema
4. `server.py` registers tools with the low-level `mcp.server.Server` API

Two modes are supported, plus a `--mock` flag for integration testing:

| Mode | CLI Flag | Behavior |
|------|----------|----------|
| **task** (default) | `--mode=task` | Returns Ansible task YAML snippets. No API key needed. |
| **live** | `--mode=live` | Executes operations against the Meraki Dashboard API. Requires `MERAKI_API_KEY`. |
| **mock** | `--mock` | Auto-starts the stateful mock server and runs in live mode against it. No API key needed. |

### CLI

The `meraki-cli` tool uses the same introspection pipeline as the MCP server to generate argparse subcommands dynamically:

```bash
meraki-cli vlan gathered --network-id L_123
meraki-cli --mock --json switch-port merged --serial Q2XX --port-id 1 --name Uplink
meraki-cli --list
```

Global flags: `--mock` (auto-start mock server), `--json`, `--yaml`, `--list`. Complex fields (Dict, List[Dict]) accept JSON strings or `@file.json` references.

### Action Plugin Simplification

With metadata on the User Model, action plugins are pure configuration:

```python
class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.vlan.UserVlan'
```

The base class loads the User Model, syncs its metadata attributes, and dispatches the operation. No per-module `run()` override needed.

---

## Section 11: Why This Matters

### For NovaCom Specifically

We are not building "Ansible modules for NovaCom." We are building a **NovaCom configuration SDK**. Ansible resource modules are the first consumer. MCP tools are the second. Both are thin.

This means:

1. **Transform mixins, convergence engine, and API client are reusable.** They do not import Ansible or know about MCP. They operate on Python data classes and dicts. Adding an MCP server does not require duplicating any of this logic.

2. **Adding a new presentation layer is trivial.** A Terraform provider, REST gateway, or Slack bot that manages VLANs would write a thin adapter and call the library. The adapter is ~10 lines of real logic per entity.

3. **Testing is cleaner.** The library is tested independently of any framework. Unit tests pass dicts in and check dicts out. No Ansible test harness needed for the core logic. No MCP server needed to test convergence.

4. **Agent/LLM interaction improves.** An LLM calling MCP tools backed by this SDK gets the same convergence guarantees as an Ansible playbook. It declares what it wants. The tool handles idempotency, diff computation, and API orchestration. The LLM does not need to understand NovaCom's API structure any more than a playbook author does.

### For the Anti-Pattern

The endpoint-wrapping anti-pattern produces bad MCP tools for exactly the same reason it produces bad Ansible modules. An LLM calling `novacom_put_networks_ssids_l3_firewall_rules` has the same problems as a playbook author chaining six endpoint-wrapper modules:

- Must know the API path structure
- Must know call ordering (basic settings before firewall, etc.)
- Must know payload format (camelCase, nested structure)
- No convergence — calls API whether or not anything changed
- No idempotency — caller's problem
- No compliance enforcement — cannot say "only these rules should exist"

A well-scoped tool says: "Tell me what you want the SSID to look like. I'll handle the rest." The library implements that. Both Ansible and MCP benefit.

### Summary

| Aspect | Endpoint Model | SDK Model |
|--------|----------------|-----------|
| **NovaCom module/tool count** | ~500 | 42-50 |
| **Tasks/tools to configure SSID** | 3-6 | 1 |
| **Convergence** | None | Built-in |
| **Idempotency** | Caller's problem | Library's responsibility |
| **Compliance enforcement** | Not possible | `state: overridden` / `action: override` |
| **Presentation layers** | Tied to one (Ansible) | Ansible, MCP, CLI, future |
| **Testing** | Framework-dependent | Library tested independently |

The SDK architecture turns infrastructure automation from framework-specific modules into a reusable product. NovaCom resource modules and NovaCom MCP tools are two views of the same underlying capability.
