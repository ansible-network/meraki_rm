"""Action plugin for meraki_camera_quality_retention_profiles module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'camera_quality_retention_profile'
    USER_MODEL = 'plugins.plugin_utils.user_models.camera_quality_retention_profile.UserCameraQualityRetentionProfile'
    PRIMARY_KEY = 'quality_retention_profile_id'
