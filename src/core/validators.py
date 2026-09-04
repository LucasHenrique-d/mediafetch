from urllib.parse import urlparse

from .exceptions import InvalidUrlError


ALLOWED_DOMAINS = {
    "instagram.com",
    "www.instagram.com",
}


def validate_instagram_url(url: str) -> str:
    url = url.strip()

    if not url:
        raise InvalidUrlError("A URL não pode estar vazia.")

    parsed = urlparse(url)

    if parsed.scheme not in {"http", "https"}:
        raise InvalidUrlError(
            "A URL precisa começar com http:// ou https://."
        )

    hostname = parsed.hostname

    if not hostname:
        raise InvalidUrlError("URL inválida.")

    hostname = hostname.lower()

    if hostname not in ALLOWED_DOMAINS:
        raise InvalidUrlError(
            "A URL precisa pertencer ao Instagram."
        )

    return url