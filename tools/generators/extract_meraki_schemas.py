#!/usr/bin/env python3
"""Extract and deduplicate inline schemas from Meraki OpenAPI spec.

The Meraki Dashboard API spec (spec3.json) has NO components/schemas.
All schemas are inline within each operation's requestBody and responses.
This tool extracts, groups, merges, and deduplicates those inline schemas
into per-entity Python dataclasses.

Usage:
    python -m tools.generators.extract_meraki_schemas \\
        --spec spec3.json \\
        --output plugins/plugin_utils/api/v1/generated/

    python -m tools.generators.extract_meraki_schemas \\
        --spec spec3.json \\
        --entity vlan \\
        --output plugins/plugin_utils/api/v1/generated/
"""

import argparse
import json
import re
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Path-to-entity mapping rules
# ---------------------------------------------------------------------------

# Each rule: (regex pattern matching the API path, entity name, domain)
# Order matters: first match wins.
ENTITY_RULES: List[Tuple[str, str, str]] = [
    # Appliance
    (r'/networks/\{networkId\}/appliance/vlans/settings$', 'vlan', 'appliance'),
    (r'/networks/\{networkId\}/appliance/vlans(/\{vlanId\})?$', 'vlan', 'appliance'),
    (r'/networks/\{networkId\}/appliance/firewall/', 'firewall', 'appliance'),
    (r'/networks/\{networkId\}/appliance/vpn/', 'vpn', 'appliance'),
    (r'/networks/\{networkId\}/appliance/trafficShaping', 'traffic_shaping', 'appliance'),
    (r'/networks/\{networkId\}/appliance/staticRoutes', 'static_route', 'appliance'),
    (r'/networks/\{networkId\}/appliance/ports', 'port', 'appliance'),
    (r'/networks/\{networkId\}/appliance/security/', 'security', 'appliance'),
    (r'/networks/\{networkId\}/appliance/warmSpare', 'warm_spare', 'appliance'),
    (r'/networks/\{networkId\}/appliance/ssids', 'appliance_ssid', 'appliance'),
    (r'/networks/\{networkId\}/appliance/prefixes', 'prefix', 'appliance'),
    (r'/networks/\{networkId\}/appliance/rfProfiles', 'appliance_rf_profile', 'appliance'),

    # Wireless
    (r'/networks/\{networkId\}/wireless/ssids/\{number\}/(firewall|trafficShaping|splash|hotspot20|identityPsks|bonjour|eapOverride|vpn|schedules|deviceTypeGroupPolicies)', 'ssid', 'wireless'),
    (r'/networks/\{networkId\}/wireless/ssids', 'ssid', 'wireless'),
    (r'/networks/\{networkId\}/wireless/rfProfiles', 'wireless_rf_profile', 'wireless'),
    (r'/networks/\{networkId\}/wireless/airMarshal', 'air_marshal', 'wireless'),
    (r'/networks/\{networkId\}/wireless/ethernet/ports/profiles', 'ethernet_port_profile', 'wireless'),

    # Switching
    (r'/devices/\{serial\}/switch/ports', 'switch_port', 'switch'),
    (r'/networks/\{networkId\}/switch/accessPolicies', 'switch_access_policy', 'switch'),
    (r'/networks/\{networkId\}/switch/dhcpServerPolicy', 'switch_dhcp_policy', 'switch'),
    (r'/networks/\{networkId\}/switch/qosRules', 'switch_qos_rule', 'switch'),
    (r'/networks/\{networkId\}/switch/routing', 'switch_routing', 'switch'),
    (r'/networks/\{networkId\}/switch/stp', 'switch_stp', 'switch'),
    (r'/networks/\{networkId\}/switch/accessControlLists', 'switch_acl', 'switch'),
    (r'/networks/\{networkId\}/switch/stacks', 'switch_stack', 'switch'),
    (r'/networks/\{networkId\}/switch/linkAggregations', 'switch_link_aggregation', 'switch'),
    (r'/networks/\{networkId\}/switch/(mtu|stormControl|dscp|alternateManagement|settings)', 'switch_settings', 'switch'),

    # Network-general
    (r'/networks/\{networkId\}/(settings|alerts/settings|netflow|snmp|syslogServers|trafficAnalysis)', 'network_settings', 'network'),
    (r'/networks/\{networkId\}/groupPolicies', 'group_policy', 'network'),
    (r'/networks/\{networkId\}/floorPlans', 'floor_plan', 'network'),
    (r'/networks/\{networkId\}/firmwareUpgrades', 'firmware_upgrade', 'network'),
    (r'/networks/\{networkId\}/webhooks', 'webhook', 'network'),
    (r'/networks/\{networkId\}/vlanProfiles', 'vlan_profile', 'network'),
    (r'/networks/\{networkId\}/merakiAuthUsers', 'meraki_auth_user', 'network'),
    (r'/networks/\{networkId\}/mqttBrokers', 'mqtt_broker', 'network'),

    # Camera/Sensor
    (r'/networks/\{networkId\}/camera/qualityRetentionProfiles', 'camera_quality_retention_profile', 'camera'),
    (r'/networks/\{networkId\}/camera/wirelessProfiles', 'camera_wireless_profile', 'camera'),
    (r'/networks/\{networkId\}/sensor/alerts/profiles', 'sensor_alert_profile', 'sensor'),

    # Organization
    (r'/organizations/\{organizationId\}/admins', 'admin', 'organization'),
    (r'/organizations/\{organizationId\}/saml', 'saml', 'organization'),
    (r'/organizations/\{organizationId\}/policyObjects', 'policy_object', 'organization'),
    (r'/organizations/\{organizationId\}/adaptivePolicy', 'adaptive_policy', 'organization'),
    (r'/organizations/\{organizationId\}/configTemplates', 'config_template', 'organization'),
    (r'/organizations/\{organizationId\}/alerts/profiles', 'org_alert_profile', 'organization'),
    (r'/organizations/\{organizationId\}/brandingPolicies', 'branding_policy', 'organization'),
    (r'/organizations/\{organizationId\}/appliance/vpn', 'org_vpn', 'organization'),

    # Device
    (r'/devices/\{serial\}/managementInterface', 'device_management_interface', 'device'),
    (r'/devices/\{serial\}/switch/routing', 'device_switch_routing', 'device'),
    (r'/devices/\{serial\}$', 'device', 'device'),
]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class FieldInfo:
    """Extracted field information from an inline schema."""
    name: str
    type_str: str
    description: str = ''
    nullable: bool = False
    enum: Optional[List[str]] = None
    is_array: bool = False
    is_object: bool = False
    nested_fields: Optional[Dict[str, 'FieldInfo']] = None
    required: bool = False


