import json
from typing import Any, Dict, List, Union


def deep_flatten(data: Union[Dict[str, Any], List[Any]], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    items: List[tuple] = []
    
    if isinstance(data, dict):
        iterable = data.items()
    elif isinstance(data, list):
        iterable = enumerate(data)
    else:
        return {parent_key: data}

    for k, v in iterable:
        new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
        if isinstance(v, (dict, list)):
            items.extend(deep_flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
            
    return dict(items)


def safe_json_load(raw_input: str) -> Dict[str, Any]:
    try:
        parsed = json.loads(raw_input)
        if isinstance(parsed, dict):
            return parsed
        return {"data": parsed}
    except (json.JSONDecodeError, TypeError):
        return {"raw_fallback": raw_input}


def chunk_sequence(sequence: List[Any], size: int) -> List[List[Any]]:
    if size <= 0:
        raise ValueError("Chunk size must be greater than zero")
    return [sequence[i:i + size] for i in range(0, len(sequence), size)]
