"""Action plugin for meraki_appliance_warm_spare module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'warm_spare'
    USER_MODEL = 'plugins.plugin_utils.user_models.warm_spare.UserWarmSpare'
    SUPPORTS_DELETE = False
