#!/usr/bin/env python3
"""Generate API coverage report by cross-referencing spec3.json against modules.

Parses the Meraki OpenAPI spec, groups endpoints by resource entity, and
compares against the collection's 48 implemented modules.  Produces
``docs/16-coverage-report.md``.

Idempotent: safe to re-run whenever the spec or modules change.

Usage::

    python tools/generate_coverage_report.py
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from plugins.plugin_utils.mcp.introspect import build_tool_definitions

ENTITY_PATTERNS: list[tuple[str, str, str]] = [
    # (regex_pattern, entity_name, domain)
    (r"/networks/\{[^}]+\}/appliance/vlans", "vlan", "Appliance"),
    (r"/networks/\{[^}]+\}/appliance/firewall", "firewall", "Appliance"),
    (r"/networks/\{[^}]+\}/appliance/vpn", "vpn", "Appliance"),
    (r"/networks/\{[^}]+\}/appliance/trafficShaping", "traffic_shaping", "Appliance"),
    (r"/networks/\{[^}]+\}/appliance/staticRoutes", "static_route", "Appliance"),
    (r"/networks/\{[^}]+\}/appliance/ports", "port", "Appliance"),
    (r"/networks/\{[^}]+\}/appliance/security", "security", "Appliance"),
    (r"/networks/\{[^}]+\}/appliance/warmSpare", "warm_spare", "Appliance"),
    (r"/networks/\{[^}]+\}/appliance/ssids", "appliance_ssid", "Appliance"),
    (r"/networks/\{[^}]+\}/appliance/prefixes/delegated/statics", "prefix", "Appliance"),
    (r"/networks/\{[^}]+\}/appliance/rfProfiles", "appliance_rf_profile", "Appliance"),
    (r"/networks/\{[^}]+\}/wireless/ssids", "ssid", "Wireless"),
    (r"/networks/\{[^}]+\}/wireless/rfProfiles", "wireless_rf_profile", "Wireless"),
    (r"/networks/\{[^}]+\}/wireless/airMarshal", "air_marshal", "Wireless"),
    (r"/networks/\{[^}]+\}/wireless/ethernet/ports/profiles", "ethernet_port_profile", "Wireless"),
    (r"/networks/\{[^}]+\}/switch/accessPolicies", "switch_access_policy", "Switching"),
    (r"/networks/\{[^}]+\}/switch/dhcpServerPolicy", "switch_dhcp_policy", "Switching"),
    (r"/networks/\{[^}]+\}/switch/qosRules", "switch_qos_rule", "Switching"),
    (r"/networks/\{[^}]+\}/switch/routing", "switch_routing", "Switching"),
    (r"/networks/\{[^}]+\}/switch/stp", "switch_stp", "Switching"),
    (r"/networks/\{[^}]+\}/switch/accessControlLists", "switch_acl", "Switching"),
    (r"/networks/\{[^}]+\}/switch/stacks", "switch_stack", "Switching"),
    (r"/networks/\{[^}]+\}/switch/linkAggregations", "switch_link_aggregation", "Switching"),
    (r"/networks/\{[^}]+\}/switch/mtu", "switch_settings", "Switching"),
    (r"/networks/\{[^}]+\}/switch/stormControl", "switch_settings", "Switching"),
    (r"/networks/\{[^}]+\}/switch/dscp", "switch_settings", "Switching"),
    (r"/networks/\{[^}]+\}/switch/alternateManagementInterface", "switch_settings", "Switching"),
    (r"/networks/\{[^}]+\}/switch/settings", "switch_settings", "Switching"),
    (r"/networks/\{[^}]+\}/settings", "network_settings", "Network"),
    (r"/networks/\{[^}]+\}/alerts", "network_settings", "Network"),
    (r"/networks/\{[^}]+\}/netflow", "network_settings", "Network"),
    (r"/networks/\{[^}]+\}/snmp", "network_settings", "Network"),
    (r"/networks/\{[^}]+\}/syslogServers", "network_settings", "Network"),
    (r"/networks/\{[^}]+\}/trafficAnalysis", "network_settings", "Network"),
    (r"/networks/\{[^}]+\}/groupPolicies", "group_policy", "Network"),
    (r"/networks/\{[^}]+\}/floorPlans", "floor_plan", "Network"),
    (r"/networks/\{[^}]+\}/firmwareUpgrades", "firmware_upgrade", "Network"),
    (r"/networks/\{[^}]+\}/webhooks", "webhook", "Network"),
    (r"/networks/\{[^}]+\}/vlanProfiles", "vlan_profile", "Network"),
    (r"/networks/\{[^}]+\}/merakiAuthUsers", "meraki_auth_user", "Network"),
    (r"/networks/\{[^}]+\}/mqttBrokers", "mqtt_broker", "Network"),
    (r"/networks/\{[^}]+\}/camera/qualityRetentionProfiles", "camera_quality_retention_profile", "Camera/Sensor"),
    (r"/networks/\{[^}]+\}/camera/wirelessProfiles", "camera_wireless_profile", "Camera/Sensor"),
    (r"/networks/\{[^}]+\}/sensor/alerts/profiles", "sensor_alert_profile", "Camera/Sensor"),
    (r"/organizations/\{[^}]+\}/admins", "admin", "Organization"),
    (r"/organizations/\{[^}]+\}/saml", "saml", "Organization"),
    (r"/organizations/\{[^}]+\}/samlRoles", "saml", "Organization"),
    (r"/organizations/\{[^}]+\}/policyObjects", "policy_object", "Organization"),
    (r"/organizations/\{[^}]+\}/adaptivePolicy", "adaptive_policy", "Organization"),
    (r"/organizations/\{[^}]+\}/configTemplates", "config_template", "Organization"),
    (r"/organizations/\{[^}]+\}/alerts/profiles", "org_alert_profile", "Organization"),
    (r"/organizations/\{[^}]+\}/brandingPolicies", "branding_policy", "Organization"),
    (r"/organizations/\{[^}]+\}/appliance/vpn", "org_vpn", "Organization"),
    (r"/devices/\{[^}]+\}/switch/routing", "device_switch_routing", "Device"),
    (r"/devices/\{[^}]+\}/switch/ports", "switch_port", "Device"),
    (r"/devices/\{[^}]+\}/managementInterface", "device_management_interface", "Device"),
    (r"/devices/\{serial\}$", "device", "Device"),
]

UNCOVERED_CATEGORIES: dict[str, str] = {
    "sm": "Systems Manager (MDM) — different management paradigm",
    "liveTools": "Live Tools — real-time diagnostics, not state management",
    "clients": "Client analytics — read-only monitoring data",
    "insight": "Insight — monitoring/analytics, not configuration",
    "summary": "Summary — read-only aggregate reports",
    "apiRequests": "API request logs — read-only",
    "configurationChanges": "Change log — read-only",
    "openapiSpec": "OpenAPI spec endpoint — meta/tooling",
    "uplinks": "Uplink status — read-only monitoring",
    "topology": "Network topology — read-only",
    "health": "Health data — read-only",
    "networkHealth": "Network health — read-only",
    "events": "Event log — read-only",
    "traffic": "Traffic data — read-only",
    "splashLoginAttempts": "Splash login data — read-only",
    "bluetoothClients": "Bluetooth client data — read-only",
    "assurance": "Assurance — monitoring/analytics",
    "wirelessController": "Wireless controller — read-only monitoring",
    "spaces": "Spaces — emerging feature",
}


def _load_spec() -> dict[str, Any]:
    """Load and return the OpenAPI spec."""
    spec_path = ROOT / "spec3.json"
    if not spec_path.exists():
        print(f"ERROR: {spec_path} not found", file=sys.stderr)
        sys.exit(1)
    with open(spec_path) as f:
        return json.load(f)


def _classify_path(path: str) -> tuple[str | None, str | None]:
    """Match a path against entity patterns.

    Returns:
        Tuple of (entity_name, domain) or (None, None) if no match.
    """
    for pattern, entity, domain in ENTITY_PATTERNS:
        if re.search(pattern, path):
            return entity, domain
    return None, None


def _get_methods(path_item: dict[str, Any]) -> list[str]:
    """Extract HTTP methods from a path item."""
    return sorted(
        m.upper() for m in path_item if m in ("get", "post", "put", "delete", "patch")
    )


def generate_report() -> str:
    """Generate the full coverage report as Markdown.

    Returns:
        Complete Markdown document string.
    """
    spec = _load_spec()
    all_paths = spec.get("paths", {})
    tool_defs = build_tool_definitions()
    module_names = {td["_metadata"]["module_name"] for td in tool_defs}

    covered: dict[str, list[tuple[str, list[str]]]] = defaultdict(list)
    uncovered: list[tuple[str, list[str]]] = []
    entity_domains: dict[str, str] = {}

    total_get = 0
    total_post = 0
    total_put = 0
    total_delete = 0
    covered_paths = 0

    for path in sorted(all_paths):
        methods = _get_methods(all_paths[path])
        for m in methods:
            if m == "GET":
                total_get += 1
            elif m == "POST":
                total_post += 1
            elif m == "PUT":
                total_put += 1
            elif m == "DELETE":
                total_delete += 1

        entity, domain = _classify_path(path)
        if entity:
            covered[entity].append((path, methods))
            entity_domains[entity] = domain
            covered_paths += 1
        else:
            uncovered.append((path, methods))

    covered_entity_count = len(covered)
    covered_method_total = sum(
        len(methods) for paths_list in covered.values() for _, methods in paths_list
    )
    total_methods = total_get + total_post + total_put + total_delete

    parts: list[str] = []

    parts.append("# API Coverage Report")
    parts.append("")
    parts.append(
        "Auto-generated from `spec3.json` and User Model introspection.  "
        "Regenerate with `python tools/generate_coverage_report.py`."
    )
    parts.append("")
    parts.append("---")
    parts.append("")

    # Summary
    parts.append("## Summary")
    parts.append("")
    parts.append("| Metric | Value |")
    parts.append("|--------|-------|")
    parts.append(f"| OpenAPI spec version | v1.67.0 |")
    parts.append(f"| Total API paths | {len(all_paths)} |")
    parts.append(
        f"| Total operations (GET/POST/PUT/DELETE) | {total_methods} "
        f"({total_get} GET, {total_post} POST, {total_put} PUT, {total_delete} DELETE) |"
    )
    parts.append(f"| Paths mapped to a module entity | {covered_paths} |")
    parts.append(f"| Paths not mapped (uncovered) | {len(uncovered)} |")
    parts.append(
        f"| Path coverage | {covered_paths}/{len(all_paths)} "
        f"({100 * covered_paths / len(all_paths):.0f}%) |"
    )
    parts.append(f"| Resource entities (modules) | {len(module_names)} |")
    parts.append(
        f"| Entities with mapped paths | {covered_entity_count} |"
    )
    parts.append("")
    parts.append("---")
    parts.append("")

    # Presentation Layer Matrix
    parts.append("## Presentation Layer Feature Matrix")
    parts.append("")
    parts.append("All three presentation layers (Ansible, MCP server, CLI) share the same ")
    parts.append("User Model introspection and PlatformService, so resource coverage is identical.")
    parts.append("")
    parts.append("| Capability | Ansible | MCP Server | CLI |")
    parts.append("|------------|---------|------------|-----|")
    parts.append(f"| Resource modules/tools/commands | {len(module_names)} | {len(module_names)} | {len(module_names)} |")

    crud_count = sum(
        1 for td in tool_defs if td["_metadata"]["supports_delete"]
    )
    singleton_count = len(module_names) - crud_count
    parts.append(f"| Full CRUD resources | {crud_count} | {crud_count} | {crud_count} |")
    parts.append(f"| Singleton resources | {singleton_count} | {singleton_count} | {singleton_count} |")
    parts.append("| State: merged | All | All | All |")
    parts.append("| State: gathered | All | All | All |")

    replaced_count = sum(
        1 for td in tool_defs if "replaced" in td["_metadata"]["valid_states"]
    )
    overridden_count = sum(
        1 for td in tool_defs if "overridden" in td["_metadata"]["valid_states"]
    )
    deleted_count = sum(
        1 for td in tool_defs if "deleted" in td["_metadata"]["valid_states"]
    )
    parts.append(f"| State: replaced | {replaced_count} | {replaced_count} | {replaced_count} |")
    parts.append(f"| State: overridden | {overridden_count} | {overridden_count} | {overridden_count} |")
    parts.append(f"| State: deleted | {deleted_count} | {deleted_count} | {deleted_count} |")
    parts.append("| Check mode | Yes | N/A | N/A |")
    parts.append("| Diff mode | Yes | N/A | N/A |")
    parts.append("| Output: JSON | Via callback | Response | `--json` |")
    parts.append("| Output: YAML | Native | Response | `--yaml` |")
    parts.append("| Output: Table | N/A | N/A | Default |")
    parts.append("| Mock server | Molecule | `--mock` | `--mock` |")
    parts.append("| Authentication | Inventory vars | Env vars | Env vars |")
    parts.append("")
    parts.append("---")
    parts.append("")

    # Per-Domain Coverage
    parts.append("## Per-Domain Coverage")
    parts.append("")

    domains: dict[str, list[str]] = defaultdict(list)
    for entity, domain in sorted(entity_domains.items()):
        domains[domain].append(entity)

    for domain in sorted(domains):
        entities = sorted(set(domains[domain]))
        total_domain_paths = sum(
            len(covered[e]) for e in entities
        )
        parts.append(f"### {domain}")
        parts.append("")
        parts.append(f"**{len(entities)} entities, {total_domain_paths} paths covered**")
        parts.append("")
        parts.append("| Entity | Module | Paths | Methods | Category |")
        parts.append("|--------|--------|-------|---------|----------|")

        for entity in entities:
            path_count = len(covered[entity])
            all_methods_set: set[str] = set()
            for _, methods in covered[entity]:
                all_methods_set.update(methods)
            methods_str = ", ".join(sorted(all_methods_set))
            in_collection = entity in module_names
            module_name = f"`meraki_{entity}`" if in_collection else "(not implemented)"

            td_match = next(
                (td for td in tool_defs if td["_metadata"]["module_name"] == entity),
                None,
            )
            if td_match:
                meta = td_match["_metadata"]
                if meta["canonical_key"] and meta["system_key"]:
                    cat = "B"
                elif meta["canonical_key"]:
                    cat = "A"
                elif meta["system_key"]:
                    cat = "C"
                else:
                    cat = "Singleton"
            else:
                cat = "—"

            parts.append(
                f"| `{entity}` | {module_name} | {path_count} | {methods_str} | {cat} |"
            )

        parts.append("")

    parts.append("---")
    parts.append("")

    # Uncovered Endpoints
    parts.append("## Uncovered API Paths")
    parts.append("")
    parts.append(
        f"**{len(uncovered)} paths** in the OpenAPI spec are not mapped to any module. "
        "These are grouped by reason for exclusion."
    )
    parts.append("")

    categorized: dict[str, list[tuple[str, list[str]]]] = defaultdict(list)
    truly_uncategorized: list[tuple[str, list[str]]] = []

    for path, methods in uncovered:
        parts_list = path.strip("/").split("/")
        matched = False

        if parts_list[0] == "administered":
            categorized["Administered endpoints (user-identity-scoped)"].append(
                (path, methods)
            )
            matched = True
        elif parts_list[0] in ("networks", "organizations", "devices"):
            segment = parts_list[2] if len(parts_list) > 2 else parts_list[0]
            for key, desc in UNCOVERED_CATEGORIES.items():
                if segment == key or key in path:
                    categorized[desc].append((path, methods))
                    matched = True
                    break

        if not matched:
            # Try to find domain-level category
            for key, desc in UNCOVERED_CATEGORIES.items():
                if key in path:
                    categorized[desc].append((path, methods))
                    matched = True
                    break

        if not matched:
            truly_uncategorized.append((path, methods))

    for category in sorted(categorized):
        items = categorized[category]
        parts.append(f"### {category}")
        parts.append("")
        parts.append(f"{len(items)} paths")
        parts.append("")
        for path, methods in sorted(items):
            parts.append(f"- `{path}` [{', '.join(methods)}]")
        parts.append("")

    if truly_uncategorized:
        parts.append("### Other Uncovered Paths")
        parts.append("")
        parts.append(
            f"{len(truly_uncategorized)} paths not mapped to any module or exclusion category. "
            "These may be candidates for future modules."
        )
        parts.append("")
        for path, methods in sorted(truly_uncategorized):
            parts.append(f"- `{path}` [{', '.join(methods)}]")
        parts.append("")

    parts.append("---")
    parts.append("")

    # Module State Summary
    parts.append("## Module State Summary")
    parts.append("")
    parts.append("| Module | Scope | Canonical Key | System Key | Category | States |")
    parts.append("|--------|-------|---------------|------------|----------|--------|")

    for td in sorted(tool_defs, key=lambda t: t["name"]):
        meta = td["_metadata"]
        ck = f"`{meta['canonical_key']}`" if meta["canonical_key"] else "—"
        sk = f"`{meta['system_key']}`" if meta["system_key"] else "—"
        states = ", ".join(sorted(meta["valid_states"]))

        if meta["canonical_key"] and meta["system_key"]:
            cat = "B"
        elif meta["canonical_key"]:
            cat = "A"
        elif meta["system_key"]:
            cat = "C"
        else:
            cat = "Singleton"

        parts.append(
            f"| `{meta['module_name']}` | `{meta['scope_param']}` | {ck} | {sk} | {cat} | {states} |"
        )

    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append(
        "*Generated by `tools/generate_coverage_report.py` from "
        "`spec3.json` and User Model introspection.*"
    )

    return "\n".join(parts)


def main() -> None:
    """Entry point: generate and write the coverage report."""
    report = generate_report()
    output_path = ROOT / "docs" / "16-coverage-report.md"
    output_path.write_text(report)
    print(f"Generated {output_path}")


if __name__ == "__main__":
    main()
