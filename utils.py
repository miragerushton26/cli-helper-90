import time
import random
import functools
from typing import Callable, Any, Type, Tuple

def retry(
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    tries: int = 4,
    delay: float = 1.0,
    backoff: float = 2.0,
    jitter: bool = True
) -> Callable:
    """
    Decorator implementing a robust retry mechanism with an iterator-driven
    delay progression to maintain clean execution state.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            def backoff_generator():
                curr_delay = delay
                for _ in range(tries):
                    yield curr_delay
                    curr_delay *= backoff
                    if jitter:
                        curr_delay += random.uniform(0, curr_delay * 0.1)

            delay_iterator = backoff_generator()
            
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    try:
                        next_delay = next(delay_iterator)
                    except StopIteration:
                        raise e
                    
                    print(f"[!] Retrying due to: {e}. Waiting {next_delay:.2f}s...", flush=True)
                    time.sleep(next_delay)
        return wrapper
    return decorator