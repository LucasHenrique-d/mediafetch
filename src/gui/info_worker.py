from PySide6.QtCore import QObject, Signal, Slot

from ..core.downloader import MidiaDownloader
from ..core.exceptions import DownloaderError


class InfoWorker(QObject):

    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, url: str):
        super().__init__()

        self.url = url

    @Slot()
    def run(self):

        try:

            downloader = MidiaDownloader()

            result = downloader.get_info(
                self.url
            )

            self.finished.emit(
                result
            )

        except DownloaderError as error:

            self.error.emit(
                str(error)
            )

        except Exception as error:

            self.error.emit(
                f"Erro inesperado: {error}"
            )