"""Action plugin for meraki_organization_branding_policies module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.branding_policy.UserBrandingPolicy'
