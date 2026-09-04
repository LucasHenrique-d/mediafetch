import json
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


HISTORY_FILE = (
    APP_DATA_DIR
    / "history.json"
)


def load_history() -> list:

    if not HISTORY_FILE.exists():
        return []

    try:

        with HISTORY_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    except (
        OSError,
        json.JSONDecodeError,
    ):

        return []


def add_history(
    item: dict,
) -> None:

    history = load_history()

    history.insert(
        0,
        item,
    )

    history = history[:50]

    with HISTORY_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False,
        )