@dataclass
class EntitySchema:
    """Merged schema for a single entity."""
    entity_name: str
    domain: str
    fields: Dict[str, FieldInfo] = field(default_factory=dict)
    source_paths: Set[str] = field(default_factory=set)
    source_operations: Set[str] = field(default_factory=set)


# ---------------------------------------------------------------------------
# Schema extraction
# ---------------------------------------------------------------------------

def classify_path(api_path: str) -> Optional[Tuple[str, str]]:
    """Match an API path to an entity name and domain.

    Returns (entity_name, domain) or None if no rule matches.
    """
    for pattern, entity, domain in ENTITY_RULES:
        if re.search(pattern, api_path):
            return entity, domain
    return None


def extract_fields_from_schema(
    schema: dict,
    required_fields: Optional[List[str]] = None,
) -> Dict[str, FieldInfo]:
    """Recursively extract fields from an inline JSON schema object.

    Args:
        schema: The JSON schema dict (type: object with properties)
        required_fields: List of required field names from parent

    Returns:
        Dict of field name -> FieldInfo
    """
    if not schema or schema.get('type') != 'object':
        return {}

    properties = schema.get('properties', {})
    required_set = set(required_fields or schema.get('required', []))
    fields: Dict[str, FieldInfo] = {}

    for prop_name, prop_schema in properties.items():
        prop_type = prop_schema.get('type', 'any')
        description = prop_schema.get('description', '')
        nullable = prop_schema.get('nullable', False) or prop_schema.get('x-nullable', False)
        enum_vals = prop_schema.get('enum')

        is_array = prop_type == 'array'
        is_object = prop_type == 'object'
        nested = None

        if is_object:
            nested = extract_fields_from_schema(prop_schema)
        elif is_array:
            items = prop_schema.get('items', {})
            if items.get('type') == 'object':
                nested = extract_fields_from_schema(items)

        fi = FieldInfo(
            name=prop_name,
            type_str=_json_type_to_python(prop_type, prop_schema, nullable),
            description=description,
            nullable=nullable,
            enum=enum_vals,
            is_array=is_array,
            is_object=is_object,
            nested_fields=nested if nested else None,
            required=prop_name in required_set,
        )
        fields[prop_name] = fi

    return fields


