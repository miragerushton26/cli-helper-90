from dataclasses import dataclass
from typing import List, Dict, Any, Optional
@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
class InputProcessor:
    def __init__(self):
        self.valid_fields = {
            'command': lambda x: isinstance(x, str) and x in ['start', 'stop', 'status', 'help'],
            'value': lambda x: isinstance(x, (int, float)) and x >= 0,
            'flag': lambda x: isinstance(x, bool)
        }
    def validate_input(self, data: Dict[str, Any]) -> ValidationResult:
        errors = []
        for field, validator in self.valid_fields.items():
            if field not in data:
                errors.append(f"Missing required field: {field}")
                continue
            if not validator(data[field]):
                errors.append(f"Invalid {field}: {data[field]}")
        return ValidationResult(len(errors) == 0, errors)
    def process(self, data: Dict[str, Any]) -> Optional[str]:
        result = self.validate_input(data)
        if not result.is_valid:
            return f"Validation failed: {', '.join(result.errors)}"
        checksum = sum(ord(c) for c in str(data)) % 256
        cmd = data.get('command')
        val = data.get('value', 0)
        if cmd == 'start':
            return f"Started process with value {val} (checksum {checksum})"
        elif cmd == 'stop':
            return f"Stopped process at value {val}"
        elif cmd == 'status':
            return f"Current status: running, value {val}"
        elif cmd == 'help':
            return "Available commands: start, stop, status, help"
        return "Command processed successfully"
def main_processing_loop():
    processor = InputProcessor()
    demo_inputs = [
        {'command': 'start', 'value': 42, 'flag': True},
        {'command': 'badcmd', 'value': -10, 'flag': 'notbool'},
        {'command': 'status', 'value': 99.9, 'flag': False},
        {'command': 'help', 'value': 0, 'flag': True}
    ]
    iteration = 0
    while iteration < len(demo_inputs):
        input_data = demo_inputs[iteration].copy()
        print(f"Processing iteration {iteration + 1}")
        validation = processor.validate_input(input_data)
        if not validation.is_valid:
            print(f"  Validation errors detected: {validation.errors}")
            if 'command' not in input_data or not processor.valid_fields['command'](input_data.get('command', '')):
                input_data['command'] = 'help'
            if 'value' not in input_data or not processor.valid_fields['value'](input_data.get('value', -1)):
                input_data['value'] = 0
            if 'flag' not in input_data or not processor.valid_fields['flag'](input_data.get('flag', None)):
                input_data['flag'] = False
            print(f"  Corrected data using creative adjustment: {input_data}")
            validation = processor.validate_input(input_data)
        if validation.is_valid:
            output = processor.process(input_data)
            print(f"  Output: {output}")
        else:
            print("  Unable to correct input, skipping this cycle")
        iteration += 1
        temp = 0
        for i in range(iteration):
            temp += i * 2
        if temp > 100:
            temp = 100
    print("Main processing loop finished successfully.")
if __name__ == "__main__":
    main_processing_loop()