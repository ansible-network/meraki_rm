# Adding Resource Modules — Step-by-Step Guide

This document is the comprehensive step-by-step guide for adding new resource modules to the collection. It uses **NovaCom Networks** as the fictitious example throughout: a cloud-managed network infrastructure provider (wireless APs, switches, appliances, cameras) with the NovaCom Dashboard API (REST/OpenAPI 3.0, collection namespace: `novacom.dashboard`).

---

## SECTION 1: Feature Implementation Workflow

### High-Level Steps with Time Estimates

| Step | Task | Time Estimate |
|------|------|---------------|
| 1 | Write DOCUMENTATION (user-facing) | 15–30 min |
| 2 | Generate User Model dataclass (automated) | < 1 min |
| 3 | Generate API models from OpenAPI (automated) | < 1 min |
| 4 | Create Transform Mixin (manual — **THIS IS WHERE YOU ADD VALUE**) | 30 min to 3 hours |
| 5 | Create API dataclass (combines generated + mixin) | Included in step 4 |
| 6 | Create Action Plugin (thin wrapper) | 10 min |
| 7 | Test with playbook | 15–30 min |

### Time Estimates by Complexity

| Complexity | Transform Mixin | Total (Steps 1–7) |
|------------|----------------|-------------------|
| **Simple** | 30–60 min | 1.5–2.5 hours |
| **With transforms** (name↔ID lookups) | 1–2 hours | 2.5–3.5 hours |
| **Multi-endpoint** (e.g., SSID with 6 sub-endpoints) | 2–3 hours | 3.5–5 hours |

### Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. DOCUMENTATION (15–30 min)                                                 │
│    plugins/plugin_utils/docs/{resource}.py                                   │
│    User-facing argspec: snake_case, names not IDs, read-only markers         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. Generate User Model (< 1 min)                                             │
│    python tools/generators/generate_user_dataclasses.py docs/admin.py        │
│    Output: plugins/plugin_utils/user_models/admin.py                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. Generate API Models (< 1 min)                                             │
│    bash tools/generators/generate_api_models.sh                              │
│    Output: plugins/plugin_utils/api/v1/generated/models.py                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 4. Transform Mixin (30 min – 3 hours) ★ CORE WORK                           │
│    plugins/plugin_utils/api/v1/admin.py                                      │
│    Field mapping, transforms, endpoint operations, API dataclass             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 5. API Dataclass (included in step 4)                                        │
│    @dataclass class APIAdmin_v1(AdminTransformMixin_v1, GeneratedAPIAdmin)   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 6. Action Plugin (10 min)                                                    │
│    plugins/action/novacom_organization_admin.py                              │
│    Thin wrapper: validate → manager → execute → validate → return            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 7. Test with Playbook (15–30 min)                                             │
│    tests/integration/test_admin.yml                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## SECTION 2: Step 1 — Write DOCUMENTATION

### File Location

`plugins/plugin_utils/docs/{resource}.py`

For NovaCom organization admins: `plugins/plugin_utils/docs/admin.py`

### Key Principles

- **User-facing**: Use names, not IDs. Users provide organization names; they never see `organizationIds`.
- **Clear descriptions**: Every option has a description explaining purpose and usage.
- **Mark read-only/write-only**: `id` and `created_at` are read-only; `password` (if applicable) is write-only.
- **Specify required fields**: Use `required: true` for fields needed on create.
- **snake_case**: All field names use snake_case (`org_access`, not `orgAccess`).

### NovaCom Admin User Example

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
      - On input: Organization names to associate
      - On output: Returns organization names
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

### DOCUMENTATION Checklist

| Principle | Example |
|-----------|---------|
| Names over IDs | `organizations: ['Engineering', 'Platform Team']` not `organization_ids: [1, 2]` |
| snake_case | `org_access`, `created_at` |
| Read-only markers | `id`, `created_at` — returned from API, not accepted as input |
| Required fields | `username` required for creation |
| Nested suboptions | `tags` and `networks` use `suboptions` for structure |
| Round-trip contract | Same fields for input and output; no separate RETURN schema |

