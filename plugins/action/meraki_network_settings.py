"""Action plugin for meraki_network_settings module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'network_settings'
    USER_MODEL = 'plugins.plugin_utils.user_models.network_settings.UserNetworkSettings'
    SUPPORTS_DELETE = False
