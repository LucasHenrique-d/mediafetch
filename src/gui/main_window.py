import os

import requests

from pathlib import Path

from PySide6.QtCore import QThread, Qt
from PySide6.QtGui import (
    QCloseEvent,
    QPixmap,
)
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ..config import DOWNLOAD_DIR
from ..history import add_history
from ..resources import resource_path
from ..settings import load_settings, save_settings
from ..version import (
    APP_AUTHOR,
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
)

from .history_widget import HistoryWidget
from .info_worker import InfoWorker
from .preview_widget import PreviewWidget
from .worker import DownloadWorker


class MainWindow(QMainWindow):

    # ==========================================================
    # CONSTRUÇÃO
    # ==========================================================

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            f"{APP_NAME} v{APP_VERSION}"
        )

        self.setMinimumSize(
            900,
            650,
        )

        self.resize(
            1100,
            760,
        )

        # ======================================================
        # THREADS
        # ======================================================

        self.thread = None
        self.worker = None

        self.info_thread = None
        self.info_worker = None

        # ======================================================
        # DADOS
        # ======================================================

        self.video_info = None

        self.settings = load_settings()

        saved_dir = self.settings.get(
            "download_dir"
        )

        if saved_dir:
            self.download_dir = Path(
                saved_dir
            )
        else:
            self.download_dir = DOWNLOAD_DIR

        # ======================================================
        # INTERFACE
        # ======================================================

        self.setup_ui()

    # ==========================================================
    # HELPERS VISUAIS
    # ==========================================================

    def create_card(self):

        card = QFrame()

        card.setObjectName(
            "Card"
        )

        card.setFrameShape(
            QFrame.StyledPanel
        )

        return card

    def create_section_title(
        self,
        text: str,
    ):

        label = QLabel(
            text
        )

        label.setObjectName(
            "SectionTitle"
        )

        return label

    def create_icon_label(
        self,
    ):

        label = QLabel()

        label.setObjectName(
            "AppLogo"
        )

        label.setAlignment(
            Qt.AlignCenter
        )

        icon_path = resource_path(
            "assets/icon.ico"
        )

        pixmap = QPixmap(
            str(icon_path)
        )

        if not pixmap.isNull():

            pixmap = pixmap.scaled(
                52,
                52,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )

            label.setPixmap(
                pixmap
            )

        label.setFixedSize(
            64,
            64,
        )

        return label

    # ==========================================================
    # CONFIGURAÇÃO DA INTERFACE
    # ==========================================================

    def setup_ui(self):

        # ======================================================
        # MENU
        # ======================================================

        menu_bar = self.menuBar()

        help_menu = menu_bar.addMenu(
            "Ajuda"
        )

        about_action = help_menu.addAction(
            "Sobre o MediaFetch  "
        )

        about_action.triggered.connect(
            self.show_about
        )

        # ======================================================
        # WIDGET PRINCIPAL
        # ======================================================

        download_widget = QWidget()

        root_layout = QVBoxLayout(
            download_widget
        )

        root_layout.setContentsMargins(
            32,
            28,
            32,
            28,
        )

        root_layout.setSpacing(
            18
        )

        # ======================================================
        # CABEÇALHO
        # ======================================================

        header_layout = QHBoxLayout()

        header_layout.setSpacing(
            16
        )

        logo = self.create_icon_label()

        header_layout.addWidget(
            logo
        )

        header_text_layout = QVBoxLayout()

        header_text_layout.setSpacing(
            2
        )

        title = QLabel(
            APP_NAME
        )

        title.setObjectName(
            "AppTitle"
        )

        subtitle = QLabel(
            "Baixe suas mídias de forma simples e rápida."
        )

        subtitle.setObjectName(
            "AppSubtitle"
        )

        header_text_layout.addWidget(
            title
        )

        header_text_layout.addWidget(
            subtitle
        )

        header_layout.addLayout(
            header_text_layout
        )

        header_layout.addStretch()

        version_label = QLabel(
            f"v{APP_VERSION}"
        )

        version_label.setObjectName(
            "VersionBadge"
        )

        header_layout.addWidget(
            version_label,
            alignment=Qt.AlignTop,
        )

        root_layout.addLayout(
            header_layout
        )

        # ======================================================
        # URL CARD
        # ======================================================

        url_card = self.create_card()

        url_layout = QVBoxLayout(
            url_card
        )

        url_layout.setContentsMargins(
            22,
            20,
            22,
            20,
        )

        url_layout.setSpacing(
            12
        )

        url_layout.addWidget(
            self.create_section_title(
                "URL da mídia"
            )
        )

        url_row = QHBoxLayout()

        url_row.setSpacing(
            10
        )

        self.url_input = QLineEdit()

        self.url_input.setObjectName(
            "UrlInput"
        )

        self.url_input.setPlaceholderText(
            "Cole aqui a URL do vídeo..."
        )

        self.url_input.setMinimumHeight(
            48
        )

        self.url_input.textChanged.connect(
            self.url_changed
        )

        url_row.addWidget(
            self.url_input,
            stretch=1,
        )

        self.paste_button = QPushButton(
            "Colar"
        )

        self.paste_button.setObjectName(
            "SecondaryButton"
        )

        self.paste_button.setMinimumHeight(
            48
        )

        self.paste_button.setMinimumWidth(
            100
        )

        self.paste_button.clicked.connect(
            self.paste_url
        )

        url_row.addWidget(
            self.paste_button
        )

        self.info_button = QPushButton(
            "Analisar mídia"
        )

        self.info_button.setObjectName(
            "PrimaryButton"
        )

        self.info_button.setMinimumHeight(
            48
        )

        self.info_button.setMinimumWidth(
            150
        )

        self.info_button.clicked.connect(
            self.get_video_info
        )

        url_row.addWidget(
            self.info_button
        )

        url_layout.addLayout(
            url_row
        )

        root_layout.addWidget(
            url_card
        )

        # ======================================================
        # PREVIEW / INFORMAÇÕES
        # ======================================================

        preview_card = self.create_card()

        preview_layout = QVBoxLayout(
            preview_card
        )

        preview_layout.setContentsMargins(
            22,
            20,
            22,
            20,
        )

        preview_layout.setSpacing(
            12
        )

        preview_layout.addWidget(
            self.create_section_title(
                "Pré-visualização"
            )
        )

        self.preview = PreviewWidget()

        self.preview.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )

        preview_layout.addWidget(
            self.preview
        )

        root_layout.addWidget(
            preview_card,
            stretch=1,
        )

        # ======================================================
        # DESTINO
        # ======================================================

        destination_card = self.create_card()

        destination_layout = QVBoxLayout(
            destination_card
        )

        destination_layout.setContentsMargins(
            22,
            18,
            22,
            18,
        )

        destination_layout.setSpacing(
            10
        )

        destination_layout.addWidget(
            self.create_section_title(
                "Pasta de destino"
            )
        )

        destination_row = QHBoxLayout()

        destination_row.setSpacing(
            10
        )

        self.folder_label = QLabel(
            str(self.download_dir)
        )

        self.folder_label.setObjectName(
            "FolderLabel"
        )

        self.folder_label.setMinimumHeight(
            42
        )

        self.folder_label.setAlignment(
            Qt.AlignVCenter | Qt.AlignLeft
        )

        self.folder_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        destination_row.addWidget(
            self.folder_label,
            stretch=1,
        )

        self.folder_button = QPushButton(
            "Escolher pasta"
        )

        self.folder_button.setObjectName(
            "SecondaryButton"
        )

        self.folder_button.setMinimumHeight(
            42
        )

        self.folder_button.clicked.connect(
            self.choose_folder
        )

        destination_row.addWidget(
            self.folder_button
        )

        self.open_folder_button = QPushButton(
            "Abrir pasta"
        )

        self.open_folder_button.setObjectName(
            "SecondaryButton"
        )

        self.open_folder_button.setMinimumHeight(
            42
        )

        self.open_folder_button.clicked.connect(
            self.open_download_folder
        )

        destination_row.addWidget(
            self.open_folder_button
        )

        destination_layout.addLayout(
            destination_row
        )

        root_layout.addWidget(
            destination_card
        )

        # ======================================================
        # DOWNLOAD / PROGRESSO
        # ======================================================

        download_card = self.create_card()

        download_layout = QVBoxLayout(
            download_card
        )

        download_layout.setContentsMargins(
            22,
            18,
            22,
            18,
        )

        download_layout.setSpacing(
            10
        )

        status_row = QHBoxLayout()

        self.status_label = QLabel(
            "Pronto para baixar."
        )

        self.status_label.setObjectName(
            "StatusLabel"
        )

        status_row.addWidget(
            self.status_label
        )

        status_row.addStretch()

        self.progress_info = QLabel(
            ""
        )

        self.progress_info.setObjectName(
            "ProgressInfo"
        )

        status_row.addWidget(
            self.progress_info
        )

        download_layout.addLayout(
            status_row
        )

        self.progress_bar = QProgressBar()

        self.progress_bar.setObjectName(
            "DownloadProgress"
        )

        self.progress_bar.setRange(
            0,
            100,
        )

        self.progress_bar.setValue(
            0
        )

        self.progress_bar.setTextVisible(
            False
        )

        self.progress_bar.setMinimumHeight(
            10
        )

        download_layout.addWidget(
            self.progress_bar
        )

        actions_layout = QHBoxLayout()

        actions_layout.setSpacing(
            10
        )

        self.download_button = QPushButton(
            "Baixar mídia"
        )

        self.download_button.setObjectName(
            "DownloadButton"
        )

        self.download_button.setMinimumHeight(
            48
        )

        self.download_button.setMinimumWidth(
            180
        )

        self.download_button.setEnabled(
            False
        )

        self.download_button.clicked.connect(
            self.start_download
        )

        actions_layout.addWidget(
            self.download_button,
            stretch=1,
        )

        self.cancel_button = QPushButton(
            "Cancelar"
        )

        self.cancel_button.setObjectName(
            "CancelButton"
        )

        self.cancel_button.setMinimumHeight(
            48
        )

        self.cancel_button.setEnabled(
            False
        )

        self.cancel_button.clicked.connect(
            self.cancel_download
        )

        actions_layout.addWidget(
            self.cancel_button
        )

        self.clear_button = QPushButton(
            "Limpar"
        )

        self.clear_button.setObjectName(
            "SecondaryButton"
        )

        self.clear_button.setMinimumHeight(
            48
        )

        self.clear_button.clicked.connect(
            self.clear_form
        )

        actions_layout.addWidget(
            self.clear_button
        )

        download_layout.addLayout(
            actions_layout
        )

        root_layout.addWidget(
            download_card
        )

        # ======================================================
        # ESTADO INICIAL
        # ======================================================

        self.preview.hide()

        # ======================================================
        # ABAS
        # ======================================================

        tabs = QTabWidget()

        tabs.setDocumentMode(
            True
        )

        tabs.addTab(
            download_widget,
            "Download",
        )

        self.history_widget = HistoryWidget()

        tabs.addTab(
            self.history_widget,
            "Histórico",
        )

        self.setCentralWidget(
            tabs
        )

    # ==========================================================
    # ABOUT
    # ==========================================================

    def show_about(self):

        QMessageBox.about(
            self,
            f"Sobre o {APP_NAME}",
            (
                f"<h2>{APP_NAME}</h2>"
                f"<p>Versão {APP_VERSION}</p>"
                f"<p>{APP_DESCRIPTION}</p>"
                f"<p>Desenvolvido por {APP_AUTHOR}.</p>"
                "<p>"
                "Tecnologia: Python + PySide6."
                "</p>"
            ),
        )

    # ==========================================================
    # URL ALTERADA
    # ==========================================================

    def url_changed(
        self,
        text: str,
    ):

        self.video_info = None

        self.download_button.setEnabled(
            False
        )

        if text.strip():

            self.status_label.setText(
                "URL alterada. Analise a mídia novamente."
            )

    # ==========================================================
    # ESCOLHER PASTA
    # ==========================================================

    def choose_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Escolher pasta",
            str(self.download_dir),
        )

        if not folder:
            return

        self.download_dir = Path(
            folder
        )

        self.settings[
            "download_dir"
        ] = str(
            self.download_dir
        )

        save_settings(
            self.settings
        )

        self.folder_label.setText(
            str(self.download_dir)
        )

    # ==========================================================
    # COLAR URL
    # ==========================================================

    def paste_url(self):

        clipboard = QApplication.clipboard()

        text = clipboard.text().strip()

        if not text:
            return

        self.url_input.setText(
            text
        )

        self.status_label.setText(
            "URL colada."
        )

    # ==========================================================
    # OBTER INFORMAÇÕES
    # ==========================================================

    def get_video_info(self):

        url = self.url_input.text().strip()

        if not url:

            QMessageBox.warning(
                self,
                "URL inválida",
                "Cole uma URL do Instagram.",
            )

            return

        if self.info_thread is not None:
            return

        self.video_info = None

        # ======================================================
        # DESABILITA CONTROLES
        # ======================================================

        self.info_button.setEnabled(
            False
        )

        self.download_button.setEnabled(
            False
        )

        self.folder_button.setEnabled(
            False
        )

        self.paste_button.setEnabled(
            False
        )

        self.status_label.setText(
            "Obtendo informações..."
        )

        # ======================================================
        # THREAD
        # ======================================================

        self.info_thread = QThread()

        self.info_worker = InfoWorker(
            url
        )

        self.info_worker.moveToThread(
            self.info_thread
        )

        # ======================================================
        # INÍCIO
        # ======================================================

        self.info_thread.started.connect(
            self.info_worker.run
        )

        # ======================================================
        # RESULTADO
        # ======================================================

        self.info_worker.finished.connect(
            self.info_finished
        )

        # ======================================================
        # ERRO
        # ======================================================

        self.info_worker.error.connect(
            self.info_error
        )

        # ======================================================
        # ENCERRAMENTO
        # ======================================================

        self.info_worker.finished.connect(
            self.info_thread.quit
        )

        self.info_worker.error.connect(
            self.info_thread.quit
        )

        # ======================================================
        # LIMPEZA
        # ======================================================

        self.info_thread.finished.connect(
            self.info_worker.deleteLater
        )

        self.info_thread.finished.connect(
            self.info_thread.deleteLater
        )

        self.info_thread.finished.connect(
            self.info_thread_finished
        )

        # ======================================================
        # INICIA
        # ======================================================

        self.info_thread.start()

    # ==========================================================
    # INFORMAÇÕES RECEBIDAS
    # ==========================================================

    def info_finished(
        self,
        data: dict,
    ):

        self.video_info = data

        # ======================================================
        # PREVIEW
        # ======================================================

        self.preview.update_info(
            data
        )

        self.preview.show()

        # ======================================================
        # THUMBNAIL
        # ======================================================

        thumbnail_url = data.get(
            "thumbnail"
        )

        if thumbnail_url:

            try:

                response = requests.get(
                    thumbnail_url,
                    timeout=10,
                )

                response.raise_for_status()

                pixmap = QPixmap()

                if pixmap.loadFromData(
                    response.content
                ):

                    self.preview.set_thumbnail(
                        pixmap
                    )

            except requests.RequestException:

                pass

        # ======================================================
        # INTERFACE
        # ======================================================

        self.status_label.setText(
            "Mídia encontrada."
        )

        self.download_button.setEnabled(
            True
        )

        self.folder_button.setEnabled(
            True
        )

        self.paste_button.setEnabled(
            True
        )

    # ==========================================================
    # ERRO NAS INFORMAÇÕES
    # ==========================================================

    def info_error(
        self,
        message: str,
    ):

        self.video_info = None

        self.status_label.setText(
            "Não foi possível obter as informações."
        )

        QMessageBox.critical(
            self,
            "Erro ao analisar mídia",
            message,
        )

    # ==========================================================
    # THREAD DE INFORMAÇÕES FINALIZADA
    # ==========================================================

    def info_thread_finished(
        self,
    ):

        self.info_button.setEnabled(
            True
        )

        self.folder_button.setEnabled(
            True
        )

        self.paste_button.setEnabled(
            True
        )

        self.info_thread = None

        self.info_worker = None

        self.download_button.setEnabled(
            self.video_info is not None
        )

    # ==========================================================
    # INICIAR DOWNLOAD
    # ==========================================================

    def start_download(self):

        url = self.url_input.text().strip()

        if not url:

            QMessageBox.warning(
                self,
                "URL inválida",
                "Cole uma URL do Instagram.",
            )

            return

        if not self.video_info:

            QMessageBox.warning(
                self,
                "Mídia não carregada",
                (
                    "Primeiro analise as informações "
                    "da mídia."
                ),
            )

            return

        if self.thread is not None:
            return

        # ======================================================
        # DESABILITA CONTROLES
        # ======================================================

        self.download_button.setEnabled(
            False
        )

        self.info_button.setEnabled(
            False
        )

        self.folder_button.setEnabled(
            False
        )

        self.paste_button.setEnabled(
            False
        )

        self.cancel_button.setEnabled(
            True
        )

        # ======================================================
        # RESET
        # ======================================================

        self.progress_bar.setValue(
            0
        )

        self.progress_info.clear()

        self.status_label.setText(
            "Preparando download..."
        )

        # ======================================================
        # THREAD
        # ======================================================

        self.thread = QThread()

        self.worker = DownloadWorker(
            url=url,
            download_dir=self.download_dir,
        )

        self.worker.moveToThread(
            self.thread
        )

        # ======================================================
        # INÍCIO
        # ======================================================

        self.thread.started.connect(
            self.worker.run
        )

        # ======================================================
        # PROGRESSO
        # ======================================================

        self.worker.progress.connect(
            self.update_progress
        )

        # ======================================================
        # FINALIZAÇÃO
        # ======================================================

        self.worker.finished.connect(
            self.download_finished
        )

        # ======================================================
        # ERRO
        # ======================================================

        self.worker.error.connect(
            self.download_error
        )

        # ======================================================
        # CANCELAMENTO
        # ======================================================

        self.worker.cancelled.connect(
            self.download_cancelled
        )

        # ======================================================
        # ENCERRAMENTO DA THREAD
        # ======================================================

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.error.connect(
            self.thread.quit
        )

        self.worker.cancelled.connect(
            self.thread.quit
        )

        # ======================================================
        # LIMPEZA
        # ======================================================

        self.thread.finished.connect(
            self.worker.deleteLater
        )

        self.thread.finished.connect(
            self.thread.deleteLater
        )

        self.thread.finished.connect(
            self.download_thread_finished
        )

        # ======================================================
        # INICIA
        # ======================================================

        self.thread.start()

    # ==========================================================
    # PROGRESSO
    # ==========================================================

    def update_progress(
        self,
        data: dict,
    ):

        status = data.get(
            "status"
        )

        if status == "downloading":

            percentage = data.get(
                "_percent_str",
                "0%",
            )

            speed = data.get(
                "_speed_str",
                "N/A",
            )

            eta = data.get(
                "_eta_str",
                "N/A",
            )

            downloaded = data.get(
                "_downloaded_bytes_str",
                "",
            )

            total = data.get(
                "_total_bytes_str",
                "",
            )

            try:

                value = float(
                    percentage
                    .replace(
                        "%",
                        "",
                    )
                    .strip()
                )

                self.progress_bar.setValue(
                    int(value)
                )

            except (
                ValueError,
                TypeError,
            ):

                pass

            self.status_label.setText(
                "Baixando mídia..."
            )

            self.progress_info.setText(
                f"{downloaded} / {total}   "
                f"{speed}   "
                f"ETA: {eta}"
            )

        elif status == "finished":

            self.progress_bar.setValue(
                100
            )

            self.status_label.setText(
                "Processando arquivo..."
            )

    # ==========================================================
    # DOWNLOAD CONCLUÍDO
    # ==========================================================

    def download_finished(
        self,
        result: dict,
    ):

        self.progress_bar.setValue(
            100
        )

        self.status_label.setText(
            "Download concluído!"
        )

        self.progress_info.setText(
            result["filename"]
        )

        # ======================================================
        # HISTÓRICO
        # ======================================================

        add_history(
            {
                "title": result.get(
                    "title",
                    "",
                ),
                "filename": result.get(
                    "filename",
                    "",
                ),
                "filepath": result.get(
                    "filepath",
                    "",
                ),
                "url": result.get(
                    "url",
                    "",
                ),
            }
        )

        if hasattr(
            self.history_widget,
            "refresh",
        ):

            self.history_widget.refresh()

        # ======================================================
        # MENSAGEM
        # ======================================================

        QMessageBox.information(
            self,
            "Download concluído",
            (
                "Mídia baixada com sucesso!\n\n"
                f"Título: {result.get('title', '')}\n\n"
                f"Arquivo: {result.get('filename', '')}\n\n"
                f"Pasta: {result.get('filepath', '')}"
            ),
        )

    # ==========================================================
    # ERRO DOWNLOAD
    # ==========================================================

    def download_error(
        self,
        message: str,
    ):

        self.status_label.setText(
            "Erro durante o download."
        )

        self.progress_bar.setValue(
            0
        )

        self.progress_info.clear()

        QMessageBox.critical(
            self,
            "Erro no download",
            message,
        )

    # ==========================================================
    # DOWNLOAD CANCELADO
    # ==========================================================

    def download_cancelled(
        self,
    ):

        self.status_label.setText(
            "Download cancelado."
        )

        self.progress_bar.setValue(
            0
        )

        self.progress_info.clear()

    # ==========================================================
    # THREAD DOWNLOAD FINALIZADA
    # ==========================================================

    def download_thread_finished(
        self,
    ):

        self.info_button.setEnabled(
            True
        )

        self.folder_button.setEnabled(
            True
        )

        self.paste_button.setEnabled(
            True
        )

        self.cancel_button.setEnabled(
            False
        )

        self.download_button.setEnabled(
            self.video_info is not None
        )

        self.thread = None

        self.worker = None

    # ==========================================================
    # CANCELAR DOWNLOAD
    # ==========================================================

    def cancel_download(
        self,
    ):

        if not self.worker:
            return

        self.cancel_button.setEnabled(
            False
        )

        self.status_label.setText(
            "Cancelando download..."
        )

        self.worker.cancel()

    # ==========================================================
    # LIMPAR
    # ==========================================================

    def clear_form(
        self,
    ):

        if self.thread is not None:
            return

        self.url_input.clear()

        self.video_info = None

        self.preview.clear()

        self.preview.hide()

        self.progress_bar.setValue(
            0
        )

        self.progress_info.clear()

        self.status_label.setText(
            "Pronto para baixar."
        )

        self.download_button.setEnabled(
            False
        )

    # ==========================================================
    # ABRIR PASTA
    # ==========================================================

    def open_download_folder(
        self,
    ):

        self.download_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:

            os.startfile(
                str(
                    self.download_dir
                )
            )

        except OSError as error:

            QMessageBox.critical(
                self,
                "Erro",
                (
                    "Não foi possível abrir "
                    "a pasta de downloads.\n\n"
                    f"{error}"
                ),
            )

    # ==========================================================
    # FECHAR APLICATIVO
    # ==========================================================

    def closeEvent(
        self,
        event: QCloseEvent,
    ):

        if self.thread is None:

            event.accept()

            return

        result = QMessageBox.question(
            self,
            "Download em andamento",
            (
                "Existe um download em andamento.\n\n"
                "Deseja cancelar e fechar o MediaFetch?"
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if result != QMessageBox.Yes:

            event.ignore()

            return

        self.status_label.setText(
            "Cancelando download..."
        )

        if self.worker:

            self.worker.cancel()

        self.thread.quit()

        self.thread.wait()

        event.accept()