def _json_type_to_python(
    json_type: str,
    schema: dict,
    nullable: bool,
) -> str:
    """Map JSON schema type to Python type hint string."""
    base_map = {
        'string': 'str',
        'integer': 'int',
        'number': 'float',
        'boolean': 'bool',
        'object': 'Dict[str, Any]',
        'array': 'List[Any]',
    }

    if json_type == 'array':
        items = schema.get('items', {})
        item_type = items.get('type', 'any')
        if item_type == 'object':
            inner = 'Dict[str, Any]'
        elif item_type == 'string':
            inner = 'str'
        elif item_type == 'integer':
            inner = 'int'
        elif item_type == 'number':
            inner = 'float'
        elif item_type == 'boolean':
            inner = 'bool'
        else:
            inner = 'Any'
        py_type = f'List[{inner}]'
    elif json_type == 'object' and schema.get('additionalProperties'):
        ap = schema['additionalProperties']
        val_type = ap.get('type', 'Any')
        if val_type == 'object':
            py_type = 'Dict[str, Dict[str, Any]]'
        else:
            py_type = f'Dict[str, {base_map.get(val_type, "Any")}]'
    else:
        py_type = base_map.get(json_type, 'Any')

    if nullable:
        py_type = f'Optional[{py_type}]'

    return py_type


def merge_fields(
    existing: Dict[str, FieldInfo],
    new_fields: Dict[str, FieldInfo],
) -> Dict[str, FieldInfo]:
    """Merge new fields into existing, keeping the superset."""
    merged = dict(existing)
    for name, fi in new_fields.items():
        if name not in merged:
            merged[name] = fi
        else:
            if fi.description and not merged[name].description:
                merged[name].description = fi.description
            if not fi.required:
                merged[name].required = False
            if fi.enum and not merged[name].enum:
                merged[name].enum = fi.enum
            if fi.nested_fields and merged[name].nested_fields:
                merged[name].nested_fields = merge_fields(
                    merged[name].nested_fields, fi.nested_fields
                )
            elif fi.nested_fields:
                merged[name].nested_fields = fi.nested_fields
    return merged


def extract_schema_from_operation(
    operation: dict,
) -> Dict[str, FieldInfo]:
    """Extract fields from an operation's requestBody and responses."""
    fields: Dict[str, FieldInfo] = {}

    # Request body
    req_body = operation.get('requestBody', {})
    req_schema = (
        req_body
        .get('content', {})
        .get('application/json', {})
        .get('schema', {})
    )
    if req_schema:
        if req_schema.get('type') == 'object':
            fields = merge_fields(
                fields,
                extract_fields_from_schema(req_schema),
            )

    # Responses (2xx)
    responses = operation.get('responses', {})
    for status_code, resp in responses.items():
        if not status_code.startswith('2'):
            continue
        resp_schema = (
            resp
            .get('content', {})
            .get('application/json', {})
            .get('schema', {})
        )
        if not resp_schema:
            continue

        # Handle array responses (list endpoints)
        if resp_schema.get('type') == 'array':
            items_schema = resp_schema.get('items', {})
            if items_schema.get('type') == 'object':
                fields = merge_fields(
                    fields,
                    extract_fields_from_schema(items_schema),
                )
        elif resp_schema.get('type') == 'object':
            fields = merge_fields(
                fields,
                extract_fields_from_schema(resp_schema),
            )

    return fields


