import logging
import platform
import sys
from pathlib import Path


APP_DATA_DIR = (
    Path.home()
    / "AppData"
    / "Local"
    / "MediaFetch"
)

APP_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


LOG_FILE = (
    APP_DATA_DIR
    / "app.log"
)


def setup_logger():

    logger = logging.getLogger(
        "MediaFetch"
    )

    if logger.handlers:
        return logger

    logger.setLevel(
        logging.INFO
    )

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )

    file_handler = (
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8",
        )
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )

    logger.info(
        "MediaFetch iniciado."
    )

    logger.info(
        "Python: %s",
        sys.version,
    )

    logger.info(
        "Sistema: %s",
        platform.platform(),
    )

    return logger