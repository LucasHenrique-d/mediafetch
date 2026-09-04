from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot

from ..core.downloader import MidiaDownloader
from ..core.exceptions import DownloaderError


class DownloadWorker(QObject):

    finished = Signal(dict)
    error = Signal(str)
    cancelled = Signal()
    progress = Signal(dict)

    def __init__(
        self,
        url: str,
        download_dir: Path,
    ):
        super().__init__()

        self.url = url
        self.download_dir = download_dir

        self.downloader = MidiaDownloader(
            download_dir=self.download_dir,
            progress_callback=self.handle_progress,
        )

    @Slot()
    def run(self):

        try:

            result = self.downloader.download(
                self.url
            )

            self.finished.emit(
                result
            )

        except DownloaderError as error:

            if (
                "cancelado pelo usuário"
                in str(error).lower()
            ):
                self.cancelled.emit()
                return

            self.error.emit(
                str(error)
            )

        except Exception as error:

            self.error.emit(
                f"Erro inesperado: {error}"
            )

    def handle_progress(
        self,
        data: dict,
    ):
        self.progress.emit(data)

    @Slot()
    def cancel(self):

        self.downloader.cancel()