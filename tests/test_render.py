from __future__ import annotations

import csv
import io
import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from gaussian_robotics_atlas.render import (
    render_all,
    render_catalog_csv,
    render_catalog_json,
    render_site,
    write_outputs,
)

from tests.helpers import resource, taxonomy


class RenderingTests(unittest.TestCase):
    def test_catalog_json_round_trips_without_html_escaping(self) -> None:
        malicious = replace(
            resource(),
            id="script-safe",
            name="Scene <Mapper> & Friends",
            summary=(
                "Maps a robot scene while preserving ordinary Unicode metadata safely for "
                "clients."
            ),
        )
        document = json.loads(render_catalog_json((malicious,)))
        self.assertEqual(document["schema_version"], 1)
        self.assertEqual(document["resources"][0]["name"], "Scene <Mapper> & Friends")

    def test_site_escapes_embedded_json_and_option_labels(self) -> None:
        attack = "</script><script>globalThis.pwned=true</script>"
        malicious = replace(
            resource(),
            id="script-safe",
            name=attack,
            summary=(
                "Safely stores hostile markup in embedded catalog data without executing "
                "scripts."
            ),
        )
        custom_taxonomy = replace(
            taxonomy(),
            categories={
                "slam-localization": 'SLAM <img src=x onerror="alert(1)">'
            },
        )
        site = render_site((malicious,), custom_taxonomy)
        self.assertNotIn(attack, site)
        self.assertIn("\\u003c/script\\u003e", site)
        self.assertIn("SLAM &lt;img src=x onerror=&quot;alert(1)&quot;&gt;", site)

    def test_csv_neutralizes_spreadsheet_formulas(self) -> None:
        malicious = replace(
            resource(),
            id="formula-safe",
            name="=HYPERLINK(\"https://evil.example\",\"click\")",
            summary="+SUM(1,1)",
        )
        row = next(csv.DictReader(io.StringIO(render_catalog_csv((malicious,)))))
        self.assertTrue(row["name"].startswith("'="))
        self.assertTrue(row["summary"].startswith("'+"))

    def test_every_export_is_deterministic_for_input_order(self) -> None:
        second = replace(
            resource(),
            id="another-map",
            name="Another Map",
            code_url="https://github.com/example/another-map",
            doi="10.1000/another-map",
            arxiv="2502.00001",
            featured=False,
        )
        forward = render_all((resource(), second), taxonomy())
        reverse = render_all((second, resource()), taxonomy())
        self.assertEqual(forward, reverse)
        self.assertEqual(
            set(forward),
            {
                Path("CATALOG.md"),
                Path("docs/catalog.json"),
                Path("docs/catalog.csv"),
                Path("docs/stats.json"),
                Path("docs/index.html"),
            },
        )

    def test_write_outputs_supports_drift_check_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outputs = {Path("docs/value.txt"): "first\n"}
            self.assertEqual(write_outputs(outputs, root), (Path("docs/value.txt"),))
            self.assertEqual(write_outputs(outputs, root, check=True), ())
            changed = {Path("docs/value.txt"): "second\n"}
            self.assertEqual(
                write_outputs(changed, root, check=True),
                (Path("docs/value.txt"),),
            )
            self.assertEqual((root / "docs/value.txt").read_text(encoding="utf-8"), "first\n")


if __name__ == "__main__":
    unittest.main()
