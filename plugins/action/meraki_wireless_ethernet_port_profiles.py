"""Action plugin for meraki_wireless_ethernet_port_profiles module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.ethernet_port_profile.UserEthernetPortProfile'
