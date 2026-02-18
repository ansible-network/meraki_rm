"""Generated API dataclass for Meraki network webhook.

Auto-generated from spec3.json inline schemas.
DO NOT EDIT MANUALLY — regenerate using:
    python -m tools.generators.extract_meraki_schemas

Source paths:
    /networks/{networkId}/webhooks/httpServers
    /networks/{networkId}/webhooks/httpServers/{httpServerId}
    /networks/{networkId}/webhooks/payloadTemplates
    /networks/{networkId}/webhooks/payloadTemplates/{payloadTemplateId}
    /networks/{networkId}/webhooks/webhookTests
    /networks/{networkId}/webhooks/webhookTests/{webhookTestId}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Webhook:
    """Meraki network webhook API schema.

    Fields use camelCase matching the Meraki Dashboard API.
    The transform mixin converts to/from snake_case User Model fields.
    """

    # The type of alert which the test webhook will send. Optional. Defaults to...
    alertTypeId: Optional[str] = None
    # The body of the payload template, in liquid template
    body: Optional[str] = None
    # A Base64 encoded file containing liquid template used for the body of the...
    bodyFile: Optional[str] = None
    # The payload template headers, will be rendered as a key-value pair in the...
    headers: Optional[List[Dict[str, Any]]] = None
    # A Base64 encoded file containing the liquid template used with the webhoo...
    headersFile: Optional[str] = None
    # A Base64 encoded ID.
    id: Optional[str] = None
    # A name for easy reference to the HTTP server
    name: Optional[str] = None
    # A Meraki network ID.
    networkId: Optional[str] = None
    # The payload template to use when posting data to the HTTP server.
    payloadTemplate: Optional[Dict[str, Any]] = None
    # Webhook payload template Id
    payloadTemplateId: Optional[str] = None
    # The name of the payload template.
    payloadTemplateName: Optional[str] = None
    # A shared secret that will be included in POSTs sent to the HTTP server. T...
    sharedSecret: Optional[str] = None
    # Information on which entities have access to the template
    sharing: Optional[Dict[str, Any]] = None
    # Current status of the webhook delivery
    status: Optional[str] = None
    # The type of the payload template
    type: Optional[str] = None
    # The URL of the HTTP server.
    url: Optional[str] = None
