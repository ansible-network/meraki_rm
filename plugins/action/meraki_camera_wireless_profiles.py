"""Action plugin for meraki_camera_wireless_profiles module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.camera_wireless_profile.UserCameraWirelessProfile'
