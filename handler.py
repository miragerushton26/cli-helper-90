import sys
from typing import Any, Callable, Dict, Optional

class ExecutionFlow:
    def __init__(self):
        self.registry: Dict[str, Callable] = {}

    def register(self, command: str):
        def decorator(func: Callable):
            self.registry[command] = func
            return func
        return decorator

    def execute(self, command: str, *args, **kwargs) -> Any:
        if command not in self.registry:
            raise ValueError(f"unknown operation: {command}")
        return self.registry[command](*args, **kwargs)

flow_manager = ExecutionFlow()

@flow_manager.register("clean")
def handle_cleanup(target_dir: str = "/tmp/cache"):
    import shutil
    import os
    try:
        shutil.rmtree(target_dir)
        os.makedirs(target_dir)
        return f"cleaned {target_dir}"
    except Exception as e:
        return f"failed: {e}"

@flow_manager.register("reorg")
def handle_reorg(data: dict) -> dict:
    keys = sorted(data.keys())
    return {k: data[k] for k in keys}

def entrypoint(cmd: str, **params):
    try:
        result = flow_manager.execute(cmd, **params)
        print(f"[SUCCESS] {result}")
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)