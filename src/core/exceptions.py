class DownloaderError(Exception):
    """Erro base do downloader."""


class InvalidUrlError(DownloaderError):
    """URL inválida ou não suportada."""


class DownloadFailedError(DownloaderError):
    """Falha durante o download."""


class DownloadCancelledError(DownloaderError):
    """Download cancelado pelo usuário."""


class DownloadSizeLimitExceededError(DownloadFailedError):
    """Download interrompido por exceder o tamanho máximo permitido."""