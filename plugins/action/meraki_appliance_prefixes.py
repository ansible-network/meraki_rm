"""Action plugin for meraki_appliance_prefixes module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'prefix'
    USER_MODEL = 'plugins.plugin_utils.user_models.prefix.UserPrefix'
    CANONICAL_KEY = 'prefix'
    SYSTEM_KEY = 'static_delegated_prefix_id'
