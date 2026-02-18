"""Generated API dataclass for Meraki camera camera_quality_retention_profile.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/camera/qualityRetentionProfiles
    /networks/{networkId}/camera/qualityRetentionProfiles/{qualityRetentionProfileId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class CameraQualityRetentionProfile:
    """Meraki camera camera_quality_retention_profile API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # Whether audio recording is enabled
    audioRecordingEnabled: Optional[bool] = None
    # Whether cloud archive is enabled
    cloudArchiveEnabled: Optional[bool] = None
    # Unique identifier for the quality retention profile
    id: Optional[str] = None
    # Maximum retention days
    maxRetentionDays: Optional[int] = None
    # Whether motion-based retention is enabled
    motionBasedRetentionEnabled: Optional[bool] = None
    # Motion detector version
    motionDetectorVersion: Optional[int] = None
    # Name of the quality retention profile
    name: Optional[str] = None
    # Network ID
    networkId: Optional[str] = None
    # Whether restricted bandwidth mode is enabled
    restrictedBandwidthModeEnabled: Optional[bool] = None
    # Schedule ID
    scheduleId: Optional[str] = None
    # Smart retention settings
    smartRetention: Optional[Dict[str, Any]] = None
    # Video quality and resolution settings for camera models
    videoSettings: Optional[Dict[str, Dict[str, Any]]] = None
