import logging
import sys
from datetime import datetime

class CustomFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',
        'INFO': '\033[92m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'CRITICAL': '\033[95m',
        'RESET': '\033[0m'
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        timestamp = datetime.now().strftime('%H:%M:%S')
        return f"{color}[{timestamp}] {record.levelname}: {record.getMessage()}{self.COLORS['RESET']}"

def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(CustomFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger

# Dynamic namespace initialization for cli-helper-90
logger = get_logger('cli-helper-90')