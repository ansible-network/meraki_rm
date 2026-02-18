# Overview

## The Problem

Vendor APIs expose hundreds of endpoints. The naive approach to building an Ansible collection from an OpenAPI spec is to generate one module per endpoint. This produces collections with 500+ modules where configuring a single logical entity -- a VLAN, an SSID, a firewall policy -- requires chaining multiple tasks across multiple modules in the correct order.

The result is an API client with YAML syntax, not infrastructure automation.

Users are forced to understand the vendor's API path structure, call ordering, payload quirks, and camelCase naming conventions. Idempotency is the caller's problem. Compliance enforcement is impossible because the modules have no concept of "only these VLANs should exist."

This is not a vendor-specific problem. It happens with every large OpenAPI spec: NovaCom, Cisco, Palo Alto, Juniper, AWS, any vendor whose API surface exceeds a few dozen endpoints. The endpoint explosion is a design failure, not a scale inevitability.

## The Vision

We are building an **SDK** that expresses entity-centric, state-driven resource management. The SDK manages **configuration entities** -- VLANs, SSIDs, firewall rules, admin accounts -- not API endpoints. Each entity has full lifecycle management: create, read, update, delete, and converge to desired state.

The SDK is **presentation-layer independent**. Ansible resource modules are one consumer. MCP tools are another. A CLI, a REST gateway, or a Terraform provider could be others. The core logic -- entity modeling, state convergence, API interaction, data transformation -- lives in a shared library that knows nothing about any framework.

The target is clear:

| Metric | Endpoint Collection | Resource Module SDK |
|--------|-------------------|-------------------|
| Module count (NovaCom) | ~500 | 42-50 |
| Tasks to configure an SSID | 3-6 | 1 |
| State management | `present`/`absent` | `merged`/`replaced`/`overridden`/`deleted`/`gathered` |
| Compliance enforcement | Not possible | `state: overridden` |
| API rate limit risk | High (one call per task) | Low (batched, action batches) |
| User must know API structure | Yes | No |
| Idempotency | Caller's problem | Built-in |
| Naming convention | Vendor camelCase | Ansible snake_case |

## Personas

### Ansible Playbook Author

Writes playbooks to automate network configuration. Expects simple, stable interfaces with industry-standard naming. Does not want to learn the vendor's API structure.

**What they care about:**
- Write once, works across API versions
- Clear validation errors at task execution
- Idempotent operations -- safe to re-run
- Compliance enforcement via `state: overridden`
- Round-trip data contract -- output matches input format

**Example:**
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

### Collection Developer

Develops and maintains resource modules. Wants to minimize manual coding and leverage code generation from OpenAPI specs and documentation strings.

**What they care about:**
- New resource module in < 2 hours (vs 2-3 days manually)
- 80% code generation, 20% custom logic (transform mixins)
- Clear patterns and conventions to follow
- Single `DOCUMENTATION` defines input AND output contract
- Manager is generic -- no resource-specific code needed there

### Platform API Developer

Maintains the vendor API and OpenAPI specifications. Needs changes to propagate to the collection automatically.

**What they care about:**
- OpenAPI spec is single source of truth
- Automated compatibility testing
- Clear deprecation path for old endpoints
- Version compatibility matrix auto-generated

### System Administrator

Deploys and operates playbooks at scale. Needs performance, reliability, and clear error messages.

**What they care about:**
- Persistent connections (50-75% faster playbook execution)
- Clear, actionable error messages with resolution suggestions
- Works across platform API versions without playbook changes
- Production-ready error handling

## User Stories

### Playbook Author Stories

**Simple resource management:** Create and manage platform resources using simple, stable action plugins without worrying about API version differences. Single, stable interface regardless of API version. Clear parameter validation with helpful error messages. Idempotent operations.

**Automatic API version detection:** The action plugin automatically detects and adapts to the API version. Playbooks work across different platform versions without modification. Explicit version override available if needed via `api_version` parameter.

**Relationship management:** Manage resource relationships (users in organizations, devices in sites) in a single task. Automatic ID resolution (names to IDs). Multi-step API calls handled transparently.

### Collection Developer Stories

**Generate from docstring:** Define a new resource module by writing an Ansible `DOCUMENTATION` docstring, then run a generator script to produce the dataclass, argument spec, and action plugin skeleton. The docstring is the single source of truth for inputs AND outputs.

**Generate from OpenAPI:** Generate API dataclasses from OpenAPI specifications. Leverage `datamodel-code-generator` for accurate, type-safe models. Version-specific models (v1, v2, etc.).

**Define field mappings:** Define mappings between user-facing and API dataclasses with transformation logic. Simple 1:1 mappings, field name translations, custom transformations (organization names to IDs), nested field mappings with dot notation.

**Multi-endpoint operations:** Define multiple API endpoints for a single resource operation. Primary endpoint plus relationship endpoints. Execution order and dependency management. Path parameter substitution.

**Version support:** Version-specific implementations that inherit from previous versions. Override only what changed. Automatic version discovery from filesystem. Fallback to closest compatible version.

### System Administrator Stories

**Persistent connection:** The collection maintains a persistent connection to the platform. Action plugins communicate with a persistent manager process via multiprocess RPC. Connection reused across all tasks in a playbook.

**Clear errors:** Validation errors show which field failed and why. API errors include HTTP status and response body. Version compatibility warnings are clear. Suggestions for resolution when possible.

**Idempotent operations:** All operations detect whether the resource already exists, compare desired vs existing state, and only make changes when needed. `changed: true` only when something was actually modified.

