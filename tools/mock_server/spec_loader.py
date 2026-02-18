"""OpenAPI spec loading, path parsing, and schema extraction.

Loads the Meraki OpenAPI spec and provides:
- Path-to-Flask route conversion
- Schema lookup by path + method + direction (request/response)
- Primary key inference from path parameters
- Response status code lookup
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PathItem = Dict[str, Any]
Schema = Dict[str, Any]


class SpecLoader:
    """Loads and indexes the OpenAPI spec for the mock server.

    Attributes:
        spec: The parsed OpenAPI spec dict
        paths: Dict of API paths to path item objects
        flask_routes: List of (flask_pattern, methods, api_path) tuples
    """

    def __init__(self, spec_path: str):
        """Load and index an OpenAPI spec file.

        Args:
            spec_path: Path to the OpenAPI JSON spec file
        """
        with open(spec_path) as f:
            self.spec = json.load(f)

        self.paths: Dict[str, PathItem] = self.spec.get('paths', {})
        self.flask_routes = self._build_flask_routes()

    def _build_flask_routes(self) -> List[Tuple[str, List[str], str]]:
        """Convert OpenAPI paths to Flask route patterns.

        OpenAPI uses {paramName}, Flask uses <paramName>.

        Returns:
            List of (flask_pattern, [http_methods], original_api_path) tuples
        """
        routes = []
        for api_path, path_item in self.paths.items():
            flask_pattern = re.sub(r'\{(\w+)\}', r'<\1>', api_path)

            methods = [
                m.upper()
                for m in ('get', 'post', 'put', 'patch', 'delete')
                if m in path_item
            ]

            if methods:
                routes.append((flask_pattern, methods, api_path))

        return routes

    def get_request_schema(
        self, api_path: str, method: str,
    ) -> Optional[Schema]:
        """Get the request body schema for a path + method.

        Args:
            api_path: Original OpenAPI path (with {params})
            method: HTTP method (lowercase)

        Returns:
            JSON schema dict, or None if no request body
        """
        path_item = self.paths.get(api_path, {})
        operation = path_item.get(method, {})

        return (
            operation
            .get('requestBody', {})
            .get('content', {})
            .get('application/json', {})
            .get('schema')
        )

    def get_response_schema(
        self, api_path: str, method: str, status_code: str = '200',
    ) -> Optional[Schema]:
        """Get the response schema for a path + method + status.

        Args:
            api_path: Original OpenAPI path
            method: HTTP method (lowercase)
            status_code: HTTP status code string

        Returns:
            JSON schema dict, or None if no response schema
        """
        path_item = self.paths.get(api_path, {})
        operation = path_item.get(method, {})

        return (
            operation
            .get('responses', {})
            .get(status_code, {})
            .get('content', {})
            .get('application/json', {})
            .get('schema')
        )

    def get_success_status(self, api_path: str, method: str) -> int:
        """Get the success status code for a path + method.

        Args:
            api_path: Original OpenAPI path
            method: HTTP method (lowercase)

        Returns:
            HTTP status code integer (e.g., 200, 201, 204)
        """
        path_item = self.paths.get(api_path, {})
        operation = path_item.get(method, {})
        responses = operation.get('responses', {})

        for code in ('200', '201', '202', '204'):
            if code in responses:
                return int(code)

        return 200

    def get_path_params(self, api_path: str) -> List[str]:
        """Extract path parameter names from an API path.

        Args:
            api_path: OpenAPI path (e.g., '/networks/{networkId}/appliance/vlans/{vlanId}')

        Returns:
            List of parameter names (e.g., ['networkId', 'vlanId'])
        """
        return re.findall(r'\{(\w+)\}', api_path)

    def infer_primary_key(self, api_path: str) -> Optional[str]:
        """Infer the primary key for a resource from path parameters.

        For item endpoints (path ends with {param}), the primary key is
        the last parameter (e.g., 'vlanId' from '...vlans/{vlanId}').

        For collection endpoints (no trailing param), look for a sibling
        item path in the spec and use its trailing parameter. This avoids
        confusing scope params (networkId) with resource identity.

        Args:
            api_path: OpenAPI path

        Returns:
            Primary key parameter name, or None if no path params
        """
        params = self.get_path_params(api_path)
        if not params:
            return None

        if api_path.endswith('}'):
            return params[-1]

        # Collection endpoint — find sibling item path
        for candidate in self.paths:
            stripped = re.sub(r'/\{[^}]+\}$', '', candidate)
            if stripped == api_path and candidate != api_path:
                sibling_params = self.get_path_params(candidate)
                if sibling_params:
                    return sibling_params[-1]

        return params[-1]

    def infer_resource_type(self, api_path: str) -> str:
        """Infer resource type name from an API path.

        Takes the path segments between the last path parameter's collection
        segment and returns a normalized key.

        Examples:
            /networks/{networkId}/appliance/vlans -> appliance_vlans
            /networks/{networkId}/appliance/vlans/{vlanId} -> appliance_vlans
            /devices/{serial}/switch/ports/{portId} -> switch_ports

        Args:
            api_path: OpenAPI path

        Returns:
            Resource type string
        """
        # Remove trailing parameter
        path = re.sub(r'/\{[^}]+\}$', '', api_path)
        # Take segments after the first path parameter
        segments = path.split('/')
        # Find first segment after a parameter-containing segment
        after_param = []
        found_param = False
        for seg in segments:
            if '{' in seg:
                found_param = True
                after_param = []
                continue
            if found_param and seg:
                after_param.append(seg)

        if after_param:
            return '_'.join(after_param)

        return path.strip('/').replace('/', '_')
