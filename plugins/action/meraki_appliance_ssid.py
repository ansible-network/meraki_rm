"""Action plugin for meraki_appliance_ssid module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'appliance_ssid'
    USER_MODEL = 'plugins.plugin_utils.user_models.appliance_ssid.UserApplianceSsid'
    SUPPORTS_DELETE = False
