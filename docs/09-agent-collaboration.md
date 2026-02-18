# Agent Collaboration Guide — AI Agents Working with Developers on NovaCom Dashboard

This document guides AI agents working with developers on the **NovaCom Dashboard** collection (namespace: `novacom.dashboard`). It defines personas, workflows, quality gates, and coding standards so agents can collaborate effectively without reinventing patterns or skipping critical steps.

**Audience**: AI agents (LLMs, coding assistants) assisting developers

**Related Documents**:
- [01-overview.md](01-overview.md) — Architecture context
- [06-foundation-components.md](06-foundation-components.md) — Foundation implementation spec
- [07-adding-resources.md](07-adding-resources.md) — Adding resource modules
- [08-code-generators.md](08-code-generators.md) — Code generation tools
- [05-design-principles.md](05-design-principles.md) — Design rules and quality gates
- [10-case-study-novacom.md](10-case-study-novacom.md) — NovaCom module map and examples

---

## SECTION 1: Purpose and Quick Start

### Purpose

When a developer starts working with an AI agent on the NovaCom Dashboard collection, the agent must:

1. **Determine their role** using Role Identification (Section 2)
2. **Load appropriate implementation guide(s)** based on that role
3. **Follow the persona-specific walkthrough** (Foundation Builder or Feature Developer)
4. **Apply coding standards consistently** (Section 8)

### Quick Start Flow

```
Developer engages agent
        │
        ▼
Agent asks: "What are you working on?" (Role Identification)
        │
        ├── A) Building core framework → Foundation Builder persona
        ├── B) Adding a new resource module → Feature Developer persona
        └── C) Something else → Clarifying questions
        │
        ▼
Agent checks: Does the foundation exist?
        │
        ├── NO → Foundation Builder needed first
        └── YES → Feature Developer can proceed
        │
        ▼
Agent loads required docs (Section 10)
        │
        ▼
Agent follows persona walkthrough (Section 3 or 4)
        │
        ▼
Agent applies coding standards (Section 8) and quality checklist (Section 9)
```

### Key Principle

**Do not assume.** Always verify the developer's role and foundation state before proceeding. A Feature Developer cannot add resources without the foundation; a Foundation Builder should not be guided through resource-specific steps.

---

## SECTION 2: Role Identification

### Question 1: What Are You Working On?

Ask the developer:

> **What are you working on?**

| Answer | Persona | Next Step |
|-------|----------|-----------|
| **A)** Building the core framework (BaseTransformMixin, Manager, Registry, Loader) | **Foundation Builder** | Proceed to Section 3 |
| **B)** Adding a new resource module (VLAN, SSID, admin, site, etc.) | **Feature Developer** | Proceed to Section 4 |
| **C)** Something else | — | Ask clarifying questions |

### Clarifying Questions for "Something Else"

- "Are you debugging an existing module?"
- "Are you updating the OpenAPI spec or regenerating models?"
- "Are you writing tests for an existing resource?"
- "Are you working on documentation or CI/CD?"

Tailor guidance based on the answer.

### Question 2: Does the Foundation Exist Yet?

Before proceeding as a Feature Developer, the agent **MUST** check for foundation files. Use the filesystem to verify.

**Check for these files:**

| File | Purpose |
|------|---------|
| `plugins/plugin_utils/platform/base_transform.py` | BaseTransformMixin — universal transformation logic |
| `plugins/plugin_utils/manager/platform_manager.py` | PlatformManager and PlatformService |
| `tools/generators/generate_user_dataclasses.py` | User model dataclass generator |

**Decision logic:**

- **If NO** (any of these missing): Redirect to **Foundation Builder** persona. The developer must build the foundation first.
- **If YES** (all present): **Feature Developer** can proceed.

### Path Conventions

- Collection root: `ansible_collections/novacom/dashboard/` or project-equivalent
- User models: `plugins/plugin_utils/user_models/`
- API models: `plugins/plugin_utils/api/v1/`, `api/v2/`, etc.
- Docs: `plugins/plugin_utils/docs/`

