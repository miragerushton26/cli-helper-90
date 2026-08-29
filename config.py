import os
from copy import deepcopy
from typing import Any, Dict, Optional

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]) -> None:
        self._defaults: Dict[str, Any] = deepcopy(defaults)
        self._config: Dict[str, Any] = deepcopy(defaults)

    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    def load(self, overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if overrides is None:
            overrides = {}
        self._config = self._deep_merge(deepcopy(self._defaults), overrides)
        prefix = "CLI_"
        for key, default_val in self._defaults.items():
            env_key = prefix + key.upper()
            if env_key in os.environ:
                raw_val = os.environ[env_key]
                if raw_val.lower() in ("true", "false"):
                    parsed = raw_val.lower() == "true"
                else:
                    try:
                        parsed = int(raw_val)
                    except ValueError:
                        try:
                            parsed = float(raw_val)
                        except ValueError:
                            parsed = raw_val
                self._config[key] = parsed
        return self._config

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        current: Any = self._config
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        return current

    def __getitem__(self, key: str) -> Any:
        return self.get(key)