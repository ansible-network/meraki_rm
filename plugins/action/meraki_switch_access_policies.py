"""Action plugin for meraki_switch_access_policies module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'switch_access_policy'
    USER_MODEL = 'plugins.plugin_utils.user_models.switch_access_policy.UserSwitchAccessPolicy'
