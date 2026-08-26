from typing import Any, List, Optional
class InputValidationError(Exception):
    """Base class for input validation errors."""
    pass
class InvalidIntegerError(InputValidationError):
    """Error for invalid integer inputs."""
    def __init__(self, value: Any, reason: str) -> None:
        self.value = value
        self.reason = reason
        super().__init__(f"Invalid integer '{value}': {reason}")
class InvalidStringError(InputValidationError):
    """Error for invalid string inputs."""
    def __init__(self, value: Any, reason: str) -> None:
        self.value = value
        self.reason = reason
        super().__init__(f"Invalid string '{value}': {reason}")
def validate_input_value(value: Any) -> Any:
    """Validate the input value using type checks and raise exceptions if invalid."""
    if isinstance(value, int):
        if value < 0:
            raise InvalidIntegerError(value, "negative values not allowed")
        if value > 1000:
            raise InvalidIntegerError(value, "value exceeds maximum threshold")
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise InvalidStringError(value, "empty or whitespace only")
        if len(stripped) > 50:
            raise InvalidStringError(value, "exceeds maximum length of 50")
        return stripped.lower()
    raise InputValidationError(f"Unsupported input type: {type(value)}")
def main_processing_loop(raw_inputs: List[Any]) -> List[Optional[Any]]:
    """Main processing loop implementing input validation for each item."""
    results: List[Optional[Any]] = []
    for position, raw in enumerate(raw_inputs):
        try:
            validated = validate_input_value(raw)
            if isinstance(validated, int):
                processed = validated ** 2
            else:
                processed = validated[::-1]
            results.append(processed)
        except InputValidationError as validation_error:
            print(f"Skipping invalid input at position {position}: {validation_error}")
            results.append(None)
        except Exception as unexpected:
            print(f"Unexpected issue at {position}: {unexpected}")
            results.append(None)
    return results
if __name__ == "__main__":
    test_data = [42, -5, "ValidString", "", 1500, "TooLongStringForThisValidation", 7, "   ", "ok"]
    output = main_processing_loop(test_data)
    print("Processed results:", output)