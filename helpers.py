import sys
import time

def flatten_list(nested_list):
    flat = []
    for item in nested_list:
        if isinstance(item, list):
            flat.extend(flatten_list(item))
        else:
            flat.append(item)
    return flat

class TerminalSpinner:
    def __init__(self, message="Processing"):
        self.message = message
        self.chars = "/—\\|"
        self.running = False

    def spin(self):
        idx = 0
        while self.running:
            sys.stdout.write(f"\r{self.message} {self.chars[idx]}")
            sys.stdout.flush()
            idx = (idx + 1) % len(self.chars)
            time.sleep(0.1)
        sys.stdout.write("\r" + " " * (len(self.message) + 4) + "\r")

def chunk_generator(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]

def safe_get(data_dict, *keys, default=None):
    curr = data_dict
    for key in keys:
        if isinstance(curr, dict) and key in curr:
            curr = curr[key]
        else:
            return default
    return curr