---

## SECTION 3: Persona 1 — Foundation Builder

### When to Use

- Building the framework from scratch
- Core components (BaseTransformMixin, Manager, Registry, Loader) do not exist yet
- Setting up code generation tools

### Required Context

**Load these documents:**

1. [01-overview.md](01-overview.md) — Architecture context, vision, component overview
2. [06-foundation-components.md](06-foundation-components.md) — Full implementation specification
3. [08-code-generators.md](08-code-generators.md) — Code generation tools

### Q&A Walkthrough: Phases 1–5

---

#### Phase 1: Understanding Architecture

**Agent asks:** "Have you reviewed the architecture? Let me summarize..."

**Agent shows:** The 6 main components and recommended build order:

| Order | Component | Purpose |
|-------|-----------|---------|
| 1 | Shared types (`EndpointOperation`) | `plugins/plugin_utils/platform/types.py` — API endpoint configuration |
| 2 | BaseTransformMixin | `plugins/plugin_utils/platform/base_transform.py` — Bidirectional User ↔ Device transformation |
| 3 | APIVersionRegistry | `plugins/plugin_utils/platform/registry.py` — Dynamic version/module discovery |
| 4 | DynamicClassLoader | `plugins/plugin_utils/platform/loader.py` — Load version-specific classes at runtime |
| 5 | PlatformManager | `plugins/plugin_utils/manager/platform_manager.py` — PlatformService + multiprocess manager |
| 6 | ManagerRPCClient | `plugins/plugin_utils/manager/rpc_client.py` — Client-side manager communication |
| 7 | Base Action Plugin pattern | `plugins/action/base_action.py` — Manager spawning, validation, common logic |

**Agent explains:** The flow: Playbook task → Action plugin → Manager (or spawn) → Transform (User→Device) → API call → Transform (Device→User) → Return.

**Agent asks:** "Does this order make sense? Ready to start with shared types?"

---

#### Phase 2: Building Core Components

For **each** component:

1. **Agent describes** purpose, features, and file location
2. **Agent asks** for confirmation before implementing
3. **Agent implements** from 06-foundation-components.md spec
4. **Agent shows** key parts (signatures, critical logic)
5. **Agent asks:** "Proceed to next component? Add tests? Refine?"

**Example for BaseTransformMixin:**

> "BaseTransformMixin lives in `plugins/plugin_utils/platform/base_transform.py`. It provides:
> - `to_api(context)` — User Model → Device Model
> - `to_ansible(context)` — Device Model → User Model
> - `_apply_forward_mapping` / `_apply_reverse_mapping` — field mapping logic
> - Dot notation for nested fields
> - Pluggable transform registry for custom logic (e.g., names↔IDs)
>
> Subclasses define `_field_mapping` and `_transform_registry`. Shall I implement it from the spec?"

**Repeat for:** types.py, registry.py, loader.py, platform_manager.py (PlatformService + PlatformManager), rpc_client.py, base_action.py.

---

#### Phase 3: Code Generators

**Agent asks:** "Do you want to implement both generators? (1) User model from DOCUMENTATION, (2) API models from OpenAPI spec."

**Agent implements** from 08-code-generators.md:

1. **`generate_user_dataclasses.py`** — Parses DOCUMENTATION YAML, generates `User*` dataclasses in `plugins/plugin_utils/user_models/`
2. **`generate_api_models.sh`** — Wraps `datamodel-code-generator` for OpenAPI → `api/v1/generated/models.py`

**Agent tests** with a sample resource (e.g., site or vlan):

```bash
# Create a minimal docs file, then:
python tools/generators/generate_user_dataclasses.py plugins/plugin_utils/docs/site.py
# Verify output in plugins/plugin_utils/user_models/site.py
```

**Agent asks:** "Generators work? Proceed to foundation testing?"

---

#### Phase 4: Foundation Testing

**Agent creates** a test script (e.g., `tools/test_manager.py`) that:

1. Instantiates PlatformService
2. Registers with PlatformManager
3. Starts manager
4. Verifies API version detection and registry discovery

