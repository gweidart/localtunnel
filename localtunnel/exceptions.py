from typing import Optional


class LocalTunnelError(Exception):
    """
    Base exception for the Localtunnel library.

    Attributes:
        message (str): A descriptive error message.
    """

    def __init__(self, message: str = "An error occurred in the Localtunnel library"):
        super().__init__(message)
        self.message = message


class TunnelConnectionError(LocalTunnelError):
    """
    Raised when a tunnel fails to connect.

    Attributes:
        host (str): The host URL attempted.
        status_code (Optional[int]): HTTP status code, if applicable.
    """

    def __init__(self, host: str, status_code: Optional[int] = None):
        message = f"Failed to connect to tunnel host '{host}'"
        if status_code:
            message += f" (HTTP status code: {status_code})"
        super().__init__(message)
        self.host = host
        self.status_code = status_code


class TunnelClosedError(LocalTunnelError):
    """
    Raised when operations are attempted on a closed tunnel.

    Attributes:
        tunnel_url (str): The URL of the closed tunnel.
    """

    def __init__(self, tunnel_url: str):
        super().__init__(f"The tunnel at '{tunnel_url}' is closed.")
        self.tunnel_url = tunnel_url


class TunnelConfigurationError(LocalTunnelError):
    """
    Raised when there is an invalid configuration for the tunnel.

    Attributes:
        parameter (str): The name of the invalid parameter.
        value: The invalid value provided.
    """

    def __init__(self, parameter: str, value):
        super().__init__(f"Invalid configuration for '{parameter}': {value}")
        self.parameter = parameter
        self.value = value


class TunnelTimeoutError(LocalTunnelError):
    """
    Raised when a tunnel operation times out.

    Attributes:
        operation (str): The operation that timed out.
        timeout (float): The timeout duration in seconds.
    """

    def __init__(self, operation: str, timeout: float):
        super().__init__(f"'{operation}' operation timed out after {timeout} seconds.")
        self.operation = operation
        self.timeout = timeout
