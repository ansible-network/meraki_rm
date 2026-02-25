"""Action plugin for meraki_auth_users module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.meraki_auth_user.UserMerakiAuthUser'