**Agent runs** and verifies output:

```
Creating PlatformService...
Starting manager at /tmp/novacom_test_manager.sock
Manager started successfully
API Version: 1
Supported versions: ['1']
```

**Agent asks:** "Test passes? Foundation complete?"

---

#### Phase 5: Foundation Complete

**Agent summarizes** what was built:

| Component | Location | Status |
|-----------|----------|--------|
| EndpointOperation | `platform/types.py` | ✓ |
| BaseTransformMixin | `platform/base_transform.py` | ✓ |
| APIVersionRegistry | `platform/registry.py` | ✓ |
| DynamicClassLoader | `platform/loader.py` | ✓ |
| PlatformService | `manager/platform_manager.py` | ✓ |
| PlatformManager | `manager/platform_manager.py` | ✓ |
| ManagerRPCClient | `manager/rpc_client.py` | ✓ |
| BaseResourceActionPlugin | `action/base_action.py` | ✓ |
| generate_user_dataclasses.py | `tools/generators/` | ✓ |
| generate_api_models.sh | `tools/generators/` | ✓ |

**Agent states next steps:**

- "Test with a real resource (e.g., `novacom_appliance_vlan`) as a Feature Developer"
- "Add resources using the Feature Developer workflow (07-adding-resources.md)"

---

## SECTION 4: Persona 2 — Feature Developer

### Prerequisites Check

**Before proceeding**, the agent MUST verify foundation files exist (Section 2). If any are missing, redirect to Foundation Builder.

### Required Context

**Load these documents:**

1. [07-adding-resources.md](07-adding-resources.md) — Main step-by-step guide
2. [05-design-principles.md](05-design-principles.md) — Rules, guardrails, quality gates
3. [10-case-study-novacom.md](10-case-study-novacom.md) — NovaCom module map, examples, complexity analysis

### Q&A Walkthrough: Phases 1–7

---

#### Phase 1: Resource Planning

**Agent asks:** "What resource are you adding? (e.g., VLAN, SSID, admin, site)"

**Agent asks about complexity:**

| Question | Purpose |
|----------|---------|
| Simple 1:1 mappings only? (like site) | No name↔ID transforms, single endpoint |
| Name↔ID transformations? (like admin) | Organizations: names in, IDs to API |
| Multiple API endpoints? (like SSID) | 6 sub-endpoints for one logical entity |

**Agent assesses:**

- **Simple** — 1–2 hours total (site, vlan with no lookups)
- **Medium** — 2–3 hours (admin with org name↔ID)
- **Complex** — 3–5 hours (SSID with 6 sub-endpoints)

**Agent provides** a similar example from the case study (e.g., "Admin is similar to your resource — see 10-case-study-novacom.md module map").

---

#### Phase 2: Documentation

**Agent creates** the DOCUMENTATION string in `plugins/plugin_utils/docs/{resource}.py`.

**Key principles (from 05-design-principles.md):**

- **User-friendly names** — snake_case, no vendor camelCase
- **Read-only markers** — `id`, `created_at` returned from API, not accepted on create
- **Write-only markers** — `password`, `psk` accepted on create/update, never returned
- **Clear descriptions** — Every option has a description
- **Names over IDs** — `organizations: ['Engineering']` not `organization_ids: [1, 2]`

**Agent iterates** on fields with the developer: "Should `org_access` have choices? Is `networks` a list of dicts with suboptions?"

---

#### Phase 3: Generate Dataclasses

**Agent runs** generators (automated):

```bash
python tools/generators/generate_user_dataclasses.py plugins/plugin_utils/docs/admin.py
bash tools/generators/generate_api_models.sh
```

**Agent reviews** generated output:

- User model in `plugins/plugin_utils/user_models/{resource}.py`
- API models in `plugins/plugin_utils/api/v1/generated/models.py`

**Agent checks:** Required vs Optional, nested types, BaseTransformMixin inheritance.

---

#### Phase 4: Transform Mixin (The Core Work)

