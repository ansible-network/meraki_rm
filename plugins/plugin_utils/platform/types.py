"""Shared type definitions for the cisco.meraki_rm collection.

This module contains dataclasses and type definitions used throughout
the framework.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class EndpointOperation:
    """
    Configuration for a single API endpoint operation.

    Defines how to call a specific API endpoint, what data to send,
    and how it relates to other operations.

    Attributes:
        path: API endpoint path (e.g., '/api/v1/networks/{networkId}/appliance/vlans')
        method: HTTP method ('GET', 'POST', 'PUT', 'DELETE')
        fields: List of dataclass field names to include in request
        path_params: Optional list of path parameter names (e.g., ['networkId', 'vlanId'])
        path_param_aliases: Optional mapping of path param -> alternative field names
            (e.g., {'networkId': ['network_id'], 'vlanId': ['vlan_id', 'id']})
        required_for: Optional operation type this is required for
            ('create', 'update', 'delete', 'find', or None for always)
        depends_on: Optional name of operation this depends on
        order: Execution order (lower runs first)
        batch_eligible: Whether this operation can be included in a Meraki
            Action Batch for atomic multi-operation transactions

    Examples:
        >>> EndpointOperation(
        ...     path='/api/v1/networks/{networkId}/appliance/vlans',
        ...     method='POST',
        ...     fields=['id', 'name', 'subnet', 'applianceIp'],
        ...     path_params=['networkId'],
        ...     required_for='create',
        ...     order=1,
        ...     batch_eligible=True,
        ... )

        >>> EndpointOperation(
        ...     path='/api/v1/networks/{networkId}/appliance/vlans/{vlanId}',
        ...     method='GET',
        ...     fields=[],
        ...     path_params=['networkId', 'vlanId'],
        ...     required_for='find',
        ...     order=1,
        ... )
    """

    path: str
    method: str
    fields: List[str]
    path_params: Optional[List[str]] = None
    path_param_aliases: Optional[Dict[str, List[str]]] = None
    required_for: Optional[str] = None
    depends_on: Optional[str] = None
    order: int = 0
    batch_eligible: bool = True


@dataclass
class ResourceModuleStates:
    """
    Defines which states a resource module supports.

    Resource modules implement a subset of the seven canonical states.
    This dataclass declares which states are available.

    Attributes:
        merged: Supports merged state (create/update, default)
        replaced: Supports replaced state (full resource replacement)
        overridden: Supports overridden state (replace all instances)
        deleted: Supports deleted state (remove resource)
        gathered: Supports gathered state (read-only)
    """

    merged: bool = True
    replaced: bool = False
    overridden: bool = False
    deleted: bool = True
    gathered: bool = True


@dataclass
class ModuleConfig:
    """
    Configuration for a resource module.

    Defines the module's identity, scope, and capabilities.

    Attributes:
        name: Module name (e.g., 'vlan', 'ssid')
        domain: API domain (e.g., 'appliance', 'wireless', 'switch')
        scope: Scope type ('network', 'organization', 'device')
        scope_param: Name of the scope path parameter (e.g., 'networkId')
        primary_key: Primary key field in the API (e.g., 'vlanId', 'number')
        states: Supported resource module states
        endpoints: Dict of operation name to EndpointOperation
    """

    name: str
    domain: str
    scope: str
    scope_param: str
    primary_key: Optional[str] = None
    states: ResourceModuleStates = field(default_factory=ResourceModuleStates)
