#!/usr/bin/env python3
"""Step 1 — Generate example task files from module DOCUMENTATION.

Pipeline position:  **1 of 4**  (run first)

Reads every ``plugins/modules/meraki_*.py`` file, parses its DOCUMENTATION
string, and emits one YAML task file per supported state into::

    examples/{module}/{state}.yml

Each file is a self-contained Ansible task list showing how to use the
module for that state (merged, replaced, overridden, gathered, deleted).

Design decisions embedded here:
  - ``RESPONSE_ONLY_FIELDS`` — fields the API returns but the user never
    sends; excluded from generated configs so Molecule verify won't fail.
  - ``FIELD_SAMPLES`` — realistic sample values for fields where the
    default ``'example'`` would be invalid (e.g. port ranges, enums).
  - ``REPLACED_OVERRIDES`` — alternate values used for replaced/overridden
    states so the test actually changes something.
  - System keys (server-assigned IDs) are never included in user configs;
    the framework resolves them at runtime.

Outputs feed into both:
  1. ``tools/generate_molecule_scenarios.py`` — Molecule test scaffolding
  2. ``tools/inject_examples.py`` — ``ansible-doc`` EXAMPLES blocks

Usage::

    python tools/generate_examples.py            # write all
    python tools/generate_examples.py --check     # dry-run
"""

import ast
import os
import re
import sys
import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
MODULES_DIR = PROJECT_ROOT / 'plugins' / 'modules'
ACTION_DIR = PROJECT_ROOT / 'plugins' / 'action'
EXAMPLES_DIR = PROJECT_ROOT / 'examples'


# ── Sample values by field name ──────────────────────────────────────

FIELD_SAMPLES = {
    'vlan_id': '"100"',
    'name': 'Test-Config',
    'network_id': 'N_123456789012345678',
    'organization_id': '123456',
    'serial': 'Q2XX-XXXX-XXXX',
    'subnet': '192.168.128.0/24',
    'appliance_ip': '192.168.128.1',
    'gateway_ip': '10.0.0.1',
    'interface_ip': '10.0.0.1',
    'cidr': '192.168.128.0/24',
    'default_gateway': '10.0.0.1',
    'virtual_ip1': '10.0.0.2',
    'virtual_ip2': '10.0.0.3',
    'spare_serial': 'Q2XX-SPARE-0001',
    'ip': '10.0.0.1',
    'fqdn': 'example.com',
    'mask': 24,
    'email': 'admin@example.com',
    'org_access': 'full',
    'auth_mode': 'open',
    'authentication_method': 'Email',
    'psk': 'testpassword123',
    'encryption_mode': 'wpa',
    'wpa_encryption_mode': 'WPA2 only',
    'dhcp_handling': 'Run a DHCP server',
    'dhcp_lease_time': '1 day',
    'dns_nameservers': 'upstream_dns',
    'dhcp_boot_options_enabled': False,
    'number': 1,
    'splash_page': 'None',
    'band_selection': 'Dual band operation',
    'min_bitrate': 11,
    'visible': True,
    'available_on_all_aps': True,
    'ip_assignment_mode': 'NAT mode',
    'port_id': '"1"',
    'type': 'access',
    'vlan': 1,
    'voice_vlan': 100,
    'allowed_vlans': 'all',
    'poe_enabled': True,
    'rstp_enabled': True,
    'stp_guard': 'disabled',
    'link_negotiation': 'Auto negotiate',
    'protocol': 'TCP',
    'mode': 'none',
    'secret': 'vpnsecret123',
    'enabled': True,
    'description': 'Managed by Ansible',
    'tags': ['ansible', 'test'],
    'url': 'https://example.com/webhook',
    'host': 'mqtt.example.com',
    'port': 1883,
    'timezone': 'America/Los_Angeles',
    'uplink_mode': 'virtual',
    'lat': 37.7749,
    'lng': -122.4194,
    'address': '500 Terry Francine Street',
    'max_retention_days': 30,
    'default_rules_enabled': True,
    'gateway_vlan_id': 1,
    'band_selection_type': 'ssid',
    'src_port_range': '1-1024',
    'dst_port_range': '1-1024',
}

# Alternate values for replaced state (to show a meaningful change)
REPLACED_OVERRIDES = {
    'name': 'Replaced-Config',
    'description': 'Replaced by Ansible',
    'subnet': '10.20.0.0/24',
    'appliance_ip': '10.20.0.1',
    'enabled': False,
    'vlan': 20,
    'mode': 'spoke',
    'tags': ['ansible', 'replaced'],
    'email': 'replaced-admin@example.com',
    'timezone': 'UTC',
}

TYPE_DEFAULTS = {
    'str': 'example',
    'int': 1,
    'float': 0.0,
    'bool': True,
    'list': [],
    'dict': {},
}