**Agent starts** with basic structure:

```python
# plugins/plugin_utils/api/v1/{resource}.py
class {Resource}TransformMixin_v1(BaseTransformMixin):
    _field_mapping = {}
    _transform_registry = {}
```

**Agent fills in** field mappings step by step:

1. Simple 1:1: `'name': 'name'`
2. Rename: `'org_access': 'orgAccess'`
3. Complex: `'organizations': {'api_field': 'organizationIds', 'forward_transform': 'names_to_ids', 'reverse_transform': 'ids_to_names'}`

**Agent adds** complex transformations if needed (name↔ID lookups, nested flattening).

**Agent configures** endpoint operations (`get_endpoint_operations()` returning `Dict[str, EndpointOperation]`).

**Agent validates** assumptions: "I see the API uses `orgIds` but your DOCUMENTATION uses `organizations`. I'll add a name→ID transform. Correct?"

---

#### Phase 5: Action Plugin

**Agent creates** thin wrapper in `plugins/action/novacom_{resource}.py`:

- Inherits from BaseResourceActionPlugin
- Sets `MODULE_NAME = '{resource}'`
- Implements `run()`: validate → manager → dataclass → execute → validate → return

Mostly boilerplate; pattern from 07-adding-resources.md.

---

#### Phase 6: Testing

**Agent creates** test playbook in `tests/integration/test_{resource}.yml`:

- Create resource
- Verify creation
- Update resource
- Verify update
- Delete resource
- Verify deletion

**Agent runs** and verifies:

```bash
ansible-playbook tests/integration/test_admin.yml -v
```

---

#### Phase 7: Feature Complete

**Agent summarizes:**

- What was built (DOCUMENTATION, user model, API model, transform mixin, action plugin, tests)
- Estimated time and lines of custom code
- Reusable patterns (e.g., name↔ID transform for future resources)

---

## SECTION 5: Agent Development Phases

### Phase A: Schema Extraction

| Task | Automation | Notes |
|------|------------|-------|
| Extract entities from OpenAPI spec | Highly automatable | Use datamodel-code-generator |
| Generate argspec from DOCUMENTATION | Highly automatable | Parse YAML, build ArgumentSpec |
| Create User Model dataclass | Highly automatable | generate_user_dataclasses.py |
| Create Device Model dataclass | Highly automatable | generate_api_models.sh |

**Agent can do this without human review** for mechanical extraction. Human reviews naming choices (05-design-principles.md Principle 4).

---

### Phase B: Transformer Scaffolding

| Task | Automation | Notes |
|------|------------|-------|
| Create InterfaceTransformerMixin skeleton | Partially automatable | Class structure, empty mapping |
| Map fields (1:1, rename) | Partially automatable | Simple mappings yes |
| Implement sinking/hoisting logic | Partially automatable | Dot notation, nested paths |
| Complex transforms (names↔IDs) | Human review | Verify lookup API paths, cache keys |
| Endpoint operations | Partially automatable | Paths from OpenAPI; order/deps need review |

**Agent implements** simple mappings. **Human reviews** complex transforms and multi-endpoint ordering.

---

### Phase C: Unit Testing

| Task | Automation | Notes |
|------|------------|-------|
| Test messy JSON → clean dataclass | Highly automatable | Mock API response, assert structure |
| Test serialization roundtrip | Highly automatable | to_api → to_ansible, compare |
| Test forward transform | Highly automatable | User → API, assert field values |
| Test reverse transform | Highly automatable | API → User, assert field values |

**Agent can generate** unit test scaffolding. Human runs and validates.

---

## SECTION 6: Human-in-the-Loop Triggers

The agent **MUST** stop and ask when encountering:

### 1. Semantic Unit Conversion

**Example:** API returns bandwidth in bytes/sec; users think in Mbps.

**Agent asks:** "Should the module convert? User Mbps → API bytes on input? API bytes → Mbps on output? Both? Document in module."

---

### 2. Multi-Step State Transitions

