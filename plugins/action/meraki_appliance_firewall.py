"""Action plugin for meraki_appliance_firewall module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.firewall.UserFirewall'
