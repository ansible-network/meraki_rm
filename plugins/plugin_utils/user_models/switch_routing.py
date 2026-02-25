"""User model for Meraki switch routing."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchRouting(BaseTransformMixin):
    """User-facing switch routing model with snake_case fields."""

    MODULE_NAME = 'switch_routing'
    SUPPORTS_DELETE = False

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    default_settings: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "Default multicast settings for the network."})
    overrides: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "Multicast overrides per switch/stack/profile."})
    enabled: Optional[bool] = field(default=None, metadata={"description": "Enable OSPF routing."})
    hello_timer_in_seconds: Optional[int] = field(default=None, metadata={"description": "OSPF hello timer in seconds."})
    dead_timer_in_seconds: Optional[int] = field(default=None, metadata={"description": "OSPF dead timer in seconds."})
    areas: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "OSPF areas."})
    md5_authentication_enabled: Optional[bool] = field(default=None, metadata={"description": "Enable MD5 authentication for OSPF."})
    md5_authentication_key: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "MD5 authentication credentials."})
    v3: Optional[Dict[str, Any]] = None

    _field_mapping = {
        'default_settings': 'defaultSettings',
        'overrides': 'overrides',
        'enabled': 'enabled',
        'hello_timer_in_seconds': 'helloTimerInSeconds',
        'dead_timer_in_seconds': 'deadTimerInSeconds',
        'areas': 'areas',
        'md5_authentication_enabled': 'md5AuthenticationEnabled',
        'md5_authentication_key': 'md5AuthenticationKey',
        'v3': 'v3',
    }

    @classmethod
    def _get_api_class(cls):
        from ..api.v1.switch_routing import APISwitchRouting_v1
        return APISwitchRouting_v1

    @classmethod
    def _get_ansible_class(cls):
        return cls
