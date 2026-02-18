"""User model for Meraki facts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserFacts(BaseTransformMixin):
    """User-facing facts model with gather options."""

    gather_subset: Optional[List[str]] = None
    organization_id: Optional[str] = None
    network_id: Optional[str] = None

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.facts import APIFacts_v1
        return APIFacts_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
