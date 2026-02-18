"""Colocated tests for UserCameraQualityRetentionProfile — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import camera_quality_retention_profile


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserCameraQualityRetentionProfile can be constructed with all fields."""

    def test_defaults(self):
        obj = camera_quality_retention_profile.UserCameraQualityRetentionProfile()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserCameraQualityRetentionProfile -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = camera_quality_retention_profile.UserCameraQualityRetentionProfile(
            quality_retention_profile_id='quality_retention_profile_id_val',
            name='name_val',
            max_retention_days=24,
            motion_based_retention_enabled=True,
            restricted_bandwidth_mode_enabled=True,
            audio_recording_enabled=True,
            cloud_archive_enabled=True,
            schedule_id='schedule_id_val',
            video_settings={'k1': {'ip': '10.0.0.1', 'name': 'host'}},
            smart_retention={'enabled': True},
        )
        api = user.to_api(_ctx())

        assert api.id == user.quality_retention_profile_id
        assert api.name == user.name
        assert api.maxRetentionDays == user.max_retention_days
        assert api.motionBasedRetentionEnabled == user.motion_based_retention_enabled
        assert api.restrictedBandwidthModeEnabled == user.restricted_bandwidth_mode_enabled
        assert api.audioRecordingEnabled == user.audio_recording_enabled
        assert api.cloudArchiveEnabled == user.cloud_archive_enabled
        assert api.scheduleId == user.schedule_id
        assert api.videoSettings == user.video_settings
        assert api.smartRetention == user.smart_retention

    def test_none_fields_omitted(self):
        user = camera_quality_retention_profile.UserCameraQualityRetentionProfile(quality_retention_profile_id='quality_retention_profile_id_val')
        api = user.to_api(_ctx())
        assert api.id == user.quality_retention_profile_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = camera_quality_retention_profile.UserCameraQualityRetentionProfile(network_id='network_id_val', quality_retention_profile_id='quality_retention_profile_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'network_id' not in api_field_names or getattr(api, 'network_id', None) is None

