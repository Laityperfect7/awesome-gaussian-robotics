from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from gaussian_robotics_atlas.cli import main

from tests.helpers import resource, taxonomy


class CliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        catalog = self.root / "catalog"
        catalog.mkdir()
        item = resource().to_dict()
        (catalog / "systems.json").write_text(
            json.dumps([item]), encoding="utf-8"
        )
        controlled = taxonomy()
        (catalog / "taxonomy.json").write_text(
            json.dumps(
                {
                    "categories": controlled.categories,
                    "kinds": list(controlled.kinds),
                    "code_statuses": list(controlled.code_statuses),
                    "inputs": list(controlled.inputs),
                    "pose_requirements": list(controlled.pose_requirements),
                    "frameworks": list(controlled.frameworks),
                    "capabilities": list(controlled.capabilities),
                    "tags": list(controlled.tags),
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_cli(self, *arguments: str) -> tuple[int, str, str]:
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(["--root", str(self.root), *arguments])
        return status, stdout.getvalue(), stderr.getvalue()

    def test_validate_build_and_drift_check(self) -> None:
        status, output, _ = self.run_cli("validate")
        self.assertEqual(status, 0)
        self.assertIn("1 resources passed", output)

        self.assertEqual(self.run_cli("build")[0], 0)
        self.assertTrue((self.root / "docs" / "catalog.json").is_file())
        self.assertEqual(self.run_cli("build", "--check")[0], 0)

        (self.root / "CATALOG.md").write_text("drift\n", encoding="utf-8")
        status, output, _ = self.run_cli("build", "--check")
        self.assertEqual(status, 1)
        self.assertIn("CATALOG.md", output)

    def test_search_recommend_and_stats_json(self) -> None:
        for arguments in (
            ("search", "camera", "--code-status", "released", "--json"),
            ("recommend", "slam", "--sensor", "rgb-d", "--json"),
            ("stats", "--format", "json"),
        ):
            status, output, _ = self.run_cli(*arguments)
            self.assertEqual(status, 0)
            self.assertTrue(json.loads(output))

    def test_missing_repository_returns_concise_error(self) -> None:
        empty = Path(self.temporary.name) / "missing"
        empty.mkdir()
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(["--root", str(empty), "validate"])
        self.assertEqual(status, 1)
        self.assertIn("Catalog data not found", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
