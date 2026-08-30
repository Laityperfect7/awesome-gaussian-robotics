"""Check repository links with only the Python standard library.

This script is intentionally separate from the offline unit suite. It is run by a
scheduled workflow because network health is external state, not a deterministic
property of a commit.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import socket
import sys
import time
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\((https://[^)\s]+)")
TRAILING_PUNCTUATION = ".,;:!?)]}"
USER_AGENT = (
    "Gaussian-Robotics-Atlas-Link-Check/1.0 "
    "(+https://github.com/Laityperfect7/awesome-gaussian-robotics)"
)
REDIRECT_CODES = frozenset({301, 302, 303, 307, 308})


class _HtmlLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.urls: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"href", "src"} and value and value.startswith("https://"):
                self.urls.add(value)


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        return None


_OPENER = build_opener(_NoRedirect)


@lru_cache(maxsize=512)
def _public_addresses(host: str) -> tuple[str, ...]:
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise ValueError("IP-literal URLs are not allowed")
    addresses = {
        result[4][0].split("%", 1)[0]
        for result in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    }
    if not addresses:
        raise ValueError("hostname did not resolve")
    if any(not ipaddress.ip_address(address).is_global for address in addresses):
        raise ValueError("hostname resolves to a non-public address")
    return tuple(sorted(addresses))


def validate_public_url(url: str) -> None:
    parts = urlsplit(url)
    if parts.scheme != "https" or not parts.hostname:
        raise ValueError("only absolute HTTPS URLs are allowed")
    if parts.username is not None or parts.password is not None:
        raise ValueError("URL user information is not allowed")
    if "\\" in url or any(character.isspace() or ord(character) < 32 for character in url):
        raise ValueError("URL contains whitespace, a control character, or a backslash")
    if parts.port not in (None, 443):
        raise ValueError("only the default HTTPS port is allowed")
    _public_addresses(parts.hostname.casefold().rstrip("."))


def _open_once(url: str, method: str, timeout: float) -> tuple[int, object]:
    headers = {"User-Agent": USER_AGENT}
    if method == "GET":
        headers["Range"] = "bytes=0-0"
    request = Request(url, headers=headers, method=method)
    try:
        with _OPENER.open(request, timeout=timeout) as response:
            return int(response.status), response.headers
    except HTTPError as exc:
        return exc.code, exc.headers


def _strings(value: object) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)


def _urls_in_file(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    candidates: Iterable[str]
    if path.suffix.casefold() == ".json":
        candidates = (
            value for value in _strings(json.loads(text)) if value.startswith("https://")
        )
    elif path.suffix.casefold() == ".html":
        parser = _HtmlLinks()
        parser.feed(text)
        candidates = parser.urls
    else:
        candidates = (match.group(1) for match in MARKDOWN_LINK_PATTERN.finditer(text))
    return {value.rstrip(TRAILING_PUNCTUATION) for value in candidates}


def collect_urls(root: Path, targets: Iterable[str]) -> tuple[str, ...]:
    urls: set[str] = set()
    for target in targets:
        path = root / target
        paths = sorted(path.rglob("*")) if path.is_dir() else [path]
        for candidate in paths:
            if candidate.is_file() and candidate.suffix.casefold() in {".md", ".json", ".html"}:
                urls.update(_urls_in_file(candidate))
    return tuple(sorted(urls))


def check_url(url: str, timeout: float, attempts: int = 2) -> tuple[bool, str]:
    """Return success and a concise status, retrying transient server failures."""

    for attempt in range(attempts):
        current = url
        try:
            for _redirect in range(6):
                validate_public_url(current)
                status, headers = _open_once(current, "HEAD", timeout)
                if status in REDIRECT_CODES:
                    location = headers.get("Location")  # type: ignore[attr-defined]
                    if not location:
                        return False, f"{status} without Location"
                    current = urljoin(current, str(location))
                    continue
                if status in {403, 405, 429}:
                    status, headers = _open_once(current, "GET", timeout)
                    if status in REDIRECT_CODES:
                        location = headers.get("Location")  # type: ignore[attr-defined]
                        if not location:
                            return False, f"{status} without Location"
                        current = urljoin(current, str(location))
                        continue
                    if status in {403, 429}:
                        return True, f"{status} (reachable but rate-limited)"
                if 200 <= status < 400:
                    return True, str(status)
                if status < 500 or attempt + 1 == attempts:
                    return False, str(status)
                break
            else:
                return False, "too many redirects"
        except (ValueError, socket.gaierror) as exc:
            return False, f"unsafe URL: {exc}"
        except (TimeoutError, URLError) as exc:
            if attempt + 1 == attempts:
                detail = getattr(exc, "reason", exc)
                return False, str(detail)
        time.sleep(0.5 * (attempt + 1))
    return False, "unknown error"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="+", help="Files or directories relative to --root.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--timeout", type=float, default=15.0)
    args = parser.parse_args(argv)

    urls = collect_urls(args.root.resolve(), args.targets)
    if not urls:
        print("No HTTPS links found.")
        return 1
    failures: list[tuple[str, str]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {executor.submit(check_url, url, args.timeout): url for url in urls}
        for future in as_completed(futures):
            url = futures[future]
            ok, status = future.result()
            print(f"{'OK' if ok else 'FAIL':4} {status:>12}  {url}")
            if not ok:
                failures.append((url, status))
    print(f"Checked {len(urls)} unique HTTPS links; {len(failures)} failed.")
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
