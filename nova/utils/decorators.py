"""Utility Decorators"""

import functools
import time
import asyncio
from typing import Callable, Any, TypeVar, Optional
from nova.logger import get_logger

logger = get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
):
    """Retry decorator with exponential backoff"""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay

            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt >= max_attempts:
                        logger.error(
                            f"Max retries reached for {func.__name__}: {e}"
                        )
                        raise

                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for {func.__name__}, "
                        f"retrying in {current_delay}s: {e}"
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper

    return decorator


def async_retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
):
    """Async retry decorator with exponential backoff"""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay

            while attempt < max_attempts:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt >= max_attempts:
                        logger.error(
                            f"Max retries reached for {func.__name__}: {e}"
                        )
                        raise

                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for {func.__name__}, "
                        f"retrying in {current_delay}s: {e}"
                    )
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff

        return wrapper

    return decorator
