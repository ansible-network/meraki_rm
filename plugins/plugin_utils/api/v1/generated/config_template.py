"""Generated API dataclass for Meraki organization config_template.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /organizations/{organizationId}/configTemplates
    /organizations/{organizationId}/configTemplates/{configTemplateId}
    /organizations/{organizationId}/configTemplates/{configTemplateId}/switch/profiles
    /organizations/{organizationId}/configTemplates/{configTemplateId}/switch/profiles/{profileId}/ports
    /organizations/{organizationId}/configTemplates/{configTemplateId}/switch/profiles/{profileId}/ports/{portId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ConfigTemplate:
    """Meraki organization config_template API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # The number of a custom access policy to configure on the switch template ...
    accessPolicyNumber: Optional[int] = None
    # The type of the access policy of the switch template port. Only applicabl...
    accessPolicyType: Optional[str] = None
    # The VLANs allowed on the switch template port. Only applicable to trunk p...
    allowedVlans: Optional[str] = None
    # The ID of the network or config template to copy configuration from
    copyFromNetworkId: Optional[str] = None
    # If true, ARP packets for this port will be considered trusted, and Dynami...
    daiTrusted: Optional[bool] = None
    # dot3az settings for the port
    dot3az: Optional[Dict[str, Any]] = None
    # The status of the switch template port.
    enabled: Optional[bool] = None
    # For supported switches (e.g. MS420/MS425), whether or not the port has fl...
    flexibleStackingEnabled: Optional[bool] = None
    # High speed port enablement settings for C9500-32QC
    highSpeed: Optional[Dict[str, Any]] = None
    # The ID of the network or config template to copy configuration from
    id: Optional[str] = None
    # The isolation status of the switch template port.
    isolationEnabled: Optional[bool] = None
    # The link speed for the switch template port.
    linkNegotiation: Optional[str] = None
    # Available link speeds for the switch template port.
    linkNegotiationCapabilities: Optional[List[str]] = None
    # Only devices with MAC addresses specified in this list will have access t...
    macAllowList: Optional[List[str]] = None
    # The maximum number of MAC addresses for regular MAC allow list. Only appl...
    macWhitelistLimit: Optional[int] = None
    # Port mirror
    mirror: Optional[Dict[str, Any]] = None
    # Switch model
    model: Optional[str] = None
    # Expansion module
    module: Optional[Dict[str, Any]] = None
    # The name of the configuration template
    name: Optional[str] = None
    # The PoE status of the switch template port.
    poeEnabled: Optional[bool] = None
    # The identifier of the switch template port.
    portId: Optional[str] = None
    # The ID of the port schedule. A value of null will clear the port schedule.
    portScheduleId: Optional[str] = None
    # The product types of the configuration template
    productTypes: Optional[List[str]] = None
    # Profile attributes
    profile: Optional[Dict[str, Any]] = None
    # The rapid spanning tree protocol status.
    rstpEnabled: Optional[bool] = None
    # The port schedule data.
    schedule: Optional[Dict[str, Any]] = None
    # The initial list of MAC addresses for sticky Mac allow list. Only applica...
    stickyMacAllowList: Optional[List[str]] = None
    # The maximum number of MAC addresses for sticky MAC allow list. Only appli...
    stickyMacAllowListLimit: Optional[int] = None
    # The storm control status of the switch template port.
    stormControlEnabled: Optional[bool] = None
    # The state of the STP guard ('disabled', 'root guard', 'bpdu guard' or 'lo...
    stpGuard: Optional[str] = None
    # The state of STP PortFast Trunk on the switch template port.
    stpPortFastTrunk: Optional[bool] = None
    # Switch template id
    switchProfileId: Optional[str] = None
    # The list of tags of the switch template port.
    tags: Optional[List[str]] = None
    # The timezone of the configuration template. For a list of allowed timezon...
    timeZone: Optional[str] = None
    # The type of the switch template port ('access', 'trunk', 'stack', 'routed...
    type: Optional[str] = None
    # The action to take when Unidirectional Link is detected (Alert only, Enfo...
    udld: Optional[str] = None
    # The VLAN of the switch template port. For a trunk port, this is the nativ...
    vlan: Optional[int] = None
    # The voice VLAN of the switch template port. Only applicable to access ports.
    voiceVlan: Optional[int] = None
