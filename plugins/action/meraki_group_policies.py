"""Action plugin for meraki_group_policies module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.group_policy.UserGroupPolicy'