---

## SECTION 3: Step 2 — Generate User Model Dataclass

### Command

```bash
python tools/generators/generate_user_dataclasses.py plugins/plugin_utils/docs/admin.py
```

### Output Location

`plugins/plugin_utils/user_models/admin.py`

### Generated Output

```python
"""Generated User model dataclass.

Auto-generated from admin module DOCUMENTATION.
DO NOT EDIT MANUALLY - regenerate using tools/generators/
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserAdmin(BaseTransformMixin):
    """
    Manage NovaCom organization administrators.

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
    tags: Optional[List[Dict[str, Any]]] = None
    networks: Optional[List[Dict[str, Any]]] = None
    organizations: Optional[List[str]] = None
    id: Optional[str] = None
    created_at: Optional[str] = None
```

### Review Checklist

- [ ] Required fields have no `Optional[]` wrapper (e.g., `username: str`)
- [ ] Optional fields use `Optional[...] = None`
- [ ] List types have correct element types (`List[Dict[str, Any]]` for nested dicts)
- [ ] `BaseTransformMixin` is imported and used as base class
- [ ] Class name follows convention: `User{Resource}` (e.g., `UserAdmin`)

---

## SECTION 4: Step 3 — Generate API Models

### Command

```bash
bash tools/generators/generate_api_models.sh
```

### Prerequisites

- OpenAPI spec in `tools/openapi_specs/` (e.g., `novacom-dashboard-v1.json`)
- `datamodel-code-generator` installed: `pip install datamodel-code-generator`

### Output Location

`plugins/plugin_utils/api/v1/generated/models.py`

### Generated Output (Excerpt)

```python
"""Generated API dataclasses from OpenAPI specification.

Auto-generated using datamodel-code-generator.
DO NOT EDIT MANUALLY - regenerate using tools/generators/generate_api_models.sh
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class Admin:
    """NovaCom Admin schema from OpenAPI."""

    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    orgAccess: Optional[str] = None
    tags: Optional[List[Dict]] = None
    networks: Optional[List[Dict]] = None
    organizationIds: Optional[List[str]] = None
    createdAt: Optional[str] = None
    # ... other API-specific fields
```

### Notes

- API models use **camelCase** (e.g., `orgAccess`, `organizationIds`, `createdAt`).
- Field names and structure mirror the OpenAPI schema.
- Do not edit generated files; create a transform mixin to bridge user model and API model.

---

## SECTION 5: Step 4 — Create Transform Mixin (THE CORE WORK)

### File Location

`plugins/plugin_utils/api/v1/admin.py`

This is where you add value: field mapping, custom transforms, and endpoint operations.

### Complete Transform Mixin for NovaCom Admin

