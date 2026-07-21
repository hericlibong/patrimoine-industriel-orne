"""Tests de l'extraction Palissy du pilote."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from patrimoine_orne.extract.pilot_objects import (
    PALISSY_REFERENCES,
    build_spec,
    validate_palissy_collection,
)


class PilotObjectsExtractionTests(TestCase):
    def test_query_contains_all_collection_references(self) -> None:
        spec = build_spec()
        self.assertEqual(spec.source_id, "pop_palissy")
        self.assertEqual(spec.query["limit"], 100)
        self.assertTrue(all(reference in spec.query["where"] for reference in PALISSY_REFERENCES))

    def test_complete_collection_is_accepted(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "palissy.json"
            path.write_text(
                json.dumps(
                    {
                        "total_count": len(PALISSY_REFERENCES),
                        "results": [
                            {"reference": reference, "reference_a_une_notice_merimee_mh": None}
                            for reference in PALISSY_REFERENCES
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = validate_palissy_collection(path)
            self.assertEqual(result["result_count"], 31)

    def test_incomplete_collection_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "palissy.json"
            path.write_text(
                json.dumps({"total_count": 1, "results": [{"reference": "PM61000916"}]}),
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                validate_palissy_collection(path)
