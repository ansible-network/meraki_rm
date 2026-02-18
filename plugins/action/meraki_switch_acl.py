"""Action plugin for meraki_switch_acl module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'switch_acl'
    USER_MODEL = 'plugins.plugin_utils.user_models.switch_acl.UserSwitchAcl'
    SUPPORTS_DELETE = False
