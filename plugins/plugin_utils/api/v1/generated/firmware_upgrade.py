"""Generated API dataclass for Meraki network firmware_upgrade.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/firmwareUpgrades
    /networks/{networkId}/firmwareUpgrades/rollbacks
    /networks/{networkId}/firmwareUpgrades/staged/events
    /networks/{networkId}/firmwareUpgrades/staged/events/defer
    /networks/{networkId}/firmwareUpgrades/staged/events/rollbacks
    /networks/{networkId}/firmwareUpgrades/staged/groups
    /networks/{networkId}/firmwareUpgrades/staged/groups/{groupId}
    /networks/{networkId}/firmwareUpgrades/staged/stages
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class FirmwareUpgrade:
    """Meraki network firmware_upgrade API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # Array of Staged Upgrade Groups
    _json: Optional[List[Dict[str, Any]]] = None
    # The devices and Switch Stacks assigned to the Group
    assignedDevices: Optional[Dict[str, Any]] = None
    # Description of the Staged Upgrade Group
    description: Optional[str] = None
    # The Staged Upgrade Group
    group: Optional[Dict[str, Any]] = None
    # Id of staged upgrade group
    groupId: Optional[str] = None
    # Boolean indicating the default Group. Any device that does not have a gro...
    isDefault: Optional[bool] = None
    # Name of the Staged Upgrade Group
    name: Optional[str] = None
    # Product type to rollback (if the network is a combined network)
    product: Optional[str] = None
    # The network devices to be updated
    products: Optional[Dict[str, Any]] = None
    # Reasons for the rollback
    reasons: Optional[List[Dict[str, Any]]] = None
    # The ordered stages in the network
    stages: Optional[List[Dict[str, Any]]] = None
    # Status of the rollback
    status: Optional[str] = None
    # Scheduled time for the rollback
    time: Optional[str] = None
    # The timezone for the network
    timezone: Optional[str] = None
    # Version to downgrade to (if the network has firmware flexibility)
    toVersion: Optional[Dict[str, Any]] = None
    # Batch ID of the firmware rollback
    upgradeBatchId: Optional[str] = None
    # Upgrade window for devices in network
    upgradeWindow: Optional[Dict[str, Any]] = None
