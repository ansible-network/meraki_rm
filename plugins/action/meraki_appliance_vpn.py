"""Action plugin for meraki_appliance_vpn module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'vpn'
    USER_MODEL = 'plugins.plugin_utils.user_models.vpn.UserVpn'
    SUPPORTS_DELETE = False
