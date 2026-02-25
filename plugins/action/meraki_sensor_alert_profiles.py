"""Action plugin for meraki_sensor_alert_profiles module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.sensor_alert_profile.UserSensorAlertProfile'
