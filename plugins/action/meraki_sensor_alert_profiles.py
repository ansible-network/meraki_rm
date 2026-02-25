"""Action plugin for meraki_sensor_alert_profiles module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'sensor_alert_profile'
    USER_MODEL = 'plugins.plugin_utils.user_models.sensor_alert_profile.UserSensorAlertProfile'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'id'
