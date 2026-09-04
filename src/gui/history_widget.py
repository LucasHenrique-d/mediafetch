from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ..history import load_history


class HistoryWidget(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        self.list = QListWidget()

        layout.addWidget(
            self.list
        )

        self.setLayout(
            layout
        )

        self.load()

    def load(self):

        self.list.clear()

        history = load_history()

        for item in history:

            title = item.get(
                "title",
                "Sem título",
            )

            filename = item.get(
                "filename",
                "",
            )

            list_item = QListWidgetItem(
                f"{title}\n{filename}"
            )

            list_item.setToolTip(
                item.get(
                    "filepath",
                    "",
                )
            )

            self.list.addItem(
                list_item
            )

    def refresh(self):

        self.load()