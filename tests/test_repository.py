from __future__ import annotations

import json
import unittest
from pathlib import Path

from gaussian_robotics_atlas.io import load_catalog, load_taxonomy
from gaussian_robotics_atlas.render import render_all
from gaussian_robotics_atlas.validate import validate_catalog

try:
    import jsonschema
except ImportError:  # pragma: no cover - the dependency-backed CI job exercises this path.
    jsonschema = None


ROOT = Path(__file__).resolve().parents[1]


class RepositoryIntegrationTests(unittest.TestCase):
    def test_real_catalog_validates_and_renders(self) -> None:
        taxonomy = load_taxonomy(ROOT / "catalog" / "taxonomy.json")
        resources = load_catalog(ROOT / "catalog")
        self.assertGreaterEqual(len(resources), 50)
        self.assertEqual(validate_catalog(resources, taxonomy), [])
        outputs = render_all(resources, taxonomy)
        self.assertEqual(len(outputs), 5)
        self.assertTrue(all(content.endswith("\n") for content in outputs.values()))

    @unittest.skipUnless(jsonschema, "jsonschema is an optional development dependency")
    def test_every_source_record_matches_published_json_schema(self) -> None:
        assert jsonschema is not None
        resource_schema = json.loads(
            (ROOT / "schema" / "resource.schema.json").read_text(encoding="utf-8")
        )
        taxonomy_schema = json.loads(
            (ROOT / "schema" / "taxonomy.schema.json").read_text(encoding="utf-8")
        )
        jsonschema.Draft202012Validator.check_schema(resource_schema)
        jsonschema.validate(
            json.loads((ROOT / "catalog" / "taxonomy.json").read_text(encoding="utf-8")),
            taxonomy_schema,
        )
        validator = jsonschema.Draft202012Validator(resource_schema)
        errors: list[str] = []
        for path in sorted((ROOT / "catalog").glob("*.json")):
            if path.name == "taxonomy.json":
                continue
            for index, record in enumerate(json.loads(path.read_text(encoding="utf-8"))):
                errors.extend(
                    f"{path.name}[{index}]: {error.message}"
                    for error in validator.iter_errors(record)
                )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
