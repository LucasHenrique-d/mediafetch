import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

DOWNLOAD_DIR = BASE_DIR / os.getenv(
    "DOWNLOAD_DIR",
    "downloads",
)


try:
    MAX_FILE_SIZE_MB = int(
        os.getenv(
            "MAX_FILE_SIZE_MB",
            "500",
        )
    )
except ValueError:
    MAX_FILE_SIZE_MB = 500


if MAX_FILE_SIZE_MB <= 0:
    MAX_FILE_SIZE_MB = 500


MAX_FILE_SIZE_BYTES = (
    MAX_FILE_SIZE_MB * 1024 * 1024
)


def ensure_directories() -> None:
    DOWNLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )