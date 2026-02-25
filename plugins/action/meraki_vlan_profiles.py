"""Action plugin for meraki_vlan_profiles module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.vlan_profile.UserVlanProfile'
