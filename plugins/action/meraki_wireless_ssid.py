"""Action plugin for meraki_wireless_ssid module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.ssid.UserSsid'
