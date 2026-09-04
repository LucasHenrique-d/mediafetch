from pathlib import Path
from typing import Any, Callable

import yt_dlp

from ..config import (
    DOWNLOAD_DIR,
    MAX_FILE_SIZE_BYTES,
)
from ..logger import setup_logger
from .exceptions import (
    DownloadCancelledError,
    DownloadFailedError,
    DownloadSizeLimitExceededError,
)
from .validators import validate_instagram_url


logger = setup_logger()


class MidiaDownloader:

    def __init__(
        self,
        download_dir: Path | None = None,
        progress_callback: Callable[[dict], None] | None = None,
    ):
        self.download_dir = (
            download_dir or DOWNLOAD_DIR
        )

        self.progress_callback = (
            progress_callback
        )

        self.cancel_requested = False

        # Arquivo parcial relacionado ao download atual.
        self._current_partial_file: Path | None = None

        self.download_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def cancel(self):
        self.cancel_requested = True

        logger.info(
            "Solicitação de cancelamento recebida."
        )

    def _progress_hook(self, data: dict):
        """
        Executado pelo yt-dlp durante o download.

        Verifica cancelamento, acompanha o arquivo
        parcial atual, controla o tamanho máximo
        permitido e atualiza a interface.
        """

        if self.cancel_requested:
            raise DownloadCancelledError(
                "Download cancelado pelo usuário."
            )

        # O yt-dlp informa o arquivo atualmente
        # utilizado durante a operação.
        filename = data.get("filename")

        if filename:
            filepath = Path(filename)

            # Durante o download o yt-dlp normalmente
            # utiliza um arquivo .part.
            if filepath.suffix == ".part":
                self._current_partial_file = filepath
            else:
                self._current_partial_file = Path(
                    f"{filepath}.part"
                )

        downloaded_bytes = data.get(
            "downloaded_bytes"
        )

        if (
            downloaded_bytes is not None
            and downloaded_bytes > MAX_FILE_SIZE_BYTES
        ):
            logger.warning(
                "Download interrompido: "
                "limite máximo de %d bytes excedido.",
                MAX_FILE_SIZE_BYTES,
            )

            raise DownloadSizeLimitExceededError(
                "O arquivo excede o tamanho máximo "
                "permitido para download."
            )

        if self.progress_callback:
            self.progress_callback(data)

    def get_info(self, url: str) -> dict:
        """
        Obtém informações da mídia sem realizar
        o download.
        """

        url = validate_instagram_url(url)

        options = {
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "skip_download": True,
        }

        try:

            with yt_dlp.YoutubeDL(
                options
            ) as ydl:

                info = ydl.extract_info(
                    url,
                    download=False,
                )

                return {
                    "title": info.get(
                        "title"
                    ),
                    "uploader": info.get(
                        "uploader"
                    ),
                    "duration": info.get(
                        "duration"
                    ),
                    "thumbnail": info.get(
                        "thumbnail"
                    ),
                    "webpage_url": info.get(
                        "webpage_url"
                    ),
                    "id": info.get(
                        "id"
                    ),
                }

        except yt_dlp.utils.DownloadError as error:

            logger.error(
                "Erro ao obter informações: %s",
                error,
            )

            raise DownloadFailedError(
                "Não foi possível obter as informações do vídeo."
            ) from error

    def download(
        self,
        url: str,
    ) -> dict:
        """
        Realiza o download da mídia.

        O nome do arquivo utiliza o título da mídia
        juntamente com o ID fornecido pelo yt-dlp,
        evitando colisões entre conteúdos diferentes
        que possuam o mesmo título.
        """

        url = validate_instagram_url(url)

        logger.info(
            "Iniciando download..."
        )

        # Limpa o estado de uma operação anterior.
        self.cancel_requested = False
        self._current_partial_file = None

        options = {
            # O ID da mídia é utilizado para evitar
            # colisões entre arquivos com o mesmo título.
            #
            # Exemplo:
            # Gameplay [ABC123].mp4
            # Gameplay [XYZ789].mp4
            "outtmpl": str(
                self.download_dir
                / "%(title).150s [%(id)s].%(ext)s"
            ),

            "format": "best",

            "noplaylist": True,

            "quiet": True,

            "no_warnings": True,

            # Limite máximo de tamanho.
            "max_filesize": MAX_FILE_SIZE_BYTES,

            "progress_hooks": [
                self._progress_hook
            ],
        }

        try:

            with yt_dlp.YoutubeDL(
                options
            ) as ydl:

                info = ydl.extract_info(
                    url,
                    download=False,
                )

                declared_size = self._get_declared_size(
                    info
                )

                if (
                    declared_size is not None
                    and declared_size > MAX_FILE_SIZE_BYTES
                ):
                    logger.warning(
                        "Download impedido: tamanho informado "
                        "%d bytes excede o limite de %d bytes.",
                        declared_size,
                        MAX_FILE_SIZE_BYTES,
                    )

                    raise DownloadSizeLimitExceededError(
                        "O arquivo excede o tamanho máximo "
                        "permitido para download."
                    )

                ydl.download(
                    [url]
                )

                filename = ydl.prepare_filename(
                    info
                )

                filepath = Path(
                    filename
                )

                if not filepath.exists():

                    raise DownloadFailedError(
                        "O download terminou, "
                        "mas o arquivo não foi encontrado."
                    )

                # Verificação final do tamanho.
                try:

                    file_size = filepath.stat().st_size

                except OSError as error:

                    logger.error(
                        "Não foi possível verificar "
                        "o tamanho do arquivo: %s",
                        error,
                    )

                    raise DownloadFailedError(
                        "Não foi possível verificar "
                        "o arquivo baixado."
                    ) from error

                if file_size > MAX_FILE_SIZE_BYTES:

                    logger.warning(
                        "Arquivo excedeu o limite máximo: "
                        "%s bytes.",
                        file_size,
                    )

                    try:

                        filepath.unlink()

                    except OSError as error:

                        logger.warning(
                            "Não foi possível remover "
                            "o arquivo excedente %s: %s",
                            filepath,
                            error,
                        )

                    raise DownloadSizeLimitExceededError(
                        "O arquivo baixado excede "
                        "o tamanho máximo permitido."
                    )

                logger.info(
                    "Download concluído: %s",
                    filepath,
                )

                return {
                    "success": True,
                    "title": info.get(
                        "title"
                    ),
                    "duration": info.get(
                        "duration"
                    ),
                    "extension": info.get(
                        "ext"
                    ),
                    "filename": filepath.name,
                    "filepath": str(
                        filepath
                    ),
                    "url": url,
                    "id": info.get(
                        "id"
                    ),
                }

        except DownloadCancelledError:

            logger.info(
                "Download cancelado."
            )

            self._cleanup_partial_file()

            raise

        except DownloadSizeLimitExceededError as error:

            logger.warning(
                "Download interrompido por exceder o limite: %s",
                error,
            )

            self._cleanup_partial_file()

            raise

        except DownloadFailedError as error:

            logger.warning(
                "Download interrompido: %s",
                error,
            )

            self._cleanup_partial_file()

            raise

        except yt_dlp.utils.DownloadError as error:

            logger.error(
                "Erro no download: %s",
                error,
            )

            self._cleanup_partial_file()

            if self._is_size_limit_error(error):
                raise DownloadSizeLimitExceededError(
                    "O arquivo excede o tamanho máximo "
                    "permitido para download."
                ) from error

            raise DownloadFailedError(
                "Não foi possível realizar o download."
            ) from error

    @staticmethod
    def _get_declared_size(info: Any) -> int | None:

        candidates = [
            info.get("filesize"),
            info.get("filesize_approx"),
        ]

        for format_info in info.get(
            "requested_formats",
            [],
        ):
            candidates.extend(
                [
                    format_info.get("filesize"),
                    format_info.get("filesize_approx"),
                ]
            )

        format_id = info.get("format_id")

        for format_info in info.get(
            "formats",
            [],
        ):
            if format_id is None or format_info.get(
                "format_id"
            ) == format_id:
                candidates.extend(
                    [
                        format_info.get("filesize"),
                        format_info.get("filesize_approx"),
                    ]
                )

                if format_id is not None:
                    break

        for size in candidates:
            if isinstance(size, int) and size >= 0:
                return size

        return None

    @staticmethod
    def _is_size_limit_error(error: Exception) -> bool:

        message = str(error).lower()

        return (
            "max-filesize" in message
            or "maximum file size" in message
            or "file size is larger" in message
        )

    def _cleanup_partial_file(self):
        """
        Remove somente o arquivo parcial associado
        ao download atual.

        Não percorre o diretório inteiro procurando
        por arquivos .part.
        """

        partial_file = (
            self._current_partial_file
        )

        if partial_file is None:

            logger.info(
                "Nenhum arquivo parcial associado "
                "ao download atual."
            )

            return

        try:

            if not partial_file.exists():

                logger.info(
                    "Arquivo parcial já não existe: %s",
                    partial_file,
                )

                return

            if not partial_file.is_file():

                logger.warning(
                    "Caminho parcial não é um arquivo regular: %s",
                    partial_file,
                )

                return

            partial_file.unlink()

            logger.info(
                "Arquivo parcial removido: %s",
                partial_file,
            )

        except OSError as error:

            logger.warning(
                "Não foi possível remover "
                "arquivo parcial %s: %s",
                partial_file,
                error,
            )

        finally:

            self._current_partial_file = None