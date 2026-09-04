import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from .gui.main_window import MainWindow
from .logger import setup_logger
from .resources import resource_path
from .version import APP_NAME


DARK_THEME = """
QWidget {
    background-color: #121212;
    color: #ffffff;
    font-size: 14px;
}

QMainWindow {
    background-color: #121212;
}

QLineEdit {
    background-color: #1e1e1e;
    color: #ffffff;
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    padding: 8px;
}

QPushButton {
    background-color: #2a2a2a;
    color: #ffffff;
    border: 1px solid #444444;
    border-radius: 6px;
    padding: 8px 14px;
}

QPushButton:hover {
    background-color: #3a3a3a;
}

QPushButton:pressed {
    background-color: #1f1f1f;
}

QPushButton:disabled {
    background-color: #202020;
    color: #666666;
}

QProgressBar {
    background-color: #1e1e1e;
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #5c6bc0;
    border-radius: 5px;
}

QLabel {
    color: #ffffff;
}
"""


def handle_exception(
    exc_type,
    exc_value,
    exc_traceback,
):
    """
    Captura exceções não tratadas e registra no logger.
    """

    if issubclass(
        exc_type,
        KeyboardInterrupt,
    ):
        sys.__excepthook__(
            exc_type,
            exc_value,
            exc_traceback,
        )
        return

    logger = setup_logger()

    logger.critical(
        "Erro não tratado.",
        exc_info=(
            exc_type,
            exc_value,
            exc_traceback,
        ),
    )


def main():

    # ==================================================
    # LOGGER
    # ==================================================

    logger = setup_logger()

    # ==================================================
    # TRATAMENTO DE EXCEÇÕES
    # ==================================================

    sys.excepthook = handle_exception

    # ==================================================
    # APLICAÇÃO
    # ==================================================

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        APP_NAME
    )

    # ==================================================
    # ÍCONE
    # ==================================================

    icon_path = resource_path(
        "assets/icon.ico"
    )

    app.setWindowIcon(
        QIcon(
            str(icon_path)
        )
    )

    # ==================================================
    # TEMA
    # ==================================================

    app.setStyleSheet(
        DARK_THEME
    )

    # ==================================================
    # JANELA PRINCIPAL
    # ==================================================

    window = MainWindow()

    window.show()

    # ==================================================
    # EXECUÇÃO
    # ==================================================

    return app.exec()


if __name__ == "__main__":
    sys.exit(
        main()
    )