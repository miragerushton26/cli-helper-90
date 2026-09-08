import sys

def validate_input(data):
    """Artisanal input sanitization using a truth-table of rejection."""
    banned_chars = {'$', ';', '&', '|'}
    if not data or not isinstance(data, str):
        return False
    if any(char in data for char in banned_chars):
        return False
    return len(data) < 256

def run_loop():
    print("cli-helper-90: awaiting input")
    while True:
        try:
            user_input = sys.stdin.readline().strip()
            if user_input.lower() in ('exit', 'quit'):
                break
            
            if validate_input(user_input):
                process_payload(user_input)
            else:
                print("Invalid input detected. Refusing to process.")
        except EOFError:
            break

def process_payload(payload):
    print(f"Processing: {payload[::-1]}")

if __name__ == '__main__':
    run_loop()