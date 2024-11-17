import asyncio
from typing import Callable, Dict, List

from localtunnel._logging import logger
from localtunnel.client import LocalTunnelClient
from localtunnel.utils import ExponentialBackoffRetryTemplate


# Singleton Metaclass
class Singleton(type):
    """
    A metaclass to enforce Singleton behavior.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# Observer Pattern for Event Handling
class EventNotifier:
    """
    Handles event subscriptions and notifications.
    """

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, callback: Callable):
        """
        Subscribe to a specific event.

        Args:
            event_name (str): Name of the event (e.g., "on_open", "on_error").
            callback (Callable): Callback function to execute when the event occurs.
        """
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(callback)
        logger.debug("Subscribed to event: {}", event_name)

    def notify(self, event_name: str, *args, **kwargs):
        """
        Notify all subscribers of an event.

        Args:
            event_name (str): Name of the event.
            *args: Positional arguments to pass to the callbacks.
            **kwargs: Keyword arguments to pass to the callbacks.
        """
        if event_name in self._subscribers:
            for callback in self._subscribers[event_name]:
                callback(*args, **kwargs)
        else:
            logger.warning("No subscribers for event: {}", event_name)


# TunnelManager with Singleton, Observer, and Strategy Integration
class TunnelManager(metaclass=Singleton):
    """
    Manages multiple LocalTunnelClient instances and handles lifecycle events.
    """

    def __init__(self, retry_strategy=None):
        self.tunnels: List[LocalTunnelClient] = []
        self.notifier = EventNotifier()
        self.retry_strategy = retry_strategy or ExponentialBackoffRetryTemplate(
            base_delay=2.0
        )

    def add_tunnel(
        self, port: int, subdomain: str, host: str = "https://localtunnel.me"
    ):
        """
        Add a new tunnel to the manager.

        Args:
            port (int): Local port to expose.
            subdomain (str): Optional subdomain for the tunnel.
            host (str): LocalTunnel server URL.
        """
        client = LocalTunnelClient(
            port, subdomain, host, retry_strategy=self.retry_strategy
        )
        self.tunnels.append(client)
        logger.info("Tunnel added for port {} with subdomain {}", port, subdomain)

    async def open_all(self):
        """
        Open all tunnels managed by the TunnelManager.
        """
        for tunnel in self.tunnels:
            try:
                await tunnel.open()
                self.notifier.notify("on_open", tunnel)
            except Exception as e:
                logger.error("Failed to open tunnel: {}", e)
                self.notifier.notify("on_error", tunnel, e)

    async def close_all(self):
        """
        Close all tunnels managed by the TunnelManager.
        """
        for tunnel in self.tunnels:
            try:
                await tunnel.close()
                self.notifier.notify("on_close", tunnel)
            except Exception as e:
                logger.error("Failed to close tunnel: {}", e)

    async def monitor_all(self):
        """
        Monitor all tunnels and handle reconnections if necessary.
        """

        async def monitor_tunnel(tunnel):
            try:
                await tunnel.monitor()
            except Exception as e:
                logger.error("Error during monitoring: {}", e)
                self.notifier.notify("on_error", tunnel, e)

        tasks = [monitor_tunnel(tunnel) for tunnel in self.tunnels]
        await asyncio.gather(*tasks)

    def subscribe(self, event_name: str, callback: Callable):
        """
        Subscribe to tunnel events.

        Args:
            event_name (str): Name of the event (e.g., "on_open", "on_close", "on_error").
            callback (Callable): Callback function to execute when the event occurs.
        """
        self.notifier.subscribe(event_name, callback)
