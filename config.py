import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str = 'config.json', defaults: Dict[str, Any] = None):
        self.path = path
        self.defaults = defaults or {}
        self.data = self._initialize_config()

    def _initialize_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                json.dump(self.defaults, f, indent=4)
            return self.defaults
        
        try:
            with open(self.path, 'r') as f:
                loaded = json.load(f)
                return {**self.defaults, **loaded}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def update(self, **kwargs):
        self.data.update(kwargs)
        self.save()