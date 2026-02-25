"""User model for Meraki webhook HTTP server."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserWebhook(BaseTransformMixin):
    """User-facing webhook HTTP server model with snake_case fields."""

    MODULE_NAME = 'webhook'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'http_server_id'

    # scope
    network_id: Optional[str] = None
    # identity
    http_server_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Name for easy reference to the HTTP server."})
    url: Optional[str] = field(default=None, metadata={"description": "URL of the HTTP server."})
    shared_secret: Optional[str] = field(default=None, metadata={"description": "Shared secret included in POSTs to the server."})
    payload_template: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Payload template for POSTs to the HTTP server."})

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
