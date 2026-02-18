"""Action plugin for meraki_switch_ports module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'switch_port'
    SCOPE_PARAM = 'serial'
    USER_MODEL = 'plugins.plugin_utils.user_models.switch_port.UserSwitchPort'
    SUPPORTS_DELETE = False
