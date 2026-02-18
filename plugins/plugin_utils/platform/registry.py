"""API version registry for dynamic version discovery.

This module provides filesystem-based discovery of available API versions
and module implementations without hardcoded version lists.

Adapted for cisco.meraki_rm. Meraki currently has only v1, but the
registry supports future multi-version expansion.
"""

from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


def _parse_version(version_str: str) -> tuple:
    """Parse version string into comparable tuple."""
    parts = version_str.split('.')
    result = []
    for part in parts:
        try:
            result.append(int(part))
        except ValueError:
            result.append(0)
    return tuple(result)


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

        self.versions: Dict[str, List[str]] = {}
        self.module_versions: Dict[str, List[str]] = {}

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

        for version_dir in self.api_base_path.iterdir():
            if not version_dir.is_dir():
                continue

            if not version_dir.name.startswith('v'):
                continue

            if version_dir.name in ('generated', '__pycache__'):
                continue

            version_str = version_dir.name[1:].replace('_', '.')

            module_files = [
                f for f in version_dir.iterdir()
                if f.is_file() and f.suffix == '.py' and not f.name.startswith('_')
            ]
            module_names = [f.stem for f in module_files]

            self.versions[version_str] = sorted(module_names)

            for module_name in module_names:
                if module_name not in self.module_versions:
                    self.module_versions[module_name] = []
                if version_str not in self.module_versions[module_name]:
                    self.module_versions[module_name].append(version_str)

        for module_name in self.module_versions:
            self.module_versions[module_name].sort(key=_parse_version)

        logger.info(
            f"Discovered {len(self.versions)} API versions: "
            f"{sorted(self.versions.keys(), key=_parse_version)}"
        )

    def get_supported_versions(self) -> List[str]:
        """
        Get all discovered API versions, sorted.

        Returns:
            List of version strings (e.g., ['1', '2', '2.1'])
        """
        return sorted(self.versions.keys(), key=_parse_version)

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

        requested = _parse_version(requested_version)
        available_parsed = [(v, _parse_version(v)) for v in available]

        if requested_version in available:
            logger.debug(
                f"Found exact version match for {module_name}: {requested_version}"
            )
            return requested_version

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
