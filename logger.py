import sys
import os
import time
from collections import deque
from typing import TextIO, Optional, List, Any


class ResilientStreamLogger:
    """Fault-tolerant logger designed for edge-case CLI environments."""

    def __init__(self, log_path: Optional[str] = None, ring_capacity: int = 100):
        self.log_path = log_path
        self.ring_buffer: deque = deque(maxlen=ring_capacity)
        self.fallback_stream: TextIO = sys.stderr
        self._active_file: Optional[TextIO] = None
        self._is_degraded: bool = False

    def _resolve_target(self) -> TextIO:
        if self._is_degraded or not self.log_path:
            return self.fallback_stream or sys.stdout

        if self._active_file is None or self._active_file.closed:
            try:
                self._active_file = open(self.log_path, "a", encoding="utf-8", errors="replace")
            except (OSError, PermissionError, FileNotFoundError):
                self._is_degraded = True
                return self.fallback_stream or sys.stdout
        return self._active_file

    def log(self, level: str, msg: Any, **payload: Any) -> bool:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        sanitized = str(msg).encode("utf-8", errors="backslashreplace").decode("utf-8")
        entry = f"[{timestamp}] [{level.upper()}] {sanitized}"
        if payload:
            entry += f" -- {payload}"

        self.ring_buffer.append(entry)

        for _ in range(2):
            target = self._resolve_target()
            try:
                target.write(entry + "\n")
                target.flush()
                return True
            except (OSError, UnicodeEncodeError, ValueError, AttributeError):
                # Edge cases: broken pipe, closed stream, non-writable output, full disk
                self._is_degraded = True
                if self._active_file and not self._active_file.closed:
                    try:
                        self._active_file.close()
                    except Exception:
                        pass
                self._active_file = None
                self.fallback_stream = sys.__stderr__ or sys.__stdout__

        return False

    def drain_emergency_logs(self) -> List[str]:
        logs = list(self.ring_buffer)
        self.ring_buffer.clear()
        return logs
