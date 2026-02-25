"""Action plugin for meraki_camera_quality_retention_profiles module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.camera_quality_retention_profile.UserCameraQualityRetentionProfile'
