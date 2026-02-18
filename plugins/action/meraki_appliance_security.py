"""Action plugin for meraki_appliance_security module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'security'
    USER_MODEL = 'plugins.plugin_utils.user_models.security.UserSecurity'
    SUPPORTS_DELETE = False
