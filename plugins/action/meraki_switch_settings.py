"""Action plugin for meraki_switch_settings module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'switch_settings'
    USER_MODEL = 'plugins.plugin_utils.user_models.switch_settings.UserSwitchSettings'
    SUPPORTS_DELETE = False
