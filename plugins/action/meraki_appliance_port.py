"""Action plugin for meraki_appliance_port module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'port'
    USER_MODEL = 'plugins.plugin_utils.user_models.port.UserPort'
    SUPPORTS_DELETE = False
