#!/usr/bin/env python3
"""Generate User Model dataclasses from DOCUMENTATION strings.

User Models use snake_case field names and are the stable, presentation-layer
independent interface for each resource module. They are generated from the
DOCUMENTATION YAML string that defines the Ansible module's argument spec.

Usage:
    python -m tools.generators.generate_user_dataclasses \\
        --docs-dir plugins/plugin_utils/docs/ \\
        --output plugins/plugin_utils/user_models/

    python -m tools.generators.generate_user_dataclasses \\
        --docs-dir plugins/plugin_utils/docs/ \\
        --output plugins/plugin_utils/user_models/ \\
        --module vlan
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


# Type mapping from Ansible argument spec types to Python types
_ANSIBLE_TYPE_MAP = {
    'str': 'str',
    'int': 'int',
    'float': 'float',
    'bool': 'bool',
    'list': 'List[Any]',
    'dict': 'Dict[str, Any]',
    'raw': 'Any',
    'path': 'str',
    'jsonarg': 'str',
}


def _extract_documentation(filepath: Path) -> Optional[str]:
    """Extract DOCUMENTATION string from a Python module file.

    Looks for:
        DOCUMENTATION = '''...'''
    or:
        DOCUMENTATION = \"\"\"...\"\"\"

    Args:
        filepath: Path to the Python file containing DOCUMENTATION

    Returns:
        The DOCUMENTATION string, or None if not found
    """
    content = filepath.read_text()

    # Match DOCUMENTATION = r'''...''' or DOCUMENTATION = '''...'''
    pattern = r"DOCUMENTATION\s*=\s*r?(?:'''|\"\"\")(.*?)(?:'''|\"\"\")"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()

    return None


def _parse_options(
    options: Dict[str, Any],
    prefix: str = '',
) -> List[Tuple[str, str, str, bool, Any]]:
    """Recursively parse options into field definitions.

    Args:
        options: The 'options' dict from DOCUMENTATION
        prefix: Prefix for nested fields (dot-delimited)

    Returns:
        List of (field_name, python_type, description, required, default)
    """
    fields = []

    for opt_name, opt_spec in options.items():
        if not isinstance(opt_spec, dict):
            continue

        full_name = f'{prefix}{opt_name}' if not prefix else f'{prefix}.{opt_name}'
        ansible_type = opt_spec.get('type', 'str')
        description = opt_spec.get('description', '')
        if isinstance(description, list):
            description = ' '.join(description)
        required = opt_spec.get('required', False)
        default = opt_spec.get('default')

        # Map type
        python_type = _ANSIBLE_TYPE_MAP.get(ansible_type, 'Any')

        # Handle list elements
        if ansible_type == 'list':
            elements = opt_spec.get('elements', 'str')
            if elements == 'dict':
                python_type = 'List[Dict[str, Any]]'
            else:
                inner = _ANSIBLE_TYPE_MAP.get(elements, 'Any')
                python_type = f'List[{inner}]'

        fields.append((opt_name, python_type, description, required, default))

        # Recurse into suboptions
        suboptions = opt_spec.get('suboptions') or opt_spec.get('options')
        if suboptions and isinstance(suboptions, dict):
            # Sub-options generate nested fields but we keep them flat
            # for the dataclass (the transform mixin handles nesting)
            pass

    return fields


def generate_user_dataclass(
    module_name: str,
    documentation: str,
) -> str:
    """Generate a User Model dataclass from a DOCUMENTATION string.

    Args:
        module_name: Module name (e.g., 'vlan')
        documentation: DOCUMENTATION YAML string

    Returns:
        Python source code for the User Model dataclass
    """
    doc_data = yaml.safe_load(documentation)
    options = doc_data.get('options', {})

    # Class name: UserVlan, UserSsid, UserSwitchPort, etc.
    class_name = 'User' + ''.join(
        part.capitalize() for part in module_name.split('_')
    )

    fields = _parse_options(options)

    # Sort: required first, then alphabetical
    fields.sort(key=lambda f: (not f[3], f[0]))

    lines = [
        f'"""User Model dataclass for Meraki {module_name} resource module.',
        '',
        'Generated from DOCUMENTATION string.',
        'Regenerate using:',
        '    python -m tools.generators.generate_user_dataclasses',
        '"""',
        '',
        'from __future__ import annotations',
        '',
        'from dataclasses import dataclass',
        'from typing import Any, Dict, List, Optional',
        '',
        'from ..platform.base_transform import BaseTransformMixin',
        '',
        '',
        '@dataclass',
        f'class {class_name}(BaseTransformMixin):',
        f'    """User Model for Meraki {module_name} resource.',
        '',
        '    Fields use snake_case matching Ansible conventions.',
        '    Transform mixins convert to/from API camelCase.',
        '    """',
        '',
    ]

    for field_name, py_type, desc, required, default in fields:
        if desc:
            desc_clean = desc.replace('\n', ' ').strip()
            if len(desc_clean) > 76:
                desc_clean = desc_clean[:73] + '...'
            lines.append(f'    # {desc_clean}')

        if required:
            lines.append(f'    {field_name}: {py_type}')
        else:
            if default is not None:
                if isinstance(default, str):
                    lines.append(f'    {field_name}: Optional[{py_type}] = {default!r}')
                elif isinstance(default, bool):
                    lines.append(f'    {field_name}: Optional[{py_type}] = {default}')
                else:
                    lines.append(f'    {field_name}: Optional[{py_type}] = {default!r}')
            else:
                lines.append(f'    {field_name}: Optional[{py_type}] = None')

    lines.append('')
    return '\n'.join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Generate User Model dataclasses from DOCUMENTATION strings'
    )
    parser.add_argument(
        '--docs-dir', required=True,
        help='Directory containing module doc files with DOCUMENTATION strings',
    )
    parser.add_argument(
        '--output', required=True,
        help='Output directory for generated User Model files',
    )
    parser.add_argument(
        '--module',
        help='Generate only this module (e.g., "vlan")',
    )
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not docs_dir.exists():
        print(f"Error: docs directory not found: {docs_dir}", file=sys.stderr)
        sys.exit(1)

    doc_files = sorted(docs_dir.glob('*.py'))
    if args.module:
        doc_files = [f for f in doc_files if f.stem == args.module]

    if not doc_files:
        print("No documentation files found.", file=sys.stderr)
        sys.exit(1)

    for doc_file in doc_files:
        if doc_file.name.startswith('_'):
            continue

        module_name = doc_file.stem
        print(f"Processing {module_name}...")

        documentation = _extract_documentation(doc_file)
        if not documentation:
            print(f"  Warning: no DOCUMENTATION found in {doc_file}", file=sys.stderr)
            continue

        code = generate_user_dataclass(module_name, documentation)
        output_file = output_dir / f'{module_name}.py'
        output_file.write_text(code)
        print(f"  Wrote {output_file}")

    print("Done.")


if __name__ == '__main__':
    main()
