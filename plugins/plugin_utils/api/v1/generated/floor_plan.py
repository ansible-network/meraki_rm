"""Generated API dataclass for Meraki network floor_plan.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/floorPlans
    /networks/{networkId}/floorPlans/autoLocate/jobs/batch
    /networks/{networkId}/floorPlans/autoLocate/jobs/{jobId}/cancel
    /networks/{networkId}/floorPlans/autoLocate/jobs/{jobId}/publish
    /networks/{networkId}/floorPlans/autoLocate/jobs/{jobId}/recalculate
    /networks/{networkId}/floorPlans/devices/batchUpdate
    /networks/{networkId}/floorPlans/{floorPlanId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class FloorPlan:
    """Meraki network floor_plan API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # List of floorplan assignments to update. Up to 100 floor plan assignments...
    assignments: Optional[List[Dict[str, Any]]] = None
    # The longitude and latitude of the bottom left corner of your floor plan.
    bottomLeftCorner: Optional[Dict[str, Any]] = None
    # The longitude and latitude of the bottom right corner of your floor plan.
    bottomRightCorner: Optional[Dict[str, Any]] = None
    # The longitude and latitude of the center of your floor plan. The 'center'...
    center: Optional[Dict[str, Any]] = None
    # List of devices for the floorplan
    devices: Optional[List[Dict[str, Any]]] = None
    # The floor number of the floor within the building.
    floorNumber: Optional[float] = None
    # Floor plan ID
    floorPlanId: Optional[str] = None
    # The height of your floor plan.
    height: Optional[float] = None
    # The file contents (a base 64 encoded string) of your image. Supported for...
    imageContents: Optional[str] = None
    # The format type of the image.
    imageExtension: Optional[str] = None
    # The file contents (a base 64 encoded string) of your new image. Supported...
    imageMd5: Optional[str] = None
    # The url link for the floor plan image.
    imageUrl: Optional[str] = None
    # The time the image url link will expire.
    imageUrlExpiresAt: Optional[str] = None
    # The list of auto locate jobs to be scheduled. Up to 100 jobs can be provi...
    jobs: Optional[List[Dict[str, Any]]] = None
    # The name of your floor plan.
    name: Optional[str] = None
    # Status of attempt to publish auto locate job
    success: Optional[bool] = None
    # The longitude and latitude of the top left corner of your floor plan.
    topLeftCorner: Optional[Dict[str, Any]] = None
    # The longitude and latitude of the top right corner of your floor plan.
    topRightCorner: Optional[Dict[str, Any]] = None
    # The width of your floor plan.
    width: Optional[float] = None
