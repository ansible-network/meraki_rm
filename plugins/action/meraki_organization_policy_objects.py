"""Action plugin for meraki_organization_policy_objects module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'policy_object'
    SCOPE_PARAM = 'organization_id'
    USER_MODEL = 'plugins.plugin_utils.user_models.policy_object.UserPolicyObject'
    PRIMARY_KEY = 'policy_object_id'
