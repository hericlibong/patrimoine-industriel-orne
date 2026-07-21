"""Tests de l'extraction du référentiel communal actuel."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from patrimoine_orne.extract.current_communes import (
    EXPECTED_MERGED_COMMUNES,
    build_spec,
    validate_current_communes,
)


class CurrentCommunesExtractionTests(TestCase):
    def test_spec_is_limited_to_orne(self) -> None:
        spec = build_spec()
        self.assertEqual(spec.source_id, "api_geo")
        self.assertEqual(spec.query["codeDepartement"], "61")

    def test_expected_communes_are_required(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "communes.json"
            rows = [
                {"code": f"61{number:03d}", "nom": f"Commune {number}", "codeDepartement": "61"}
                for number in range(301)
            ]
            rows.extend(
                {"code": code, "nom": name, "codeDepartement": "61"}
                for code, name in EXPECTED_MERGED_COMMUNES.items()
            )
            path.write_text(json.dumps(rows), encoding="utf-8")
            result = validate_current_communes(path)
            self.assertGreaterEqual(result["result_count"], 300)

    def test_wrong_merged_commune_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "communes.json"
            rows = [
                {"code": f"61{number:03d}", "nom": f"Commune {number}", "codeDepartement": "61"}
                for number in range(301)
            ]
            path.write_text(json.dumps(rows), encoding="utf-8")
            with self.assertRaises(ValueError):
                validate_current_communes(path)
