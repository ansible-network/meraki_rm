"""Action plugin for meraki_device_switch_routes module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.device_switch_routing.UserDeviceSwitchRouting'
