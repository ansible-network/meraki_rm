"""Platform Manager - Persistent service for Meraki Dashboard API communication.

This module provides:
- PlatformService: The server-side service that maintains persistent
  connections to the Meraki Dashboard API and handles all data transformations.
- PlatformManager: The multiprocessing.Manager subclass that shares the
  PlatformService across Ansible task processes via RPC.

Adapted from the NovaCom reference pattern for the Meraki Dashboard API.
Key Meraki-specific changes:
- X-Cisco-Meraki-API-Key authentication header
- Rate limit handling (429 + Retry-After)
- Automatic pagination via Link header
- Base URL: https://api.meraki.com/api/v1
- Single API version (v1)
"""

import requests
import logging
import threading
import time
import re
from multiprocessing.managers import BaseManager
from socketserver import ThreadingMixIn
from typing import Any, Dict, Optional, List
from dataclasses import asdict, fields, is_dataclass

from ..platform.registry import APIVersionRegistry
from ..platform.loader import DynamicClassLoader
from ..platform.types import EndpointOperation

logger = logging.getLogger(__name__)

# Meraki rate limit: 10 req/s per org
_DEFAULT_MAX_RETRIES = 5
_DEFAULT_RETRY_WAIT = 1


class PlatformService:
    """
    Generic platform service for Meraki Dashboard API - resource agnostic.

    Maintains a persistent connection to the Meraki Dashboard API and
    handles all resource operations generically. Works for any module
    (vlan, ssid, organization, etc.).

    Attributes:
        base_url: Meraki Dashboard base URL
        session: Persistent HTTP session with Meraki auth
        api_version: Detected/cached API version (always '1' for Meraki)
        registry: Version registry
        loader: Class loader
        cache: Lookup cache (org names <-> IDs, network names <-> IDs, etc.)
    """

    def __init__(self, base_url: str, api_key: str):
        """
        Initialize platform service with Meraki credentials.

        Args:
            base_url: Meraki Dashboard base URL
                (e.g., 'https://api.meraki.com/api/v1')
            api_key: Meraki API key
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key

        self.session = requests.Session()
        self.session.headers.update({
            'X-Cisco-Meraki-API-Key': api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'cisco.meraki_rm Ansible Collection',
        })

        self.api_version = self._detect_version()
        logger.info(f"PlatformService initialized with API v{self.api_version}")

        self.registry = APIVersionRegistry()
        self.loader = DynamicClassLoader(self.registry)

        self.cache: Dict[str, Any] = {}

    def _detect_version(self) -> str:
        """
        Detect Meraki API version. Currently always v1.

        Returns:
            Version string (always '1' for Meraki Dashboard API)
        """
        return '1'

    def _handle_rate_limit(self, response: requests.Response) -> bool:
        """
        Handle 429 rate limit response from Meraki.

        Args:
            response: HTTP response

        Returns:
            True if rate limited (caller should retry), False otherwise
        """
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', _DEFAULT_RETRY_WAIT))
            logger.warning(f"Rate limited. Retrying after {retry_after}s")
            time.sleep(retry_after)
            return True
        return False

    def _api_call(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Make API call with rate limit retry.

        Args:
            method: HTTP method
            url: Full URL
            **kwargs: Passed to requests.Session.request

        Returns:
            HTTP response

        Raises:
            RuntimeError: If rate limit exceeded after max retries
        """
        for attempt in range(_DEFAULT_MAX_RETRIES):
            response = self.session.request(method, url, **kwargs)
            if not self._handle_rate_limit(response):
                return response
        raise RuntimeError(
            f"Rate limit exceeded after {_DEFAULT_MAX_RETRIES} retries for {method} {url}"
        )

    def _paginated_get(self, url: str, **kwargs) -> List[dict]:
        """
        GET with automatic pagination via Link header.

        Meraki list endpoints return paginated results with Link headers
        containing rel=next for the next page URL.

        Args:
            url: Initial GET URL
            **kwargs: Passed to requests.Session.request

        Returns:
            Combined list of all pages
        """
        results = []
        current_url: Optional[str] = url

        while current_url:
            response = self._api_call('GET', current_url, **kwargs)
            response.raise_for_status()

            data = response.json()
            if isinstance(data, list):
                results.extend(data)
            else:
                results.append(data)

            current_url = self._parse_next_link(
                response.headers.get('Link')
            )

        return results

    @staticmethod
    def _parse_next_link(link_header: Optional[str]) -> Optional[str]:
        """
        Parse Link header for next page URL.

        Meraki format: <url>; rel=next

        Args:
            link_header: Link header value

        Returns:
            Next page URL, or None if no more pages
        """
        if not link_header:
            return None

        match = re.search(r'<([^>]+)>;\s*rel=next', link_header)
        return match.group(1) if match else None

    def execute(
        self,
        operation: str,
        module_name: str,
        user_data_dict: dict
    ) -> dict:
        """
        Execute a generic operation on any resource.

        This is the main entry point called by action plugins via RPC.

        Args:
            operation: Operation type ('create', 'update', 'replace', 'delete', 'find')
            module_name: Module name (e.g., 'vlan', 'ssid')
            user_data_dict: User Model dataclass as dict

        Returns:
            Result as dict (User Model format)

        Raises:
            ValueError: If operation is unknown or execution fails
        """
        thread_id = threading.get_ident()
        logger.info(
            f"Executing {operation} on {module_name} [Thread: {thread_id}]"
        )

        if module_name == 'facts' and operation == 'find':
            result = self._gather_facts(user_data_dict)
            logger.info(
                f"Operation {operation} on {module_name} completed "
                f"[Thread: {thread_id}]"
            )
            return result

        UserClass, APIClass, MixinClass = self.loader.load_classes_for_module(
            module_name,
            self.api_version
        )

        user_instance = UserClass(**user_data_dict)

        context = {
            'manager': self,
            'session': self.session,
            'cache': self.cache,
            'api_version': self.api_version,
            'base_url': self.base_url
        }

        try:
            if operation == 'create':
                result = self._create_resource(
                    user_instance, MixinClass, APIClass, context
                )
            elif operation in ('update', 'replace'):
                result = self._update_resource(
                    user_instance, MixinClass, APIClass, context
                )
            elif operation == 'delete':
                result = self._delete_resource(
                    user_instance, MixinClass, context
                )
            elif operation == 'find':
                result = self._find_resource(
                    user_instance, MixinClass, APIClass, context
                )
            else:
                raise ValueError(f"Unknown operation: {operation}")

            logger.info(
                f"Operation {operation} on {module_name} completed "
                f"[Thread: {thread_id}]"
            )

            return result

        except Exception as e:
            logger.error(
                f"Operation {operation} on {module_name} failed: {e}",
                exc_info=True
            )
            raise

    def _gather_facts(self, user_data_dict: dict) -> dict:
        """
        Gather facts about organizations, networks, devices, and inventory.

        Called when module_name == 'facts' and operation == 'find'.
        Makes direct API calls based on gather_subset.

        Args:
            user_data_dict: Dict with gather_subset, organization_id, network_id

        Returns:
            Dict with organizations, networks, devices, inventory lists
        """
        gather_subset = set(user_data_dict.get('gather_subset', ['all']))
        org_id = user_data_dict.get('organization_id')
        network_id = user_data_dict.get('network_id')

        result = {}

        if 'all' in gather_subset or 'organizations' in gather_subset:
            orgs = self._paginated_get(f'{self.base_url}/organizations')
            result['organizations'] = orgs

        if org_id:
            if 'all' in gather_subset or 'networks' in gather_subset:
                nets = self._paginated_get(
                    f'{self.base_url}/organizations/{org_id}/networks'
                )
                if network_id:
                    nets = [n for n in nets if n.get('id') == network_id]
                result['networks'] = nets

            if 'all' in gather_subset or 'devices' in gather_subset:
                devs = self._paginated_get(
                    f'{self.base_url}/organizations/{org_id}/devices'
                )
                if network_id:
                    devs = [d for d in devs if d.get('networkId') == network_id]
                result['devices'] = devs

            if 'all' in gather_subset or 'inventory' in gather_subset:
                inv = self._paginated_get(
                    f'{self.base_url}/organizations/{org_id}/inventory/devices'
                )
                result['inventory'] = inv

        return result

    @staticmethod
    def _safe_construct(cls: type, data: dict) -> Any:
        """Construct a dataclass filtering out unknown keys."""
        if is_dataclass(cls):
            valid = {f.name for f in fields(cls)}
            data = {k: v for k, v in data.items() if k in valid}
        return cls(**data)

    def _create_resource(
        self,
        user_data: Any,
        mixin_class: type,
        api_class: type,
        context: dict
    ) -> dict:
        """Create resource with transformation."""
        api_data = user_data.to_api(context)
        operations = self._get_endpoint_operations(mixin_class, 'create')
        api_result = self._execute_operations(
            operations, api_data, context, user_data
        )

        if api_result:
            api_result_instance = self._safe_construct(api_class, api_result)
            user_result = api_result_instance.to_ansible(context)
            return asdict(user_result)

        return {}

    def _update_resource(
        self,
        user_data: Any,
        mixin_class: type,
        api_class: type,
        context: dict
    ) -> dict:
        """Update resource with transformation."""
        api_data = user_data.to_api(context)
        operations = self._get_endpoint_operations(mixin_class, 'update')
        api_result = self._execute_operations(
            operations, api_data, context, user_data
        )

        if api_result:
            api_result_instance = self._safe_construct(api_class, api_result)
            user_result = api_result_instance.to_ansible(context)
            return asdict(user_result)

        return {}

    def _delete_resource(
        self,
        user_data: Any,
        mixin_class: type,
        context: dict
    ) -> dict:
        """Delete resource."""
        api_data = user_data.to_api(context)
        operations = self._get_endpoint_operations(mixin_class, 'delete')
        self._execute_operations(
            operations, api_data, context, user_data
        )
        return {}

    def _find_resource(
        self,
        user_data: Any,
        mixin_class: type,
        api_class: type,
        context: dict
    ) -> dict:
        """Find/get resource with transformation."""
        api_data = user_data.to_api(context)
        api_data_dict = asdict(api_data) if is_dataclass(api_data) else api_data
        user_data_dict = asdict(user_data) if is_dataclass(user_data) else user_data

        operations = self._get_endpoint_operations(mixin_class, 'find')
        sorted_ops = self._sort_operations(operations)

        results = {}
        for op_name in sorted_ops:
            endpoint_op = operations[op_name]
            path = endpoint_op.path
            skip_op = False
            if endpoint_op.path_params:
                for param in endpoint_op.path_params:
                    val = self._resolve_path_param(
                        param, endpoint_op, api_data_dict,
                        user_data_dict, results
                    )
                    if val is not None:
                        path = path.replace(f'{{{param}}}', str(val))
                    else:
                        skip_op = True
                        break

            if skip_op or '{' in path:
                logger.debug(f"Skipping {op_name} - missing path params")
                continue

            url = f"{self.base_url}{path}"
            logger.debug(f"Calling {endpoint_op.method} {url}")

            if endpoint_op.method == 'GET' and not endpoint_op.path_params:
                result_data = self._paginated_get(url)
            else:
                response = self._api_call(endpoint_op.method, url)
                if response.status_code == 404:
                    logger.debug(f"Resource not found (404) for {op_name}")
                    continue
                response.raise_for_status()
                result_data = response.json()

            results[op_name] = result_data

        main_result = results.get('find')
        if main_result is None:
            main_result = results.get('main')
        if main_result is None and results:
            main_result = list(results.values())[0]

        if isinstance(main_result, list):
            user_results = []
            for item in main_result:
                api_inst = self._safe_construct(api_class, item)
                user_inst = api_inst.to_ansible(context)
                user_results.append(asdict(user_inst))
            return {'config': user_results}
        elif main_result:
            api_result_instance = self._safe_construct(api_class, main_result)
            user_result = api_result_instance.to_ansible(context)
            return asdict(user_result)

        return {'config': []}

    def _resolve_path_param(
        self,
        param: str,
        endpoint_op: EndpointOperation,
        api_data_dict: dict,
        user_data_dict: dict,
        results: dict
    ) -> Optional[Any]:
        """Resolve a path parameter value, including aliases for snake_case."""
        if param in results:
            r = results[param]
            return r.get('id', r) if isinstance(r, dict) else r
        val = api_data_dict.get(param) or user_data_dict.get(param)
        if val is not None:
            return val
        aliases = (endpoint_op.path_param_aliases or {}).get(param, [])
        for alt in aliases:
            val = api_data_dict.get(alt) or user_data_dict.get(alt)
            if val is not None:
                return val
        return None

    def _get_endpoint_operations(
        self,
        mixin_class: type,
        required_for: str
    ) -> Dict[str, EndpointOperation]:
        """Get endpoint operations from mixin, filtered by operation type."""
        if hasattr(mixin_class, 'get_endpoint_operations'):
            all_ops = mixin_class.get_endpoint_operations()
        else:
            return {}

        return {
            name: op for name, op in all_ops.items()
            if op.required_for is None or op.required_for == required_for
        }

    def _execute_operations(
        self,
        operations: Dict[str, EndpointOperation],
        api_data: Any,
        context: dict,
        user_data: Any
    ) -> dict:
        """Execute potentially multiple API endpoint operations."""
        if not operations:
            return {}

        sorted_ops = self._sort_operations(operations)
        api_data_dict = asdict(api_data) if is_dataclass(api_data) else api_data
        user_data_dict = asdict(user_data) if is_dataclass(user_data) else user_data

        results = {}
        for op_name in sorted_ops:
            endpoint_op = operations[op_name]

            request_data = {}
            for field_name in endpoint_op.fields:
                if field_name in api_data_dict and api_data_dict[field_name] is not None:
                    request_data[field_name] = api_data_dict[field_name]
                elif field_name in user_data_dict and user_data_dict[field_name] is not None:
                    request_data[field_name] = user_data_dict[field_name]

            path = endpoint_op.path
            skip_op = False
            if endpoint_op.path_params:
                for param in endpoint_op.path_params:
                    val = self._resolve_path_param(
                        param, endpoint_op, api_data_dict,
                        user_data_dict, results
                    )
                    if val is not None:
                        path = path.replace(f'{{{param}}}', str(val))
                    else:
                        skip_op = True
                        break

            if skip_op or '{' in path:
                logger.debug(f"Skipping {op_name} - missing path params")
                continue

            url = f"{self.base_url}{path}"

            if endpoint_op.method == 'DELETE':
                response = self._api_call(endpoint_op.method, url)
            else:
                response = self._api_call(
                    endpoint_op.method,
                    url,
                    json=request_data if request_data else None
                )

            response.raise_for_status()

            try:
                result_data = response.json()
            except ValueError:
                result_data = {}

            results[op_name] = result_data
            if isinstance(result_data, dict) and 'id' in result_data:
                results['id'] = result_data['id']

        return (
            results.get('create')
            or results.get('update')
            or results.get('main')
            or {}
        )

    def _sort_operations(
        self,
        operations: Dict[str, EndpointOperation]
    ) -> List[str]:
        """Sort operations by dependencies and order."""
        sorted_ops: List[str] = []
        remaining = dict(operations)

        while remaining:
            ready = [
                name for name, op in remaining.items()
                if op.depends_on is None or op.depends_on in sorted_ops
            ]

            if not ready:
                raise ValueError(
                    f"Circular dependency in operations: "
                    f"{list(remaining.keys())}"
                )

            ready.sort(key=lambda name: remaining[name].order)
            sorted_ops.append(ready[0])
            remaining.pop(ready[0])

        return sorted_ops

    def lookup_org_ids(self, org_names: list) -> list:
        """
        Convert organization names to IDs.

        Args:
            org_names: List of organization names

        Returns:
            List of organization IDs
        """
        ids = []
        for name in org_names:
            cache_key = f'org_name:{name}'
            if cache_key in self.cache:
                ids.append(self.cache[cache_key])
                continue

            response = self._api_call(
                'GET',
                f'{self.base_url}/organizations',
            )
            response.raise_for_status()
            orgs = response.json()

            found = False
            for org in orgs:
                if org.get('name') == name:
                    org_id = org['id']
                    self.cache[cache_key] = org_id
                    self.cache[f'org_id:{org_id}'] = name
                    ids.append(org_id)
                    found = True
                    break

            if not found:
                raise ValueError(f"Organization '{name}' not found")

        return ids

    def lookup_network_ids(self, org_id: str, network_names: list) -> list:
        """
        Convert network names to IDs within an organization.

        Args:
            org_id: Organization ID
            network_names: List of network names

        Returns:
            List of network IDs
        """
        ids = []
        for name in network_names:
            cache_key = f'net_name:{org_id}:{name}'
            if cache_key in self.cache:
                ids.append(self.cache[cache_key])
                continue

            networks = self._paginated_get(
                f'{self.base_url}/organizations/{org_id}/networks'
            )

            for net in networks:
                net_name = net.get('name', '')
                net_id = net['id']
                self.cache[f'net_name:{org_id}:{net_name}'] = net_id
                self.cache[f'net_id:{net_id}'] = net_name

            if cache_key in self.cache:
                ids.append(self.cache[cache_key])
            else:
                raise ValueError(
                    f"Network '{name}' not found in organization {org_id}"
                )

        return ids


