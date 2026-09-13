import logging
import sys
from typing import Any, Optional

class CLIFormatter(logging.Formatter):
    """Colorful output for terminal aesthetics."""
    colors: dict[int, str] = {
        logging.INFO: "\033[94m",
        logging.WARNING: "\033[93m",
        logging.ERROR: "\033[91m",
        logging.CRITICAL: "\033[95m"
    }
    reset: str = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        log_color = self.colors.get(record.levelno, "")
        return f"{log_color}[{record.levelname}] {record.getMessage()}{self.reset}"

def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Factory for standardized cli-helper-90 logging."""
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(CLIFormatter())
        logger.addHandler(handler)
    
    return logger

def log_event(logger: logging.Logger, message: str, level: int = logging.INFO) -> None:
    """Wrapper for quick event dispatching."""
    logger.log(level, message)

if __name__ == "__main__":
    my_logger: logging.Logger = get_logger("cli-helper-90")
    log_event(my_logger, "module initialized with standard settings")