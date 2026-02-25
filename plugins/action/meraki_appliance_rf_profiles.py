"""Action plugin for meraki_appliance_rf_profiles module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'appliance_rf_profile'
    USER_MODEL = 'plugins.plugin_utils.user_models.appliance_rf_profile.UserApplianceRfProfile'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'rf_profile_id'
