import json
from pathlib import Path


APP_NAME = "MediaFetch"

APP_DATA_DIR = (
    Path.home()
    / "AppData"
    / "Local"
    / APP_NAME
)

APP_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

SETTINGS_FILE = (
    APP_DATA_DIR
    / "settings.json"
)


DEFAULT_SETTINGS = {
    "download_dir": None,
}


def load_settings() -> dict:

    if not SETTINGS_FILE.exists():
        return DEFAULT_SETTINGS.copy()

    try:

        with SETTINGS_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:

            settings = json.load(file)

        return {
            **DEFAULT_SETTINGS,
            **settings,
        }

    except (
        OSError,
        json.JSONDecodeError,
    ):

        return DEFAULT_SETTINGS.copy()


def save_settings(
    settings: dict,
) -> None:

    with SETTINGS_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            settings,
            file,
            indent=4,
            ensure_ascii=False,
        )