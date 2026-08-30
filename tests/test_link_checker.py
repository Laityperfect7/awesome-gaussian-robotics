from __future__ import annotations

import socket
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests import check_links


def _address(value: str) -> tuple[object, ...]:
    return (socket.AF_INET, socket.SOCK_STREAM, 6, "", (value, 443))


class LinkCheckerSafetyTests(unittest.TestCase):
    def tearDown(self) -> None:
        check_links._public_addresses.cache_clear()

    def test_rejects_userinfo_ip_literals_and_private_dns(self) -> None:
        with self.assertRaises(ValueError):
            check_links.validate_public_url("https://github.com@evil.example/repo")
        with self.assertRaises(ValueError):
            check_links.validate_public_url("https://127.0.0.1/metadata")
        with patch.object(check_links.socket, "getaddrinfo", return_value=[_address("10.0.0.8")]):
            with self.assertRaises(ValueError):
                check_links.validate_public_url("https://internal.example/resource")

    def test_allows_a_hostname_only_when_every_address_is_public(self) -> None:
        with patch.object(check_links.socket, "getaddrinfo", return_value=[_address("8.8.8.8")]):
            check_links.validate_public_url("https://public.example/resource")

    def test_revalidates_redirect_targets(self) -> None:
        with (
            patch.object(check_links.socket, "getaddrinfo", return_value=[_address("8.8.8.8")]),
            patch.object(
                check_links,
                "_open_once",
                return_value=(302, {"Location": "https://169.254.169.254/latest/meta-data"}),
            ),
        ):
            ok, status = check_links.check_url("https://public.example/start", timeout=0.1)
        self.assertFalse(ok)
        self.assertIn("unsafe URL", status)

    def test_collect_urls_parses_markdown_and_html_without_script_false_positives(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                "[![badge](https://img.shields.io/badge/x)](LICENSE) "
                "[project](https://example.org/project)\n",
                encoding="utf-8",
            )
            (root / "index.html").write_text(
                '<a href="https://example.org/catalog">Catalog</a>'
                '<script>{"url":"https://example.org/SLAM\\u0026Render"}</script>',
                encoding="utf-8",
            )
            urls = check_links.collect_urls(root, ("README.md", "index.html"))
        self.assertEqual(
            urls,
            (
                "https://example.org/catalog",
                "https://example.org/project",
                "https://img.shields.io/badge/x",
            ),
        )
        self.assertTrue(all("](" not in url and "\\u" not in url for url in urls))


if __name__ == "__main__":
    unittest.main()
