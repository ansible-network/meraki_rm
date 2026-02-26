# Feedback Questions for Meraki Stakeholders

This document contains structured questions for Meraki engineering, product, and developer-experience teams. Responses will guide the next iteration of the `cisco.meraki_rm` Ansible collection, MCP server, and CLI.

---

## 1. Usability and UX

### 1.1 Module Naming

Modules follow the pattern `meraki_{domain}_{entity}` (e.g., `meraki_appliance_vlans`, `meraki_switch_ports`). The domain segment mirrors the API path hierarchy.

- Are these names intuitive for Meraki customers already familiar with the Dashboard API?
- Would a flatter naming scheme (e.g., `meraki_vlan` instead of `meraki_appliance_vlans`) be preferred, even though it loses the domain grouping?
- Does the plural vs singular convention (e.g., `meraki_appliance_vlans` vs `meraki_appliance_vlan`) matter to your users?

### 1.2 State Model

The collection uses Ansible resource module states: `merged`, `replaced`, `overridden`, `gathered`, `deleted`.

- Is this state model understood by your customer base, or would action-oriented verbs (create, update, delete, get) be more approachable?
- Is `overridden` (declarative "only these should exist") a capability your customers actively need, or is `replaced` sufficient?
- For singletons (firewall, VPN, network settings) where `deleted` is not supported — should we offer a "reset to defaults" state?

### 1.3 Config List Wrapper

All resource modules accept configuration as `config: [...]` — a list of items, even for singletons where only one item is valid.

- Is the uniform `config:` list wrapper acceptable, or would singletons benefit from a flat parameter interface (key-value pairs at the top level)?
- For resources that manage a single item at a time (e.g., switch ports by serial + port ID), is the list wrapper confusing?

### 1.4 CLI Subcommand Names

The `meraki-cli` tool uses short names derived from `MODULE_NAME` (e.g., `meraki-cli vlan`, `meraki-cli switch-port`, `meraki-cli admin`).

- Are these short names clear enough, or should the CLI mirror the full module name (e.g., `meraki-cli appliance-vlan`)?
- Is the `meraki-cli --list` output (48 subcommands) overwhelming? Should commands be grouped by domain?

### 1.5 Output Formats

The CLI defaults to human-readable table output, with `--json` and `--yaml` flags.

- Is the default table format useful, or would JSON be a better default for automation?
- Are there additional output formats your customers expect (e.g., CSV for bulk operations)?

---

## 2. Entity Scope and Completeness

### 2.1 Entity Aggregation

The collection aggregates multiple API endpoints into single entities. For example, `meraki_appliance_firewall` consolidates 7 sub-endpoints (L3 rules, L7 rules, inbound rules, cellular rules, firewalled services, settings, inbound cellular rules) into one module.

- Is this level of aggregation correct for the firewall entity?
- Should `meraki_wireless_ssid` (14 sub-endpoints covering SSID settings, firewall, traffic shaping, splash, hotspot 2.0, identity PSKs, bonjour, EAP, VPN, schedules, device type policies) remain a single module, or be split?
- Are there cases where we have aggregated too aggressively or not enough?

### 2.2 Missing Resources

The collection covers 48 resource entities. Notable API areas **not** covered:

| Area | Approximate Endpoints | Reason for Exclusion |
|------|----------------------|---------------------|
| Systems Manager (SM/MDM) | ~40 | Different management paradigm |
| Insight | ~15 | Monitoring/analytics, not configuration |
| Licensing | ~10 | Org-level admin operations |
| Live Tools | ~10 | Real-time diagnostics, not state management |
| Administered endpoints | ~10 | User-identity-scoped, not org/network-scoped |
| Bulk operations | ~8 | Batch claim/provision, different pattern |

- Which of these areas are highest priority for your customers?
- Are there specific resources within covered domains that are missing and high-value?
- Should `organizations/` bulk endpoints (e.g., bulk device claims, inventory management) be modeled as resource modules?

### 2.3 Facts Module

`meraki_facts` is a gather-only module that collects organization, network, device, and inventory data.

- What additional facts would be most valuable? (e.g., license status, firmware versions, topology)
- Should facts support filtering (e.g., gather facts only for a specific product type)?

---

## 3. API Identity and Limitations

### 3.1 Resource Identity Categories

