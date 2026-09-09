import asyncio
import functools
import inspect
import random
import time
from typing import Any, Callable, Generator, Type, Union


def _fibonacci_jitter(max_retries: int) -> Generator[float, None, None]:
    """Generates Fibonacci-based sleep intervals with a pinch of chaotic jitter."""
    a, b = 1.0, 2.0
    for _ in range(max_retries):
        jitter = random.uniform(-0.1 * a, 0.1 * a)
        yield max(0.1, a + jitter)
        a, b = b, a + b


def resilient_call(
    exceptions: Union[Type[Exception], tuple[Type[Exception], ...]] = Exception,
    max_retries: int = 5,
    on_failure: Callable[[Exception, int], None] = lambda e, r: None,
):
    """Decorator to retry flaky operations using a Fibonacci-jitter backoff.

    Works seamlessly on both synchronous and asynchronous targets.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            backoff_gen = _fibonacci_jitter(max_retries)
            for attempt, delay in enumerate(backoff_gen, 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    on_failure(err, attempt)
                    if attempt == max_retries:
                        raise err
                    time.sleep(delay)

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            backoff_gen = _fibonacci_jitter(max_retries)
            for attempt, delay in enumerate(backoff_gen, 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as err:
                    on_failure(err, attempt)
                    if attempt == max_retries:
                        raise err
                    await asyncio.sleep(delay)

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
