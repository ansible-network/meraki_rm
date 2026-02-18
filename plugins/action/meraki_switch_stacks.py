"""Action plugin for meraki_switch_stacks module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'switch_stack'
    USER_MODEL = 'plugins.plugin_utils.user_models.switch_stack.UserSwitchStack'
