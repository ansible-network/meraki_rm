# Foundation Components — Complete Implementation Specification

This document is the **LARGEST and most critical** specification for the NovaCom Dashboard collection. It provides the full implementation specification for ALL core framework components. Developers build from this document. Every piece of code from the original implementation foundation is preserved and adapted for the **novacom.dashboard** collection namespace.

**Audience**: Framework/infrastructure developers

**Namespace**: `novacom.dashboard` (NovaCom Networks)

**Key Conventions**:
- Use `user_models` instead of `ansible_models` to reflect SDK/presentation-layer independence
- Keep method names `to_ansible()` and `_get_ansible_class()` for Ansible presentation layer compatibility
- User Model classes: `UserVlan`, `UserSsid`, etc. (stable, presentation-layer independent)

---

## Table of Contents

1. [Architecture Overview](#section-1-architecture-overview)
2. [Directory Structure](#section-2-directory-structure)
3. [Component 1 — BaseTransformMixin](#section-3-component-1-basetransformmixin)
4. [Component 2 — Shared Types (EndpointOperation)](#section-4-component-2-shared-types-endpointoperation)
5. [Component 3 — APIVersionRegistry](#section-5-component-3-apiversionregistry)
6. [Component 4 — DynamicClassLoader](#section-6-component-4-dynamicclassloader)
7. [Component 5 — PlatformService](#section-7-component-5-platformservice)
8. [Component 6 — PlatformManager and Multiprocess Manager Pattern](#section-8-component-6-platformmanager-and-the-multiprocess-manager-pattern)
9. [Component 7 — ManagerRPCClient](#section-9-component-7-managerrpcclient)
10. [Component 8 — BaseResourceActionPlugin](#section-10-component-8-baseresourceactionplugin)
11. [Manager Lifecycle](#section-11-manager-lifecycle)
12. [Testing the Foundation](#section-12-testing-the-foundation)

---

## SECTION 1: Architecture Overview

### High-Level Flow

```
PLAYBOOK TASK 1
    ↓
1. Action Plugin spawns Manager (if not running)
    ↓
2. Manager detects API version, loads registry
    ↓
3. Action Plugin validates input (ArgumentSpec)
    ↓
4. Creates User Model dataclass, sends to Manager
    ↓
5. Manager transforms (User → Device)
    ↓
6. Manager calls Platform API
    ↓
7. Manager transforms (Device → User)
    ↓
8. Action Plugin validates output, returns

PLAYBOOK TASK 2+ reuse same Manager (persistent connection)
```

### Component Responsibility Table

| Component | Location | Responsibility |
|-----------|----------|----------------|
| `BaseTransformMixin` | `plugins/plugin_utils/platform/` | Universal transformation logic |
| `PlatformManager` | `plugins/plugin_utils/manager/` | Persistent service, API calls, transformations |
| `RPC Client` | `plugins/plugin_utils/manager/` | Client-side manager communication |
| `Version Registry` | `plugins/plugin_utils/platform/` | Dynamic version/module discovery |
| `Class Loader` | `plugins/plugin_utils/platform/` | Load version-specific classes |
| `Base Action Plugin` | `plugins/action/base_action.py` | Manager spawning, validation, common logic |
| `Generators` | `tools/generators/` | Code generation scripts |

---

## SECTION 2: Directory Structure

Full directory tree with NovaCom namespace:

```
novacom.dashboard/
├── galaxy.yml
├── meta/
│   └── runtime.yml
├── plugins/
│   ├── action/
│   │   ├── __init__.py
│   │   ├── base_action.py              # Base action plugin class (FOUNDATION)
│   │   └── novacom_appliance_vlan.py   # Example resource action plugin
│   ├── plugin_utils/
│   │   ├── __init__.py
│   │   ├── platform/                   # Core framework
│   │   │   ├── __init__.py
│   │   │   ├── base_transform.py       # BaseTransformMixin
│   │   │   ├── types.py                # EndpointOperation, etc.
│   │   │   ├── registry.py             # APIVersionRegistry
│   │   │   └── loader.py               # DynamicClassLoader
│   │   ├── manager/                    # Manager service
│   │   │   ├── __init__.py
│   │   │   ├── platform_manager.py     # PlatformManager (server)
│   │   │   └── rpc_client.py           # ManagerRPCClient (client)
│   │   ├── user_models/                # User-facing dataclasses (stable)
│   │   │   ├── __init__.py
│   │   │   └── vlan.py                 # UserVlan (generated)
│   │   ├── api/                        # API dataclasses (versioned)
│   │   │   ├── v1/
│   │   │   │   ├── generated/
│   │   │   │   │   └── models.py       # Auto-generated from OpenAPI
│   │   │   │   └── vlan.py             # VlanTransformMixin_v1
│   │   │   └── v2/
│   │   └── docs/                       # Module documentation
│   │       └── vlan.py                 # DOCUMENTATION string
│   └── module_utils/
│       └── __init__.py
├── tools/
│   ├── generators/
│   │   ├── generate_user_dataclasses.py
│   │   └── generate_api_models.sh
│   └── openapi_specs/
│       └── novacom-v1.json
└── requirements.txt
```

### Key Principles

1. **`plugins/plugin_utils/`** — All common code (framework)
2. **`plugins/action/`** — Action plugins only
3. **`tools/`** — Development only, not shipped
4. **Version hierarchy in `api/`** — v1/, v2/, etc.
5. **Stable models in `user_models/`** — No versions; presentation-layer independent

---

## SECTION 3: Component 1 — BaseTransformMixin

**File**: `plugins/plugin_utils/platform/base_transform.py`

**Purpose**: Universal transformation logic inherited by all dataclasses. Provides bidirectional data transformation between User Model and Device Model.

### Complete Implementation

```python
"""Base transformation mixin for bidirectional data transformation.

This module provides the core transformation logic used by all User Model
and API (Device) dataclasses in the novacom.dashboard collection.
"""

from abc import ABC
from dataclasses import asdict
from typing import TypeVar, Type, Optional, Dict, Any

T = TypeVar('T')


class BaseTransformMixin(ABC):
    """
    Base transformation mixin providing bidirectional data transformation.

    All User Model dataclasses and API (Device) dataclasses inherit from this
    mixin. It provides generic transformation logic that works with the
    specific field mappings and transform functions defined in subclasses.

    The method names to_ansible() and _get_ansible_class() are retained for
    Ansible presentation layer compatibility. In this context, "ansible"
    refers to the User Model format presented to Ansible.

    Attributes:
        _field_mapping: Dict defining field mappings (set by subclasses)
        _transform_registry: Dict of transformation functions (set by subclasses)
    """

    # Subclasses must define these class variables
    _field_mapping: Optional[Dict] = None
    _transform_registry: Optional[Dict] = None

    def to_api(self, context: Optional[Dict] = None) -> Any:
        """
        Transform from User Model format to Device (API) format.

        Args:
            context: Optional context dict containing:
                - manager: PlatformService instance for lookups
                - session: HTTP session
                - cache: Lookup cache
                - api_version: Current API version

        Returns:
            API (Device) dataclass instance
        """
        return self._transform(
            target_class=self._get_api_class(),
            direction='forward',
            context=context or {}
        )

    def to_ansible(self, context: Optional[Dict] = None) -> Any:
        """
        Transform from Device (API) format to User Model format.

        Note: Method name kept as to_ansible for Ansible presentation layer
        compatibility. Returns User Model dataclass.

        Args:
            context: Optional context dict (same as to_api)

        Returns:
            User Model dataclass instance
        """
        return self._transform(
            target_class=self._get_ansible_class(),
            direction='reverse',
            context=context or {}
        )

    def _transform(
        self,
        target_class: Type[T],
        direction: str,
        context: Dict
    ) -> T:
        """
        Generic bidirectional transformation logic.

        Args:
            target_class: Target dataclass type to instantiate
            direction: 'forward' (User→Device) or 'reverse' (Device→User)
            context: Context dict for transformation functions

        Returns:
            Instance of target_class with transformed data
        """
        # Convert self to dict
        source_data = asdict(self)
        transformed_data = {}

        # Get field mapping from subclass
        mapping = self._field_mapping or {}

        # Apply mapping based on direction
        if direction == 'forward':
            transformed_data = self._apply_forward_mapping(
                source_data, mapping, context
            )
        elif direction == 'reverse':
            transformed_data = self._apply_reverse_mapping(
                source_data, mapping, context
            )
        else:
            raise ValueError(f"Invalid direction: {direction}")

        # Allow subclass post-processing hook
        transformed_data = self._post_transform_hook(
            transformed_data, direction, context
        )

        # Create and return target class instance
        return target_class(**transformed_data)

    def _apply_forward_mapping(
        self,
        source_data: dict,
        mapping: dict,
        context: dict
    ) -> dict:
        """
        Apply forward mapping (User Model → Device Model).

        Args:
            source_data: Source data as dict
            mapping: Field mapping configuration
            context: Transform context

        Returns:
            Transformed data dict
        """
        result = {}

        for user_field, spec in mapping.items():
            # Get value from source
            value = self._get_nested(source_data, user_field)

            if value is None:
                continue

            # Apply forward transformation if specified
            if isinstance(spec, dict) and 'forward_transform' in spec:
                transform_name = spec['forward_transform']
                value = self._apply_transform(value, transform_name, context)

            # Get target field name
            if isinstance(spec, str):
                target_field = spec
            elif isinstance(spec, dict):
                target_field = spec.get('api_field', user_field)
            else:
                target_field = user_field

            # Set in result
            self._set_nested(result, target_field, value)

        return result

    def _apply_reverse_mapping(
        self,
        source_data: dict,
        mapping: dict,
        context: dict
    ) -> dict:
        """
        Apply reverse mapping (Device Model → User Model).

        Args:
            source_data: Source data as dict
            mapping: Field mapping configuration
            context: Transform context

        Returns:
            Transformed data dict
        """
        result = {}

        for user_field, spec in mapping.items():
            # Determine source field name
            if isinstance(spec, str):
                source_field = spec
            elif isinstance(spec, dict):
                source_field = spec.get('api_field', user_field)
            else:
                source_field = user_field

            # Get value from source
            value = self._get_nested(source_data, source_field)

            if value is None:
                continue

            # Apply reverse transformation if specified
            if isinstance(spec, dict) and 'reverse_transform' in spec:
                transform_name = spec['reverse_transform']
                value = self._apply_transform(value, transform_name, context)

            # Set in result
            self._set_nested(result, user_field, value)

        return result

    def _apply_transform(
        self,
        value: Any,
        transform_name: str,
        context: Dict
    ) -> Any:
        """
        Apply a named transformation function.

        Args:
            value: Value to transform
            transform_name: Name of transform function in registry
            context: Transform context

        Returns:
            Transformed value
        """
        if self._transform_registry and transform_name in self._transform_registry:
            transform_func = self._transform_registry[transform_name]
            return transform_func(value, context)
        return value

    def _get_nested(self, data: dict, path: str) -> Any:
        """
        Get value from nested dict using dot-delimited path.

        Args:
            data: Source dict
            path: Dot-delimited path (e.g., 'user.address.city')

        Returns:
            Value at path, or None if not found
        """
        keys = path.split('.')
        current = data

        for key in keys:
            if isinstance(current, dict):
                current = current.get(key)
                if current is None:
                    return None
            else:
                return None

        return current

    def _set_nested(self, data: dict, path: str, value: Any) -> None:
        """
        Set value in nested dict using dot-delimited path.

        Args:
            data: Target dict
            path: Dot-delimited path
            value: Value to set
        """
        keys = path.split('.')
        current = data

        # Navigate to parent
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        # Set final value
        current[keys[-1]] = value

    def _post_transform_hook(
        self,
        data: dict,
        direction: str,
        context: dict
    ) -> dict:
        """
        Hook for module-specific post-processing after transformation.

        Subclasses can override this to add custom logic.

        Args:
            data: Transformed data
            direction: Transform direction
            context: Transform context

        Returns:
            Possibly modified data
        """
        return data

    @classmethod
    def _get_api_class(cls) -> Type:
        """
        Get the API (Device) dataclass type for this resource.

        Must be overridden by module-specific mixins.

        Returns:
            API dataclass type

        Raises:
            NotImplementedError: If not overridden
        """
        raise NotImplementedError(
            f"{cls.__name__} must implement _get_api_class()"
        )

    @classmethod
    def _get_ansible_class(cls) -> Type:
        """
        Get the User Model dataclass type for this resource.

        Note: Method name kept for Ansible presentation layer compatibility.
        Returns the User Model class (e.g., UserVlan).

        Must be overridden by module-specific mixins.

        Returns:
            User Model dataclass type

        Raises:
            NotImplementedError: If not overridden
        """
        raise NotImplementedError(
            f"{cls.__name__} must implement _get_ansible_class()"
        )

    def validate(self) -> bool:
        """
        Hook for module-specific validation.

        Subclasses can override to add custom validation logic.

        Returns:
            True if valid, False otherwise
        """
        return True
```

**Key Features**:
- Generic transformation logic (no resource-specific code)
- Supports dot-notation for nested fields
- Pluggable transformation functions via registry
- Bidirectional (forward and reverse) transforms
- Post-transform hooks for custom logic

---

## SECTION 4: Component 2 — Shared Types (EndpointOperation)

**File**: `plugins/plugin_utils/platform/types.py`

**Purpose**: Type definitions used across the framework.

### Complete Implementation

```python
"""Shared type definitions for the novacom.dashboard platform collection.

This module contains dataclasses and type definitions used throughout
the framework.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class EndpointOperation:
    """
    Configuration for a single API endpoint operation.

    Defines how to call a specific API endpoint, what data to send,
    and how it relates to other operations.

    Attributes:
        path: API endpoint path (e.g., '/api/v1/networks/{network_id}/appliance/vlans/')
        method: HTTP method ('GET', 'POST', 'PATCH', 'PUT', 'DELETE')
        fields: List of dataclass field names to include in request
        path_params: Optional list of path parameter names (e.g., ['id', 'network_id'])
        path_param_aliases: Optional mapping of path param to alternative field names
        required_for: Optional operation type this is required for
            ('create', 'update', 'delete', 'find', or None for always)
        depends_on: Optional name of operation this depends on
        order: Execution order (lower runs first)
        batch_eligible: Whether this operation can be batched (default True)

    Examples:
        >>> # Main create operation
        >>> EndpointOperation(
        ...     path='/api/v1/networks/{network_id}/appliance/vlans/',
        ...     method='POST',
        ...     fields=['vlan_id', 'name', 'subnet'],
        ...     path_params=['network_id'],
        ...     required_for='create',
        ...     order=1
        ... )

        >>> # Dependent operation (runs after create)
        >>> EndpointOperation(
        ...     path='/api/v1/networks/{network_id}/appliance/vlans/{vlan_id}/ports/',
        ...     method='PUT',
        ...     fields=['ports'],
        ...     path_params=['network_id', 'vlan_id'],
        ...     required_for='create',
        ...     depends_on='create',
        ...     order=2
        ... )

        >>> # Update operation
        >>> EndpointOperation(
        ...     path='/api/v1/networks/{network_id}/appliance/vlans/{vlan_id}',
        ...     method='PUT',
        ...     fields=['name', 'subnet', 'dhcp_handling'],
        ...     path_params=['network_id', 'vlan_id'],
        ...     required_for='update',
        ...     order=1
        ... )

        >>> # Find/Get operation
        >>> EndpointOperation(
        ...     path='/api/v1/networks/{network_id}/appliance/vlans/{vlan_id}',
        ...     method='GET',
        ...     fields=[],
        ...     path_params=['network_id', 'vlan_id'],
        ...     required_for='find',
        ...     order=1
        ... )

        >>> # Delete operation
        >>> EndpointOperation(
        ...     path='/api/v1/networks/{network_id}/appliance/vlans/{vlan_id}',
        ...     method='DELETE',
        ...     fields=[],
        ...     path_params=['network_id', 'vlan_id'],
        ...     required_for='delete',
        ...     order=1
        ... )
    """

    path: str
    method: str
    fields: List[str]
    path_params: Optional[List[str]] = None
    path_param_aliases: Optional[Dict[str, List[str]]] = None
    required_for: Optional[str] = None
    depends_on: Optional[str] = None
    order: int = 0
    batch_eligible: bool = True
```

**Usage**: Imported by transform mixins to define API endpoint operations. Mixins implement `get_endpoint_operations()` returning `Dict[str, EndpointOperation]`.

---

## SECTION 5: Component 3 — APIVersionRegistry

**File**: `plugins/plugin_utils/platform/registry.py`

**Purpose**: Discover available API versions and modules by scanning filesystem.

### Complete Implementation

```python
"""API version registry for dynamic version discovery.

This module provides filesystem-based discovery of available API versions
and module implementations without hardcoded version lists.
"""

from pathlib import Path
from typing import Dict, List, Optional
import logging
from packaging import version

logger = logging.getLogger(__name__)


class APIVersionRegistry:
    """
    Registry that discovers and manages API version information.

    Scans the api/ directory to find available versions and tracks
    which modules are implemented for each version.

    Attributes:
        api_base_path: Path to api/ directory containing versioned modules
        user_models_path: Path to user_models/ with stable interfaces
        versions: Dict mapping version string to available modules
        module_versions: Dict mapping module name to available versions
    """

    def __init__(
        self,
        api_base_path: Optional[str] = None,
        user_models_path: Optional[str] = None
    ):
        """
        Initialize registry and discover versions.

        Args:
            api_base_path: Path to api/ directory (auto-detected if None)
            user_models_path: Path to user_models/ (auto-detected if None)
        """
        # Auto-detect paths if not provided
        if api_base_path is None:
            current_file = Path(__file__)
            plugin_utils = current_file.parent.parent
            api_base_path = str(plugin_utils / 'api')

        if user_models_path is None:
            current_file = Path(__file__)
            plugin_utils = current_file.parent.parent
            user_models_path = str(plugin_utils / 'user_models')

        self.api_base_path = Path(api_base_path)
        self.user_models_path = Path(user_models_path)

        # Storage for discovered information
        self.versions: Dict[str, List[str]] = {}  # version -> [modules]
        self.module_versions: Dict[str, List[str]] = {}  # module -> [versions]

        # Discover on init
        self._discover_versions()

    def _discover_versions(self) -> None:
        """
        Scan filesystem to discover API versions and modules.

        Scans api/ directory for version directories (v1/, v2/, etc.)
        and identifies module implementations in each.
        """
        if not self.api_base_path.exists():
            logger.warning(f"API base path not found: {self.api_base_path}")
            return

        # Scan api/ directory for version directories (v1/, v2/, etc.)
        for version_dir in self.api_base_path.iterdir():
            if not version_dir.is_dir():
                continue

            # Must start with 'v' and contain digits
            if not version_dir.name.startswith('v'):
                continue

            # Skip 'generated' and other non-version dirs
            if version_dir.name == 'generated':
                continue

            # Extract version string: v1 -> 1, v2_1 -> 2.1
            version_str = version_dir.name[1:].replace('_', '.')

            # Find module implementations in this version (direct .py files only)
            module_files = [
                f for f in version_dir.iterdir()
                if f.is_file() and f.suffix == '.py' and not f.name.startswith('_')
            ]
            module_names = [f.stem for f in module_files]

            # Store version info
            self.versions[version_str] = sorted(module_names)

            # Update module -> versions mapping
            for module_name in module_names:
                if module_name not in self.module_versions:
                    self.module_versions[module_name] = []
                if version_str not in self.module_versions[module_name]:
                    self.module_versions[module_name].append(version_str)

        # Sort version lists
        for module_name in self.module_versions:
            self.module_versions[module_name].sort(key=version.parse)

        logger.info(
            f"Discovered {len(self.versions)} API versions: "
            f"{sorted(self.versions.keys(), key=version.parse)}"
        )

    def get_supported_versions(self) -> List[str]:
        """
        Get all discovered API versions, sorted.

        Returns:
            List of version strings (e.g., ['1', '2', '2.1'])
        """
        return sorted(self.versions.keys(), key=version.parse)

    def get_latest_version(self) -> Optional[str]:
        """
        Get the latest available API version.

        Returns:
            Latest version string, or None if no versions found
        """
        versions = self.get_supported_versions()
        return versions[-1] if versions else None

    def get_modules_for_version(self, api_version: str) -> List[str]:
        """
        Get list of modules available for a specific API version.

        Args:
            api_version: Version string (e.g., '1', '2.1')

        Returns:
            List of module names
        """
        return self.versions.get(api_version, [])

    def get_versions_for_module(self, module_name: str) -> List[str]:
        """
        Get list of API versions that implement a module.

        Args:
            module_name: Module name (e.g., 'vlan', 'ssid')

        Returns:
            List of version strings
        """
        return self.module_versions.get(module_name, [])

    def find_best_version(
        self,
        requested_version: str,
        module_name: str
    ) -> Optional[str]:
        """
        Find the best available version for a module.

        Strategy:
        1. Try exact match
        2. Try closest lower version (backward compatible)
        3. Try closest higher version (forward compatible, with warning)

        Args:
            requested_version: Desired API version
            module_name: Module name

        Returns:
            Best matching version string, or None if not found
        """
        available = self.get_versions_for_module(module_name)

        if not available:
            logger.error(
                f"Module '{module_name}' not found in any API version"
            )
            return None

        requested = version.parse(requested_version)
        available_parsed = [(v, version.parse(v)) for v in available]

        # Exact match
        if requested_version in available:
            logger.debug(
                f"Found exact version match for {module_name}: {requested_version}"
            )
            return requested_version

        # Find closest lower version (prefer backward compatibility)
        lower_versions = [
            (v, vp) for v, vp in available_parsed if vp <= requested
        ]

        if lower_versions:
            best = max(lower_versions, key=lambda x: x[1])[0]
            logger.warning(
                f"Using version {best} for {module_name} "
                f"(requested {requested_version}, closest lower version)"
            )
            return best

        # Fallback: closest higher version
        higher_versions = [
            (v, vp) for v, vp in available_parsed if vp > requested
        ]

        if higher_versions:
            best = min(higher_versions, key=lambda x: x[1])[0]
            logger.warning(
                f"Using version {best} for {module_name} "
                f"(requested {requested_version}, closest higher version - "
                f"may have compatibility issues)"
            )
            return best

        return None

    def module_supports_version(
        self,
        module_name: str,
        api_version: str
    ) -> bool:
        """
        Check if a module has an implementation for an API version.

        Args:
            module_name: Module name
            api_version: Version string

        Returns:
            True if module exists for version
        """
        return api_version in self.get_versions_for_module(module_name)
```

**Key Features**:
- No hardcoded version lists
- Filesystem-based discovery
- Version fallback logic
- Tracks module × version matrix

---

## SECTION 6: Component 4 — DynamicClassLoader

**File**: `plugins/plugin_utils/platform/loader.py`

**Purpose**: Load version-appropriate classes at runtime.

### Complete Implementation

```python
"""Dynamic class loader for version-specific implementations.

This module loads User Model and API dataclasses based on the detected
API version without hardcoded imports.
"""

import importlib
import inspect
from typing import Type, Tuple, Optional, Dict
from pathlib import Path
import logging

from .base_transform import BaseTransformMixin
from .registry import APIVersionRegistry

logger = logging.getLogger(__name__)


class DynamicClassLoader:
    """
    Dynamically load version-specific classes at runtime.

    Loads the appropriate User Model dataclass and API dataclass/mixin
    based on the module name and API version.

    Attributes:
        registry: APIVersionRegistry for version discovery
        class_cache: Cache of loaded classes to avoid repeated imports
    """

    def __init__(self, registry: APIVersionRegistry):
        """
        Initialize loader with a version registry.

        Args:
            registry: Version registry for discovering available versions
        """
        self.registry = registry
        self._class_cache: Dict[str, Tuple[Type, Type, Type]] = {}

    def load_classes_for_module(
        self,
        module_name: str,
        api_version: str
    ) -> Tuple[Type, Type, Type]:
        """
        Load classes for a module and API version.

        Args:
            module_name: Module name (e.g., 'vlan', 'ssid')
            api_version: API version (e.g., '1', '2.1')

        Returns:
            Tuple of (UserClass, APIClass, MixinClass)

        Raises:
            ValueError: If classes cannot be loaded
        """
        # Find best matching version
        best_version = self.registry.find_best_version(api_version, module_name)

        if not best_version:
            raise ValueError(
                f"No compatible API version found for module '{module_name}' "
                f"with requested version '{api_version}'"
            )

        # Check cache
        cache_key = f"{module_name}_{best_version.replace('.', '_')}"
        if cache_key in self._class_cache:
            logger.debug(f"Using cached classes for {cache_key}")
            return self._class_cache[cache_key]

        # Load classes
        logger.info(
            f"Loading classes for {module_name} (API version {best_version})"
        )

        user_class = self._load_user_class(module_name)
        api_class, mixin_class = self._load_api_classes(module_name, best_version)

        # Cache and return
        result = (user_class, api_class, mixin_class)
        self._class_cache[cache_key] = result

        return result

    def _load_user_class(self, module_name: str) -> Type:
        """
        Load stable User Model dataclass, from user_models/.

        Args:
            module_name: Module name (e.g., 'vlan')

        Returns:
            User Model dataclass type (e.g., UserVlan)

        Raises:
            ImportError: If module cannot be imported
            ValueError: If class cannot be found
        """
        # Import from user_models/<module_name>.py
        module_path = f'ansible_collections.novacom.dashboard.plugins.plugin_utils.user_models.{module_name}'

        try:
            module = importlib.import_module(module_path)
        except ImportError as e:
            raise ImportError(
                f"Failed to import User Model module {module_path}: {e}"
            ) from e

        # Find User Model dataclass (e.g., UserVlan)
        class_name = f'User{module_name.title()}'

        if hasattr(module, class_name):
            return getattr(module, class_name)

        # Fallback: find any class starting with 'User'
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name.startswith('User'):
                logger.warning(
                    f"Using {name} instead of expected {class_name}"
                )
                return obj

        raise ValueError(
            f"No User Model dataclass found in {module_path} "
            f"(expected {class_name})"
        )

    def _load_api_classes(
        self,
        module_name: str,
        api_version: str
    ) -> Tuple[Type, Type]:
        """
        Load API dataclass and transform mixin for a version.

        Args:
            module_name: Module name
            api_version: API version

        Returns:
            Tuple of (APIClass, MixinClass)

        Raises:
            ImportError: If module cannot be imported
            ValueError: If classes cannot be found
        """
        # Import from api/v<version>/<module_name>.py
        version_normalized = api_version.replace('.', '_')
        module_path = (
            f'ansible_collections.novacom.dashboard.plugins.plugin_utils.api.'
            f'v{version_normalized}.{module_name}'
        )

        try:
            module = importlib.import_module(module_path)
        except ImportError as e:
            raise ImportError(
                f"Failed to import API module {module_path}: {e}"
            ) from e

        # Find API dataclass (e.g., APIVlan_v1 or Vlan_v1)
        api_class_name = f'API{module_name.title()}_v{version_normalized}'
        api_class = self._find_class_in_module(
            module,
            [api_class_name, f'API{module_name.title()}', 'API*'],
            f"API dataclass for {module_name}"
        )

        # Find transform mixin (e.g., VlanTransformMixin_v1)
        mixin_class_name = f'{module_name.title()}TransformMixin_v{version_normalized}'
        mixin_class = self._find_class_in_module(
            module,
            [mixin_class_name, f'{module_name.title()}TransformMixin', '*TransformMixin'],
            f"Transform mixin for {module_name}",
            base_class=BaseTransformMixin
        )

        return api_class, mixin_class

    def _find_class_in_module(
        self,
        module,
        patterns: list,
        description: str,
        base_class: Optional[Type] = None
    ) -> Type:
        """
        Find a class in a module matching patterns.

        Args:
            module: Imported module
            patterns: List of patterns to try (wildcards supported)
            description: Description for error messages
            base_class: Optional base class to filter by

        Returns:
            Matched class type

        Raises:
            ValueError: If no matching class found
        """
        # Get all classes from module
        classes = inspect.getmembers(module, inspect.isclass)

        # Filter by base class if specified
        if base_class:
            classes = [
                (name, cls) for name, cls in classes
                if issubclass(cls, base_class) and cls != base_class
            ]

        # Try each pattern
        for pattern in patterns:
            if '*' in pattern:
                # Wildcard pattern
                prefix = pattern.replace('*', '')
                for name, cls in classes:
                    if name.startswith(prefix):
                        logger.debug(
                            f"Found {description}: {name} (pattern: {pattern})"
                        )
                        return cls
            else:
                # Exact match
                for name, cls in classes:
                    if name == pattern:
                        logger.debug(f"Found {description}: {name}")
                        return cls

        # Not found
        raise ValueError(
            f"No {description} found in {module.__name__}. "
            f"Tried patterns: {patterns}"
        )
```

**Key Features**:
- Dynamic imports (no hardcoded class names)
- Pattern matching for class discovery
- Caching for performance
- Fallback logic
- Uses `user_models` path and `User*` class naming

---

## SECTION 7: Component 5 — PlatformService

**File**: `plugins/plugin_utils/manager/platform_manager.py` (first class)

**Purpose**: Persistent service that handles API communication and transformations. Generic, resource-agnostic.

### Complete Implementation

```python
"""Platform Manager - Persistent service for API communication.

This module provides the server-side manager that maintains persistent
connections to the NovaCom Dashboard API and handles all data transformations.
"""

import requests
import logging
import threading
from typing import Any, Dict, Optional, List
from dataclasses import asdict, is_dataclass

from ..platform.registry import APIVersionRegistry
from ..platform.loader import DynamicClassLoader
from ..platform.types import EndpointOperation

logger = logging.getLogger(__name__)


class PlatformService:
    """
    Generic platform service - resource agnostic.

    Maintains a persistent connection to the NovaCom Dashboard API and
    handles all resource operations generically. Works for any module
    (vlan, ssid, organization, etc.).

    Attributes:
        base_url: Platform base URL
        session: Persistent HTTP session
        api_version: Detected/cached API version
        registry: Version registry
        loader: Class loader
        cache: Lookup cache (org names ↔ IDs, etc.)
    """

    def __init__(self, base_url: str):
        """
        Initialize platform service.

        Args:
            base_url: Platform base URL (e.g., https://api.novacom.io)
        """
        self.base_url = base_url.rstrip('/')

        # Initialize persistent session (thread-safe)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NovaCom Dashboard Ansible Collection',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

        # Detect API version (cached for lifetime)
        self.api_version = self._detect_version()
        logger.info(f"PlatformService initialized with API v{self.api_version}")

        # Initialize registry and loader
        self.registry = APIVersionRegistry()
        self.loader = DynamicClassLoader(self.registry)

        # Cache for lookups
        self.cache: Dict[str, Any] = {}

    def _detect_version(self) -> str:
        """
        Detect platform API version.

        Queries the platform API for version information.

        Returns:
            Version string (e.g., '1', '2.1')
        """
        try:
            # Try to get version from API
            response = self.session.get(f'{self.base_url}/api/v2/ping/')
            response.raise_for_status()
            version_str = response.json().get('version', '1')

            # Normalize version string
            if version_str.startswith('v'):
                version_str = version_str[1:]

            logger.info(f"Detected platform API version: {version_str}")
            return version_str

        except Exception as e:
            logger.warning(f"Failed to detect API version: {e}, using default '1'")
            return '1'

    def execute(
        self,
        operation: str,
        module_name: str,
        user_data_dict: dict
    ) -> dict:
        """
        Execute a generic operation on any resource.

        This is the main entry point called by action plugins via RPC.

        Args:
            operation: Operation type ('create', 'update', 'delete', 'find')
            module_name: Module name (e.g., 'vlan', 'ssid')
            user_data_dict: User Model dataclass as dict

        Returns:
            Result as dict (User Model format)

        Raises:
            ValueError: If operation is unknown or execution fails
        """
        thread_id = threading.get_ident()
        logger.info(
            f"Executing {operation} on {module_name} [Thread: {thread_id}]"
        )

        # Load version-appropriate classes
        UserClass, APIClass, MixinClass = self.loader.load_classes_for_module(
            module_name,
            self.api_version
        )

        # Reconstruct User Model dataclass
        user_instance = UserClass(**user_data_dict)

        # Build transformation context
        context = {
            'manager': self,
            'session': self.session,
            'cache': self.cache,
            'api_version': self.api_version,
            'base_url': self.base_url
        }

        # Execute operation
        try:
            if operation == 'create':
                result = self._create_resource(
                    user_instance, MixinClass, APIClass, context
                )
            elif operation == 'update':
                result = self._update_resource(
                    user_instance, MixinClass, APIClass, context
                )
            elif operation == 'delete':
                result = self._delete_resource(
                    user_instance, MixinClass, context
                )
            elif operation == 'find':
                result = self._find_resource(
                    user_instance, MixinClass, APIClass, context
                )
            else:
                raise ValueError(f"Unknown operation: {operation}")

            logger.info(
                f"Operation {operation} on {module_name} completed "
                f"[Thread: {thread_id}]"
            )

            return result

        except Exception as e:
            logger.error(
                f"Operation {operation} on {module_name} failed: {e}",
                exc_info=True
            )
            raise

    def _create_resource(
        self,
        user_data: Any,
        mixin_class: type,
        api_class: type,
        context: dict
    ) -> dict:
        """
        Create resource with transformation.

        Args:
            user_data: User Model dataclass instance
            mixin_class: Transform mixin class
            api_class: API dataclass type
            context: Transformation context

        Returns:
            Created resource as dict (User Model format)
        """
        # FORWARD TRANSFORM: User → Device
        api_data = user_data.to_api(context)

        # Get endpoint operations from mixin
        operations = self._get_endpoint_operations(mixin_class, 'create')

        # Execute operations (potentially multi-endpoint)
        api_result = self._execute_operations(
            operations, api_data, context, user_data
        )

        # REVERSE TRANSFORM: Device → User
        if api_result:
            api_result_instance = api_class(**api_result)
            user_result = api_result_instance.to_ansible(context)
            return asdict(user_result)

        return {}

    def _update_resource(
        self,
        user_data: Any,
        mixin_class: type,
        api_class: type,
        context: dict
    ) -> dict:
        """
        Update resource with transformation.

        Args:
            user_data: User Model dataclass instance
            mixin_class: Transform mixin class
            api_class: API dataclass type
            context: Transformation context

        Returns:
            Updated resource as dict (User Model format)
        """
        # FORWARD TRANSFORM: User → Device
        api_data = user_data.to_api(context)

        # Get endpoint operations from mixin
        operations = self._get_endpoint_operations(mixin_class, 'update')

        # Execute operations
        api_result = self._execute_operations(
            operations, api_data, context, user_data
        )

        # REVERSE TRANSFORM: Device → User
        if api_result:
            api_result_instance = api_class(**api_result)
            user_result = api_result_instance.to_ansible(context)
            return asdict(user_result)

        return {}

    def _delete_resource(
        self,
        user_data: Any,
        mixin_class: type,
        context: dict
    ) -> dict:
        """
        Delete resource.

        Args:
            user_data: User Model dataclass instance
            mixin_class: Transform mixin class
            context: Transformation context

        Returns:
            Empty dict on success
        """
        # FORWARD TRANSFORM: User → Device (for path params)
        api_data = user_data.to_api(context)

        # Get endpoint operations from mixin
        operations = self._get_endpoint_operations(mixin_class, 'delete')

        # Execute delete operations
        self._execute_operations(
            operations, api_data, context, user_data
        )

        return {}

    def _find_resource(
        self,
        user_data: Any,
        mixin_class: type,
        api_class: type,
        context: dict
    ) -> dict:
        """
        Find/get resource with transformation.

        Args:
            user_data: User Model dataclass instance (contains identifiers)
            mixin_class: Transform mixin class
            api_class: API dataclass type
            context: Transformation context

        Returns:
            Found resource as dict (User Model format)
        """
        # FORWARD TRANSFORM: User → Device (for path params)
        api_data = user_data.to_api(context)
        api_data_dict = asdict(api_data) if is_dataclass(api_data) else api_data
        user_data_dict = asdict(user_data) if is_dataclass(user_data) else user_data

        # Get endpoint operations from mixin
        operations = self._get_endpoint_operations(mixin_class, 'find')

        # Execute operations (typically GET)
        sorted_ops = self._sort_operations(operations)

        results = {}
        for op_name in sorted_ops:
            endpoint_op = operations[op_name]
            path = endpoint_op.path
            if endpoint_op.path_params:
                for param in endpoint_op.path_params:
                    val = api_data_dict.get(param) or user_data_dict.get(param)
                    if val is not None:
                        path = path.replace(f'{{{param}}}', str(val))

            url = f"{self.base_url}{path}"
            logger.debug(f"Calling {endpoint_op.method} {url}")
            response = self.session.request(endpoint_op.method, url)
            response.raise_for_status()
            result_data = response.json()
            results[op_name] = result_data

        # REVERSE TRANSFORM: Device → User
        main_result = results.get('find') or results.get('main') or list(results.values())[0]
        if main_result:
            api_result_instance = api_class(**main_result)
            user_result = api_result_instance.to_ansible(context)
            return asdict(user_result)

        return {}

    def _get_endpoint_operations(
        self,
        mixin_class: type,
        required_for: str
    ) -> Dict[str, EndpointOperation]:
        """
        Get endpoint operations from mixin, filtered by operation type.

        Args:
            mixin_class: Transform mixin class
            required_for: Operation type filter

        Returns:
            Dict of operation name to EndpointOperation
        """
        if hasattr(mixin_class, 'get_endpoint_operations'):
            all_ops = mixin_class.get_endpoint_operations()
        else:
            return {}

        return {
            name: op for name, op in all_ops.items()
            if op.required_for is None or op.required_for == required_for
        }

    def _execute_operations(
        self,
        operations: Dict[str, EndpointOperation],
        api_data: Any,
        context: dict,
        user_data: Any
    ) -> dict:
        """
        Execute potentially multiple API endpoint operations.

        Args:
            operations: Dict of EndpointOperations
            api_data: API dataclass instance
            context: Context
            user_data: User Model instance (for path param resolution)

        Returns:
            Combined API response dict
        """
        if not operations:
            return {}

        # Sort by dependencies and order
        sorted_ops = self._sort_operations(operations)
        api_data_dict = asdict(api_data) if is_dataclass(api_data) else api_data
        user_data_dict = asdict(user_data) if is_dataclass(user_data) else user_data

        results = {}
        for op_name in sorted_ops:
            endpoint_op = operations[op_name]

            # Extract fields for this endpoint
            request_data = {}
            for field in endpoint_op.fields:
                if field in api_data_dict and api_data_dict[field] is not None:
                    request_data[field] = api_data_dict[field]
                elif field in user_data_dict and user_data_dict[field] is not None:
                    request_data[field] = user_data_dict[field]

            # Build path with parameters (from results, api_data, or user_data)
            path = endpoint_op.path
            if endpoint_op.path_params:
                for param in endpoint_op.path_params:
                    val = None
                    if param in results:
                        r = results[param]
                        val = r.get('id', r) if isinstance(r, dict) else r
                    if val is None:
                        val = api_data_dict.get(param) or user_data_dict.get(param)
                    if val is not None:
                        path = path.replace(f'{{{param}}}', str(val))

            url = f"{self.base_url}{path}"

            # Skip body for DELETE
            if endpoint_op.method == 'DELETE':
                response = self.session.request(endpoint_op.method, url)
            else:
                response = self.session.request(
                    endpoint_op.method,
                    url,
                    json=request_data if request_data else None
                )

            response.raise_for_status()

            # Store result
            try:
                result_data = response.json()
            except ValueError:
                result_data = {}

            results[op_name] = result_data
            if 'id' in result_data:
                results['id'] = result_data['id']

        return results.get('create') or results.get('update') or results.get('main') or {}

    def _sort_operations(
        self,
        operations: Dict[str, EndpointOperation]
    ) -> List[str]:
        """
        Sort operations by dependencies and order.

        Args:
            operations: Dict of EndpointOperations

        Returns:
            List of operation names in execution order
        """
        sorted_ops = []
        remaining = dict(operations)

        # Topological sort based on depends_on
        while remaining:
            ready = [
                name for name, op in remaining.items()
                if op.depends_on is None or op.depends_on in sorted_ops
            ]

            if not ready:
                raise ValueError(
                    f"Circular dependency in operations: "
                    f"{list(remaining.keys())}"
                )

            ready.sort(key=lambda name: remaining[name].order)
            sorted_ops.append(ready[0])
            remaining.pop(ready[0])

        return sorted_ops

    def lookup_org_ids(self, org_names: list) -> list:
        """
        Convert organization names to IDs.

        Args:
            org_names: List of organization names

        Returns:
            List of organization IDs
        """
        ids = []
        for name in org_names:
            cache_key = f'org_name:{name}'
            if cache_key in self.cache:
                ids.append(self.cache[cache_key])
                continue

            response = self.session.get(
                f'{self.base_url}/api/v{self.api_version}/organizations/',
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

    def lookup_org_names(self, org_ids: list) -> list:
        """
        Convert organization IDs to names.

        Args:
            org_ids: List of organization IDs

        Returns:
            List of organization names
        """
        names = []
        for org_id in org_ids:
            cache_key = f'org_id:{org_id}'
            if cache_key in self.cache:
                names.append(self.cache[cache_key])
                continue

            response = self.session.get(
                f'{self.base_url}/api/v{self.api_version}/organizations/{org_id}/'
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

## SECTION 8: Component 6 — PlatformManager and the Multiprocess Manager Pattern

**File**: `plugins/plugin_utils/manager/platform_manager.py` (second class, same file as PlatformService)

### PlatformManager Class

The following class is defined in the same file as `PlatformService`, after the `PlatformService` class:

```python
from multiprocessing.managers import BaseManager
from socketserver import ThreadingMixIn


class PlatformManager(ThreadingMixIn, BaseManager):
    """
    Custom Manager for sharing PlatformService across processes.

    Uses ThreadingMixIn to handle concurrent client connections.
    Enables multiple Ansible tasks to communicate with the same
    PlatformService instance via RPC.

    Attributes:
        daemon_threads: Threads exit when main process exits
    """
    daemon_threads = True
```

### The Multiprocess Manager Pattern (Abstract Explanation)

Python's `multiprocessing.managers.BaseManager` provides RPC over Unix domain sockets (or TCP). The pattern works as follows:

1. **BaseManager** — Provides a way to share Python objects across processes. It starts a server that accepts connections and proxies method calls to the actual object.

2. **ThreadingMixIn** — Enables the manager server to handle multiple client connections concurrently. Each connection gets a new thread, so tasks can execute in parallel without blocking each other.

3. **Proxy objects** — When a client calls `manager.get_platform_service()`, it receives a proxy object. Method calls on the proxy are serialized, sent over the socket, executed on the server-side object, and the result is returned. The client uses the proxy transparently.

4. **Persistent Session** — A persistent `requests.Session` lives on the server. It is reused across all client calls. Authentication, connection pooling, and cookies persist. The session is thread-safe for typical usage.

5. **Spawn once, serve many** — The manager process spawns once (on the first playbook task) and serves all subsequent tasks in the playbook run. Connection info (socket path, authkey) is stored in Ansible facts so later tasks can connect.

6. **Process isolation** — The manager runs in a separate process. If it crashes, the playbook process continues (though subsequent tasks would fail). This provides fault isolation.

**Benefits**:
- **Persistent connections** — No re-authentication per task
- **Shared state** — Caches, version detection done once
- **Concurrent access** — ThreadingMixIn allows parallel requests
- **Process isolation** — Manager crash doesn't kill playbook

---

## SECTION 9: Component 7 — ManagerRPCClient

**File**: `plugins/plugin_utils/manager/rpc_client.py`

**Purpose**: Client-side connection to manager service.

### Complete Implementation

```python
"""RPC Client for communicating with Platform Manager.

Provides the client-side interface for action plugins to communicate
with the persistent Platform Manager service.
"""

from multiprocessing.managers import BaseManager
from typing import Any
from dataclasses import asdict, is_dataclass
import logging

logger = logging.getLogger(__name__)


class ManagerRPCClient:
    """
    Client for communicating with Platform Manager.

    Handles connection to the manager service and provides a simple
    interface for action plugins to execute operations.

    Attributes:
        base_url: Platform base URL
        socket_path: Path to Unix socket (or address tuple)
        authkey: Authentication key
        manager: Manager instance
        service_proxy: Proxy to PlatformService
    """

    def __init__(self, base_url: str, socket_path: str, authkey: bytes):
        """
        Initialize RPC client.

        Args:
            base_url: Platform base URL
            socket_path: Path to Unix socket or address
            authkey: Authentication key for manager connection
        """
        self.base_url = base_url
        self.socket_path = socket_path
        self.authkey = authkey

        # Import manager class
        from .platform_manager import PlatformManager

        # Register remote service (must match server registration)
        PlatformManager.register('get_platform_service')

        # Connect to manager
        logger.debug(f"Connecting to manager at {socket_path}")
        self.manager = PlatformManager(
            address=socket_path,
            authkey=authkey
        )
        self.manager.connect()

        # Get service proxy
        self.service_proxy = self.manager.get_platform_service()
        logger.info("Connected to Platform Manager")

    def execute(
        self,
        operation: str,
        module_name: str,
        user_data: Any
    ) -> Any:
        """
        Execute operation via manager.

        Args:
            operation: Operation type ('create', 'update', 'delete', 'find')
            module_name: Module name (e.g., 'vlan', 'ssid')
            user_data: User Model dataclass instance or dict

        Returns:
            Result as dict (User Model format)
        """
        # Convert to dict for RPC serialization
        if is_dataclass(user_data):
            data_dict = asdict(user_data)
        else:
            data_dict = user_data

        # Execute via proxy
        result_dict = self.service_proxy.execute(
            operation,
            module_name,
            data_dict
        )

        return result_dict
```

---

## SECTION 10: Component 8 — BaseResourceActionPlugin

**File**: `plugins/action/base_action.py`

**Purpose**: Common functionality for all resource action plugins.

### Complete Implementation

```python
"""Base action plugin for NovaCom Dashboard platform resources.

Provides common functionality inherited by all resource action plugins.
"""

from ansible.plugins.action import ActionBase
from ansible.module_utils.common.arg_spec import ArgumentSpecValidator
from ansible.errors import AnsibleError
from pathlib import Path
import yaml
import logging
import tempfile
import secrets
import base64
from multiprocessing import Process
import time

logger = logging.getLogger(__name__)


class BaseResourceActionPlugin(ActionBase):
    """
    Base action plugin for all NovaCom Dashboard platform resources.

    Provides common functionality:
    - Manager spawning/connection (_get_or_spawn_manager)
    - Input/output validation (_validate_data)
    - ArgumentSpec generation (_build_argspec_from_docs)
    - Operation detection (_detect_operation)

    Subclasses must define:
    - MODULE_NAME: Name of the resource (e.g., 'vlan', 'ssid')
    - DOCUMENTATION: Module documentation string
    - USER_DATACLASS: The User Model dataclass type

    Example subclass:
        class ActionModule(BaseResourceActionPlugin):
            MODULE_NAME = 'vlan'

            def run(self, tmp=None, task_vars=None):
                manager = self._get_or_spawn_manager(task_vars)
                argspec = self._build_argspec_from_docs(DOCUMENTATION)
                validated_args = self._validate_data(self._task.args, argspec, 'input')
                user_data = UserVlan(**validated_args)
                operation = self._detect_operation(self._task.args)
                result_dict = manager.execute(operation, self.MODULE_NAME, user_data)
                validated_result = self._validate_data(result_dict, argspec, 'output')
                return {'changed': True, 'vlan': validated_result}
    """

    MODULE_NAME = None  # Subclass must override

    def _get_or_spawn_manager(self, task_vars: dict):
        """
        Get existing manager or spawn new one.

        Checks if a manager is already running (stored in hostvars).
        If found, connects to it. If not, spawns a new manager process.

        Args:
            task_vars: Task variables from Ansible

        Returns:
            ManagerRPCClient instance

        Raises:
            AnsibleError: If novacom_url not configured
            RuntimeError: If manager fails to start
        """
        from ansible_collections.novacom.dashboard.plugins.plugin_utils.manager.rpc_client import ManagerRPCClient

        hostvars = task_vars.get('hostvars', {})
        inventory_hostname = task_vars.get('inventory_hostname', 'localhost')
        host_vars = hostvars.get(inventory_hostname, {})

        socket_path = host_vars.get('platform_manager_socket')
        authkey_b64 = host_vars.get('platform_manager_authkey')
        novacom_url = host_vars.get('novacom_url')

        if not novacom_url:
            raise AnsibleError(
                "novacom_url must be defined in inventory or host_vars"
            )

        # If manager already running, try to connect
        if socket_path and authkey_b64 and Path(socket_path).exists():
            try:
                authkey = base64.b64decode(authkey_b64)
                client = ManagerRPCClient(novacom_url, socket_path, authkey)
                logger.info("Connected to existing manager")
                return client
            except Exception as e:
                logger.warning(
                    f"Failed to connect to existing manager: {e}. "
                    f"Spawning new one..."
                )

        # Spawn new manager
        logger.info("Spawning new Platform Manager")

        socket_dir = Path(tempfile.gettempdir()) / 'novacom_dashboard'
        socket_dir.mkdir(exist_ok=True)
        socket_path = str(socket_dir / f'manager_{inventory_hostname}.sock')
        authkey = secrets.token_bytes(32)

        if Path(socket_path).exists():
            try:
                Path(socket_path).unlink()
            except Exception as e:
                logger.warning(f"Failed to remove old socket: {e}")

        def start_manager():
            """Manager process entry point."""
            from ansible_collections.novacom.dashboard.plugins.plugin_utils.manager.platform_manager import (
                PlatformManager,
                PlatformService
            )

            service = PlatformService(novacom_url)
            PlatformManager.register(
                'get_platform_service',
                callable=lambda: service
            )
            manager = PlatformManager(address=socket_path, authkey=authkey)
            manager.start()

            import signal
            signal.pause()

        process = Process(target=start_manager, daemon=True)
        process.start()

        # Wait for socket to be created
        max_wait = 50
        for _ in range(max_wait):
            if Path(socket_path).exists():
                break
            time.sleep(0.1)
        else:
            raise RuntimeError(
                f"Manager failed to start within {max_wait * 0.1} seconds"
            )

        authkey_b64 = base64.b64encode(authkey).decode('utf-8')

        try:
            self._execute_module(
                module_name='ansible.builtin.set_fact',
                module_args={
                    'platform_manager_socket': socket_path,
                    'platform_manager_authkey': authkey_b64,
                    'cacheable': True
                },
                task_vars=task_vars
            )
        except Exception as e:
            logger.warning(f"Failed to set facts: {e}")

        client = ManagerRPCClient(novacom_url, socket_path, authkey)
        logger.info(f"Spawned and connected to new manager at {socket_path}")

        return client

    def _build_argspec_from_docs(self, documentation: str) -> dict:
        """
        Build argument spec from DOCUMENTATION string.

        Parses the YAML documentation and converts it to Ansible's
        ArgumentSpec format for validation.

        Args:
            documentation: DOCUMENTATION string from module

        Returns:
            ArgumentSpec dict suitable for ArgumentSpecValidator

        Raises:
            ValueError: If documentation cannot be parsed
        """
        try:
            doc_data = yaml.safe_load(documentation)
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse DOCUMENTATION: {e}") from e

        options = doc_data.get('options', {})

        argspec = {
            'options': options,
            'mutually_exclusive': doc_data.get('mutually_exclusive', []),
            'required_together': doc_data.get('required_together', []),
            'required_one_of': doc_data.get('required_one_of', []),
            'required_if': doc_data.get('required_if', []),
        }

        return argspec

    def _validate_data(
        self,
        data: dict,
        argspec: dict,
        direction: str
    ) -> dict:
        """
        Validate data against argument spec.

        Uses Ansible's ArgumentSpecValidator to validate
        both input (from playbook) and output (from manager).

        Args:
            data: Data dict to validate
            argspec: Argument specification
            direction: 'input' or 'output' (for error messages)

        Returns:
            Validated and normalized data dict

        Raises:
            AnsibleError: If validation fails
        """
        validator = ArgumentSpecValidator(argspec)
        result = validator.validate(data)

        if result.error_messages:
            error_msg = (
                f"{direction.title()} validation failed: " +
                ", ".join(result.error_messages)
            )
            raise AnsibleError(error_msg)

        return result.validated_parameters

    def _detect_operation(self, args: dict) -> str:
        """
        Detect operation type from arguments.

        Maps resource module state to API operation:
        - merged   -> 'update'  (create if not exists, update if exists)
        - replaced -> 'replace' (full resource replacement)
        - overridden -> 'override' (replace all instances of this resource type)
        - deleted  -> 'delete'
        - gathered -> 'find'

        Args:
            args: Module arguments

        Returns:
            Operation name ('update', 'replace', 'override', 'delete', 'find')

        Raises:
            AnsibleError: If state is unknown
        """
        state_to_operation = {
            'merged': 'update',
            'replaced': 'replace',
            'overridden': 'override',
            'deleted': 'delete',
            'gathered': 'find',
        }
        state = args.get('state', 'merged')
        operation = state_to_operation.get(state)
        if operation is None:
            raise AnsibleError(f"Unknown state: {state}")
        return operation
```

### Example Usage Pattern (Resource-Specific Action Plugin)

```python
# plugins/action/novacom_appliance_vlan.py

from ansible_collections.novacom.dashboard.plugins.action.base_action import BaseResourceActionPlugin
from ansible_collections.novacom.dashboard.plugins.plugin_utils.docs.vlan import DOCUMENTATION
from ansible_collections.novacom.dashboard.plugins.plugin_utils.user_models.vlan import UserVlan


class ActionModule(BaseResourceActionPlugin):
    """Action plugin for novacom_appliance_vlan resource module."""

    MODULE_NAME = 'vlan'

    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)

        if task_vars is None:
            task_vars = {}

        args = self._task.args.copy()

        try:
            # 1. Validate input
            argspec = self._build_argspec_from_docs(DOCUMENTATION)
            validated_args = self._validate_data(args, argspec, 'input')

            # 2. Get manager
            manager = self._get_or_spawn_manager(task_vars)

            # 3. Create User Model dataclass
            user_data = UserVlan(**validated_args)

            # 4. Execute
            operation = self._detect_operation(args)
            result_dict = manager.execute(operation, self.MODULE_NAME, user_data)

            # 5. Validate output
            validated_result = self._validate_data(result_dict, argspec, 'output')

            # 6. Return
            return {
                'failed': False,
                'changed': operation in ('create', 'update', 'delete'),
                'vlan': validated_result
            }
        except Exception as e:
            return {'failed': True, 'msg': str(e)}
```

> **Meraki improvement**: The `cisco.meraki_rm` collection eliminates per-module
> `run()` methods entirely. `BaseResourceActionPlugin` provides a data-driven `run()`
> that auto-discovers DOCUMENTATION from the module file and resolves the User Model
> via `importlib`. Each action plugin becomes pure configuration (~8 lines):
>
> ```python
> class ActionModule(BaseResourceActionPlugin):
>     MODULE_NAME = 'vlan'
>     USER_MODEL = 'plugins.plugin_utils.user_models.vlan.UserVlan'
> ```
>
> See [meraki-implementation-guide.md](meraki-implementation-guide.md) §7 for details.

---

## SECTION 11: Manager Lifecycle

### Flow

1. **First task** calls `_get_or_spawn_manager(task_vars)`
2. No manager exists → spawns new manager process
3. Sets facts: `platform_manager_socket`, `platform_manager_authkey`
4. Returns `ManagerRPCClient` connected to new manager
5. **Subsequent tasks** call `_get_or_spawn_manager(task_vars)` → finds existing manager in facts → reuses it

### Inventory Setup

```yaml
# inventory/hosts.yml
all:
  hosts:
    localhost:
      ansible_connection: local
      novacom_url: https://api.novacom.io
      novacom_api_key: "{{ vault_novacom_api_key }}"
      # platform_manager_socket and platform_manager_authkey set by first task
```

### Connection Info Storage

The first task that spawns the manager uses `set_fact` with `cacheable: True` to store:
- `platform_manager_socket`: Path to the Unix socket
- `platform_manager_authkey`: Base64-encoded authkey for manager authentication

These facts persist across plays, enabling all tasks targeting the same host to reuse the manager.

---

## SECTION 12: Testing the Foundation

**File**: `tools/test_manager.py`

Test script to verify the manager can be spawned and responds correctly.

### Complete Implementation

```python
"""Test script for NovaCom Dashboard Platform Manager.

Run from collection root:
    cd ansible_collections/novacom/dashboard
    python ../../tools/test_manager.py

Or with path setup:
    PYTHONPATH=plugins python tools/test_manager.py
"""

import sys
from pathlib import Path

# Add collection root and ansible_collections parent to path
# Structure: ansible_collections/novacom/dashboard/tools/test_manager.py
_collection_root = Path(__file__).parent.parent  # dashboard/
_plugins_path = _collection_root / 'plugins'
if str(_plugins_path) not in sys.path:
    sys.path.insert(0, str(_collection_root))

# Parent of ansible_collections (for "from ansible_collections.novacom...")
_collections_parent = _collection_root.parent.parent.parent
if str(_collections_parent) not in sys.path:
    sys.path.insert(0, str(_collections_parent))


def main():
    """Run manager test."""
    from ansible_collections.novacom.dashboard.plugins.plugin_utils.manager.platform_manager import (
        PlatformManager,
        PlatformService
    )

    base_url = 'https://api.novacom.io'
    socket_path = '/tmp/novacom_test_manager.sock'
    authkey = b'test_secret_32_bytes_long!!!!'

    # Clean up old socket
    if Path(socket_path).exists():
        Path(socket_path).unlink()

    # Create service
    print("Creating PlatformService...")
    service = PlatformService(base_url)

    # Register with manager
    PlatformManager.register('get_platform_service', callable=lambda: service)

    # Start manager
    print(f"Starting manager at {socket_path}")
    manager = PlatformManager(address=socket_path, authkey=authkey)
    manager.start()

    print("Manager started successfully")
    print(f"API Version: {service.api_version}")
    print(f"Supported versions: {service.registry.get_supported_versions()}")

    # Keep running until interrupted
    import signal
    try:
        signal.pause()
    except AttributeError:
        # signal.pause() not available on Windows
        import time
        while True:
            time.sleep(3600)


if __name__ == '__main__':
    main()
```

### Running the Test

```bash
cd ansible_collections/novacom/dashboard
python ../../tools/test_manager.py
```

Or from project root with proper PYTHONPATH:

```bash
PYTHONPATH=ansible_collections/novacom/dashboard/plugins:ansible_collections \
  python tools/test_manager.py
```

Expected output:
```
Creating PlatformService...
Starting manager at /tmp/novacom_test_manager.sock
Manager started successfully
API Version: 1
Supported versions: ['1']
```

Press Ctrl+C to stop.

---

## Summary

The foundation provides:

| Component | Purpose |
|-----------|---------|
| **BaseTransformMixin** | Universal transformation logic (User ↔ Device) |
| **EndpointOperation** | API endpoint configuration type |
| **APIVersionRegistry** | Dynamic version/module discovery |
| **DynamicClassLoader** | Load version-specific classes |
| **PlatformService** | Persistent service, API calls, transformations |
| **PlatformManager** | Multiprocess manager with ThreadingMixIn |
| **ManagerRPCClient** | Client-side manager communication |
| **BaseResourceActionPlugin** | Manager spawning, validation, common logic |
| **Manager Lifecycle** | First task spawns, subsequent tasks reuse |

**All components are generic and work for ANY resource module.**

---

## Related Documents

- **07-implementation-features.md** — Adding new resource modules (vlan, ssid, organization)
- **08-implementation-generators.md** — Code generation tools
- **03-sdk-architecture.md** — Presentation-layer independence, SDK boundary
- **04-data-model-transformation.md** — User Model, Device Model, transformation patterns
