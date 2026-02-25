"""Action plugin for meraki_appliance_vlans module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'vlan'
    SCOPE_PARAM = 'network_id'
    USER_MODEL = 'plugins.plugin_utils.user_models.vlan.UserVlan'
    CANONICAL_KEY = 'vlan_id'
    SUPPORTS_DELETE = True
