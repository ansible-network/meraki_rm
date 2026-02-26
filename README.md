# cisco.meraki_rm

An Ansible collection for managing Meraki Dashboard resources using the **resource module pattern**. Configuration is expressed as declarative desired state (`merged`, `replaced`, `overridden`, `gathered`, `deleted`) and reconciled against the live API.

The collection includes 48 resource modules, a dynamically generated MCP server for AI agent integration, and a CLI tool — all driven by a single set of User Model dataclasses.

## Quick Start

```yaml
- name: Ensure VLAN 100 exists
  cisco.meraki_rm.meraki_appliance_vlans:
    state: merged
    network_id: L_123456
    config:
      - vlan_id: 100
        name: Engineering
        subnet: 10.100.0.0/24
        appliance_ip: 10.100.0.1
```

## Install

```bash
ansible-galaxy collection install cisco.meraki_rm
```

For the MCP server and CLI (standalone Python package):

```bash
pip install './plugins/plugin_utils/[mcp,cli]'
```

## Documentation

### Architecture and Design

| Doc | Description |
|-----|-------------|
| [Overview](docs/01-overview.md) | Project goals, scope, and high-level architecture |
| [Resource Module Pattern](docs/02-resource-module-pattern.md) | The state-driven CRUD pattern all modules follow |
| [SDK Architecture](docs/03-sdk-architecture.md) | Internal package layout, install modes, and extension points |
| [Data Model Transformation](docs/04-data-model-transformation.md) | How user-facing snake_case maps to API camelCase |
| [Design Principles](docs/05-design-principles.md) | Architectural guardrails, validation strategy, and quality gates |

### Implementation

| Doc | Description |
|-----|-------------|
| [Foundation Components](docs/06-foundation-components.md) | PlatformService, BaseResourceActionPlugin, User Models |
| [Adding Resources](docs/07-adding-resources.md) | Step-by-step guide for adding a new resource module |
| [Code Generators](docs/08-code-generators.md) | Schema extraction, model generation, doc generation tooling |
| [Meraki Implementation Guide](docs/meraki-implementation-guide.md) | Meraki-specific patterns, endpoint grouping, and identity categories |

### Tools and Interfaces

| Doc | Description |
|-----|-------------|
| [MCP Server Reference](docs/12-mcp-server.md) | AI agent integration via Model Context Protocol |
| [CLI Reference](docs/13-cli.md) | `meraki-cli` command-line tool for direct API interaction |

### Testing and Quality

| Doc | Description |
|-----|-------------|
| [Testing Strategy](docs/11-testing-strategy.md) | Unit tests, Molecule integration tests, and mock server |

### Process

| Doc | Description |
|-----|-------------|
| [Agent Collaboration Guide](docs/09-agent-collaboration.md) | Working with AI agents on the codebase |
| [Case Study: NovaCom](docs/10-case-study-novacom.md) | Fictional walkthrough illustrating the framework in action |

### Presentation and Feedback

| Doc | Description |
|-----|-------------|
| [Feedback Questions](docs/14-feedback-questions.md) | Structured questions for Meraki stakeholder review |
| [API Limitations](docs/15-api-limitations.md) | How API design drives module states and identity categories |
| [Coverage Report](docs/16-coverage-report.md) | Spec-vs-module coverage analysis (auto-generated) |

## Project Layout

```
plugins/
  action/          # Action plugins (one per resource)
  modules/         # Module definitions (DOCUMENTATION + argspec)
  plugin_utils/    # Shared SDK: User Models, PlatformService, MCP, CLI
tools/             # Code generators, mock server, doc renderers
tests/             # Unit and integration tests
extensions/        # Molecule test scenarios
docs/              # Architecture and reference documentation
examples/          # Per-module Ansible playbook examples
```

## License

See [LICENSE](LICENSE).
