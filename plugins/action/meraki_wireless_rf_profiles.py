"""Action plugin for meraki_wireless_rf_profiles module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'wireless_rf_profile'
    USER_MODEL = 'plugins.plugin_utils.user_models.wireless_rf_profile.UserWirelessRfProfile'
    PRIMARY_KEY = 'rf_profile_id'
