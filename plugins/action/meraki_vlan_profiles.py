"""Action plugin for meraki_vlan_profiles module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'vlan_profile'
    USER_MODEL = 'plugins.plugin_utils.user_models.vlan_profile.UserVlanProfile'
    PRIMARY_KEY = 'iname'
