"""Action plugin for meraki_webhooks module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'webhook'
    USER_MODEL = 'plugins.plugin_utils.user_models.webhook.UserWebhook'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'http_server_id'
