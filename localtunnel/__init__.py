"""
LocalTunnel Python Client

This package provides the functionality to expose local servers to the internet
using the LocalTunnel protocol. The library is modular and allows use both
as a CLI tool and a Python library.

Modules:
- client.py: Manages the individual LocalTunnel connections.
- tunnel_manager.py: Handles multiple tunnels and their lifecycle.
- header_transformer.py: Provides utilities for header transformations.
- utils.py: Contains utility functions like retry strategies.
- exceptions.py: Defines custom exceptions for tunnel operations.
"""

__version__ = "{version}"

# Expose key classes and modules for easy imports
from .client import LocalTunnelClient
from ._logging import logger
from .tunnel_manager import TunnelManager
from .header_transformer import (
    HeaderTransformer,
    HostHeaderTransformer,
    AuthorizationHeaderTransformer,
    HeaderTransformerFactory,
)
from .exceptions import (
    TunnelConnectionError,
    TunnelClosedError,
)
