"""User model for Meraki appliance static route."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserStaticRoute(BaseTransformMixin):
    """User-facing static route model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # identity
    static_route_id: Optional[str] = None
    # fields
    name: Optional[str] = None
    subnet: Optional[str] = None
    gateway_ip: Optional[str] = None
    gateway_vlan_id: Optional[int] = None
    enabled: Optional[bool] = None
    fixed_ip_assignments: Optional[Dict[str, Any]] = None
    reserved_ip_ranges: Optional[List[Dict[str, Any]]] = None
    ip_version: Optional[int] = None

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
