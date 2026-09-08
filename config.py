import os
import json
from pathlib import Path
from typing import Any, Dict, Iterator
from contextlib import contextmanager

class DynamicConfig:
    _DEFAULTS: Dict[str, Any] = {
        "debug": False,
        "timeout": 30,
        "api_url": "https://api.cli-helper.com/v1",
        "output_format": "json",
        "max_retries": 3,
    }

    def __init__(self, filepath: str = ".cli-helper.json", env_prefix: str = "CLI_") -> None:
        self._filepath = Path(filepath)
        self._env_prefix = env_prefix
        self._overrides: Dict[str, Any] = {}
        self._loaded_data: Dict[str, Any] = {}
        self.reload()

    def reload(self) -> None:
        self._loaded_data.clear()
        if self._filepath.exists():
            try:
                with open(self._filepath, "r", encoding="utf-8") as f:
                    self._loaded_data.update(json.load(f))
            except (json.JSONDecodeError, OSError):
                pass

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(f"No such private attribute: {name}")

        if name in self._overrides:
            return self._overrides[name]

        env_key = f"{self._env_prefix}{name.upper()}"
        if env_key in os.environ:
            val = os.environ[env_key]
            if val.lower() in ("true", "yes", "1"): return True
            if val.lower() in ("false", "no", "0"): return False
            try: return int(val)
            except ValueError: pass
            try: return float(val)
            except ValueError: pass
            return val

        if name in self._loaded_data:
            return self._loaded_data[name]

        if name in self._DEFAULTS:
            return self._DEFAULTS[name]

        raise AttributeError(f"Configuration key '{name}' is not defined")

    @contextmanager
    def override(self, **kwargs: Any) -> Iterator["DynamicConfig"]:
        original = self._overrides.copy()
        self._overrides.update(kwargs)
        try:
            yield self
        finally:
            self._overrides = original

config = DynamicConfig()
