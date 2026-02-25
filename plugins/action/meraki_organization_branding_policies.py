"""Action plugin for meraki_organization_branding_policies module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'branding_policy'
    SCOPE_PARAM = 'organization_id'
    USER_MODEL = 'plugins.plugin_utils.user_models.branding_policy.UserBrandingPolicy'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'branding_policy_id'