RESPONSE_ONLY_FIELDS = {
    'meraki_organization_admins': {'account_status', 'two_factor_auth_enabled', 'has_api_key', 'last_active'},
    'meraki_wireless_ethernet_port_profiles': {'is_default'},
    'meraki_switch_stacks': {'virtual_mac', 'is_monitor_only'},
    'meraki_wireless_rf_profiles': {'is_indoor_default', 'is_outdoor_default'},
}


def sample_value(field_name, field_type, choices=None, replaced=False):
    if choices:
        return choices[1] if replaced and len(choices) > 1 else choices[0]
    if replaced and field_name in REPLACED_OVERRIDES:
        return REPLACED_OVERRIDES[field_name]
    if field_name in FIELD_SAMPLES:
        return FIELD_SAMPLES[field_name]
    return TYPE_DEFAULTS.get(field_type, 'example')


def yaml_value(val):
    if isinstance(val, bool):
        return 'true' if val else 'false'
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, list):
        if not val:
            return '[]'
        return val  # handled specially in format_config
    if isinstance(val, str):
        if val.startswith('"') and val.endswith('"'):
            return val
        if any(c in val for c in ':{}[]#&*!|>\',@'):
            return f'"{val}"'
        return val
    return str(val)


def format_config(items, base_indent=6):
    """Format a YAML config list item with correct indentation."""
    if not items:
        return f'{" " * base_indent}- name: example'

    pad_first = ' ' * base_indent
    pad_rest = ' ' * (base_indent + 2)
    lines = []

    for i, (key, val) in enumerate(items):
        prefix = f'{pad_first}- ' if i == 0 else f'{pad_rest}'
        if isinstance(val, list) and val:
            lines.append(f'{prefix}{key}:')
            tag_pad = pad_rest + '  ' if i > 0 else pad_first + '    '
            for v in val:
                lines.append(f'{tag_pad}- {yaml_value(v)}')
        else:
            lines.append(f'{prefix}{key}: {yaml_value(val)}')

    return '\n'.join(lines)


def parse_action_keys(module_name: str) -> dict:
    """Parse CANONICAL_KEY and SYSTEM_KEY from the corresponding action plugin."""
    action_file = ACTION_DIR / f'{module_name}.py'
    if not action_file.exists():
        return {}
    source = action_file.read_text()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {}
    result = {'CANONICAL_KEY': None, 'SYSTEM_KEY': None}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == 'ActionModule':
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name) and target.id in result:
                            if isinstance(item.value, ast.Constant):
                                result[target.id] = item.value.value
            break
    return result


def build_items(subopts, replaced=False, max_fields=8, system_key=None,
                canonical_key=None, response_only=None):
    """Build (key, value) pairs from suboptions, skipping the system key."""
    items = []
    skip = response_only or set()
    for fname, fspec in subopts.items():
        if fname == system_key or fname in skip:
            continue
        ftype = fspec.get('type', 'str')
        choices = fspec.get('choices')
        if ftype == 'dict' and fname not in FIELD_SAMPLES:
            continue
        if ftype == 'list' and fname not in FIELD_SAMPLES:
            continue
        use_replaced = replaced and fname != canonical_key
        items.append((fname, sample_value(fname, ftype, choices, replaced=use_replaced)))
        if len(items) >= max_fields:
            break
    return items


def id_items(subopts, canonical_key=None, system_key=None):
    """Extract identity fields for delete operations using the canonical key."""
    if canonical_key and canonical_key in subopts:
        fspec = subopts[canonical_key]
        return [(canonical_key, sample_value(canonical_key, fspec.get('type', 'str'),
                                             choices=fspec.get('choices')))]

    items = []
    for fname, fspec in subopts.items():
        if fname == system_key:
            continue
        if fspec.get('required') or fname.endswith('_id') or fname == 'number':
            items.append((fname, sample_value(fname, fspec.get('type', 'str'),
                                              choices=fspec.get('choices'))))
            if len(items) >= 2:
                break
    if not items:
        first = next((k for k in subopts if k != system_key), None)
        if first:
            fspec = subopts[first]
            ftype = fspec.get('type', 'str')
            if ftype in ('list', 'dict'):
                return items
            items.append((first, sample_value(first, ftype,
                                              choices=fspec.get('choices'))))
    return items