```python
"""Transform mixin for NovaCom Admin resource (API v1).

Bridges the user-facing Admin model and the NovaCom Dashboard API Admin schema.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional

from ..platform.base_transform import BaseTransformMixin
from ..platform.types import EndpointOperation
from .generated.models import Admin as GeneratedAPIAdmin


class AdminTransformMixin_v1(BaseTransformMixin):
    """
    Transform mixin for NovaCom Admin resource (API v1).

    Defines:
    - Field mappings (user snake_case <-> API camelCase)
    - Custom transforms (organizations: names <-> IDs)
    - Endpoint operations for CRUD
    """

    # --- FIELD MAPPING ---
    _field_mapping = {
        # Simple 1:1 (same semantic name, different casing)
        'username': 'username',
        'email': 'email',
        'name': 'name',

        # Rename: org_access -> orgAccess
        'org_access': 'orgAccess',

        # Pass-through for nested structures (API uses same structure)
        'tags': 'tags',
        'networks': 'networks',

        # Complex: organizations (names) <-> organizationIds (IDs)
        'organizations': {
            'api_field': 'organizationIds',
            'forward_transform': 'names_to_ids',
            'reverse_transform': 'ids_to_names',
        },

        # Read-only fields (API -> user only)
        'id': 'id',
        'created_at': 'createdAt',
    }

    # --- TRANSFORMATION REGISTRY ---
    _transform_registry = {
        'names_to_ids': lambda value, context: (
            context['manager'].lookup_organization_ids(value) if value else []
        ),
        'ids_to_names': lambda value, context: (
            context['manager'].lookup_organization_names(value) if value else []
        ),
    }

    # --- ENDPOINT OPERATIONS ---
    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        """Define API endpoint operations for Admin resource."""
        return {
            'create': EndpointOperation(
                path='/organizations/{orgId}/admins/',
                method='POST',
                fields=['username', 'email', 'name', 'orgAccess', 'tags', 'networks', 'organizationIds'],
                path_params=['orgId'],
                order=1,
            ),
            'update': EndpointOperation(
                path='/organizations/{orgId}/admins/{adminId}',
                method='PUT',
                fields=['email', 'name', 'orgAccess', 'tags', 'networks', 'organizationIds'],
                path_params=['orgId', 'adminId'],
                order=1,
            ),
            'delete': EndpointOperation(
                path='/organizations/{orgId}/admins/{adminId}',
                method='DELETE',
                fields=[],
                path_params=['orgId', 'adminId'],
                order=1,
            ),
            'get': EndpointOperation(
                path='/organizations/{orgId}/admins/{adminId}',
                method='GET',
                fields=[],
                path_params=['orgId', 'adminId'],
                order=1,
            ),
            'list': EndpointOperation(
                path='/organizations/{orgId}/admins',
                method='GET',
                fields=[],
                path_params=['orgId'],
                order=1,
            ),
        }

    # --- CLASS REFERENCES ---
    @classmethod
    def _get_api_class(cls):
        """Return API dataclass type."""
        return APIAdmin_v1

    @classmethod
    def _get_ansible_class(cls):
        """Return user/Ansible dataclass type."""
        from ...user_models.admin import UserAdmin
        return UserAdmin


@dataclass
class APIAdmin_v1(AdminTransformMixin_v1, GeneratedAPIAdmin):
    """
    API Admin dataclass (v1) with transformation capabilities.

    Combines:
    - Generated API structure (from OpenAPI)
    - Transformation logic (from mixin)
    """
    pass
```

### Field Mapping Types

| Type | Example | Use Case |
|------|---------|----------|
| **1:1 simple** | `'name': 'name'` | Same name, possibly different casing handled by mixin |
| **Rename** | `'org_access': 'orgAccess'` | snake_case → camelCase |
| **Complex** | `'organizations': {'api_field': 'organizationIds', 'forward_transform': 'names_to_ids', ...}` | Names ↔ IDs via lookup |

### Context for Transforms

The `context` dict passed to transform functions contains:

- `manager`: PlatformService instance with `lookup_organization_ids()` and `lookup_organization_names()`
- `session`: Persistent HTTP session
- `cache`: Lookup cache (org name↔ID)
- `api_version`: Detected API version
- Path params: `orgId`, `adminId`, etc., when available

---

## SECTION 6: Step 5 — Create Action Plugin

### File Location

`plugins/action/novacom_organization_admin.py`

### Complete Action Plugin Code

