from abc import ABC, abstractmethod
import asyncio
from typing import Optional

from aiohttp import ClientSession

from localtunnel._logging import logger
from localtunnel.exceptions import TunnelClosedError, TunnelConnectionError
from localtunnel.utils import FixedRetryTemplate


# State Pattern Implementation
class TunnelState(ABC):
    """
    Abstract base class for tunnel states.
    """

    @abstractmethod
    async def open(self, client):
        pass

    @abstractmethod
    async def close(self, client):
        pass

    @abstractmethod
    async def monitor(self, client):
        pass


class ClosedState(TunnelState):
    """
    Behavior for a closed tunnel.
    """

    async def open(self, client):
        await client._open_tunnel()
        client.state = client.open_state

    async def close(self, client):
        logger.warning("Tunnel is already closed.")

    async def monitor(self, client):
        logger.warning("Cannot monitor a closed tunnel.")


class OpenState(TunnelState):
    """
    Behavior for an open tunnel.
    """

    async def open(self, client):
        logger.warning("Tunnel is already open.")

    async def close(self, client):
        await client._close_tunnel()
        client.state = client.closed_state

    async def monitor(self, client):
        await client._monitor_tunnel()


class ErrorState(TunnelState):
    """
    Behavior for a tunnel in an error state.
    """

    async def open(self, client):
        logger.warning("Cannot open tunnel in error state. Attempting recovery...")
        await client._open_tunnel()
        client.state = client.open_state

    async def close(self, client):
        logger.warning("Closing tunnel from error state...")
        await client._close_tunnel()
        client.state = client.closed_state

    async def monitor(self, client):
        logger.warning("Cannot monitor tunnel in error state.")


# LocalTunnelClient with State Pattern
class LocalTunnelClient:
    """
    LocalTunnelClient manages the creation and lifecycle of a local tunnel.

    Attributes:
        port (int): The local port number to expose.
        subdomain (Optional[str]): The optional subdomain for the tunnel.
        host (str): The LocalTunnel server URL (default is "https://localtunnel.me").
        tunnel_url (Optional[str]): The public URL of the tunnel (once open).
        client_id (Optional[str]): The server-assigned ID for the tunnel.
        session (Optional[ClientSession]): The HTTP session for managing requests.
    """

    def __init__(
        self,
        port: int,
        subdomain: Optional[str] = None,
        host: str = "https://localtunnel.me",
        retry_strategy=None,
    ):
        self.port = port
        self.subdomain = subdomain
        self.host = host.rstrip("/")
        self.tunnel_url: Optional[str] = None
        self.client_id: Optional[str] = None
        self.session: Optional[ClientSession] = None
        self.retry_strategy = retry_strategy or FixedRetryTemplate(delay_time=1.0)

        # State Management
        self.closed_state = ClosedState()
        self.open_state = OpenState()
        self.error_state = ErrorState()
        self.state = self.closed_state  # Initial state

    async def open(self):
        await self.state.open(self)

    async def close(self):
        await self.state.close(self)

    async def monitor(self):
        await self.state.monitor(self)

    async def _open_tunnel(self):
        """
        Internal logic to open the tunnel.
        """

        async def attempt_open():
            self.session = ClientSession()
            endpoint = (
                f"{self.host}/{self.subdomain}"
                if self.subdomain
                else f"{self.host}/?new"
            )
            logger.info("Attempting to connect to the LocalTunnel server: {}", endpoint)

            async with self.session.get(endpoint) as response:
                if response.status != 200:
                    raise TunnelConnectionError(endpoint, response.status)

                data = await response.json()
                logger.debug("Server response: {}", data)

                self.tunnel_url = data.get("url")
                self.client_id = data.get("id")

                if not self.tunnel_url or not self.client_id:
                    raise ValueError("Invalid server response: Missing 'url' or 'id'.")

        await self.retry_strategy.retry(attempt_open, retries=3)
        logger.info("Tunnel successfully opened at {}", self.tunnel_url)

    async def _close_tunnel(self):
        """
        Internal logic to close the tunnel.
        """
        if self.session:
            logger.info("Closing the HTTP session...")
            await self.session.close()
        self.tunnel_url = None
        self.client_id = None
        logger.info("Tunnel has been closed.")

    async def _monitor_tunnel(self):
        """
        Internal logic to monitor the tunnel.
        """
        while True:
            try:
                async with self.session.get(self.tunnel_url) as response:
                    if response.status != 200:
                        raise TunnelConnectionError(self.tunnel_url, response.status)
                    logger.debug("Tunnel is active: {}", self.tunnel_url)
                await asyncio.sleep(10)
            except Exception as e:
                logger.error("Error during monitoring: {}", e)
                self.state = self.error_state
                break

    def get_tunnel_url(self) -> str:
        """
        Retrieve the public URL of the tunnel.

        Returns:
            str: The public tunnel URL.

        Raises:
            TunnelClosedError: If the tunnel is not yet open or the URL is unavailable.
        """
        if not self.tunnel_url:
            raise TunnelClosedError("Tunnel is not open. Please call `open()` first.")
        return self.tunnel_url