def parse_module(filepath):
    content = filepath.read_text()
    m = re.search(r"DOCUMENTATION\s*=\s*r?'''(.*?)'''", content, re.DOTALL)
    if not m:
        return None
    try:
        doc = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None

    opts = doc.get('options', {})
    module_name = doc.get('module', filepath.stem)
    scope = None
    scope_value = None
    state_choices = []
    config_subopts = {}
    is_facts = False

    for k, v in opts.items():
        if k in ('network_id', 'organization_id', 'serial'):
            scope = k
            scope_value = FIELD_SAMPLES.get(k, 'N_12345')
        elif k == 'state':
            state_choices = v.get('choices', ['merged', 'gathered'])
        elif k == 'config':
            config_subopts = v.get('suboptions', {})
        elif k == 'gather_subset':
            is_facts = True

    if not scope and is_facts:
        scope = 'organization_id'
        scope_value = '123456'

    action_keys = parse_action_keys(module_name)

    return {
        'module_name': module_name,
        'fqcn': f'cisco.meraki_rm.{module_name}',
        'scope': scope,
        'scope_value': scope_value,
        'state_choices': state_choices,
        'config_subopts': config_subopts,
        'is_facts': is_facts,
        'short_desc': doc.get('short_description', module_name),
        'canonical_key': action_keys.get('CANONICAL_KEY'),
        'system_key': action_keys.get('SYSTEM_KEY'),
        'response_only': RESPONSE_ONLY_FIELDS.get(module_name, set()),
    }


# ── Shared assertion block (subset-style via path_contained_in filter) ──

ASSERT_BLOCK = """\
- name: Compare expected paths to result (subset check)
  ansible.builtin.set_fact:
    path_check: "{{{{ expected_paths | cisco.meraki_rm.path_contained_in(result_paths) }}}}"
  vars:
    expected_paths: "{{{{ expected_config | ansible.utils.to_paths }}}}"
    result_paths: "{{{{ {result_var}.config[0] | ansible.utils.to_paths }}}}"

- name: Assert all expected fields are present and match
  ansible.builtin.assert:
    that: path_check.contained | bool
    success_msg: "{{{{ success_msg }}}}"
    fail_msg: "{{{{ fail_msg }}}}"
  vars:
    success_msg: "All expected fields match. Extras: {{{{ path_check.extras }}}}"
    fail_msg: "Missing or mismatch: {{{{ path_check.missing }}}}. Extras: {{{{ path_check.extras }}}}"
"""


def format_set_fact(items, indent=4):
    """Format items as a set_fact YAML block."""
    pad = ' ' * indent
    lines = [f'{pad}expected_config:']
    for key, val in items:
        formatted = yaml_value(val)
        if isinstance(val, list) and val:
            lines.append(f'{pad}  {key}:')
            for v in val:
                lines.append(f'{pad}    - {yaml_value(v)}')
        else:
            lines.append(f'{pad}  {key}: {formatted}')
    return '\n'.join(lines)


def assert_block(result_var):
    """Return the to_paths assertion block for a given result variable."""
    return ASSERT_BLOCK.format(result_var=result_var)


# ── Per-state file generators ───────────────────────────────────────

def gen_merged(meta):
    fqcn, scope, sv = meta['fqcn'], meta['scope'], meta['scope_value']
    short = meta['short_desc']
    items = build_items(meta['config_subopts'], system_key=meta.get('system_key'),
                        canonical_key=meta.get('canonical_key'),
                        response_only=meta.get('response_only'))
    fact_block = format_set_fact(items)
    return f"""---
# {short} — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
{fact_block}

- name: Create {meta['module_name'].replace('meraki_', '')} with merged state
  {fqcn}:
    {scope}: "{sv}"
    state: merged
    config:
      - "{{{{ expected_config }}}}"
  register: merge_result

- name: Assert resource was created
  ansible.builtin.assert:
    that:
      - merge_result is changed
      - merge_result.config | length == 1

{assert_block('merge_result')}"""


def gen_replaced(meta):
    fqcn, scope, sv = meta['fqcn'], meta['scope'], meta['scope_value']
    short = meta['short_desc']
    items = build_items(meta['config_subopts'], replaced=True, system_key=meta.get('system_key'),
                        canonical_key=meta.get('canonical_key'),
                        response_only=meta.get('response_only'))
    fact_block = format_set_fact(items)
    return f"""---
# {short} — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
{fact_block}

- name: Replace {meta['module_name'].replace('meraki_', '')} configuration
  {fqcn}:
    {scope}: "{sv}"
    state: replaced
    config:
      - "{{{{ expected_config }}}}"
  register: replace_result

- name: Assert resource was replaced
  ansible.builtin.assert:
    that:
      - replace_result is changed
      - replace_result.config | length == 1

{assert_block('replace_result')}"""


