"""Stateful Flask mock server for Meraki Dashboard API.

Auto-generates routes from the OpenAPI spec, validates requests against
the spec, maintains in-memory CRUD state, and generates spec-compliant
responses.

Usage:
    # Start server
    python -m tools.mock_server.server --spec spec3.json --port 29443

    # Start as daemon (for Molecule)
    python -m tools.mock_server.server --spec spec3.json --port 29443 --daemon

    # Specify host
    python -m tools.mock_server.server --spec spec3.json --host 0.0.0.0 --port 29443
"""

import argparse
import json
import logging
import os
import re
import sys
from typing import Any, Dict, Optional, Tuple

from flask import Flask, Response, jsonify, request

from .spec_loader import SpecLoader
from .state_store import StateStore
from .response_generator import (
    generate_default_from_schema,
    merge_with_schema_defaults,
    unwrap_array_schema,
)

try:
    from openapi_core import OpenAPI
    from openapi_core.contrib.flask import FlaskOpenAPIRequest
    from openapi_core.contrib.flask.responses import FlaskOpenAPIResponse
    HAS_OPENAPI_CORE = True
except ImportError:
    HAS_OPENAPI_CORE = False

logger = logging.getLogger(__name__)


def create_app(spec_path: str) -> Flask:
    """Create and configure the Flask mock server application.

    Args:
        spec_path: Path to the OpenAPI spec file

    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    app.config['SPEC_PATH'] = spec_path

    loader = SpecLoader(spec_path)
    store = StateStore()

    app.config['SPEC_LOADER'] = loader
    app.config['STATE_STORE'] = store

    # openapi-core spec validation (Layer 1)
    openapi = None
    if HAS_OPENAPI_CORE:
        openapi = OpenAPI.from_file_path(spec_path)
        app.config['OPENAPI'] = openapi
        logger.info("openapi-core loaded — request/response validation enabled")
    else:
        logger.warning(
            "openapi-core not installed — spec validation disabled. "
            "Install with: pip install openapi-core>=0.19"
        )

    _INTERNAL_PREFIXES = ('/health', '/_state/')

    @app.before_request
    def validate_request():
        """Validate incoming request against OpenAPI spec."""
        if openapi is None:
            return None
        if any(request.path.startswith(p) for p in _INTERNAL_PREFIXES):
            return None
        try:
            openapi_request = FlaskOpenAPIRequest(request)
            openapi.unmarshal_request(openapi_request)
        except Exception as exc:
            logger.warning("Request validation failed: %s", exc)
            return jsonify({
                'errors': [str(exc)],
                '_validation': 'request',
            }), 400

    @app.after_request
    def validate_response(response):
        """Validate outgoing response against OpenAPI spec."""
        if openapi is None:
            return response
        if any(request.path.startswith(p) for p in _INTERNAL_PREFIXES):
            return response
        if response.status_code >= 400:
            return response
        try:
            openapi_request = FlaskOpenAPIRequest(request)
            openapi_response = FlaskOpenAPIResponse(response)
            openapi.unmarshal_response(openapi_request, openapi_response)
        except Exception as exc:
            logger.warning("Response validation failed: %s %s — %s",
                           request.method, request.path, exc)
        return response

    # Register health check
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({
            'status': 'ok',
            'spec_paths': len(loader.paths),
            'spec_validation': HAS_OPENAPI_CORE,
        })

    # Register state management endpoints
    @app.route('/_state/reset', methods=['POST'])
    def reset_state():
        """Reset all mock server state."""
        store.clear()
        return jsonify({'status': 'reset'})

    @app.route('/_state/dump', methods=['GET'])
    def dump_state():
        """Dump current state for debugging."""
        return jsonify(store.dump())

    # Auto-register routes from the spec
    _register_spec_routes(app, loader, store)

    logger.info(
        f"Mock server created with {len(loader.flask_routes)} routes "
        f"from {spec_path}"
    )

    return app


def _register_spec_routes(
    app: Flask,
    loader: SpecLoader,
    store: StateStore,
) -> None:
    """Register Flask routes for every path in the OpenAPI spec.

    Each route is a generic handler that:
    1. Extracts path parameters
    2. Determines resource type and primary key
    3. Routes to appropriate CRUD operation on the state store
    4. Returns spec-compliant responses

    Args:
        app: Flask application
        loader: Loaded OpenAPI spec
        store: State store instance
    """
    for flask_pattern, methods, api_path in loader.flask_routes:
        resource_type = loader.infer_resource_type(api_path)
        primary_key = loader.infer_primary_key(api_path)
        path_params = loader.get_path_params(api_path)

        # Determine if this is a collection endpoint or item endpoint
        # Item endpoints have a trailing path parameter
        is_item_endpoint = api_path.endswith('}')

        _register_route(
            app=app,
            flask_pattern=flask_pattern,
            methods=methods,
            api_path=api_path,
            resource_type=resource_type,
            primary_key=primary_key,
            path_params=path_params,
            is_item_endpoint=is_item_endpoint,
            loader=loader,
            store=store,
        )


def _register_route(
    app: Flask,
    flask_pattern: str,
    methods: list,
    api_path: str,
    resource_type: str,
    primary_key: Optional[str],
    path_params: list,
    is_item_endpoint: bool,
    loader: SpecLoader,
    store: StateStore,
) -> None:
    """Register a single route with its handler.

    Creates a closure-based view function that captures the route metadata.

    Args:
        app: Flask application
        flask_pattern: Flask URL pattern
        methods: List of HTTP methods
        api_path: Original OpenAPI path
        resource_type: Inferred resource type
        primary_key: Inferred primary key parameter
        path_params: List of path parameter names
        is_item_endpoint: Whether this is a single-item endpoint
        loader: Spec loader
        store: State store
    """
    # Create a unique endpoint name for Flask
    endpoint_name = (
        api_path
        .replace('/', '_')
        .replace('{', '')
        .replace('}', '')
        .strip('_')
    )

    def route_handler(**kwargs):
        method = request.method.lower()

        if method == 'get':
            return _handle_get(
                loader, store, api_path, resource_type,
                primary_key, path_params, is_item_endpoint, kwargs,
            )
        elif method == 'post':
            return _handle_post(
                loader, store, api_path, resource_type,
                primary_key, path_params, kwargs,
            )
        elif method in ('put', 'patch'):
            return _handle_put(
                loader, store, api_path, resource_type,
                primary_key, path_params, is_item_endpoint, kwargs,
            )
        elif method == 'delete':
            return _handle_delete(
                loader, store, api_path, resource_type,
                primary_key, path_params, kwargs,
            )

        return jsonify({'errors': [f'Method {method} not supported']}), 405

    app.add_url_rule(
        flask_pattern,
        endpoint=endpoint_name,
        view_func=route_handler,
        methods=methods,
    )


def _handle_get(
    loader: SpecLoader,
    store: StateStore,
    api_path: str,
    resource_type: str,
    primary_key: Optional[str],
    path_params: list,
    is_item_endpoint: bool,
    kwargs: dict,
) -> Tuple[Response, int]:
    """Handle GET requests — list or retrieve resources."""
    status = loader.get_success_status(api_path, 'get')
    resp_schema = loader.get_response_schema(api_path, 'get', str(status))

    if is_item_endpoint and primary_key and primary_key in kwargs:
        # Single item GET
        key_value = kwargs[primary_key]
        item = store.get(resource_type, key_value)

        if item is None:
            return jsonify({'errors': ['Resource not found']}), 404

        if resp_schema and resp_schema.get('type') == 'object':
            item = merge_with_schema_defaults(item, resp_schema)

        return jsonify(item), status

    else:
        # List GET — return all items matching scope filters
        filters = {}
        for param in path_params:
            if param in kwargs and param != primary_key:
                filters[param] = kwargs[param]

        items = store.list(resource_type, filters if filters else None)

        # If the response schema wraps items in an array, return as list
        if resp_schema:
            item_schema = unwrap_array_schema(resp_schema)
            if item_schema:
                items = [
                    merge_with_schema_defaults(item, item_schema)
                    for item in items
                ]

        return jsonify(items), status


def _handle_post(
    loader: SpecLoader,
    store: StateStore,
    api_path: str,
    resource_type: str,
    primary_key: Optional[str],
    path_params: list,
    kwargs: dict,
) -> Tuple[Response, int]:
    """Handle POST requests — create resources."""
    status = loader.get_success_status(api_path, 'post')
    resp_schema = loader.get_response_schema(api_path, 'post', str(status))

    data = request.get_json(silent=True) or {}

    for param in path_params:
        if param in kwargs:
            data[param] = kwargs[param]

    # When primary_key isn't in the body (e.g. vlanId vs body "id"),
    # copy the body "id" field into the primary_key slot so the store
    # indexes by the correct key.
    if primary_key and primary_key not in data and 'id' in data:
        data[primary_key] = data['id']

    created = store.create(resource_type, primary_key, data)

    if resp_schema:
        item_schema = unwrap_array_schema(resp_schema) or resp_schema
        if item_schema.get('type') == 'object':
            created = merge_with_schema_defaults(created, item_schema)

    return jsonify(created), status


def _handle_put(
    loader: SpecLoader,
    store: StateStore,
    api_path: str,
    resource_type: str,
    primary_key: Optional[str],
    path_params: list,
    is_item_endpoint: bool,
    kwargs: dict,
) -> Tuple[Response, int]:
    """Handle PUT/PATCH requests — update resources."""
    status = loader.get_success_status(api_path, 'put')
    resp_schema = loader.get_response_schema(api_path, 'put', str(status))

    data = request.get_json(silent=True) or {}

    key_value = None
    if is_item_endpoint and primary_key and primary_key in kwargs:
        key_value = kwargs[primary_key]
    elif 'id' in data:
        key_value = str(data['id'])

    if key_value:
        updated = store.update(resource_type, key_value, data)

        if updated is None:
            # Auto-create on PUT if not found (upsert semantics)
            for param in path_params:
                if param in kwargs:
                    data[param] = kwargs[param]
            # Ensure 'id' is set from the primary key value — real APIs
            # always include the resource identity in the response.
            if 'id' not in data and key_value is not None:
                data['id'] = key_value
            updated = store.create(resource_type, primary_key, data)

        # Ensure 'id' is present in the response even for updates where
        # the PUT body omitted it — real APIs return the full resource.
        if updated and 'id' not in updated and key_value is not None:
            updated['id'] = key_value

        if resp_schema:
            item_schema = unwrap_array_schema(resp_schema) or resp_schema
            if item_schema.get('type') == 'object':
                updated = merge_with_schema_defaults(updated, item_schema)

        return jsonify(updated), status
    else:
        # Singleton resource (no primary key — e.g., settings endpoints)
        singleton_key = '_'.join(
            str(kwargs.get(p, '')) for p in path_params
        ) or '_singleton'
        updated = store.update(resource_type, singleton_key, data)
        if updated is None:
            for param in path_params:
                if param in kwargs:
                    data[param] = kwargs[param]
            updated = store.create(resource_type, None, data)
            updated = store.update(resource_type, list(store._store.get(resource_type, {}).keys())[-1], data) or updated

        if resp_schema:
            item_schema = unwrap_array_schema(resp_schema) or resp_schema
            if item_schema.get('type') == 'object':
                updated = merge_with_schema_defaults(updated, item_schema)

        return jsonify(updated), status


def _handle_delete(
    loader: SpecLoader,
    store: StateStore,
    api_path: str,
    resource_type: str,
    primary_key: Optional[str],
    path_params: list,
    kwargs: dict,
) -> Tuple[Response, int]:
    """Handle DELETE requests — remove resources."""
    key_value = None
    if primary_key and primary_key in kwargs:
        key_value = kwargs[primary_key]

    if key_value:
        deleted = store.delete(resource_type, key_value)
        if not deleted:
            return jsonify({'errors': ['Resource not found']}), 404
    else:
        # Delete by scope filter
        singleton_key = '_'.join(
            str(kwargs.get(p, '')) for p in path_params
        ) or '_singleton'
        store.delete(resource_type, singleton_key)

    return Response(status=204)


def main() -> None:
    """CLI entry point for running the mock server."""
    parser = argparse.ArgumentParser(
        description='Meraki Dashboard API mock server'
    )
    parser.add_argument(
        '--spec', required=True,
        help='Path to OpenAPI spec file (spec3.json)',
    )
    parser.add_argument(
        '--host', default='127.0.0.1',
        help='Host to bind to (default: 127.0.0.1)',
    )
    parser.add_argument(
        '--port', type=int, default=29443,
        help='Port to listen on (default: 29443)',
    )
    parser.add_argument(
        '--daemon', action='store_true',
        help='Run as daemon (fork to background, print PID)',
    )
    parser.add_argument(
        '--debug', action='store_true',
        help='Enable Flask debug mode',
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    )

    if args.daemon:
        pid = os.fork()
        if pid > 0:
            # Parent — print child PID and exit
            print(pid)
            sys.exit(0)
        # Child — detach from controlling terminal
        os.setsid()
        # Close inherited file descriptors so the parent (Ansible command
        # module) doesn't block waiting for pipe EOF.
        log_path = os.environ.get(
            'MOCK_SERVER_LOG', os.devnull,
        )
        devnull = os.open(os.devnull, os.O_RDWR)
        os.dup2(devnull, 0)
        os.close(devnull)
        log_fd = os.open(
            log_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644,
        )
        os.dup2(log_fd, 1)
        os.dup2(log_fd, 2)
        if log_fd > 2:
            os.close(log_fd)

    app = create_app(args.spec)
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
