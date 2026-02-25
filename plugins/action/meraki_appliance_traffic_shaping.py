"""Action plugin for meraki_appliance_traffic_shaping module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.traffic_shaping.UserTrafficShaping'
