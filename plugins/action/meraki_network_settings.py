"""Action plugin for meraki_network_settings module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.network_settings.UserNetworkSettings'
