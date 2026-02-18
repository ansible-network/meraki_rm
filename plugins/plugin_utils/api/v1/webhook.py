"""Versioned API model and transform mixin for Meraki webhook HTTP server (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.webhook import Webhook as GeneratedWebhook

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'httpServerId': ['http_server_id', 'id'],
}

# All mutable fields for create
_CREATE_FIELDS = [
    'name', 'url', 'sharedSecret', 'payloadTemplate',
]

# All mutable fields for update
_UPDATE_FIELDS = [
    'name', 'url', 'sharedSecret', 'payloadTemplate',
]


class WebhookTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki webhook HTTP server (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/webhooks/httpServers',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/webhooks/httpServers/{httpServerId}',
                method='GET',
                fields=[],
                path_params=['networkId', 'httpServerId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/webhooks/httpServers',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/webhooks/httpServers/{httpServerId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'httpServerId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/webhooks/httpServers/{httpServerId}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'httpServerId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APIWebhook_v1(GeneratedWebhook, WebhookTransformMixin_v1):
    """Versioned API model for Meraki webhook HTTP server (v1)."""

    _field_mapping = {
        'http_server_id': 'id',
        'name': 'name',
        'url': 'url',
        'shared_secret': 'sharedSecret',
        'payload_template': 'payloadTemplate',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.webhook import UserWebhook
        return UserWebhook