```python
"""Action plugin for NovaCom organization admin resource."""

from ansible.plugins.action import ActionBase
from ansible.module_utils.common.arg_spec import ArgumentSpecValidator
from ansible.errors import AnsibleError
import yaml
import logging

from ansible_collections.novacom.dashboard.plugins.plugin_utils.docs.admin import DOCUMENTATION
from ansible_collections.novacom.dashboard.plugins.plugin_utils.user_models.admin import UserAdmin
from ansible_collections.novacom.dashboard.plugins.plugin_utils.action.base_resource import BaseResourceActionPlugin

logger = logging.getLogger(__name__)


class ActionModule(BaseResourceActionPlugin):
    """
    Action plugin for managing NovaCom organization administrators.

    Thin wrapper that:
    1. Validates input
    2. Gets/spawns manager
    3. Creates user model dataclass
    4. Detects operation (create/update/delete/gather)
    5. Executes via manager
    6. Validates output
    7. Returns result
    """

    MODULE_NAME = 'admin'

    def run(self, tmp=None, task_vars=None):
        """Execute action plugin."""
        super(ActionModule, self).run(tmp, task_vars)

        if task_vars is None:
            task_vars = {}

        args = self._task.args.copy()

        try:
            # 1. INPUT VALIDATION
            argspec = self._build_argspec_from_docs(DOCUMENTATION)
            validated_args = self._validate_data(args, argspec, 'input')

            # 2. GET/SPAWN MANAGER
            manager_client = self._get_or_spawn_manager(task_vars)

            # 3. CREATE USER MODEL DATACLASS
            # Extract config list (resource modules use config: [...])
            config = validated_args.get('config', [])
            if not config and validated_args.get('username'):
                config = [validated_args]

            # 4. DETECT OPERATION
            state = args.get('state', 'merged')
            if state == 'gathered':
                operation = 'gather'
            elif state == 'deleted':
                operation = 'delete'
            else:
                operation = self._detect_operation(args)

            # 5. EXECUTE VIA MANAGER
            results = []
            for item in config:
                user_admin = UserAdmin(**{k: v for k, v in item.items() if v is not None})
                result_dict = manager_client.execute(
                    operation=operation,
                    module_name=self.MODULE_NAME,
                    ansible_data=user_admin,
                    context=self._build_context(args, task_vars),
                )
                if result_dict:
                    results.append(result_dict)

            # 6. OUTPUT VALIDATION
            if results:
                validated_result = self._validate_data(
                    results[0] if len(results) == 1 else {'config': results},
                    argspec,
                    'output',
                )
            else:
                validated_result = {'config': []}

            # 7. RETURN
            return {
                'failed': False,
                'changed': len(results) > 0,
                'admin': validated_result if len(results) == 1 else None,
                'config': validated_result.get('config', results) if len(results) != 1 else None,
            }

        except Exception as e:
            logger.error(f"Action plugin failed: {e}", exc_info=True)
            return {
                'failed': True,
                'msg': str(e),
            }

    def _build_context(self, args, task_vars):
        """Build context dict for manager (orgId, networkId, etc.)."""
        return {
            'org_id': args.get('org_id') or task_vars.get('org_id'),
            'api_key': task_vars.get('novacom_api_key'),
            'base_url': task_vars.get('novacom_base_url', 'https://api.novacom.io/v1/'),
        }
```

### Action Plugin Pattern Summary

| Step | Responsibility |
|------|----------------|
| 1 | Validate input via ArgumentSpec from DOCUMENTATION |
| 2 | Get or spawn manager (persistent PlatformService) |
| 3 | Create UserAdmin dataclass from validated args |
| 4 | Detect operation from `state` and presence of `id` |
| 5 | Execute via manager RPC client |
| 6 | Validate output against same argspec |
| 7 | Return `changed`, result data, and `failed`/`msg` on error |

---

## SECTION 7: Step 6 — Test with Playbook

### File Location

`tests/integration/test_admin.yml`

### Test Playbook

