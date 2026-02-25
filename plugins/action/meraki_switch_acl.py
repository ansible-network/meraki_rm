"""Action plugin for meraki_switch_acl module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.switch_acl.UserSwitchAcl'
