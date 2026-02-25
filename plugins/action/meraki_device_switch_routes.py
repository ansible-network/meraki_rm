"""Action plugin for meraki_device_switch_routes module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'device_switch_routing'
    SCOPE_PARAM = 'serial'
    USER_MODEL = 'plugins.plugin_utils.user_models.device_switch_routing.UserDeviceSwitchRouting'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'interface_id'
