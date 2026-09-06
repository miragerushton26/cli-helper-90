import sys
import time
import shutil
import threading
from typing import Any, Callable

class CLIHelper:
    """A whimsical terminal manager offering automatic spinners and dynamic borders."""
    def __init__(self, theme_char: str = "◈"):
        self.theme_char = theme_char

    def print_boxed(self, text: str) -> None:
        """Prints text wrapped in dynamically sized borders matching terminal width."""
        cols, _ = shutil.get_terminal_size((80, 20))
        padding = 4
        max_len = max(10, cols - padding - 4)
        lines = [text[i:i+max_len] for i in range(0, len(text), max_len)] or [""]
        
        box_width = max(len(l) for l in lines) + padding
        border = self.theme_char * box_width
        print(f"\n{border}")
        for line in lines:
            padded_line = line.ljust(box_width - 4)
            print(f"{self.theme_char} {padded_line} {self.theme_char}")
        print(f"{border}\n")

    class spin_context:
        """A creative spinner context manager running on a daemon thread."""
        def __init__(self, message: str = "Processing"):
            self.message = message
            self.stop_event = threading.Event()
            self._thread = None

        def __enter__(self):
            def _spin():
                glyphs = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
                idx = 0
                while not self.stop_event.is_set():
                    sys.stdout.write(f"\r{glyphs[idx % len(glyphs)]} {self.message}...")
                    sys.stdout.flush()
                    idx += 1
                    time.sleep(0.08)
            self._thread = threading.Thread(target=_spin, daemon=True)
            self._thread.start()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.stop_event.set()
            if self._thread:
                self._thread.join()
            sys.stdout.write("\r\033[K✓ Done!\n")
            sys.stdout.flush()

if __name__ == "__main__":
    helper = CLIHelper("★")
    helper.print_boxed("Welcome to cli-helper-90. Let us process your complex CLI requirements instantly.")
    with helper.spin_context("Analyzing dynamic configuration bytes"):
        time.sleep(1.5)
    helper.print_boxed("Success! All operations completed cleanly.")