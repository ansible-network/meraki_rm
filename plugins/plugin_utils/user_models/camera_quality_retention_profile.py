"""User model for Meraki camera quality retention profile."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserCameraQualityRetentionProfile(BaseTransformMixin):
    """User-facing camera quality retention profile model with snake_case fields."""

    MODULE_NAME = 'camera_quality_retention_profile'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'quality_retention_profile_id'

    # scope
    network_id: Optional[str] = None
    # identity
    quality_retention_profile_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Name of the quality retention profile."})
    max_retention_days: Optional[int] = field(default=None, metadata={"description": "Maximum retention days for recordings."})
    motion_based_retention_enabled: Optional[bool] = field(default=None, metadata={"description": "Enable motion-based retention."})
    restricted_bandwidth_mode_enabled: Optional[bool] = field(default=None, metadata={"description": "Enable restricted bandwidth mode."})
    audio_recording_enabled: Optional[bool] = field(default=None, metadata={"description": "Enable audio recording."})
    cloud_archive_enabled: Optional[bool] = field(default=None, metadata={"description": "Enable cloud archive."})
    schedule_id: Optional[str] = field(default=None, metadata={"description": "Schedule ID for recording."})
    video_settings: Optional[Dict[str, Dict[str, Any]]] = field(default=None, metadata={"description": "Video quality and resolution settings per camera model."})
    smart_retention: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Smart retention settings."})

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
