"""Dynamic class loader for version-specific implementations.

This module loads User Model and API dataclasses based on the detected
API version without hardcoded imports.

Adapted for cisco.meraki_rm collection.
"""

import importlib
import inspect
from typing import Type, Tuple, Optional, Dict
import logging

from .base_transform import BaseTransformMixin
from .registry import APIVersionRegistry

logger = logging.getLogger(__name__)

def _detect_collection_prefix() -> str:
    """Derive import prefix from this module's own package path.

    When running inside Ansible, __name__ is something like
    'ansible_collections.cisco.meraki_rm.plugins.plugin_utils.platform.loader'.
    We need 'ansible_collections.cisco.meraki_rm.plugins.plugin_utils'.

    When running directly from the workspace (tests/dev), __name__ is
    'plugins.plugin_utils.platform.loader' and we need 'plugins.plugin_utils'.
    """
    parts = __name__.split('.')
    # Drop the last two segments (.platform.loader) to get the prefix
    if len(parts) > 2:
        return '.'.join(parts[:-2])
    return 'plugins.plugin_utils'


_COLLECTION_PREFIX = _detect_collection_prefix()


class DynamicClassLoader:
    """
    Dynamically load version-specific classes at runtime.

    Loads the appropriate User Model dataclass and API dataclass/mixin
    based on the module name and API version.

    Attributes:
        registry: APIVersionRegistry for version discovery
        class_cache: Cache of loaded classes to avoid repeated imports
        collection_prefix: Import path prefix for the collection
    """

    def __init__(
        self,
        registry: APIVersionRegistry,
        collection_prefix: Optional[str] = None,
    ):
        """
        Initialize loader with a version registry.

        Args:
            registry: Version registry for discovering available versions
            collection_prefix: Import path prefix (defaults to flat-layout path)
        """
        self.registry = registry
        self._class_cache: Dict[str, Tuple[Type, Type, Type]] = {}
        self.collection_prefix = collection_prefix or _COLLECTION_PREFIX

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
        best_version = self.registry.find_best_version(api_version, module_name)

        if not best_version:
            raise ValueError(
                f"No compatible API version found for module '{module_name}' "
                f"with requested version '{api_version}'"
            )

        cache_key = f"{module_name}_{best_version.replace('.', '_')}"
        if cache_key in self._class_cache:
            logger.debug(f"Using cached classes for {cache_key}")
            return self._class_cache[cache_key]

        logger.info(
            f"Loading classes for {module_name} (API version {best_version})"
        )

        user_class = self._load_user_class(module_name)
        api_class, mixin_class = self._load_api_classes(module_name, best_version)

        result = (user_class, api_class, mixin_class)
        self._class_cache[cache_key] = result

        return result

    def _load_user_class(self, module_name: str) -> Type:
        """
        Load stable User Model dataclass from user_models/.

        Args:
            module_name: Module name (e.g., 'vlan')

        Returns:
            User Model dataclass type (e.g., UserVlan)

        Raises:
            ImportError: If module cannot be imported
            ValueError: If class cannot be found
        """
        module_path = f'{self.collection_prefix}.user_models.{module_name}'

        try:
            module = importlib.import_module(module_path)
        except ImportError as e:
            raise ImportError(
                f"Failed to import User Model module {module_path}: {e}"
            ) from e

        class_name = f'User{module_name.title().replace("_", "")}'

        if hasattr(module, class_name):
            return getattr(module, class_name)

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
        version_normalized = api_version.replace('.', '_')
        module_path = (
            f'{self.collection_prefix}.api.'
            f'v{version_normalized}.{module_name}'
        )

        try:
            module = importlib.import_module(module_path)
        except ImportError as e:
            raise ImportError(
                f"Failed to import API module {module_path}: {e}"
            ) from e

        title_name = module_name.title().replace('_', '')
        api_class_name = f'API{title_name}_v{version_normalized}'
        api_class = self._find_class_in_module(
            module,
            [api_class_name, f'API{title_name}', 'API*'],
            f"API dataclass for {module_name}"
        )

        mixin_class_name = f'{title_name}TransformMixin_v{version_normalized}'
        mixin_class = self._find_class_in_module(
            module,
            [mixin_class_name, f'{title_name}TransformMixin', '*TransformMixin'],
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
        classes = inspect.getmembers(module, inspect.isclass)

        if base_class:
            classes = [
                (name, cls) for name, cls in classes
                if issubclass(cls, base_class) and cls != base_class
            ]

        for pattern in patterns:
            if '*' in pattern:
                prefix = pattern.replace('*', '')
                for name, cls in classes:
                    if name.startswith(prefix):
                        logger.debug(
                            f"Found {description}: {name} (pattern: {pattern})"
                        )
                        return cls
            else:
                for name, cls in classes:
                    if name == pattern:
                        logger.debug(f"Found {description}: {name}")
                        return cls

        raise ValueError(
            f"No {description} found in {module.__name__}. "
            f"Tried patterns: {patterns}"
        )
