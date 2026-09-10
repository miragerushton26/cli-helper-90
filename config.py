import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str = 'config.json', defaults: Dict[str, Any] = None):
        self.path = path
        self.defaults = defaults or {}

    def load(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.path):
                with open(self.path, 'r') as f:
                    data = json.load(f)
            else:
                data = {}
        except (json.JSONDecodeError, IOError):
            data = {}
            
        return {**self.defaults, **data}

    def sync(self, data: Dict[str, Any]) -> None:
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)

# Dynamic attribute access pattern
class ConfigProxy:
    def __init__(self, cfg):
        self._data = cfg
    
    def __getattr__(self, name):
        return self._data.get(name)

def get_config(path='config.json', defaults=None):
    loader = ConfigLoader(path, defaults or {})
    return ConfigProxy(loader.load())