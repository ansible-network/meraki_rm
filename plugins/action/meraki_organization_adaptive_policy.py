"""Action plugin for meraki_organization_adaptive_policy module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'adaptive_policy'
    SCOPE_PARAM = 'organization_id'
    USER_MODEL = 'plugins.plugin_utils.user_models.adaptive_policy.UserAdaptivePolicy'
    SUPPORTS_DELETE = False
