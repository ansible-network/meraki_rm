"""Generated API dataclass for Meraki network mqtt_broker.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/mqttBrokers
    /networks/{networkId}/mqttBrokers/{mqttBrokerId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class MqttBroker:
    """Meraki network mqtt_broker API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # Authentication settings of the MQTT broker
    authentication: Optional[Dict[str, Any]] = None
    # Host name/IP address where the MQTT broker runs.
    host: Optional[str] = None
    # ID of the MQTT Broker.
    id: Optional[str] = None
    # Name of the MQTT Broker.
    name: Optional[str] = None
    # Host port though which the MQTT broker can be reached.
    port: Optional[int] = None
    # Security settings of the MQTT broker.
    security: Optional[Dict[str, Any]] = None
