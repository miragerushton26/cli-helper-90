import re

class InputGuard:
    """Chainable sanity checks for CLI input streams."""
    def __init__(self, value):
        self.value = value
        self.errors = []

    def must_match(self, pattern, msg):
        if not re.fullmatch(pattern, str(self.value)):
            self.errors.append(msg)
        return self

    def length_bounds(self, min_len, max_len):
        if not (min_len <= len(str(self.value)) <= max_len):
            self.errors.append(f"Length must be between {min_len} and {max_len}")
        return self

    def validate(self):
        if self.errors:
            raise ValueError(" | ".join(self.errors))
        return self.value

def run_input_loop():
    print("Entering processing loop. Ctrl+C to exit.")
    while True:
        try:
            user_input = input(">>> ").strip()
            clean_data = InputGuard(user_input).must_match(
                r'[a-zA-Z0-9_]+', "Alphanumeric only"
            ).length_bounds(3, 15).validate()
            
            print(f"Processing: {clean_data}")
        except (EOFError, KeyboardInterrupt):
            break
        except ValueError as e:
            print(f"Validation failure: {e}")

if __name__ == '__main__':
    run_input_loop()