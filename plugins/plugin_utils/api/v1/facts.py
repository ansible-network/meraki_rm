"""Versioned API model for Meraki facts (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin


class FactsTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki facts (v1). No endpoint operations."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, Any]:
        return {}


@dataclass
class APIFacts_v1(FactsTransformMixin_v1):
    """Versioned API model for Meraki facts (v1)."""

    organizations: Optional[List[Dict[str, Any]]] = None
    networks: Optional[List[Dict[str, Any]]] = None
    devices: Optional[List[Dict[str, Any]]] = None
    inventory: Optional[List[Dict[str, Any]]] = None

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.facts import UserFacts
        return UserFacts