```yaml
---
- name: Test NovaCom Organization Admin
  hosts: localhost
  gather_facts: false

  vars:
    novacom_base_url: https://api.novacom.io/v1
    novacom_api_key: "{{ lookup('env', 'NOVACOM_API_KEY') }}"
    org_id: "{{ lookup('env', 'NOVACOM_ORG_ID', '12345') }}"

  tasks:
    - name: Create admin
      novacom.dashboard.novacom_organization_admin:
        org_id: "{{ org_id }}"
        config:
          - username: test_admin_{{ ansible_date_time.epoch }}
            email: testadmin@example.com
            name: Test Admin
            org_access: read-only
            organizations:
              - Engineering
        state: merged
      register: create_result

    - name: Verify admin was created
      assert:
        that:
          - not create_result.failed
          - create_result.changed | default(false)
          - create_result.admin is defined or create_result.config is defined
          - (create_result.admin.username | default(create_result.config[0].username)) is match('test_admin_.*')
          - (create_result.admin.id | default(create_result.config[0].id)) is defined
      fail_msg: "Admin creation failed or verification failed"

    - name: Update admin
      novacom.dashboard.novacom_organization_admin:
        org_id: "{{ org_id }}"
        config:
          - username: "{{ (create_result.admin.username or create_result.config[0].username) }}"
            id: "{{ create_result.admin.id or create_result.config[0].id }}"
            email: updated@example.com
            name: Updated Test Admin
            org_access: full
        state: merged
      register: update_result

    - name: Verify update
      assert:
        that:
          - not update_result.failed
          - update_result.admin.email == 'updated@example.com' or
            (update_result.config | length > 0 and update_result.config[0].email == 'updated@example.com')
      fail_msg: "Admin update verification failed"

    - name: Delete admin
      novacom.dashboard.novacom_organization_admin:
        org_id: "{{ org_id }}"
        config:
          - username: "{{ (create_result.admin.username or create_result.config[0].username) }}"
            id: "{{ create_result.admin.id or create_result.config[0].id }}"
        state: deleted
      register: delete_result

    - name: Verify deletion
      assert:
        that:
          - not delete_result.failed
      fail_msg: "Admin deletion failed"
```

### Run Command

```bash
# Set required environment variables
export NOVACOM_API_KEY="your-api-key"
export NOVACOM_ORG_ID="12345"

# Run integration test
ansible-playbook tests/integration/test_admin.yml -v
```

---

## SECTION 8: Complete Example — NovaCom Site Resource (Simple)

A simpler resource with no custom transformations and 1:1 field mapping.

### 1. DOCUMENTATION

```python
# plugins/plugin_utils/docs/site.py

DOCUMENTATION = """
---
module: novacom_site
short_description: Manage NovaCom sites
description:
  - Create, update, or delete NovaCom sites within an organization
options:
  name:
    description: Site name
    required: true
    type: str
  address:
    description: Physical address
    type: str
  timezone:
    description: Timezone (e.g., America/New_York)
    type: str
  org_id:
    description: Organization ID (from context)
    type: str
  id:
    description: Site ID (read-only)
    type: str
"""
```

### 2. Generated User Model

```python
# plugins/plugin_utils/user_models/site.py (after generation)

@dataclass
class UserSite(BaseTransformMixin):
    name: str
    address: Optional[str] = None
    timezone: Optional[str] = None
    org_id: Optional[str] = None
    id: Optional[str] = None
```

### 3. Transform Mixin (Simple, No _transform_registry)

```python
# plugins/plugin_utils/api/v1/site.py

from dataclasses import dataclass
from typing import Dict

from ..platform.base_transform import BaseTransformMixin
from ..platform.types import EndpointOperation
from .generated.models import Site as GeneratedAPISite


class SiteTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for NovaCom Site (v1). Simple 1:1 mapping."""

    _field_mapping = {
        'name': 'name',
        'address': 'address',
        'timezone': 'timezone',
        'org_id': 'organizationId',
        'id': 'id',
    }

    _transform_registry = {}

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/organizations/{orgId}/sites/',
                method='POST',
                fields=['name', 'address', 'timezone'],
                path_params=['orgId'],
                order=1,
            ),
            'update': EndpointOperation(
                path='/organizations/{orgId}/sites/{siteId}',
                method='PUT',
                fields=['name', 'address', 'timezone'],
                path_params=['orgId', 'siteId'],
                order=1,
            ),
            'delete': EndpointOperation(
                path='/organizations/{orgId}/sites/{siteId}',
                method='DELETE',
                fields=[],
                path_params=['orgId', 'siteId'],
                order=1,
            ),
        }

    @classmethod
    def _get_api_class(cls):
        return APISite_v1

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.site import UserSite
        return UserSite


@dataclass
class APISite_v1(SiteTransformMixin_v1, GeneratedAPISite):
    pass
```

