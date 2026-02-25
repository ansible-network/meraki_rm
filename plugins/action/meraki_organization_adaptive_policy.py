"""Action plugin for meraki_organization_adaptive_policy module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.adaptive_policy.UserAdaptivePolicy'
