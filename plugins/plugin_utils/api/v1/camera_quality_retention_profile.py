"""Versioned API model and transform mixin for Meraki camera quality retention profile (v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ...platform.base_transform import BaseTransformMixin
from ...platform.types import EndpointOperation
from .generated.camera_quality_retention_profile import CameraQualityRetentionProfile as GeneratedCameraQualityRetentionProfile

# Path param aliases for snake_case user model -> camelCase API path
_PATH_PARAM_ALIASES = {
    'networkId': ['network_id'],
    'qualityRetentionProfileId': ['quality_retention_profile_id', 'id'],
}

# All mutable fields for create (API creates profile, returns id)
_CREATE_FIELDS = [
    'name', 'maxRetentionDays', 'motionBasedRetentionEnabled',
    'restrictedBandwidthModeEnabled', 'audioRecordingEnabled', 'cloudArchiveEnabled',
    'scheduleId', 'videoSettings', 'smartRetention',
]

# All mutable fields for update (no id in body)
_UPDATE_FIELDS = [
    'name', 'maxRetentionDays', 'motionBasedRetentionEnabled',
    'restrictedBandwidthModeEnabled', 'audioRecordingEnabled', 'cloudArchiveEnabled',
    'scheduleId', 'videoSettings', 'smartRetention',
]


class CameraQualityRetentionProfileTransformMixin_v1(BaseTransformMixin):
    """Transform mixin for Meraki camera quality retention profile (v1)."""

    @classmethod
    def get_endpoint_operations(cls) -> Dict[str, EndpointOperation]:
        return {
            'create': EndpointOperation(
                path='/networks/{networkId}/camera/qualityRetentionProfiles',
                method='POST',
                fields=_CREATE_FIELDS,
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='create',
                order=1,
            ),
            'find': EndpointOperation(
                path='/networks/{networkId}/camera/qualityRetentionProfiles/{qualityRetentionProfileId}',
                method='GET',
                fields=[],
                path_params=['networkId', 'qualityRetentionProfileId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'find_all': EndpointOperation(
                path='/networks/{networkId}/camera/qualityRetentionProfiles',
                method='GET',
                fields=[],
                path_params=['networkId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='find',
                order=1,
            ),
            'update': EndpointOperation(
                path='/networks/{networkId}/camera/qualityRetentionProfiles/{qualityRetentionProfileId}',
                method='PUT',
                fields=_UPDATE_FIELDS,
                path_params=['networkId', 'qualityRetentionProfileId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='update',
                order=1,
            ),
            'delete': EndpointOperation(
                path='/networks/{networkId}/camera/qualityRetentionProfiles/{qualityRetentionProfileId}',
                method='DELETE',
                fields=[],
                path_params=['networkId', 'qualityRetentionProfileId'],
                path_param_aliases=_PATH_PARAM_ALIASES,
                required_for='delete',
                order=1,
            ),
        }


@dataclass
class APICameraQualityRetentionProfile_v1(GeneratedCameraQualityRetentionProfile, CameraQualityRetentionProfileTransformMixin_v1):
    """Versioned API model for Meraki camera quality retention profile (v1)."""

    _field_mapping = {
        'quality_retention_profile_id': 'id',
        'name': 'name',
        'max_retention_days': 'maxRetentionDays',
        'motion_based_retention_enabled': 'motionBasedRetentionEnabled',
        'restricted_bandwidth_mode_enabled': 'restrictedBandwidthModeEnabled',
        'audio_recording_enabled': 'audioRecordingEnabled',
        'cloud_archive_enabled': 'cloudArchiveEnabled',
        'schedule_id': 'scheduleId',
        'video_settings': 'videoSettings',
        'smart_retention': 'smartRetention',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        from ...user_models.camera_quality_retention_profile import UserCameraQualityRetentionProfile
        return UserCameraQualityRetentionProfile
