import json
import os
import time
from typing import Any, Callable, Optional

def robust_json_loader(path: str, default: Any = None) -> Any:
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def time_execution(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f'[DEBUG] {func.__name__} took {elapsed:.6f}s')
        return result
    return wrapper

def ensure_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def smart_dict_flatten(d: dict, parent_key: str = '', sep: str = '_') -> dict:
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(smart_dict_flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

class DynamicContext:
    def __init__(self, **entries: Any):
        self.__dict__.update(entries)
    
    def __repr__(self) -> str:
        return str(self.__dict__)