**Example:** Changing SSID `auth_mode` from `open` to `psk` may require: (1) set PSK first, (2) then change mode. Order is domain-specific.

**Agent asks:** "State transition order for auth_mode change. Document in module. Implement ordered steps in convergence logic."

---

### 3. Conditional Dependencies

**Example:** `auth_mode: psk` requires `psk` field; `auth_mode: radius` requires `radius_servers`; `auth_mode: open` forbids both.

**Agent asks:** "Validate conditional requirements for auth_mode. Document in DOCUMENTATION. Add validation in argspec or custom validator."

---

### 4. Ambiguous Overridden Logic

**Example:** NovaCom SSID 0 is default and cannot be deleted. What does `state: overridden` mean for SSID 0?

**Agent asks:** "Override semantics for non-deletable default SSID. Document and implement."

---

### 5. Entity Boundary Disputes

**Example:** NovaCom has `/vpn/siteToSite` and `/vpn/client`. One module `novacom_vpn` with `type`, or two modules?

**Agent asks:** "Entity boundary: one novacom_vpn module with type, or two separate modules? Consider UX, idempotency, and future API evolution."

---

**Rule:** Do not guess. Escalate to human.

---

## SECTION 7: Common Agent Patterns

### Ask vs Look Up

| DO | DON'T |
|----|-------|
| Check existing files before asking | Ask about things you can discover from filesystem |
| Grep for class names, imports | Ask "what's the structure?" when you can list directories |
| Read 06-foundation-components.md for implementation | Ask "how does BaseTransformMixin work?" |

**Example:** Before asking "Does the foundation exist?", run a filesystem check for the three key files.

---

### Progressive Disclosure

| DO | DON'T |
|----|-------|
| Build complexity gradually | Dump entire complex implementation at once |
| Simple fields first → transforms → multi-endpoint | Show 200-line transform mixin before discussing field mapping |
| One component at a time for Foundation Builder | Implement all 7 components in one response |

---

### Show, Don't Tell

| DO | DON'T |
|----|-------|
| Show code snippets for review | Just describe abstractly |
| "Here's the field mapping for organizations:" + code block | "You need to add a name-to-ID transform" |
| Reference line numbers when citing | "The mixin handles transforms" (vague) |

---

### Reference the Guides

| DO | DON'T |
|----|-------|
| Point to specific sections in implementation docs | Reinvent documented patterns |
| "See 06-foundation-components.md Section 3 for BaseTransformMixin" | Rewrite BaseTransformMixin from scratch |
| "07-adding-resources.md Section 5 has the admin mixin example" | Invent a different structure |

---

### Validate Assumptions

| DO | DON'T |
|----|-------|
| Confirm before complex work | Make assumptions silently |
| "I see the API uses `orgIds` but your DOCUMENTATION uses `organizations`. I'll add a name→ID transform. Correct?" | Implement name→ID transform without mentioning |
| "The OpenAPI has both site-to-site and client VPN. One module or two?" | Pick one without asking |

---

## SECTION 8: Coding Standards

### Type Hints

Every function and method must have type hints:

```python
def transform(self, data: Dict[str, Any]) -> Dict[str, Any]:
    ...

def _apply_forward_mapping(
    self,
    source_data: Dict[str, Any],
    mapping: Dict[str, Any],
    context: Dict[str, Any]
) -> Dict[str, Any]:
    ...
```

---

### Google-Style Docstrings

Every module, class, and function:

```python
def example(param1: str, param2: int) -> bool:
    """One-line summary.
    
    Longer description if needed.
    
    Args:
        param1: Description
        param2: Description
    
    Returns:
        Description
    
    Raises:
        ValueError: When raised
    """
```

---

### Import Organization

```python
# Standard library
import os
from pathlib import Path
from typing import Dict, List, Optional, Any

# Third-party
import requests

# Local
from ..platform.base_transform import BaseTransformMixin
```

---

### Error Handling

Explicit and informative:

```python
try:
    result = operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
    raise ValueError(f"Failed to ...: {e}") from e
```

---

