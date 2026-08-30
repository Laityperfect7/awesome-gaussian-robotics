from __future__ import annotations

import unittest

from gaussian_robotics_atlas.urls import (
    arxiv_identity,
    canonical_url,
    doi_identity,
    github_identity,
)


class CanonicalUrlTests(unittest.TestCase):
    def test_normalizes_host_path_query_fragment_and_git_suffix(self) -> None:
        actual = canonical_url(
            " HTTPS://GitHub.com//Example//Atlas.git/?utm_source=newsletter&b=2&a=1#readme "
        )
        self.assertEqual(actual, "https://github.com/Example/Atlas?a=1&b=2")

    def test_removes_default_https_port_and_trailing_slash(self) -> None:
        self.assertEqual(
            canonical_url("https://EXAMPLE.org:443/a/path/"),
            "https://example.org/a/path",
        )

    def test_rejects_non_https_or_relative_urls(self) -> None:
        for value in (
            "http://example.org/a",
            "github.com/example/a",
            "/relative",
            "https://github.com@evil.example/owner/repo",
            "https://example.org/path\\@github.com/owner/repo",
            "https://example.org/a\nb",
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                canonical_url(value)

    def test_extracts_stable_external_identities(self) -> None:
        self.assertEqual(
            github_identity("https://github.com/Example/Atlas/tree/main"),
            "example/atlas",
        )
        self.assertEqual(doi_identity("https://doi.org/10.1000/ABC"), "10.1000/abc")
        self.assertEqual(arxiv_identity("https://arxiv.org/pdf/2501.12345v3.pdf"), "2501.12345")

    def test_non_github_urls_have_no_github_identity(self) -> None:
        self.assertIsNone(github_identity("https://gitlab.com/example/atlas"))
        self.assertIsNone(github_identity(None))


if __name__ == "__main__":
    unittest.main()
