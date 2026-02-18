"""Action plugin for meraki_meraki_auth_users module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'meraki_auth_users'
    USER_MODEL = 'plugins.plugin_utils.user_models.meraki_auth_users.UserMerakiAuthUser'
