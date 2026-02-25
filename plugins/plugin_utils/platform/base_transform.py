"""Base transformation mixin for bidirectional data transformation.

This module provides the core transformation logic used by all User Model
and API (Device) dataclasses in the cisco.meraki_rm collection.

Adapted from the NovaCom reference pattern for Meraki Dashboard API.
"""

from abc import ABC
from dataclasses import asdict, fields, is_dataclass
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

    Resource metadata (overridden by User Model subclasses):
        MODULE_NAME: Resource identifier used by PlatformManager (e.g. 'vlan')
        SCOPE_PARAM: Scope kwarg name ('network_id', 'organization_id', 'serial')
        CANONICAL_KEY: User-facing stable identifier field (e.g. 'name', 'vlan_id')
        SYSTEM_KEY: API-generated opaque identifier for URL routing (e.g. 'admin_id')
        SUPPORTS_DELETE: False for singletons that cannot be removed
        VALID_STATES: Frozenset of states this resource supports
    """

    _field_mapping: Optional[Dict] = None
    _transform_registry: Optional[Dict] = None

    MODULE_NAME: str = None
    SCOPE_PARAM: str = 'network_id'
    CANONICAL_KEY: str = None
    SYSTEM_KEY: str = None
    SUPPORTS_DELETE: bool = True
    VALID_STATES: frozenset = frozenset({
        'merged', 'replaced', 'overridden', 'deleted', 'gathered',
    })

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
            direction: 'forward' (User->Device) or 'reverse' (Device->User)
            context: Context dict for transformation functions

        Returns:
            Instance of target_class with transformed data
        """
        source_data = asdict(self)
        transformed_data = {}

        mapping = self._field_mapping or {}

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

        transformed_data = self._post_transform_hook(
            transformed_data, direction, context
        )

        # Only pass fields the target dataclass actually accepts — scope
        # parameters like networkId live in path_params, not in the body.
        if is_dataclass(target_class):
            valid_fields = {f.name for f in fields(target_class)}
            transformed_data = {
                k: v for k, v in transformed_data.items()
                if k in valid_fields
            }

        return target_class(**transformed_data)

    def _apply_forward_mapping(
        self,
        source_data: dict,
        mapping: dict,
        context: dict
    ) -> dict:
        """
        Apply forward mapping (User Model -> Device Model).

        Args:
            source_data: Source data as dict
            mapping: Field mapping configuration
            context: Transform context

        Returns:
            Transformed data dict
        """
        result = {}

        for user_field, spec in mapping.items():
            value = self._get_nested(source_data, user_field)

            if value is None:
                continue

            if isinstance(spec, dict) and 'forward_transform' in spec:
                transform_name = spec['forward_transform']
                value = self._apply_transform(value, transform_name, context)

            if isinstance(spec, str):
                target_field = spec
            elif isinstance(spec, dict):
                target_field = spec.get('api_field', user_field)
            else:
                target_field = user_field

            self._set_nested(result, target_field, value)

        return result

    def _apply_reverse_mapping(
        self,
        source_data: dict,
        mapping: dict,
        context: dict
    ) -> dict:
        """
        Apply reverse mapping (Device Model -> User Model).

        Args:
            source_data: Source data as dict
            mapping: Field mapping configuration
            context: Transform context

        Returns:
            Transformed data dict
        """
        result = {}

        for user_field, spec in mapping.items():
            if isinstance(spec, str):
                source_field = spec
            elif isinstance(spec, dict):
                source_field = spec.get('api_field', user_field)
            else:
                source_field = user_field

            value = self._get_nested(source_data, source_field)

            if value is None:
                continue

            if isinstance(spec, dict) and 'reverse_transform' in spec:
                transform_name = spec['reverse_transform']
                value = self._apply_transform(value, transform_name, context)

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

        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

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

    def validate(self) -> None:
        """Validate field values against spec-derived constraints.

        Checks _FIELD_CONSTRAINTS (emitted by the generator on API
        dataclasses) for enum membership.  Raises ValueError listing
        every violation so the caller gets a single, complete report.

        Subclasses can call super().validate() and add custom checks.

        Raises:
            ValueError: One or more fields violate their constraints.
        """
        constraints = getattr(self, '_FIELD_CONSTRAINTS', None)
        if not constraints:
            return

        errors = []
        for field_name, rules in constraints.items():
            value = getattr(self, field_name, None)
            if value is None:
                continue
            allowed = rules.get('enum')
            if allowed and value not in allowed:
                errors.append(
                    f"{field_name}={value!r} not in {allowed}"
                )

        if errors:
            cls_name = type(self).__name__
            raise ValueError(
                f"{cls_name} constraint violations: {'; '.join(errors)}"
            )
