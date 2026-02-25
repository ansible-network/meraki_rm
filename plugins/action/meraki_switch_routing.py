"""Action plugin for meraki_switch_routing module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.switch_routing.UserSwitchRouting'
