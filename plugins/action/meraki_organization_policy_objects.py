"""Action plugin for meraki_organization_policy_objects module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.policy_object.UserPolicyObject'