def gen_overridden(meta):
    fqcn, scope, sv = meta['fqcn'], meta['scope'], meta['scope_value']
    short = meta['short_desc']
    items = build_items(meta['config_subopts'], replaced=True, system_key=meta.get('system_key'),
                        canonical_key=meta.get('canonical_key'),
                        response_only=meta.get('response_only'))
    fact_block = format_set_fact(items)
    return f"""---
# {short} — override all instances
# Ensures ONLY these resources exist; any not listed are deleted.

- name: Define desired-state configuration
  ansible.builtin.set_fact:
{fact_block}

- name: Override all {meta['module_name'].replace('meraki_', '')} — desired state only
  {fqcn}:
    {scope}: "{sv}"
    state: overridden
    config:
      - "{{{{ expected_config }}}}"
  register: override_result

- name: Assert resources were overridden
  ansible.builtin.assert:
    that:
      - override_result is changed
      - override_result.config | length == 1

{assert_block('override_result')}"""


def gen_gathered(meta):
    fqcn, scope, sv = meta['fqcn'], meta['scope'], meta['scope_value']
    short = meta['short_desc']
    return f"""---
# {short} — gather current configuration

- name: Gather current {meta['module_name'].replace('meraki_', '')} configuration
  {fqcn}:
    {scope}: "{sv}"
    state: gathered
  register: gathered

- name: Assert gathered config is not empty
  ansible.builtin.assert:
    that:
      - gathered.config is defined
      - gathered.config | length > 0
    fail_msg: "Gathered config is empty — expected at least one resource"

- name: Display gathered configuration
  ansible.builtin.debug:
    var: gathered.config
"""


def gen_deleted(meta):
    fqcn, scope, sv = meta['fqcn'], meta['scope'], meta['scope_value']
    short = meta['short_desc']
    items = id_items(meta['config_subopts'],
                     canonical_key=meta.get('canonical_key'),
                     system_key=meta.get('system_key'))
    fact_block = format_set_fact(items)
    return f"""---
# {short} — remove configuration

- name: Define resource to delete
  ansible.builtin.set_fact:
{fact_block}

- name: Delete {meta['module_name'].replace('meraki_', '')} configuration
  {fqcn}:
    {scope}: "{sv}"
    state: deleted
    config:
      - "{{{{ expected_config }}}}"
  register: delete_result

- name: Assert resource was deleted
  ansible.builtin.assert:
    that:
      - delete_result is changed
      - delete_result is not failed
"""


def gen_facts(meta):
    sv = meta['scope_value']
    fqcn = meta['fqcn']
    return {
        'gathered': f"""---
# Gather all Meraki facts

- name: Gather all Meraki facts
  {fqcn}:
    organization_id: "{sv}"
    gather_subset:
      - all
  register: all_facts

- name: Display gathered facts
  ansible.builtin.debug:
    var: all_facts

- name: Gather only organization info
  {fqcn}:
    organization_id: "{sv}"
    gather_subset:
      - organizations

- name: Gather networks for a specific org
  {fqcn}:
    organization_id: "{sv}"
    gather_subset:
      - networks
""",
    }


STATE_GENERATORS = {
    'merged': gen_merged,
    'replaced': gen_replaced,
    'overridden': gen_overridden,
    'gathered': gen_gathered,
    'deleted': gen_deleted,
}


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--check', action='store_true',
                        help='Dry-run: report what would be generated without writing files')
    args = parser.parse_args()

    dry_run = args.check
    prefix = 'DRY RUN — ' if dry_run else ''

    module_files = sorted(MODULES_DIR.glob('meraki_*.py'))
    created = 0
    modules = 0
    errors = []

    for mf in module_files:
        meta = parse_module(mf)
        if not meta:
            errors.append(f'  SKIP {mf.name}: could not parse DOCUMENTATION')
            continue

        dir_name = mf.stem.replace('meraki_', '')
        module_dir = EXAMPLES_DIR / dir_name
        if not dry_run:
            module_dir.mkdir(parents=True, exist_ok=True)
        modules += 1

        if meta['is_facts']:
            files = gen_facts(meta)
            for state_name, content in files.items():
                if not dry_run:
                    (module_dir / f'{state_name}.yml').write_text(content)
                created += 1
            print(f'  OK {dir_name}/ (gathered)')
            continue

        states = meta['state_choices']
        generated_states = []

        for state in ['merged', 'replaced', 'overridden', 'gathered', 'deleted']:
            if state in states:
                gen_fn = STATE_GENERATORS[state]
                content = gen_fn(meta)
                if not dry_run:
                    (module_dir / f'{state}.yml').write_text(content)
                created += 1
                generated_states.append(state)

        if not dry_run:
            for old in module_dir.glob('*.yml'):
                if old.stem not in generated_states:
                    old.unlink()

        print(f'  OK {dir_name}/ ({", ".join(generated_states)})')

    print(f'\n{"="*60}')
    verb = 'Would create' if dry_run else 'Created'
    print(f'{prefix}{verb}: {created} state files across {modules} modules')
    if errors:
        print(f'\nErrors ({len(errors)}):')
        for e in errors:
            print(e)
    return 0


if __name__ == '__main__':
    sys.exit(main())
