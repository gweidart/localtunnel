from abc import ABC, abstractmethod
from typing import Callable, Dict


# Abstract Base Class for Header Transformation
class HeaderTransformer(ABC):
    """
    Abstract base class for transforming headers.
    """

    @abstractmethod
    def transform(self, headers: Dict[str, str]) -> Dict[str, str]:
        """
        Transform the given headers.

        Args:
            headers (Dict[str, str]): Original headers.

        Returns:
            Dict[str, str]: Transformed headers.
        """
        pass


# Concrete Implementation for Host Header Transformation
class HostHeaderTransformer(HeaderTransformer):
    """
    Transforms the 'Host' header in HTTP requests.
    """

    def __init__(self, host: str):
        self.host = host

    def transform(self, headers: Dict[str, str]) -> Dict[str, str]:
        headers["Host"] = self.host
        return headers


# Concrete Implementation for Authorization Header Transformation
class AuthorizationHeaderTransformer(HeaderTransformer):
    """
    Transforms the 'Authorization' header in HTTP requests.
    """

    def __init__(self, token: str):
        self.token = token

    def transform(self, headers: Dict[str, str]) -> Dict[str, str]:
        headers["Authorization"] = f"Bearer {self.token}"
        return headers


# HeaderTransformerFactory for Creating Transformers
class HeaderTransformerFactory:
    """
    Factory for creating header transformers.
    """

    @staticmethod
    def create_transformer(transformer_type: str, **kwargs) -> HeaderTransformer:
        """
        Create a header transformer based on the type.

        Args:
            transformer_type (str): Type of transformer to create.
            **kwargs: Additional arguments required by the transformer.

        Returns:
            HeaderTransformer: Instance of a header transformer.
        """
        if transformer_type == "host":
            return HostHeaderTransformer(kwargs.get("host"))
        elif transformer_type == "authorization":
            return AuthorizationHeaderTransformer(kwargs.get("token"))
        else:
            raise ValueError(f"Unknown transformer type: {transformer_type}")


# Decorator for Applying Multiple Transformations
def header_transformer_decorator(transformers: Callable):
    """
    Decorator for applying multiple header transformations.

    Args:
        transformers (Callable): List of HeaderTransformer instances.

    Returns:
        Callable: A function wrapper that applies all transformations.
    """

    def decorator(func: Callable):
        def wrapper(headers: Dict[str, str], *args, **kwargs):
            for transformer in transformers:
                headers = transformer.transform(headers)
            return func(headers, *args, **kwargs)

        return wrapper

    return decorator
