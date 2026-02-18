"""RPC Client for communicating with Platform Manager.

Provides the client-side interface for action plugins to communicate
with the persistent Platform Manager service.

Adapted for cisco.meraki_rm collection.
"""

from multiprocessing.managers import BaseManager
from typing import Any
from dataclasses import asdict, is_dataclass
import logging

logger = logging.getLogger(__name__)


class ManagerRPCClient:
    """
    Client for communicating with Platform Manager.

    Handles connection to the manager service and provides a simple
    interface for action plugins to execute operations.

    Attributes:
        base_url: Meraki Dashboard base URL
        socket_path: Path to Unix socket (or address tuple)
        authkey: Authentication key
        manager: Manager instance
        service_proxy: Proxy to PlatformService
    """

    def __init__(self, base_url: str, socket_path: str, authkey: bytes):
        """
        Initialize RPC client.

        Args:
            base_url: Meraki Dashboard base URL
            socket_path: Path to Unix socket or address
            authkey: Authentication key for manager connection
        """
        self.base_url = base_url
        self.socket_path = socket_path
        self.authkey = authkey

        from .platform_manager import PlatformManager

        PlatformManager.register('get_platform_service')

        logger.debug(f"Connecting to manager at {socket_path}")
        self.manager = PlatformManager(
            address=socket_path,
            authkey=authkey
        )
        self.manager.connect()

        self.service_proxy = self.manager.get_platform_service()
        logger.info("Connected to Platform Manager")

    def execute(
        self,
        operation: str,
        module_name: str,
        user_data: Any
    ) -> Any:
        """
        Execute operation via manager.

        Args:
            operation: Operation type ('create', 'update', 'delete', 'find')
            module_name: Module name (e.g., 'vlan', 'ssid')
            user_data: User Model dataclass instance or dict

        Returns:
            Result as dict (User Model format)
        """
        if is_dataclass(user_data):
            data_dict = asdict(user_data)
        else:
            data_dict = user_data

        result_dict = self.service_proxy.execute(
            operation,
            module_name,
            data_dict
        )

        return result_dict
