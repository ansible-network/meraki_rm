"""Action plugin for meraki_appliance_warm_spare module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.warm_spare.UserWarmSpare'
