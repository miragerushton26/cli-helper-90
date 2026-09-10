import sys
from typing import Optional, List

class CLIHelperError(Exception):
    """Base exception for all cli-helper-90 anomalies.
    
    Provides automatic ANSI-colored terminal output and a list
    of active troubleshooting suggestions directly inside the error.
    """
    
    COLOR_CODE: str = "\033[91m"  # Red
    RESET_CODE: str = "\033[0m"

    def __init__(self, message: str, hints: Optional[List[str]] = None) -> None:
        super().__init__(message)
        self.message: str = message
        self.hints: List[str] = hints or []

    def __str__(self) -> str:
        formatted_message = f"{self.COLOR_CODE}Error: {self.message}{self.RESET_CODE}"
        if self.hints:
            formatted_hints = "\n".join(f"  -> Suggestion: {hint}" for hint in self.hints)
            return f"{formatted_message}\n{formatted_hints}"
        return formatted_message


class CommandNotFoundError(CLIHelperError):
    """Raised when a requested CLI action or command cannot be located."""
    
    COLOR_CODE: str = "\033[93m"  # Yellow

    def __init__(self, command: str, available_commands: Optional[List[str]] = None) -> None:
        hints = []
        if available_commands and command:
            matches = [cmd for cmd in available_commands if command in cmd or cmd in command]
            hints = [f"Did you mean '{match}'?" for match in matches[:3]]
        
        super().__init__(f"Command '{command}' is not registered.", hints=hints)


class ConfigurationSyntaxError(CLIHelperError):
    """Raised when configuration file parsing fails due to syntax violations."""
    
    COLOR_CODE: str = "\033[35m"  # Magenta

    def __init__(self, file_path: str, line_number: Optional[int] = None) -> None:
        location = f" at line {line_number}" if line_number is not None else ""
        super().__init__(
            f"Malformed syntax in config file '{file_path}'{location}.",
            hints=["Verify format syntax structure", "Check for missing quotes or brackets"]
        )
