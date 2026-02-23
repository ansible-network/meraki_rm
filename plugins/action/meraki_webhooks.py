"""Action plugin for meraki_webhooks module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'webhook'
    USER_MODEL = 'plugins.plugin_utils.user_models.webhook.UserWebhook'
    PRIMARY_KEY = 'http_server_id'
