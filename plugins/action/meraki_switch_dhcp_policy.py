"""Action plugin for meraki_switch_dhcp_policy module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.switch_dhcp_policy.UserSwitchDhcpPolicy'