## SECTION 9: Quality Checklist

For **every** resource module, verify before considering it complete:

### Argspec and User Model

- [ ] **Flat, human-readable argspec** — No nested vendor namespaces in user model
- [ ] **No vendor namespaces in user model** — camelCase, internal terms excluded
- [ ] **All fields have descriptions** — Every option and suboption documented

### Round-Trip and State

- [ ] **Gathered state matches merged state format** — What you gather can be fed back into merged
- [ ] **Read-only fields filtered from writes** — `id`, `created_at` not accepted on create/update
- [ ] **Write-only fields filtered from reads** — `password`, `psk` never returned in gathered

### State Parameter

- [ ] **state parameter supports merged, deleted, gathered at minimum** — Full lifecycle coverage

### Naming and Idempotency

- [ ] **Entity naming** — `novacom_appliance_vlan` not `novacom_networks_appliance_vlans`
- [ ] **Primary key identified** — Document which field(s) uniquely identify the resource

### Multi-Endpoint Resources

- [ ] **Multi-endpoint resources use ordered operations** — `depends_on`, `order` in EndpointOperation; no ad-hoc sequencing

---

## SECTION 10: Which Document to Load When

### For Foundation Work

| Order | Document | Purpose |
|-------|----------|---------|
| 1 | 01-overview.md | Architecture context, component overview |
| 2 | 06-foundation-components.md | Implementation details for all components |
| 3 | 08-code-generators.md | Code generation tools |

### For Feature Work

| Order | Document | Purpose |
|-------|----------|---------|
| 1 | 07-adding-resources.md | Main step-by-step guide |
| 2 | 06-foundation-components.md | Reference as needed (BaseTransformMixin, EndpointOperation) |
| 3 | 05-design-principles.md | Rules, guardrails, quality gates |

---

## SECTION 11: Example Conversation Flows

### Foundation Builder Example

**Developer:** "I need to build the NovaCom Dashboard collection from scratch."

**Agent:** "I'll help. First, let me check what exists."

*[Agent checks filesystem: plugins/plugin_utils/platform/base_transform.py, platform_manager.py, generate_user_dataclasses.py]*

**Agent:** "None of the foundation files exist yet. You're a **Foundation Builder**. I'll load the architecture and implementation guides.

**Summary of what we'll build:**

1. **Shared types** — EndpointOperation in types.py
2. **BaseTransformMixin** — Bidirectional User↔Device transformation
3. **APIVersionRegistry** — Dynamic version discovery

4. **DynamicClassLoader** — Load version-specific classes
5. **PlatformManager** — Persistent service + multiprocess manager
6. **ManagerRPCClient** — Client-side RPC
7. **Base Action Plugin** — Manager spawning, validation

Recommended order: 1→2→3→4→5→6→7. Shall we start with shared types (EndpointOperation)?"

**Developer:** "Yes."

**Agent:** *[Implements types.py from 06-foundation-components.md Section 4, shows key parts]*

**Agent:** "types.py is done. Proceed to BaseTransformMixin?"

*[Continues through all components, then code generators, then test script]*

**Agent:** "Foundation complete. Next: add a test resource (e.g., novacom_appliance_vlan) using the Feature Developer workflow."

---

### Feature Developer Example

**Developer:** "I want to add the novacom_organization_admin module."

**Agent:** "Let me verify the foundation exists."

*[Agent checks: base_transform.py, platform_manager.py, generate_user_dataclasses.py — all present]*

**Agent:** "Foundation exists. You're a **Feature Developer**.

**Resource:** novacom_organization_admin

**Complexity:** Medium — admin has organization name↔ID transforms (users provide names, API uses IDs). Similar to the admin example in 07-adding-resources.md. Estimated 2–3 hours.

**Phase 1:** Do you have DOCUMENTATION already, or shall I create it from the OpenAPI schema?"

**Developer:** "Create it."

**Agent:** *[Creates plugins/plugin_utils/docs/admin.py with DOCUMENTATION string, following principles: names not IDs, read-only markers, snake_case]*

