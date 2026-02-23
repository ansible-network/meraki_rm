"""Action plugin for meraki_auth_users module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'meraki_auth_user'
    USER_MODEL = 'plugins.plugin_utils.user_models.meraki_auth_user.UserMerakiAuthUser'
    PRIMARY_KEY = 'meraki_auth_user_id'