Resources fall into three identity categories based on how the API identifies them:

| Category | Description | Example | Count |
|----------|-------------|---------|-------|
| A | User-meaningful key is the API key | VLAN (vlan_id), VLAN Profile (iname) | 3 |
| B | User key + separate system-generated ID | Admin (email / admin_id), Webhook (name / http_server_id) | 19 |
| C | No user-meaningful key; system ID only | QoS Rule (qos_rule_id), Link Aggregation (link_aggregation_id) | 4 |

- For Category C resources, our collection uses content-based matching with positional fallback. Is there a better approach you would recommend?
- Are there plans to add user-meaningful keys (names, labels) to Category C resources in future API versions?
- For Category B resources, is the canonical key (name, email) guaranteed unique within scope, or can collisions occur?

### 3.2 Singleton Behavior

Singletons (firewall, VPN, network settings, etc.) only support GET and PUT — no POST or DELETE. This means `deleted` state is not supported.

- Should we implement a "reset to factory defaults" operation for singletons?
- If so, what does "factory default" mean for each singleton? Is there a documented default state?
- Are there singletons where the API supports partial updates (PATCH semantics) even though the method is PUT?

### 3.3 OpenAPI Spec

The Meraki spec (`spec3.json`, v1.67.0) has 594 paths but **no `components/schemas`** — all schemas are inline.

- Are there plans to add shared schemas to the OpenAPI spec?
- How often does the spec change in ways that affect request/response shapes (vs adding new endpoints)?
- Is there a changelog or diff mechanism between spec versions that we could consume programmatically?

### 3.4 Action Batches

The collection can use Action Batches (`POST /organizations/{id}/actionBatches`) for atomic multi-endpoint operations (e.g., `overridden` state on complex modules).

- What is the recommended maximum batch size?
- Are there endpoints that are not batch-eligible?
- Is synchronous mode (`"synchronous": true`) reliable for batches under 20 actions?

### 3.5 Rate Limiting

The API enforces 10 requests/second per organization with `Retry-After` on 429.

- Is the 10 req/s limit per API key, per organization, or per organization-per-key?
- For `overridden` state (which may require gather + diff + multiple deletes + multiple creates), can we request a temporary rate increase?
- Are there plans for a bulk/batch API that reduces the number of individual calls needed?

---

## 4. Developer Experience and Ecosystem

### 4.1 Documentation Site

The GitHub Pages site has three sections: Modules (ansible-doc rendered HTML), MCP Server (tool reference), and CLI (command reference).

- Is this structure sufficient, or should we add sections (e.g., tutorials, migration guides from existing Meraki Ansible modules)?
- Should the doc site include interactive examples or a playground?
- Is the dark/light theme toggle and zoom useful, or are there other accessibility needs?

### 4.2 MCP Server

The MCP server exposes 48 tools dynamically generated from User Model introspection, supporting both task generation (Ansible YAML) and live execution modes.

- Is `--mode=task` (generating Ansible YAML snippets) useful for your AI/automation workflows, or is `--mode=live` (direct API execution) the primary use case?
- Should the MCP server support additional output formats beyond the current Ansible YAML and JSON?
- Are there meta-operations the MCP server should expose (e.g., "show me all VLANs across all networks in an org")?

### 4.3 Mock Server

The stateful mock server (`--mock` flag on both MCP and CLI) enables testing without a real API key.

- Would a hosted/shared mock server be more useful than a local one for CI/CD pipelines?
- Should the mock server support seeding with realistic data (e.g., a "demo org" dataset)?
- Are there API behaviors the mock should simulate that are hard to test against production (e.g., rate limiting, async operations)?

### 4.4 Integration with Existing Ecosystem

- How should this collection coexist with the existing `cisco.meraki` Ansible collection (which uses the endpoint-wrapping pattern)?
- Is there a migration path you would recommend for customers moving from `cisco.meraki` to `cisco.meraki_rm`?
- Should the collection integrate with Meraki's Terraform provider or other IaC tools?

---

## How to Provide Feedback

For each question:

1. **Priority**: Is this question relevant to your team? (High / Medium / Low / N/A)
2. **Answer**: Your response or recommendation
3. **Context**: Any additional context, constraints, or customer feedback that informs your answer

Please return responses in whatever format is most convenient — inline annotations, a separate document, or a meeting discussion.
