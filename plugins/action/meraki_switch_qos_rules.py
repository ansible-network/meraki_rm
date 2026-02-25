"""Action plugin for meraki_switch_qos_rules module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'switch_qos_rule'
    USER_MODEL = 'plugins.plugin_utils.user_models.switch_qos_rule.UserSwitchQosRule'
    SYSTEM_KEY = 'qos_rule_id'
