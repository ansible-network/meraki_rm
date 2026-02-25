# Code Generators — Complete Implementation Guide

This document covers the **code generation tools** that automate creation of dataclasses from documentation strings and OpenAPI specs. It uses **NovaCom Networks** as the example throughout: a cloud-managed network infrastructure provider with the NovaCom Dashboard API (collection namespace: `novacom.dashboard`).

**Audience**: Framework developers setting up code generation infrastructure

**Related Documents**:
- [06-foundation-components.md](06-foundation-components.md) — Core framework components
- [07-adding-resources.md](07-adding-resources.md) — Using these tools to add new features

---

## Table of Contents

1. [Code Generation Strategy](#section-1-code-generation-strategy)
2. [User Model Dataclass Generator](#section-2-user-model-dataclass-generator)
3. [API Dataclass Generator (Device Models)](#section-3-api-dataclass-generator-device-models)
3B. [Field Description Sync Generator](#section-3b-field-description-sync-generator)
4. [Usage Examples](#section-4-usage-examples)
5. [Verification Checklist](#section-5-verification-checklist)
6. [CI/CD Integration](#section-6-cicd-integration)
7. [Integration with Feature Workflow](#section-7-integration-with-feature-workflow)

---

## SECTION 1: Code Generation Strategy

### What Gets Generated vs What Requires Manual Work

| Component | Generated From | Output Location | Frequency |
|-----------|---------------|-----------------|-----------|
| User Model Dataclass | DOCUMENTATION string | `plugins/plugin_utils/user_models/` | Once per module |
| Device Model Dataclass | OpenAPI spec | `plugins/plugin_utils/api/v{X}/generated/` | Once per API version |
| Transform Mixin skeleton | Manual template | `plugins/plugin_utils/api/v{X}/` | Once per module+version |

### What Requires Manual Work

- **Field mapping** in transform mixins
- **Custom transformation functions** (names ↔ IDs)
- **Endpoint operations configuration**
- **Business logic validation**

### Generation Workflow Diagram (Text-Based)

```
Write docstring (DOCUMENTATION)
           │
           ▼
Generate User Model (auto)
           │
           ▼
Generate API models from OpenAPI (auto)
           │
           ▼
Create Transform Mixin (manual)
           │
           ▼
Test & refine
```

---

## SECTION 2: User Model Dataclass Generator

### Tool: `generate_user_dataclasses.py`

**Location**: `tools/generators/generate_user_dataclasses.py`

**Purpose**: Parse DOCUMENTATION strings and generate typed Python dataclasses that represent the user-facing data model.

### Complete Implementation

```python
"""Generate user-facing dataclasses from DOCUMENTATION strings.

This script parses module documentation (DOCUMENTATION blocks) and generates
strongly-typed Python dataclasses that represent the user-facing data model.
These dataclasses are the stable interface that crosses the RPC boundary.

Used by: novacom.dashboard collection (NovaCom Dashboard API)
"""

import yaml
import argparse
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class FieldSpec:
    """Specification for a single field in the generated dataclass.

    Attributes:
        name: Field name (snake_case).
        python_type: Python type annotation string (e.g., 'str', 'List[str]').
        required: Whether the field is required (no default).
        description: Docstring description for the field.
        default: Default value as Python code string, or None.
    """
    name: str
    python_type: str
    required: bool
    description: str
    default: Optional[str] = None


class UserDataclassGenerator:
    """
    Generator for user-facing dataclasses from DOCUMENTATION strings.

    Parses YAML-structured DOCUMENTATION blocks (Ansible-style) and produces
    Python dataclasses with proper typing, docstrings, and BaseTransformMixin
    inheritance.

    Attributes:
        nested_classes: Accumulated nested class code during generation.
    """

    # Type mapping: documentation type -> Python type
    TYPE_MAPPING = {
        'str': 'str',
        'int': 'int',
        'float': 'float',
        'bool': 'bool',
        'list': 'List',
        'dict': 'Dict',
        'path': 'str',
        'raw': 'Any',
        'jsonarg': 'Dict',
    }

    def __init__(self) -> None:
        """Initialize generator with empty nested classes list."""
        self.nested_classes: List[str] = []

    def parse_documentation(self, doc_string: str) -> Dict[str, Any]:
        """
        Parse DOCUMENTATION YAML string into a dictionary.

        Args:
            doc_string: Raw DOCUMENTATION string from module (YAML format).

        Returns:
            Parsed documentation dict with keys: module, short_description,
            options, etc.

        Raises:
            yaml.YAMLError: If YAML parsing fails.
        """
        return yaml.safe_load(doc_string)

    def generate_from_file(self, doc_file: Path, output_file: Path) -> None:
        """
        Generate dataclass from a file containing DOCUMENTATION.

        Reads the file, extracts the DOCUMENTATION block via regex, parses it,
        and writes the generated Python code to output_file.

        Args:
            doc_file: Path to file containing DOCUMENTATION block.
            output_file: Path to output Python file.

        Raises:
            ValueError: If no DOCUMENTATION block found in file.
        """
        content = doc_file.read_text()

        # Extract DOCUMENTATION string (handles triple-quoted and single-quoted)
        doc_match = re.search(
            r'DOCUMENTATION\s*=\s*["\']+(.*?)["\']',
            content,
            re.DOTALL
        )

        if not doc_match:
            raise ValueError(f"No DOCUMENTATION found in {doc_file}")

        doc_string = doc_match.group(1)

        doc_data = self.parse_documentation(doc_string)
        module_name = doc_data.get('module', doc_file.stem)

        generated_code = self.generate_dataclass(module_name, doc_data)

        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(generated_code)
        print(f"Generated {output_file}")

    def generate_dataclass(
        self,
        module_name: str,
        doc_data: Dict[str, Any]
    ) -> str:
        """
        Generate dataclass code from parsed documentation.

        Args:
            module_name: Module name (e.g., 'admin', 'site').
            doc_data: Parsed documentation dict.

        Returns:
            Complete Python source code as string.
        """
        self.nested_classes = []

        options = doc_data.get('options', {})
        fields = self._build_fields(options, prefix='')

        class_name = f'User{module_name.title().replace("_", "")}'

        code_parts = []

        # Header comment
        code_parts.append('"""Generated User model dataclass.')
        code_parts.append('')
        code_parts.append(f'Auto-generated from {module_name} module DOCUMENTATION.')
        code_parts.append('DO NOT EDIT MANUALLY - regenerate using tools/generators/')
        code_parts.append('"""')
        code_parts.append('')
        code_parts.append('from dataclasses import dataclass')
        code_parts.append('from typing import Optional, List, Dict, Any')
        code_parts.append('')
        code_parts.append('from ..platform.base_transform import BaseTransformMixin')
        code_parts.append('')
        code_parts.append('')

        # Nested classes first (child before parent)
        for nested_code in self.nested_classes:
            code_parts.append(nested_code)
            code_parts.append('')

        # Main class
        code_parts.append('@dataclass')
        code_parts.append(f'class {class_name}(BaseTransformMixin):')
        code_parts.append('    """')
        description = doc_data.get('short_description', f'{module_name.replace("_", " ").title()} resource')
        code_parts.append(f'    {description}')
        code_parts.append('    ')
        code_parts.append('    This dataclass represents the user-facing data model.')
        code_parts.append('    It is the stable interface that crosses the RPC boundary.')
        code_parts.append('    ')
        code_parts.append('    Attributes:')
        for field in fields:
            code_parts.append(f'        {field.name}: {field.description}')
        code_parts.append('    """')
        code_parts.append('    ')

        # Fields: required first, then optional with defaults
        for field in fields:
            field_line = f'    {field.name}: '
            if not field.required:
                field_line += 'Optional['
            field_line += field.python_type
            if not field.required:
                field_line += ']'
            if field.default is not None:
                field_line += f' = {field.default}'
            elif not field.required:
                field_line += ' = None'
            code_parts.append(field_line)

        return '\n'.join(code_parts)

    def _build_fields(
        self,
        options: Dict[str, Any],
        prefix: str = ''
    ) -> List[FieldSpec]:
        """
        Build field specifications from options dict.

        Handles nested suboptions by generating nested dataclasses and
        registering them in self.nested_classes.

        Args:
            options: Options dict from DOCUMENTATION (key = field name).
            prefix: Prefix for nested class names.

        Returns:
            List of FieldSpec objects, required fields first.
        """
        fields = []
        for field_name, field_spec in options.items():
            field_type = field_spec.get('type', 'str')
            required = field_spec.get('required', False)
            description = field_spec.get('description', '')
            default = field_spec.get('default')

            if isinstance(description, list):
                description = ' '.join(description)

            python_type = self._map_type(field_type, field_spec)

            if 'suboptions' in field_spec:
                nested_class_name = f'{prefix}{field_name.replace("_", " ").title().replace(" ", "")}'
                nested_fields = self._build_fields(
                    field_spec['suboptions'],
                    prefix=nested_class_name
                )
                nested_code = self._generate_nested_class(
                    nested_class_name,
                    nested_fields
                )
                self.nested_classes.append(nested_code)

                if field_type == 'list':
                    elements = field_spec.get('elements', 'dict')
                    if elements == 'dict':
                        python_type = f'List[{nested_class_name}]'
                    else:
                        elem_type = self.TYPE_MAPPING.get(elements, 'Any')
                        python_type = f'List[{elem_type}]'
                else:
                    python_type = nested_class_name

            formatted_default = self._format_default(default)
            field = FieldSpec(
                name=field_name,
                python_type=python_type,
                required=required,
                description=description,
                default=formatted_default
            )
            fields.append(field)

        # Sort: required first, then optional
        fields.sort(key=lambda f: (f.required, f.name), reverse=True)
        return fields

    def _map_type(self, ansible_type: str, field_spec: Dict[str, Any]) -> str:
        """
        Map documentation type to Python type string.

        Args:
            ansible_type: Type from DOCUMENTATION (str, list, dict, etc.).
            field_spec: Full field specification for elements/suboptions.

        Returns:
            Python type annotation string.
        """
        base_type = self.TYPE_MAPPING.get(ansible_type, 'Any')

        if ansible_type == 'list':
            elements = field_spec.get('elements', 'str')
            element_type = self.TYPE_MAPPING.get(elements, 'Any')
            return f'List[{element_type}]'

        if ansible_type == 'dict':
            return 'Dict[str, Any]'

        return base_type

    def _generate_nested_class(
        self,
        class_name: str,
        fields: List[FieldSpec]
    ) -> str:
        """
        Generate nested dataclass code.

        Args:
            class_name: Name of nested class.
            fields: List of field specifications.

        Returns:
            Generated class code as string.
        """
        lines = []
        lines.append('@dataclass')
        lines.append(f'class {class_name}:')
        lines.append('    """Nested dataclass for structured option."""')
        lines.append('    ')

        for field in fields:
            field_line = f'    {field.name}: '
            if not field.required:
                field_line += 'Optional['
            field_line += field.python_type
            if not field.required:
                field_line += ']'
            if field.default is not None:
                field_line += f' = {field.default}'
            elif not field.required:
                field_line += ' = None'
            lines.append(field_line)

        return '\n'.join(lines)

    def _format_default(self, default: Any) -> Optional[str]:
        """
        Format default value for Python code.

        Args:
            default: Default value from documentation.

        Returns:
            Formatted string for Python source, or None.
        """
        if default is None:
            return None
        if isinstance(default, bool):
            return str(default)
        if isinstance(default, (int, float)):
            return str(default)
        if isinstance(default, str):
            return f"'{default}'"
        return repr(default)


def main() -> None:
    """Main entry point with argparse."""
    parser = argparse.ArgumentParser(
        description='Generate user dataclasses from DOCUMENTATION strings'
    )
    parser.add_argument(
        'doc_file',
        type=Path,
        help='Path to file containing DOCUMENTATION block'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=None,
        help='Output file path (default: infer from module name)'
    )

    args = parser.parse_args()

    if args.output is None:
        module_name = args.doc_file.stem
        output_dir = Path('plugins/plugin_utils/user_models')
        output_dir.mkdir(parents=True, exist_ok=True)
        args.output = output_dir / f'{module_name}.py'

    generator = UserDataclassGenerator()
    generator.generate_from_file(args.doc_file, args.output)


if __name__ == '__main__':
    main()
```

### Usage

```bash
python tools/generators/generate_user_dataclasses.py \
    plugins/plugin_utils/docs/admin.py \
    --output plugins/plugin_utils/user_models/admin.py
```

---

## SECTION 3: API Dataclass Generator (Device Models)

### Tool: datamodel-code-generator (Third-Party)

**Installation**:
```bash
pip install datamodel-code-generator
```

### Why This Tool

- **Industry standard** for OpenAPI → Python
- **Handles complex schemas** (nested, oneOf, allOf)
- **Generates dataclass models** (not just Pydantic)
- **Well-maintained** and widely used

### Wrapper Script: `generate_api_models.sh`

**Location**: `tools/generators/generate_api_models.sh`

### Complete Script

```bash
#!/bin/bash
# Generate API dataclasses from OpenAPI specs
#
# Uses datamodel-code-generator to produce Python dataclasses from
# NovaCom Dashboard API OpenAPI specifications.
#
# Prerequisites:
#   pip install datamodel-code-generator
#
# Usage:
#   Place OpenAPI specs in tools/openapi_specs/ (novacom-v1.json, novacom-v2.json)
#   cd novacom.dashboard && bash tools/generators/generate_api_models.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SPECS_DIR="$SCRIPT_DIR/../openapi_specs"
OUTPUT_BASE="$PROJECT_ROOT/plugins/plugin_utils/api"

echo "Generating API dataclasses from OpenAPI specs..."
echo "Specs dir: $SPECS_DIR"
echo "Output base: $OUTPUT_BASE"
echo ""

if [ ! -d "$SPECS_DIR" ]; then
    echo "Error: Specs directory not found: $SPECS_DIR"
    echo "Create it and add novacom-v1.json, novacom-v2.json, etc."
    exit 1
fi

for spec_file in "$SPECS_DIR"/novacom-v*.json; do
    if [ ! -f "$spec_file" ]; then
        echo "No OpenAPI specs found matching novacom-v*.json in $SPECS_DIR"
        exit 1
    fi

    filename=$(basename "$spec_file")
    version=$(echo "$filename" | sed -E 's/novacom-v([0-9]+(_[0-9]+)?)\.json/\1/')

    echo "Processing $filename (version $version)..."

    output_dir="$OUTPUT_BASE/v${version}/generated"
    mkdir -p "$output_dir"

    datamodel-codegen \
        --input "$spec_file" \
        --input-file-type openapi \
        --output "$output_dir/models.py" \
        --output-model-type dataclasses.dataclass \
        --field-constraints \
        --use-standard-collections \
        --use-schema-description \
        --use-title-as-name \
        --target-python-version 3.9 \
        --collapse-root-models \
        --disable-timestamp

    # Prepend header comment
    temp_file=$(mktemp)
    cat > "$temp_file" << 'HEADER'
"""Generated API dataclasses from OpenAPI specification.

Auto-generated using datamodel-code-generator.
DO NOT EDIT MANUALLY - regenerate using tools/generators/generate_api_models.sh

These are pure API data models. To add transformation logic, create a
companion file (e.g., admin.py) with a TransformMixin that inherits from
BaseTransformMixin.
"""

HEADER
    cat "$output_dir/models.py" >> "$temp_file"
    mv "$temp_file" "$output_dir/models.py"

    # Create __init__.py
    cat > "$output_dir/__init__.py" << 'INIT'
"""Generated API models for NovaCom Dashboard API."""
from .models import *

INIT

    echo "  Generated: $output_dir/models.py"
done

echo ""
echo "API dataclass generation complete!"
echo ""
echo "Next steps:"
echo "  1. Review generated files in plugins/plugin_utils/api/"
echo "  2. Create transform mixins for each resource"
echo "  3. Import generated classes in your transform mixin files"
```

### Usage

```bash
# Place OpenAPI specs in tools/openapi_specs/
# novacom-v1.json, novacom-v2.json

cd novacom.dashboard
bash tools/generators/generate_api_models.sh
```

---

## SECTION 3B: Field Description Sync Generator

### Tool: `generate_model_descriptions.py`

**Location**: `tools/generate_model_descriptions.py`

**Purpose**: Sync field descriptions from module `DOCUMENTATION` YAML strings into User Model dataclass `field(metadata={"description": "..."})` annotations. This keeps the User Model self-describing — the MCP server reads these descriptions at runtime to populate tool input schemas.

### How It Works

1. Scans `plugins/modules/meraki_*.py` for `DOCUMENTATION` assignments
2. Extracts per-field descriptions from `options.config.suboptions`
3. Reads the corresponding action plugin to find the `USER_MODEL` path
4. Rewrites the User Model file, transforming bare field defaults:

```python
# Before
name: Optional[str] = None

# After
name: Optional[str] = field(default=None, metadata={"description": "VLAN name."})
```

### Usage

```bash
python tools/generate_model_descriptions.py
```

The tool is **idempotent**: running it again updates existing descriptions if the `DOCUMENTATION` string has changed, and leaves already-current fields untouched.

### Why This Exists

Module `DOCUMENTATION` strings define field descriptions for `ansible-doc` but are not accessible at Python import time (they are string constants in module files, not importable metadata). The MCP server needs descriptions when generating JSON Schema tool definitions. This generator bridges the gap by copying descriptions into the dataclass `field(metadata=...)` where they are available via `dataclasses.fields()`.

---

## SECTION 4: Usage Examples

### Example 1: Generate NovaCom Admin Dataclasses

#### Step 1: Create docs file with DOCUMENTATION

```python
# plugins/plugin_utils/docs/admin.py

DOCUMENTATION = """
---
module: novacom_organization_admin
short_description: Manage NovaCom organization administrators
description:
  - Create, update, or delete NovaCom organization admin users
  - Manage admin attributes and RBAC permissions
options:
  username:
    description: Username for the admin
    required: true
    type: str
  email:
    description: Email address
    type: str
  name:
    description: Full name of the admin
    type: str
  org_access:
    description: Organization access level
    type: str
    choices: ['full', 'read-only', 'none']
  tags:
    description:
      - List of network tag-based access permissions
    type: list
    elements: dict
    suboptions:
      tag:
        description: Network tag
        type: str
      access:
        description: Access level for this tag
        type: str
  networks:
    description:
      - List of network-level access permissions
    type: list
    elements: dict
    suboptions:
      network_id:
        description: Network identifier
        type: str
      access:
        description: Access level for this network
        type: str
  organizations:
    description:
      - List of organization names (NOT IDs)
    type: list
    elements: str
  id:
    description:
      - Admin ID (read-only, returned after creation)
    type: str
  created_at:
    description:
      - Creation timestamp (read-only)
    type: str
"""
```

#### Step 2: Generate user model dataclass

```bash
python tools/generators/generate_user_dataclasses.py \
    plugins/plugin_utils/docs/admin.py \
    --output plugins/plugin_utils/user_models/admin.py
```

#### Step 3: Generated output

```python
"""Generated User model dataclass.

Auto-generated from admin module DOCUMENTATION.
DO NOT EDIT MANUALLY - regenerate using tools/generators/
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from ..platform.base_transform import BaseTransformMixin


@dataclass
class Tags:
    """Nested dataclass for structured option."""
    tag: Optional[str] = None
    access: Optional[str] = None


@dataclass
class Networks:
    """Nested dataclass for structured option."""
    network_id: Optional[str] = None
    access: Optional[str] = None


@dataclass
class UserAdmin(BaseTransformMixin):
    """
    Manage NovaCom organization administrators

    This dataclass represents the user-facing data model.
    It is the stable interface that crosses the RPC boundary.

    Attributes:
        username: Username for the admin
        email: Email address
        name: Full name of the admin
        org_access: Organization access level
        tags: List of network tag-based access permissions
        networks: List of network-level access permissions
        organizations: List of organization names (NOT IDs)
        id: Admin ID (read-only, returned after creation)
        created_at: Creation timestamp (read-only)
    """

    username: str
    email: Optional[str] = None
    name: Optional[str] = None
    org_access: Optional[str] = None
    tags: Optional[List[Tags]] = None
    networks: Optional[List[Networks]] = None
    organizations: Optional[List[str]] = None
    id: Optional[str] = None
    created_at: Optional[str] = None
```

#### Step 4: Generate API models

```bash
# Ensure novacom-v1.json is in tools/openapi_specs/
bash tools/generators/generate_api_models.sh
```

#### Step 5: Generated API output (excerpt)

`plugins/plugin_utils/api/v1/generated/models.py` contains classes like:

- `Admin` — From `/components/schemas/Admin`
- `Organization` — From `/components/schemas/Organization`
- `Site` — From `/components/schemas/Site`
- etc.

### Example 2: Regeneration After Schema Changes

When the OpenAPI spec changes:

1. **Update spec file**: Replace `tools/openapi_specs/novacom-v1.json` with the new version.
2. **Regenerate API models**: Run `bash tools/generators/generate_api_models.sh`.
3. **Review changes**: `git diff plugins/plugin_utils/api/v1/generated/models.py`.
4. **Update transform mixins** if field names changed (manual step): Edit `plugins/plugin_utils/api/v1/admin.py` and other mixin files.

---

## SECTION 5: Verification Checklist

After generation, verify:

- [ ] **Imports are correct**: `dataclass`, `typing` (Optional, List, Dict, Any), `BaseTransformMixin`
- [ ] **Field types match expectations**: Required vs Optional
- [ ] **List types** have correct element types
- [ ] **Nested objects** handled correctly (nested dataclasses defined before parent)
- [ ] **Docstrings present**: Module-level, class, attributes

### Common Issues and Fixes

| Issue | Fix |
|-------|-----|
| Missing imports | Add `from typing import List, Optional, Dict, Any` at top |
| Wrong default value | Fix Optional annotation: `is_active: Optional[bool] = True` |
| Nested class order | Define child class before parent class |
| Invalid type for suboptions | Ensure `elements: dict` with `suboptions` for list of objects |

---

## SECTION 6: CI/CD Integration

### Automated Model Regeneration

GitHub Actions workflow that triggers on OpenAPI spec changes:

```yaml
# .github/workflows/regenerate-models.yml

name: Regenerate API Models

on:
  push:
    paths:
      - 'tools/openapi_specs/*.json'
  pull_request:
    paths:
      - 'tools/openapi_specs/*.json'

jobs:
  regenerate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install datamodel-code-generator
        run: pip install datamodel-code-generator

      - name: Regenerate API models
        run: |
          cd novacom.dashboard
          bash tools/generators/generate_api_models.sh

      - name: Check for changes
        id: changes
        run: |
          git diff --exit-code plugins/plugin_utils/api/ || echo "changed=true" >> $GITHUB_OUTPUT
          git diff --stat plugins/plugin_utils/api/

      - name: Run tests
        run: |
          cd novacom.dashboard
          pip install -e .
          pytest tests/ -v --tb=short

      - name: Create PR if changes detected
        if: steps.changes.outputs.changed == 'true' && github.event_name == 'push'
        uses: peter-evans/create-pull-request@v5
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          commit-message: "chore: regenerate API models from OpenAPI specs"
          title: "Regenerate API models"
          body: |
            Auto-generated changes from OpenAPI spec updates.
            Please review and merge.
          branch: auto/regenerate-models
```

### Version Compatibility Matrix

Script to produce module × API version support matrix:

```python
# tools/generators/version_matrix.py

"""Generate module x API version compatibility matrix."""

import json
from pathlib import Path

REGISTRY_PATH = Path("plugins/plugin_utils/platform/registry.py")
API_DIR = Path("plugins/plugin_utils/api")


def extract_modules_from_registry() -> dict:
    """Parse registry or api dir for module/version support."""
    matrix = {}
    if not API_DIR.exists():
        return matrix

    for version_dir in sorted(API_DIR.iterdir()):
        if not version_dir.is_dir() or not version_dir.name.startswith("v"):
            continue
        ver = version_dir.name
        for py_file in version_dir.glob("*.py"):
            if py_file.name.startswith("_"):
                continue
            module = py_file.stem
            if module not in matrix:
                matrix[module] = {}
            matrix[module][ver] = "Y"

    return matrix


def print_matrix(matrix: dict) -> None:
    """Print markdown table."""
    versions = sorted(set(v for m in matrix.values() for v in m))
    print("| Module         |", " | ".join(f"API {v}" for v in versions), "|")
    print("|----------------|", "|".join("--------|" for _ in versions), "|")
    for module in sorted(matrix.keys()):
        row = [matrix[module].get(v, "N") for v in versions]
        print(f"| {module:<14} |", " | ".join(f"  {x}    " for x in row), "|")


if __name__ == "__main__":
    m = extract_modules_from_registry()
    print_matrix(m)
```

**Example output**:

```
| Module         | API v1 | API v2 
|----------------|--------|--------
| admin          |   Y    |   Y    
| organization   |   Y    |   Y    
| site           |   N    |   Y    
```

---

## SECTION 7: Integration with Feature Workflow

How generators feed into the feature implementation workflow:

```
GENERATORS (this doc)
    │
    ├── Generate UserAdmin (auto)
    ├── Generate APIAdmin from OpenAPI (auto)
    │
    ▼
FEATURES (doc 07)
    │
    ├── Create AdminTransformMixin (manual)
    │   - Field mapping
    │   - Custom transforms (names ↔ IDs)
    │   - Endpoint operations
    │
    ├── Create Action Plugin (manual)
    │   - novacom_organization_admin.py
    │
    └── Test with playbook
```

**Summary**:

| Step | Tool | Output |
|------|------|--------|
| 1 | `generate_user_dataclasses.py` | `UserAdmin` in `user_models/admin.py` |
| 2 | `generate_api_models.sh` | `Admin`, `Organization`, etc. in `api/v1/generated/` |
| 3 | Manual | `AdminTransformMixin_v1`, `APIAdmin_v1` in `api/v1/admin.py` |
| 4 | Manual | Action plugin `novacom_organization_admin.py` |

---

## Related Documents

- [06-foundation-components.md](06-foundation-components.md) — Core framework (uses generated classes)
- [07-adding-resources.md](07-adding-resources.md) — Adding features (uses these tools)
- [10-case-study-novacom.md](10-case-study-novacom.md) — NovaCom context and module map
