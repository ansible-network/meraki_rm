"""User model for Meraki appliance static route."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserStaticRoute(BaseTransformMixin):
    """User-facing static route model with snake_case fields."""

    MODULE_NAME = 'static_route'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'static_route_id'

    # scope
    network_id: Optional[str] = None
    # identity
    static_route_id: Optional[str] = field(default=None, metadata={"description": "Server-assigned ID, resolved automatically by matching on C(name). Provide only to disambiguate when duplicate names exist."})
    # fields
    name: Optional[str] = field(default=None, metadata={"description": "Name of the route."})
    subnet: Optional[str] = field(default=None, metadata={"description": "Subnet of the route (e.g., 192.168.1.0/24)."})
    gateway_ip: Optional[str] = field(default=None, metadata={"description": "Gateway IP address (next hop)."})
    gateway_vlan_id: Optional[int] = field(default=None, metadata={"description": "Gateway VLAN ID."})
    enabled: Optional[bool] = field(default=None, metadata={"description": "Whether the route is enabled."})
    fixed_ip_assignments: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Fixed DHCP IP assignments on the route."})
    reserved_ip_ranges: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "DHCP reserved IP ranges."})
    ip_version: Optional[int] = field(default=None, metadata={"description": "IP protocol version (4 or 6)."})

    _field_mapping = {
        'static_route_id': 'id',
        'name': 'name',
        'subnet': 'subnet',
        'gateway_ip': 'gatewayIp',
        'gateway_vlan_id': 'gatewayVlanId',
        'enabled': 'enabled',
        'fixed_ip_assignments': 'fixedIpAssignments',
        'reserved_ip_ranges': 'reservedIpRanges',
        'ip_version': 'ipVersion',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.static_route import APIStaticRoute_v1
        return APIStaticRoute_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
