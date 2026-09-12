import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

class EmojiFormatter(logging.Formatter):
    LEVEL_EMOJIS = {
        logging.DEBUG: "🔍",
        logging.INFO: "ℹ️",
        logging.WARNING: "⚠️",
        logging.ERROR: "💥",
        logging.CRITICAL: "🚨"
    }

    def format(self, record):
        emoji = self.LEVEL_EMOJIS.get(record.levelno, "📝")
        record.msg = f"{emoji} {record.msg}"
        return super().format(record)

def setup_logger(log_filename: str = "cli_helper.log") -> logging.Logger:
    log_path = Path(log_filename)
    logger = logging.getLogger("cli-helper-90")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = EmojiFormatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S")
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)

        file_handler = RotatingFileHandler(log_path, maxBytes=1048576, backupCount=3, encoding="utf-8")
        file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) - %(message)s")
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

    return logger

cli_logger = setup_logger()
