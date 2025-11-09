import logging
import os
from datetime import datetime

def init_logger():
    # Ensure logs folder exists
    log_dir = "logs/logs_records"
    os.makedirs(log_dir, exist_ok=True)

    # Log filename based on current date
    log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
    log_path = os.path.join(log_dir, log_filename)

    # Define log format (readable and detailed)
    log_format = (
        "\n%(asctime)s | %(levelname)-8s | %(name)s | "
        "%(funcName)s | Line %(lineno)d | %(message)s"
    )

    # Create handlers: one for file, one for console
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    console_handler = logging.StreamHandler()

    # Formatter
    formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers when re-running init
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    else:
        # Update existing handlers
        logger.handlers.clear()
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    logger.info("Logger initialized successfully.")
    return logger
