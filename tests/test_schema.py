from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SchemaSmokeTests(unittest.TestCase):
    def test_schemas_are_valid_json_and_closed_at_the_top_level(self) -> None:
        for name in ("resource.schema.json", "taxonomy.schema.json"):
            with self.subTest(name=name):
                schema = json.loads((ROOT / "schema" / name).read_text(encoding="utf-8"))
                self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertFalse(schema["additionalProperties"])
                self.assertTrue(schema["required"])


if __name__ == "__main__":
    unittest.main()
