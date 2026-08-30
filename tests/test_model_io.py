from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from gaussian_robotics_atlas.io import load_catalog, load_taxonomy
from gaussian_robotics_atlas.model import Resource, Taxonomy

from tests.helpers import resource, taxonomy


class ResourceModelTests(unittest.TestCase):
    def test_round_trip_preserves_all_fields(self) -> None:
        expected = resource()
        self.assertEqual(Resource.from_dict(expected.to_dict()), expected)

    def test_rejects_unknown_and_missing_fields(self) -> None:
        raw = resource().to_dict()
        raw["mystery"] = True
        raw.pop("venue")
        expected = r"Unknown fields \['mystery'\].*missing fields \['venue'\]"
        with self.assertRaisesRegex(ValueError, expected):
            Resource.from_dict(raw)

    def test_rejects_coercible_but_schema_invalid_types(self) -> None:
        for field, value in (
            ("featured", "false"),
            ("inputs", {"rgb-d": "not-an-array"}),
            ("year", "2025"),
            ("code_url", 42),
        ):
            raw = resource().to_dict()
            raw[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                Resource.from_dict(raw)

    def test_taxonomy_requires_exact_top_level_fields(self) -> None:
        raw = {
            "categories": {},
            "kinds": [],
            "code_statuses": [],
            "inputs": [],
            "pose_requirements": [],
            "frameworks": [],
            "capabilities": [],
            "tags": [],
            "extra": [],
        }
        with self.assertRaisesRegex(ValueError, "Taxonomy fields must be exactly"):
            Taxonomy.from_dict(raw)


class CatalogIoTests(unittest.TestCase):
    def test_load_catalog_is_deterministic_across_files(self) -> None:
        older = resource(
            id="alpha-map",
            name="Alpha Map",
            year=2024,
            doi="10.1000/alpha",
            arxiv="2401.00001",
            code_url="https://github.com/example/alpha-map",
            sources=("https://github.com/example/alpha-map",),
        )
        semantic = resource(
            id="semantic-splat",
            name="Semantic Splat",
            category="semantic-perception",
            capabilities=("open-vocabulary",),
            doi="10.1000/semantic",
            arxiv="2501.00002",
            code_url="https://github.com/example/semantic-splat",
            sources=("https://github.com/example/semantic-splat",),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "taxonomy.json").write_text(
                json.dumps(
                    {
                        "categories": {},
                        "kinds": [],
                        "code_statuses": [],
                        "inputs": [],
                        "pose_requirements": [],
                        "frameworks": [],
                        "capabilities": [],
                        "tags": [],
                    }
                ),
                encoding="utf-8",
            )
            (root / "z.json").write_text(
                json.dumps([semantic.to_dict()]), encoding="utf-8"
            )
            (root / "a.json").write_text(
                json.dumps([resource().to_dict(), older.to_dict()]), encoding="utf-8"
            )
            loaded = load_catalog(root)
        self.assertEqual(
            [item.id for item in loaded],
            ["semantic-splat", "splat-track", "alpha-map"],
        )

    def test_load_catalog_rejects_wrong_roots_and_empty_directories(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "bad.json").write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "must contain an array"):
                load_catalog(root)
            (root / "bad.json").unlink()
            with self.assertRaisesRegex(ValueError, "No catalog resources found"):
                load_catalog(root)

    def test_load_taxonomy_from_json_object(self) -> None:
        expected = taxonomy()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "taxonomy.json"
            path.write_text(
                json.dumps(
                    {
                        "categories": expected.categories,
                        "kinds": list(expected.kinds),
                        "code_statuses": list(expected.code_statuses),
                        "inputs": list(expected.inputs),
                        "pose_requirements": list(expected.pose_requirements),
                        "frameworks": list(expected.frameworks),
                        "capabilities": list(expected.capabilities),
                        "tags": list(expected.tags),
                    }
                ),
                encoding="utf-8",
            )
            actual = load_taxonomy(path)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
