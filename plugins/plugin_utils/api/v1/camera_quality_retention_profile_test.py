"""Colocated tests for APICameraQualityRetentionProfile_v1 — reverse transform, roundtrip & endpoints."""

from dataclasses import fields as dc_fields
from . import camera_quality_retention_profile as camera_quality_retention_profile_api
from ...user_models import camera_quality_retention_profile as camera_quality_retention_profile_user


def _ctx():
    return {'manager': None, 'cache': {}}


class TestReverseTransform:
    """API -> User (to_ansible) field mapping."""

    def test_mapped_fields(self):
        api = camera_quality_retention_profile_api.APICameraQualityRetentionProfile_v1(
            id='id_val',
            name='name_val',
            maxRetentionDays=24,
            motionBasedRetentionEnabled=True,
            restrictedBandwidthModeEnabled=True,
            audioRecordingEnabled=True,
            cloudArchiveEnabled=True,
            scheduleId='scheduleId_val',
            videoSettings={'k1': {'ip': '10.0.0.1', 'name': 'host'}},
            smartRetention={'enabled': True},
        )
        user = api.to_ansible(_ctx())

        assert user.quality_retention_profile_id == api.id
        assert user.name == api.name
        assert user.max_retention_days == api.maxRetentionDays
        assert user.motion_based_retention_enabled == api.motionBasedRetentionEnabled
        assert user.restricted_bandwidth_mode_enabled == api.restrictedBandwidthModeEnabled
        assert user.audio_recording_enabled == api.audioRecordingEnabled
        assert user.cloud_archive_enabled == api.cloudArchiveEnabled
        assert user.schedule_id == api.scheduleId
        assert user.video_settings == api.videoSettings
        assert user.smart_retention == api.smartRetention


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = camera_quality_retention_profile_user.UserCameraQualityRetentionProfile(
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
        ctx = _ctx()
        api = original.to_api(ctx)
        roundtripped = api.to_ansible(ctx)

        assert roundtripped.quality_retention_profile_id == original.quality_retention_profile_id
        assert roundtripped.name == original.name
        assert roundtripped.max_retention_days == original.max_retention_days
        assert roundtripped.motion_based_retention_enabled == original.motion_based_retention_enabled
        assert roundtripped.restricted_bandwidth_mode_enabled == original.restricted_bandwidth_mode_enabled
        assert roundtripped.audio_recording_enabled == original.audio_recording_enabled
        assert roundtripped.cloud_archive_enabled == original.cloud_archive_enabled
        assert roundtripped.schedule_id == original.schedule_id
        assert roundtripped.video_settings == original.video_settings
        assert roundtripped.smart_retention == original.smart_retention


class TestEndpointOperations:
    """Validate endpoint operations are well-formed."""

    def test_operations_exist(self):
        ops = camera_quality_retention_profile_api.APICameraQualityRetentionProfile_v1.get_endpoint_operations()
        assert len(ops) > 0

    def test_operations_have_required_fields(self):
        ops = camera_quality_retention_profile_api.APICameraQualityRetentionProfile_v1.get_endpoint_operations()
        for name, op in ops.items():
            assert op.path, f'{name} missing path'
            assert op.method, f'{name} missing method'
            assert op.path_params is not None, f'{name} missing path_params'

