"""User model for Meraki camera quality retention profile."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserCameraQualityRetentionProfile(BaseTransformMixin):
    """User-facing camera quality retention profile model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    quality_retention_profile_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    max_retention_days: Optional[int] = None
    motion_based_retention_enabled: Optional[bool] = None
    restricted_bandwidth_mode_enabled: Optional[bool] = None
    audio_recording_enabled: Optional[bool] = None
    cloud_archive_enabled: Optional[bool] = None
    schedule_id: Optional[str] = None
    video_settings: Optional[Dict[str, Dict[str, Any]]] = None
    smart_retention: Optional[Dict[str, Any]] = None

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
        from ..api.v1.camera_quality_retention_profile import APICameraQualityRetentionProfile_v1
        return APICameraQualityRetentionProfile_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
