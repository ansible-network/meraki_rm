"""Action plugin for meraki_appliance_firewall module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'firewall'
    USER_MODEL = 'plugins.plugin_utils.user_models.firewall.UserFirewall'
    SUPPORTS_DELETE = False
