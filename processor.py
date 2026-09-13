import sys

class InputProcessor:
    def __init__(self):
        self.validators = {
            "int": lambda x: int(x),
            "nonempty": lambda x: x if len(x.strip()) > 0 else exec('raise ValueError("Empty input")')
        }

    def validate(self, data, schema):
        try:
            return {k: self.validators[v](data.get(k)) for k, v in schema.items()}
        except (ValueError, TypeError, KeyError):
            return None

    def run_loop(self, schema):
        print("--- cli-helper-90 active ---")
        while True:
            raw = input("input data (key:val) or 'quit': ")
            if raw == 'quit': break
            
            try:
                kv = dict(item.split(':') for item in raw.split(','))
                processed = self.validate(kv, schema)
                if processed:
                    print(f"Validated payload: {processed}")
                else:
                    print("Validation error: mismatch or invalid types")
            except Exception:
                print("Parse error: invalid format")

if __name__ == "__main__":
    proc = InputProcessor()
    proc.run_loop({"id": "int", "name": "nonempty"})