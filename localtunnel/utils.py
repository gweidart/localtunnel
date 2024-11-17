from abc import ABC, abstractmethod
import asyncio
from typing import Any, Callable

from localtunnel._logging import logger


class RetryTemplate(ABC):
    """
    Abstract base class for defining a retry workflow using the Template Method Pattern.
    """

    async def retry(self, func: Callable, retries: int, *args, **kwargs) -> Any:
        """
        Executes the retry workflow.

        Args:
            func (Callable): The async function to execute.
            retries (int): Number of retries.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            Any: The result of the async function if successful.

        Raises:
            Exception: The last exception raised if all retries fail.
        """
        for attempt in range(1, retries + 1):
            self.before_attempt(attempt)
            try:
                result = await func(*args, **kwargs)
                self.on_success(attempt, result)
                return result
            except Exception as e:
                self.on_failure(attempt, e)
                if attempt == retries:
                    self.on_final_failure(e)
                    raise e
                await self.delay(attempt)

    @abstractmethod
    def before_attempt(self, attempt: int):
        pass

    @abstractmethod
    async def delay(self, attempt: int):
        pass

    @abstractmethod
    def on_success(self, attempt: int, result: Any):
        pass

    @abstractmethod
    def on_failure(self, attempt: int, exception: Exception):
        pass

    @abstractmethod
    def on_final_failure(self, exception: Exception):
        pass


class FixedRetryTemplate(RetryTemplate):
    """
    Retry workflow with a fixed delay between attempts.
    """

    def __init__(self, delay_time: float = 1.0):
        self.delay_time = delay_time

    def before_attempt(self, attempt: int):
        logger.info(f"Attempt {attempt} started.")

    async def delay(self, attempt: int):
        await asyncio.sleep(self.delay_time)

    def on_success(self, attempt: int, result: Any):
        logger.info(f"Attempt {attempt} succeeded with result: {result}")

    def on_failure(self, attempt: int, exception: Exception):
        logger.info(f"Attempt {attempt} failed with exception: {exception}")

    def on_final_failure(self, exception: Exception):
        logger.info(f"All attempts failed. Last exception: {exception}")


class ExponentialBackoffRetryTemplate(RetryTemplate):
    """
    Retry workflow with exponential backoff between attempts.
    """

    def __init__(self, base_delay: float = 1.0):
        self.base_delay = base_delay

    def before_attempt(self, attempt: int):
        logger.info(f"Attempt {attempt} started with exponential backoff.")

    async def delay(self, attempt: int):
        await asyncio.sleep(self.base_delay * (2 ** (attempt - 1)))

    def on_success(self, attempt: int, result: Any):
        logger.info(f"Attempt {attempt} succeeded with result: {result}")

    def on_failure(self, attempt: int, exception: Exception):
        logger.info(f"Attempt {attempt} failed with exception: {exception}")

    def on_final_failure(self, exception: Exception):
        logger.info(f"All attempts failed. Last exception: {exception}")
