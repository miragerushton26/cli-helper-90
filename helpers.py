import time
import functools
import random
from typing import Callable, Any

def retry_operation(retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            local_delay = delay
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries - 1:
                        raise e
                    time.sleep(local_delay + random.uniform(0, 0.1))
                    local_delay *= backoff
            return None
        return wrapper
    return decorator

def persistent_request(max_attempts: int = 5):
    """
    A higher-order execution harness for fragile network calls
    that employs exponential backoff with jitter.
    """
    def execute(operation: Callable, *args, **kwargs):
        attempt = 0
        while attempt < max_attempts:
            try:
                return operation(*args, **kwargs)
            except (ConnectionError, TimeoutError):
                attempt += 1
                if attempt >= max_attempts: raise
                time.sleep((2 ** attempt) * 0.1)
    return execute