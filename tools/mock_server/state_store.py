"""In-memory stateful CRUD store for the mock server.

Maintains resource state across requests within a test session,
enabling convergence testing (gather -> diff -> act -> verify).

State is stored as nested dicts keyed by (resource_type, primary_key_values).
"""

import copy
import uuid
from typing import Any, Dict, List, Optional, Tuple


class StateStore:
    """In-memory resource state store.

    Supports CRUD operations keyed by resource type and primary key.
    State persists across requests within a process lifetime.

    Attributes:
        _store: Nested dict of resource_type -> primary_key -> resource_data
    """

    def __init__(self):
        self._store: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def create(
        self,
        resource_type: str,
        primary_key: Optional[str],
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Create a new resource.

        Args:
            resource_type: Type of resource (e.g., 'appliance_vlans')
            primary_key: Field name for the primary key (e.g., 'vlanId')
            data: Resource data dict

        Returns:
            Created resource data (with generated ID if needed)
        """
        if resource_type not in self._store:
            self._store[resource_type] = {}

        # Determine key value
        key_value = None
        if primary_key and primary_key in data:
            key_value = str(data[primary_key])
        elif 'id' in data:
            key_value = str(data['id'])
        else:
            key_value = str(uuid.uuid4())[:8]
            data['id'] = key_value

        self._store[resource_type][key_value] = copy.deepcopy(data)
        return copy.deepcopy(data)

    def get(
        self,
        resource_type: str,
        key_value: str,
    ) -> Optional[Dict[str, Any]]:
        """Get a single resource by primary key.

        Args:
            resource_type: Type of resource
            key_value: Primary key value

        Returns:
            Resource data dict, or None if not found
        """
        bucket = self._store.get(resource_type, {})
        item = bucket.get(str(key_value))
        return copy.deepcopy(item) if item else None

    def list(
        self,
        resource_type: str,
        filters: Optional[Dict[str, str]] = None,
    ) -> List[Dict[str, Any]]:
        """List all resources of a type, optionally filtered.

        Args:
            resource_type: Type of resource
            filters: Optional dict of field_name -> value to filter by

        Returns:
            List of matching resource data dicts
        """
        bucket = self._store.get(resource_type, {})
        items = list(bucket.values())

        if filters:
            for field, value in filters.items():
                items = [
                    item for item in items
                    if str(item.get(field)) == str(value)
                ]

        return copy.deepcopy(items)

    def update(
        self,
        resource_type: str,
        key_value: str,
        data: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """Update an existing resource (merge semantics).

        Args:
            resource_type: Type of resource
            key_value: Primary key value
            data: Fields to update

        Returns:
            Updated resource data, or None if not found
        """
        bucket = self._store.get(resource_type, {})
        existing = bucket.get(str(key_value))

        if existing is None:
            return None

        existing.update(data)
        return copy.deepcopy(existing)

    def delete(
        self,
        resource_type: str,
        key_value: str,
    ) -> bool:
        """Delete a resource by primary key.

        Args:
            resource_type: Type of resource
            key_value: Primary key value

        Returns:
            True if deleted, False if not found
        """
        bucket = self._store.get(resource_type, {})
        if str(key_value) in bucket:
            del bucket[str(key_value)]
            return True
        return False

    def clear(self, resource_type: Optional[str] = None) -> None:
        """Clear state.

        Args:
            resource_type: If provided, clear only this type.
                If None, clear all state.
        """
        if resource_type:
            self._store.pop(resource_type, None)
        else:
            self._store.clear()

    def dump(self) -> Dict[str, Any]:
        """Dump the entire state for debugging.

        Returns:
            Deep copy of the full store
        """
        return copy.deepcopy(self._store)