**Agent:** "DOCUMENTATION created. Key fields: username, email, name, org_access, tags, networks, organizations (names), id (read-only), created_at (read-only). Review? Any changes?"

**Developer:** "Looks good."

**Agent:** "Phase 2: Generating dataclasses."

*[Runs generate_user_dataclasses.py, generate_api_models.sh]*

**Agent:** "Generated UserAdmin in user_models/admin.py and API models in api/v1/generated/. Phase 3: Transform mixin. I'll map organizations (names) → organizationIds (IDs) via lookup. The API uses orgIds; your DOCUMENTATION uses organizations. Correct?"

**Developer:** "Yes."

**Agent:** *[Implements AdminTransformMixin_v1 with field mapping, transform registry, endpoint operations]*

**Agent:** "Phase 4: Action plugin and test playbook."

*[Creates action plugin, test playbook]*

**Agent:** "Feature complete. Summary: DOCUMENTATION, UserAdmin, APIAdmin_v1, AdminTransformMixin_v1, action plugin, integration test. ~150 lines custom code. Reusable: name↔ID pattern for future resources (sites, networks)."

---

## SECTION 12: Troubleshooting

### Issue: Developer Unclear About Role

**Solution:** Use direct questions.

> "What are you working on?
> A) Building the core framework (BaseTransformMixin, Manager, etc.)
> B) Adding a new resource module (VLAN, SSID, admin, etc.)
> C) Something else"

If C, ask: "Are you debugging, regenerating models, writing tests, or something else?"

---

### Issue: Foundation Partially Complete

**Solution:** Audit what exists, offer to complete.

> "I found base_transform.py and types.py, but platform_manager.py and generate_user_dataclasses.py are missing. You have a partial foundation. I can:
> 1) Complete the missing components (Manager, RPC client, generators)
> 2) Or, if you prefer, start over with a clean foundation.
> Which do you prefer?"

---

### Issue: Developer Wants to Skip Steps

**Solution:** Explain dependencies.

> "We need the DOCUMENTATION before generating the user model — the generator reads it. We need the user model before the transform mixin — the mixin references UserAdmin. Order: DOCUMENTATION → generate user model → generate API model → transform mixin → action plugin → test."

---

### Issue: Generated Code Has Errors

**Solution:** Identify, fix, explain why.

> "The generator produced `List[Dict[str, Any]]` for `networks` but the nested structure expects a `Networks` dataclass. Fix: add suboptions to DOCUMENTATION for networks, or manually adjust the generated user model to use a nested dataclass. I'll show the fix."

---

## SECTION 13: Success Metrics

### Foundation Builder Success

- [ ] All core components implemented (types, BaseTransformMixin, Registry, Loader, PlatformService, PlatformManager, RPC client, Base action plugin)
- [ ] Test manager script runs and reports API version
- [ ] Code generators work (user model + API model)
- [ ] First test resource works end-to-end (e.g., novacom_appliance_vlan)

### Feature Developer Success

- [ ] DOCUMENTATION complete with all fields, descriptions, read-only/write-only markers
- [ ] Dataclasses generated correctly (User* in user_models/, API in api/v1/generated/)
- [ ] Transform mixin handles all field mappings, including complex transforms
- [ ] Action plugin validates input and output
- [ ] Test playbook passes (create, update, delete, verify)

---

## Summary

| Persona | When | Key Docs | Outcome |
|---------|------|----------|---------|
| **Foundation Builder** | Framework doesn't exist | 01, 06, 08 | Core components + generators |
| **Feature Developer** | Foundation exists, adding resource | 07, 05, 10 | Resource module end-to-end |

**Conventions:** NovaCom naming throughout; `user_models` directory; snake_case user-facing; camelCase only in API layer.

**Agent rules:** Ask vs look up; progressive disclosure; show don't tell; reference guides; validate assumptions; stop on human-in-the-loop triggers.

---

*Document version: 1.0 | NovaCom Dashboard (novacom.dashboard) | Agent Collaboration Guide*
