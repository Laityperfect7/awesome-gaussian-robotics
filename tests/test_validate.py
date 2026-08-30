from __future__ import annotations

import unittest
from datetime import date

from gaussian_robotics_atlas.model import Severity
from gaussian_robotics_atlas.validate import (
    validate_catalog,
    validate_resource,
    validation_failed,
)

from tests.helpers import resource, taxonomy


TODAY = date(2026, 8, 30)


class ResourceValidationTests(unittest.TestCase):
    def test_valid_evidence_backed_resource_has_no_issues(self) -> None:
        self.assertEqual(validate_resource(resource(), taxonomy(), today=TODAY), [])

    def test_reports_structural_taxonomy_and_evidence_errors(self) -> None:
        item = resource(
            id="Bad ID",
            category="unknown",
            kind="dataset",
            code_status="released",
            code_url=None,
            paper_url=None,
            project_url=None,
            inputs=("thermal",),
            sources=(),
            year=2030,
            verified_date="2026/08/01",
        )
        codes = {issue.code for issue in validate_resource(item, taxonomy(), today=TODAY)}
        self.assertTrue(
            {
                "invalid-id",
                "unknown-category",
                "unknown-taxonomy-value",
                "missing-code-url",
                "missing-primary-link",
                "missing-evidence",
                "invalid-year",
                "invalid-verified-date",
            }.issubset(codes)
        )

    def test_rejects_duplicate_array_values_and_empty_capabilities(self) -> None:
        item = resource(
            inputs=("rgb-d", "rgb-d"),
            capabilities=(),
            sources=("https://example.org/evidence", "https://example.org/evidence"),
        )
        codes = [issue.code for issue in validate_resource(item, taxonomy(), today=TODAY)]
        self.assertEqual(codes.count("duplicate-field-value"), 2)
        self.assertIn("missing-capability", codes)

    def test_rejects_unsafe_urls_and_future_verification(self) -> None:
        item = resource(
            paper_url="http://example.org/paper",
            sources=("https://example.org/evidence", "javascript:alert(1)"),
            verified_date="2026-09-01",
        )
        codes = [issue.code for issue in validate_resource(item, taxonomy(), today=TODAY)]
        self.assertEqual(codes.count("unsafe-url"), 2)
        self.assertIn("future-verified-date", codes)

    def test_advisory_warnings_do_not_fail_default_validation(self) -> None:
        item = resource(
            summary="The best system",
            verified_date="2024-01-01",
        )
        issues = validate_resource(item, taxonomy(), today=TODAY)
        self.assertTrue(issues)
        self.assertTrue(all(issue.severity is Severity.WARNING for issue in issues))
        self.assertFalse(validation_failed(issues))
        self.assertTrue(validation_failed(issues, strict=True))


class CatalogValidationTests(unittest.TestCase):
    def test_detects_canonical_duplicates_for_all_stable_identities(self) -> None:
        duplicate = resource(
            id="splat-track-copy",
            name="sPLATtRACK",
            code_url="https://github.com/EXAMPLE/splat-track.git/",
            doi="https://doi.org/10.1000/SPLAT-TRACK",
            arxiv="https://arxiv.org/pdf/2501.12345v2.pdf",
        )
        issues = validate_catalog((resource(), duplicate), taxonomy(), today=TODAY)
        codes = {issue.code for issue in issues}
        self.assertEqual(
            codes.intersection(
                {"duplicate-name", "duplicate-github", "duplicate-doi", "duplicate-arxiv"}
            ),
            {"duplicate-name", "duplicate-github", "duplicate-doi", "duplicate-arxiv"},
        )
        self.assertEqual(sum(issue.code == "duplicate-name" for issue in issues), 2)

    def test_error_sorting_is_stable(self) -> None:
        bad = resource(id="Bad", sources=())
        issues = validate_catalog((bad,), taxonomy(), today=TODAY)
        keys = [(-int(issue.severity), issue.code, issue.resource_id or "") for issue in issues]
        self.assertEqual(keys, sorted(keys))


if __name__ == "__main__":
    unittest.main()