class PlatformManager(ThreadingMixIn, BaseManager):
    """Custom Manager for sharing PlatformService across processes.

    Uses ThreadingMixIn to handle concurrent client connections.
    Enables multiple Ansible tasks to communicate with the same
    PlatformService instance via RPC.

    Lifecycle (handled inside the server child process):

      1. ``os.setsid()`` detaches from the parent's process group.
      2. A watchdog daemon thread decides when to shut down:

         - **No ``.survive`` flag at startup (production)** — watch
           ``os.getppid()``.  When the parent ``ansible-playbook``
           exits, the watchdog sends ``SIGTERM`` to itself.
         - **``.survive`` flag present at startup (Molecule)** — watch
           the flag file.  When ``destroy.yml`` removes it, the
           watchdog sends ``SIGTERM`` to itself.

      The watchdog always runs; the only difference is what it watches.
    """

    daemon_threads = True

    @staticmethod
    def _run_server(*args, **kwargs):
        """Detach into own session, arm watchdog, then serve."""
        import os
        import signal

        os.setsid()

        address = args[1] if len(args) > 1 else kwargs.get('address')
        survive_file = None
        if address and isinstance(address, str):
            from pathlib import Path
            sf = Path(address).with_suffix('.survive')
            if sf.exists():
                survive_file = sf

        parent_pid = os.getppid()

        def _watchdog():
            while True:
                time.sleep(2)
                if survive_file is not None:
                    if not survive_file.exists():
                        logger.info(
                            ".survive removed — shutting down manager"
                        )
                        os.kill(os.getpid(), signal.SIGTERM)
                        break
                else:
                    if os.getppid() != parent_pid:
                        logger.info(
                            "Parent PID %d gone — shutting down manager",
                            parent_pid,
                        )
                        os.kill(os.getpid(), signal.SIGTERM)
                        break

        t = threading.Thread(target=_watchdog, daemon=True)
        t.start()

        BaseManager._run_server(*args, **kwargs)
