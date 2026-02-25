"""Action plugin for meraki_switch_qos_rules module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.switch_qos_rule.UserSwitchQosRule'