def extract_entities(spec: dict) -> Dict[str, EntitySchema]:
    """Extract all entity schemas from an OpenAPI spec.

    Iterates over all paths, classifies each into an entity,
    and merges all inline schemas for that entity.

    Args:
        spec: Parsed OpenAPI spec dict

    Returns:
        Dict of entity_name -> EntitySchema
    """
    entities: Dict[str, EntitySchema] = {}
    unmatched_paths: List[str] = []

    paths = spec.get('paths', {})

    for api_path, path_item in paths.items():
        result = classify_path(api_path)
        if result is None:
            unmatched_paths.append(api_path)
            continue

        entity_name, domain = result

        if entity_name not in entities:
            entities[entity_name] = EntitySchema(
                entity_name=entity_name,
                domain=domain,
            )

        entity = entities[entity_name]
        entity.source_paths.add(api_path)

        for method in ('get', 'post', 'put', 'patch', 'delete'):
            operation = path_item.get(method)
            if not operation:
                continue

            op_id = operation.get('operationId', f'{method}:{api_path}')
            entity.source_operations.add(op_id)

            op_fields = extract_schema_from_operation(operation)
            entity.fields = merge_fields(entity.fields, op_fields)

    if unmatched_paths:
        print(
            f"  Note: {len(unmatched_paths)} paths did not match any entity rule.",
            file=sys.stderr,
        )

    return entities


# ---------------------------------------------------------------------------
# Code generation
# ---------------------------------------------------------------------------

def _field_to_dataclass_line(fi: FieldInfo, indent: str = '    ') -> str:
    """Generate a dataclass field line for a FieldInfo."""
    py_type = fi.type_str

    # Wrap all fields as Optional for flexibility unless already Optional
    if not py_type.startswith('Optional'):
        py_type = f'Optional[{py_type}]'

    return f'{indent}{fi.name}: {py_type} = None'


def _build_constraints(fields: Dict[str, FieldInfo]) -> Dict[str, Dict[str, Any]]:
    """Build a field constraints dict from FieldInfo entries.

    Only includes fields that have actionable constraints (enum values).
    """
    constraints: Dict[str, Dict[str, Any]] = {}
    for fi in fields.values():
        entry: Dict[str, Any] = {}
        if fi.enum:
            entry['enum'] = fi.enum
        if entry:
            constraints[fi.name] = entry
    return constraints


def generate_dataclass(entity: EntitySchema) -> str:
    """Generate Python dataclass source code for an entity.

    Args:
        entity: Merged entity schema

    Returns:
        Python source code string
    """
    class_name = ''.join(
        part.capitalize() for part in entity.entity_name.split('_')
    )

    # Sort fields: required first, then alphabetical
    sorted_fields = sorted(
        entity.fields.values(),
        key=lambda f: (not f.required, f.name),
    )

    constraints = _build_constraints(entity.fields)

    lines = [
        f'"""Generated API dataclass for Meraki {entity.domain} {entity.entity_name}.',
        '',
        'Auto-generated from spec3.json inline schemas.',
        'DO NOT EDIT MANUALLY — regenerate using:',
        '    python -m tools.generators.extract_meraki_schemas',
        '',
        'Source paths:',
    ]
    for p in sorted(entity.source_paths):
        lines.append(f'    {p}')
    lines.extend([
        '"""',
        '',
        'from __future__ import annotations',
        '',
        'from dataclasses import dataclass',
        f'from typing import Any, {"ClassVar, " if constraints else ""}Dict, List, Optional',
        '',
        '',
        '@dataclass',
        f'class {class_name}:',
        f'    """Meraki {entity.domain} {entity.entity_name} API schema.',
        '',
        '    Fields use camelCase matching the Meraki Dashboard API.',
        '    The transform mixin converts to/from snake_case User Model fields.',
        '    """',
        '',
    ])

    if constraints:
        lines.append('    _FIELD_CONSTRAINTS: ClassVar[dict] = {')
        for fname in sorted(constraints):
            entry = constraints[fname]
            lines.append(f'        {fname!r}: {entry!r},')
        lines.append('    }')
        lines.append('')

    for fi in sorted_fields:
        if fi.description:
            desc = fi.description.replace('\n', ' ').strip()
            if len(desc) > 76:
                desc = desc[:73] + '...'
            lines.append(f'    # {desc}')
        lines.append(_field_to_dataclass_line(fi))

    lines.append('')
    code = '\n'.join(lines)

    return code


