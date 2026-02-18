"""User model for Meraki webhook HTTP server."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserWebhook(BaseTransformMixin):
    """User-facing webhook HTTP server model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    http_server_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    url: Optional[str] = None
    shared_secret: Optional[str] = None
    payload_template: Optional[Dict[str, Any]] = None

    _field_mapping = {
        'http_server_id': 'id',
        'name': 'name',
        'url': 'url',
        'shared_secret': 'sharedSecret',
        'payload_template': 'payloadTemplate',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.webhook import APIWebhook_v1
        return APIWebhook_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
