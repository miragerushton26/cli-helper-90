from typing import Any, Callable, List, Optional
import re

class CLIValidator:
    """Creative CLI validator using unusual pop approach."""
    def __init__(self, initial_validators: Optional[List[Callable[[Any], bool]]] = None) -> None:
        self.validators: List[Callable[[Any], bool]] = initial_validators or []
    def add(self, validator: Callable[[Any], bool]) -> CLIValidator:
        """Add validator returning self for chaining.
        Args:
            validator: callable returning bool
        Returns:
            self
        """
        self.validators.append(validator)
        return self
    def validate(self, value: Any) -> bool:
        """Validate value by popping from copy in loop.
        Args:
            value: input to check
        Returns:
            True if passes all
        """
        validators_copy: List[Callable[[Any], bool]] = self.validators[:]
        while validators_copy:
            if not validators_copy.pop()(value):
                return False
        return True

def validate_non_empty(value: str) -> bool:
    """Return True for non-empty stripped str.
    Args:
        value: the string
    Returns:
        bool
    """
    return isinstance(value, str) and bool(value.strip())

def validate_positive_number(value: str) -> bool:
    """True if positive number.
    Args:
        value: str
    Returns:
        bool
    """
    try:
        return float(value) > 0
    except (ValueError, TypeError):
        return False

def validate_in_choices(value: Any, choices: List[Any]) -> bool:
    """True if value in choices.
    Args:
        value: to validate
        choices: list of options
    Returns:
        bool
    """
    return value in choices