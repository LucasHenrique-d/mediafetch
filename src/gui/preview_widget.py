from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)


class PreviewWidget(QFrame):

    def __init__(self):

        super().__init__()

        self.setObjectName(
            "previewCard"
        )

        self.thumbnail = QLabel()

        self.thumbnail.setFixedSize(
            180,
            180,
        )

        self.thumbnail.setAlignment(
            Qt.AlignCenter
        )

        self.thumbnail.setText(
            "Thumbnail"
        )

        self.title = QLabel(
            "Título"
        )

        self.title.setWordWrap(
            True
        )

        self.title.setStyleSheet(
            """
            font-size: 18px;
            font-weight: bold;
            """
        )

        self.author = QLabel(
            "Autor"
        )

        self.duration = QLabel(
            "Duração"
        )

        info_layout = QVBoxLayout()

        info_layout.addWidget(
            self.title
        )

        info_layout.addWidget(
            self.author
        )

        info_layout.addWidget(
            self.duration
        )

        info_layout.addStretch()

        layout = QHBoxLayout()

        layout.addWidget(
            self.thumbnail
        )

        layout.addLayout(
            info_layout
        )

        self.setLayout(
            layout
        )

        self.hide()

    def update_info(
        self,
        data: dict,
    ):

        self.title.setText(
            data.get(
                "title"
            ) or "Sem título"
        )

        self.author.setText(
            f"@{data.get('uploader') or 'desconhecido'}"
        )

        duration = data.get(
            "duration"
        )

        if duration:

            minutes = duration // 60
            seconds = duration % 60

            self.duration.setText(
                f"Duração: "
                f"{minutes:02d}:{seconds:02d}"
            )

        else:

            self.duration.setText(
                "Duração: desconhecida"
            )

        self.show()

    def set_thumbnail(
        self,
        pixmap: QPixmap,
    ):

        scaled = pixmap.scaled(
            self.thumbnail.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        self.thumbnail.setPixmap(
            scaled
        )