### 4. Action Plugin

```python
# plugins/action/novacom_site.py

from ansible_collections.novacom.dashboard.plugins.plugin_utils.docs.site import DOCUMENTATION
from ansible_collections.novacom.dashboard.plugins.plugin_utils.user_models.site import UserSite
from ansible_collections.novacom.dashboard.plugins.plugin_utils.action.base_resource import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'site'

    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        # ... same pattern as admin (validate, manager, dataclass, execute, validate, return)
```

### 5. Test Playbook

```yaml
---
- name: Test NovaCom Site
  hosts: localhost
  gather_facts: false
  vars:
    org_id: "12345"
  tasks:
    - name: Create site
      novacom.dashboard.novacom_site:
        org_id: "{{ org_id }}"
        config:
          - name: Test Site
            address: "123 Main St"
            timezone: America/New_York
      register: result

    - name: Verify
      assert:
        that: not result.failed and result.changed
```

---

## SECTION 9: Common Patterns Catalog

### Pattern 1: Name to ID Transformation

**Use case:** User provides names; API requires IDs.

**Field mapping:**

```python
_field_mapping = {
    'organizations': {
        'api_field': 'organizationIds',
        'forward_transform': 'names_to_ids',
        'reverse_transform': 'ids_to_names',
    },
}

_transform_registry = {
    'names_to_ids': lambda value, context: (
        context['manager'].lookup_organization_ids(value) if value else []
    ),
    'ids_to_names': lambda value, context: (
        context['manager'].lookup_organization_names(value) if value else []
    ),
}
```

**PlatformService helper methods:**

```python
def lookup_organization_ids(self, names: List[str]) -> List[str]:
    ids = []
    for name in names:
        cache_key = f'org_name:{name}'
        if cache_key in self.cache:
            ids.append(self.cache[cache_key])
            continue
        response = self.session.get(
            f'{self.base_url}/organizations/',
            params={'name': name}
        )
        response.raise_for_status()
        results = response.json().get('results', [])
        if results:
            org_id = results[0]['id']
            self.cache[cache_key] = org_id
            ids.append(org_id)
        else:
            raise ValueError(f"Organization '{name}' not found")
    return ids

def lookup_organization_names(self, ids: List[str]) -> List[str]:
    names = []
    for org_id in ids:
        cache_key = f'org_id:{org_id}'
        if cache_key in self.cache:
            names.append(self.cache[cache_key])
            continue
        response = self.session.get(
            f'{self.base_url}/organizations/{org_id}/'
        )
        response.raise_for_status()
        org = response.json()
        name = org['name']
        self.cache[cache_key] = name
        self.cache[f'org_name:{name}'] = org_id
        names.append(name)
    return names
```

---

### Pattern 2: Nested Object Flattening

**Use case:** API has nested structure; user model uses flat fields.

**Field mapping:**

```python
_field_mapping = {
    'address_street': 'address.street',
    'address_city': 'address.city',
    'address_state': 'address.state',
    'address_zip': 'address.zip',
}
```

`BaseTransformMixin` handles dot notation automatically for both forward and reverse transforms.

---

### Pattern 3: Conditional Fields

**Use case:** Field only relevant for certain operations.

```python
@classmethod
def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
    return {
        'create': EndpointOperation(
            path='/api/v1/resources/',
            method='POST',
            fields=['name', 'initial_config', 'password'],  # Only on create
            order=1,
        ),
        'update': EndpointOperation(
            path='/api/v1/resources/{id}/',
            method='PATCH',
            fields=['name'],  # No initial_config or password on update
            path_params=['id'],
            order=1,
        ),
    }
```

---

### Pattern 4: Multi-Step Create

**Use case:** Create resource, then configure sub-resources.

