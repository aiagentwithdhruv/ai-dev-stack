"""
Retry with exponential backoff for tool execution.
Wraps any function to handle transient failures (rate limits, timeouts, network errors).
Logic bugs and budget limits are deliberately NOT retried.
"""

import time
import functools
from shared.logger import get_logger

logger = get_logger(__name__)


# Only retry on transient/network errors — not on logic bugs or budget limits
TRANSIENT_EXCEPTIONS = (
    ConnectionError,
    TimeoutError,
    OSError,  # covers network-level socket errors
)

# Exceptions that should NEVER be retried
NON_RETRYABLE = (
    ValueError,
    TypeError,
    KeyError,
    FileNotFoundError,
    PermissionError,
    NotImplementedError,
)


def retry(
    max_attempts: int = 3,
    base_delay: float = 2.0,
    max_delay: float = 30.0,
    backoff: str = "exponential",
    retryable_exceptions: tuple = TRANSIENT_EXCEPTIONS,
):
    """Decorator that retries a function on transient failures only.

    Args:
        max_attempts: Maximum number of attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay cap in seconds
        backoff: "exponential" | "linear" | "fixed"
        retryable_exceptions: Tuple of exception types to retry on
            (defaults to network/timeout errors only)
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e

                    if attempt == max_attempts:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}: {e}"
                        )
                        raise

                    # Calculate delay
                    if backoff == "exponential":
                        delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                    elif backoff == "linear":
                        delay = min(base_delay * attempt, max_delay)
                    else:
                        delay = base_delay

                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}. "
                        f"Retrying in {delay:.1f}s..."
                    )
                    time.sleep(delay)

            raise last_exception

        return wrapper

    return decorator
