"""Action plugin for meraki_switch_stp module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'switch_stp'
    USER_MODEL = 'plugins.plugin_utils.user_models.switch_stp.UserSwitchStp'
    SUPPORTS_DELETE = False