```python
@classmethod
def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
    return {
        # Step 1: Create team
        'create': EndpointOperation(
            path='/api/v1/teams/',
            method='POST',
            fields=['name', 'description'],
            order=1,
        ),
        # Step 2: Add members (depends on create)
        'add_members': EndpointOperation(
            path='/api/v1/teams/{id}/members/',
            method='POST',
            fields=['member_ids'],
            path_params=['id'],
            depends_on='create',
            required_for='create',
            order=2,
        ),
        # Step 3: Set permissions (depends on create)
        'set_permissions': EndpointOperation(
            path='/api/v1/teams/{id}/permissions/',
            method='POST',
            fields=['permission_ids'],
            path_params=['id'],
            depends_on='create',
            required_for='create',
            order=3,
        ),
    }
```

Manager executes in dependency order: create → add_members → set_permissions.

---

### Pattern 5: Version-Specific Overrides

**Use case:** API v2 changes a field name.

```python
# plugins/plugin_utils/api/v2/admin.py

class AdminTransformMixin_v2(AdminTransformMixin_v1):
    """V2 overrides v1. Only override what changed."""

    _field_mapping = {
        **AdminTransformMixin_v1._field_mapping,
        'org_access': 'organizationAccess',  # Changed in v2
    }


@dataclass
class APIAdmin_v2(AdminTransformMixin_v2, GeneratedAPIAdmin_v2):
    pass
```

---

## SECTION 10: Testing

### Unit Tests

Test transformation logic in isolation.

**File:** `tests/unit/transforms/test_admin_transform.py`

```python
"""Unit tests for Admin transform mixin."""

import pytest
from unittest.mock import MagicMock

from ansible_collections.novacom.dashboard.plugins.plugin_utils.user_models.admin import UserAdmin
from ansible_collections.novacom.dashboard.plugins.plugin_utils.api.v1.admin import APIAdmin_v1


class MockManager:
    """Mock PlatformService for lookups."""

    def lookup_organization_ids(self, names):
        return ['1', '2'] if names else []

    def lookup_organization_names(self, ids):
        return ['Engineering', 'Platform Team'] if ids else []


def test_forward_transform():
    """Test UserAdmin -> APIAdmin_v1 (user -> API)."""
    user_admin = UserAdmin(
        username='jdoe',
        email='jdoe@example.com',
        name='Jane Doe',
        org_access='full',
        organizations=['Engineering', 'Platform Team'],
    )
    context = {'manager': MockManager(), 'cache': {}}

    api_admin = user_admin.to_api(context)

    assert api_admin.username == 'jdoe'
    assert api_admin.email == 'jdoe@example.com'
    assert api_admin.orgAccess == 'full'
    assert api_admin.organizationIds == ['1', '2']


def test_reverse_transform():
    """Test APIAdmin_v1 -> UserAdmin (API -> user)."""
    api_admin = APIAdmin_v1(
        username='jdoe',
        email='jdoe@example.com',
        name='Jane Doe',
        orgAccess='full',
        organizationIds=['1', '2'],
    )
    context = {'manager': MockManager(), 'cache': {}}

    user_admin = api_admin.to_ansible(context)

    assert user_admin.username == 'jdoe'
    assert user_admin.org_access == 'full'
    assert user_admin.organizations == ['Engineering', 'Platform Team']
```

### Integration Tests

Test via playbooks (see Section 7). Run with:

```bash
ansible-playbook tests/integration/test_admin.yml -v
```

---

## Summary

| Step | Output | Automation |
|------|--------|------------|
| 1 | `docs/{resource}.py` | Manual |
| 2 | `user_models/{resource}.py` | Automated |
| 3 | `api/v1/generated/models.py` | Automated |
| 4 | `api/v1/{resource}.py` (mixin + API dataclass) | Manual |
| 5 | (included in step 4) | — |
| 6 | `action/novacom_{resource}.py` | Manual (thin) |
| 7 | `tests/integration/test_{resource}.yml` | Manual |

The transform mixin (step 4) is where you add value: field mapping, name↔ID lookups, and endpoint operations. Everything else follows established patterns.
