"""User model for Meraki switch routing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..platform.base_transform import BaseTransformMixin


@dataclass
class UserSwitchRouting(BaseTransformMixin):
    """User-facing switch routing model with snake_case fields."""

    # scope
    network_id: Optional[str] = None
    # fields (singleton - no primary key)
    default_settings: Optional[Dict[str, Any]] = None
    overrides: Optional[List[Dict[str, Any]]] = None
    enabled: Optional[bool] = None
    hello_timer_in_seconds: Optional[int] = None
    dead_timer_in_seconds: Optional[int] = None
    areas: Optional[List[Dict[str, Any]]] = None
    md5_authentication_enabled: Optional[bool] = None
    md5_authentication_key: Optional[Dict[str, Any]] = None
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