def write_entity(
    entity: EntitySchema,
    output_dir: Path,
) -> Path:
    """Write a single entity dataclass to a file.

    Args:
        entity: Entity schema to write
        output_dir: Directory to write files into

    Returns:
        Path to the written file
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / f'{entity.entity_name}.py'
    code = generate_dataclass(entity)
    filepath.write_text(code)
    return filepath


def write_init(entities: Dict[str, EntitySchema], output_dir: Path) -> None:
    """Write __init__.py that imports all generated entity classes."""
    lines = [
        '"""Generated API model classes for Meraki Dashboard API v1.',
        '',
        'Auto-generated. DO NOT EDIT MANUALLY.',
        '"""',
        '',
    ]

    for entity_name in sorted(entities.keys()):
        class_name = ''.join(
            part.capitalize() for part in entity_name.split('_')
        )
        lines.append(
            f'from .{entity_name} import {class_name}  # noqa: F401'
        )

    lines.append('')
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / '__init__.py').write_text('\n'.join(lines))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Extract inline schemas from Meraki OpenAPI spec'
    )
    parser.add_argument(
        '--spec', required=True,
        help='Path to spec3.json',
    )
    parser.add_argument(
        '--output', required=True,
        help='Output directory for generated files',
    )
    parser.add_argument(
        '--entity',
        help='Generate only this entity (e.g., "vlan")',
    )
    parser.add_argument(
        '--list-entities', action='store_true',
        help='List all discovered entities and exit',
    )
    parser.add_argument(
        '--check', action='store_true',
        help='Dry-run: report what would be generated without writing files',
    )
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"Error: spec file not found: {spec_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading spec from {spec_path}...")
    with open(spec_path) as f:
        spec = json.load(f)

    print("Extracting entity schemas...")
    entities = extract_entities(spec)

    print(f"Found {len(entities)} entities:")
    for name, entity in sorted(entities.items()):
        print(
            f"  {name:30s}  {entity.domain:12s}  "
            f"{len(entity.fields):3d} fields  "
            f"{len(entity.source_paths):2d} paths"
        )

    if args.list_entities:
        return

    output_dir = Path(args.output)

    verb = 'Would write' if args.check else 'Wrote'

    if args.entity:
        if args.entity not in entities:
            print(
                f"Error: entity '{args.entity}' not found. "
                f"Available: {sorted(entities.keys())}",
                file=sys.stderr,
            )
            sys.exit(1)
        entity = entities[args.entity]
        if args.check:
            filepath = output_dir / f'{entity.entity_name}.py'
            print(f"{verb} {filepath} ({len(entity.fields)} fields)")
        else:
            filepath = write_entity(entity, output_dir)
            print(f"{verb} {filepath} ({len(entity.fields)} fields)")
    else:
        for name, entity in sorted(entities.items()):
            if args.check:
                filepath = output_dir / f'{entity.entity_name}.py'
                print(f"  {filepath} ({len(entity.fields)} fields)")
            else:
                filepath = write_entity(entity, output_dir)
                print(f"  {filepath} ({len(entity.fields)} fields)")

        if not args.check:
            write_init(entities, output_dir)
        print(f"\n{verb} {len(entities)} entity files to {output_dir}/")


if __name__ == '__main__':
    main()
