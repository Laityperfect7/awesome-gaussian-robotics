"""URL identity and safety helpers."""

from __future__ import annotations

import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def canonical_url(url: str) -> str:
    raw = url.strip()
    if "\\" in raw or any(character.isspace() or ord(character) < 32 for character in raw):
        raise ValueError(f"URL contains whitespace, a control character, or a backslash: {url!r}")
    parts = urlsplit(raw)
    if parts.scheme.lower() != "https" or not parts.netloc:
        raise ValueError(f"Only absolute HTTPS URLs are allowed: {url!r}")
    if parts.username is not None or parts.password is not None:
        raise ValueError(f"URL user information is not allowed: {url!r}")
    host = parts.hostname.lower().rstrip(".") if parts.hostname else ""
    if not host:
        raise ValueError(f"URL must contain a hostname: {url!r}")
    port = f":{parts.port}" if parts.port and parts.port != 443 else ""
    path = re.sub(r"/+", "/", parts.path)
    if path != "/":
        path = path.rstrip("/")
    if host == "github.com" and path.endswith(".git"):
        path = path[:-4]
    query = urlencode(
        sorted((key, value) for key, value in parse_qsl(parts.query) if not key.startswith("utm_"))
    )
    return urlunsplit(("https", host + port, path, query, ""))


def github_identity(url: str | None) -> str | None:
    if not url:
        return None
    canonical = canonical_url(url)
    parts = urlsplit(canonical)
    if parts.hostname != "github.com":
        return None
    segments = [segment for segment in parts.path.split("/") if segment]
    if len(segments) < 2:
        return None
    return f"{segments[0].casefold()}/{segments[1].casefold()}"


def doi_identity(doi: str | None) -> str | None:
    if not doi:
        return None
    value = doi.strip().lower()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value)
    return value or None


def arxiv_identity(arxiv: str | None) -> str | None:
    if not arxiv:
        return None
    value = arxiv.strip().lower()
    value = re.sub(r"^https?://arxiv\.org/(?:abs|pdf)/", "", value)
    value = value.removesuffix(".pdf")
    return re.sub(r"v\d+$", "", value)