## Success Metrics

### For Playbook Authors
- Write once, works across API versions
- Clear validation errors at task execution (fail fast)
- 50-75% faster playbook execution (persistent connections)
- Idempotent operations (safe to re-run)
- Round-trip data contract (output matches input format)

### For Collection Developers
- New resource in < 2 hours (vs 2-3 days)
- 80% code generation, 20% custom logic
- API version update in < 1 hour (regenerate + test)
- Single `DOCUMENTATION` defines input AND output contract
- Transform logic isolated in dataclass mixins

### For Platform Team
- OpenAPI spec is single source of truth
- Automated compatibility testing
- Changes propagate automatically to collection
- Version compatibility matrix auto-generated

### For System Administrators
- Reliable, predictable behavior
- Clear error messages with resolution steps
- Fast execution (persistent connections)
- Works across platform versions

## Technical Stack

### Core Technologies
- **Python 3.10+** -- type hints, dataclasses
- **Ansible 2.14+** -- action plugins, ArgumentSpecValidator
- **OpenAPI 3.0+** -- API specifications
- **datamodel-code-generator** -- OpenAPI to Python dataclasses
- **PyYAML** -- docstring parsing
- **multiprocessing** -- persistent manager connections

### Generated Code
- **User Model dataclasses** -- from `DOCUMENTATION` strings
- **Device Model dataclasses** -- from OpenAPI specs
- **Action plugin skeletons** -- basic structure
- **ArgumentSpec** -- from `DOCUMENTATION` strings

### Manual Code
- **Transform Mixins** -- field mappings, business logic (the developer's value-add)
- **BaseTransformMixin** -- universal transformation logic
- **PlatformManager** -- persistent connection management
- **Convergence Engine** -- state comparison and operation planning

## Roadmap

### Phase 1: Foundation
Build core SDK components. See [06-foundation-components.md](06-foundation-components.md).

### Phase 2: Code Generation
Set up automated dataclass generation from docstrings and OpenAPI specs. See [08-code-generators.md](08-code-generators.md).

### Phase 3: First Resources
Implement high-value resource modules (VLAN, SSID, switch ports, admin users). See [07-adding-resources.md](07-adding-resources.md) and [10-case-study-novacom.md](10-case-study-novacom.md).

### Phase 4: Broad Coverage
Remaining resource modules, agent-assisted development.

### Phase 5: Advanced Features
- Check mode / diff mode support
- Bulk operations
- Action Batch integration for atomic transactions
- Inventory plugin for device discovery
- Change tracking and performance metrics

### Phase 6: Additional Presentation Layers
- MCP server (see [03-sdk-architecture.md](03-sdk-architecture.md))
- CLI tool
- Documentation generator

## Document Guide

This documentation suite is structured for different audiences reading at different depths.

### For Product Managers / Architects
Start here, then read:
- [02-resource-module-pattern.md](02-resource-module-pattern.md) -- what resource modules are and why they matter
- [03-sdk-architecture.md](03-sdk-architecture.md) -- presentation-layer independence, MCP tool parity
- [10-case-study-novacom.md](10-case-study-novacom.md) -- concrete before/after with NovaCom

### For Architects / Senior Developers
All of the above, plus:
- [04-data-model-transformation.md](04-data-model-transformation.md) -- the three-tier data flow pattern
- [05-design-principles.md](05-design-principles.md) -- guardrails, validation strategy, quality gates

### For Developers Building the Framework
All of the above, plus:
- [06-foundation-components.md](06-foundation-components.md) -- full implementation spec for all core components
- [08-code-generators.md](08-code-generators.md) -- code generation tooling

### For Developers Adding Resources
- [07-adding-resources.md](07-adding-resources.md) -- step-by-step workflow with complete examples
- [05-design-principles.md](05-design-principles.md) -- rules to follow
- [10-case-study-novacom.md](10-case-study-novacom.md) -- the module map for NovaCom

### For AI Agents
- [09-agent-collaboration.md](09-agent-collaboration.md) -- personas, phases, quality gates, coding standards

### For Testing
- [11-testing-strategy.md](11-testing-strategy.md) -- mock server, Molecule integration, three-layer validation, adding tests for new modules

### Document Dependency Map

```
01-overview (you are here)
  |
  +-- 02-resource-module-pattern (what)
  |     |
  |     +-- 03-sdk-architecture (how it's packaged)
  |           |
  |           +-- 04-data-model-transformation (the transformation pattern)
  |           |
  |           +-- 05-design-principles (the rules)
  |
  +-- 06-foundation-components (build the framework)
  |     |
  |     +-- 07-adding-resources (use the framework)
  |     |
  |     +-- 08-code-generators (automate the repetitive parts)
  |
  +-- 09-agent-collaboration (AI agent guidance)
  |
  +-- 10-case-study-novacom (concrete application)
  |
  +-- 11-testing-strategy (how to test everything)
```

### Time Estimates

| Task | Who | First Time | Subsequent |
|------|-----|-----------|------------|
| Build foundation | Framework team | 8-12 hours | N/A |
| Set up generators | Framework team | 2-3 hours | N/A |
| Add simple resource | Feature developer | 1-2 hours | 1-2 hours |
| Add complex resource | Feature developer | 3-4 hours | 2-3 hours |
| Add API version | Framework team | 1-2 hours | 1-2 hours |

**Total to working system:** ~15 hours initial investment, then 1-4 hours per resource.
