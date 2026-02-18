"""Action plugin for meraki_wireless_ethernet_port_profiles module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'ethernet_port_profile'
    USER_MODEL = 'plugins.plugin_utils.user_models.ethernet_port_profile.UserEthernetPortProfile'
