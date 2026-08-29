import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def init_rotating_logger(
    logger_name: str = "cli_helper_90",
    log_filename: str = "app.log",
    max_mb: int = 10,
    backups: int = 2,
    level: int = logging.INFO
) -> logging.Logger:
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / log_filename
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    # remove any existing handlers for clean setup
    for h in logger.handlers[:]:
        logger.removeHandler(h)
        h.close()
    max_bytes = max_mb * 1024 * 1024
    file_handler = RotatingFileHandler(
        str(log_path),
        maxBytes=max_bytes,
        backupCount=backups,
        encoding="utf-8"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    # unusual creative approach: add a stream handler for cli output
    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter("%(levelname)s %(message)s")
    stream_handler.setFormatter(stream_formatter)
    stream_handler.setLevel(logging.WARNING)
    logger.addHandler(stream_handler)
    # set a flag in unusual way using __dict__
    logger.__dict__["_is_configured"] = True
    return logger

def get_configured_logger(name: str = "cli_helper_90") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.__dict__.get("_is_configured", False):
        init_rotating_logger(logger_name=name)
    return logger