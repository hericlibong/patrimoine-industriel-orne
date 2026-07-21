"""Tests de préparation de l'extraction POP du pilote."""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from patrimoine_orne.extract.pilot import build_specs, load_references


class PilotExtractionTests(TestCase):
    def test_references_are_loaded_once(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "sample.yml"
            path.write_text(
                "sites:\n  - ia_reference: IA00000001\n  - ia_reference: IA00000002\n",
                encoding="utf-8",
            )
            self.assertEqual(load_references(path), ["IA00000001", "IA00000002"])

    def test_duplicate_reference_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "sample.yml"
            path.write_text(
                "sites:\n  - ia_reference: IA00000001\n  - ia_reference: IA00000001\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                load_references(path)

    def test_specs_target_pop_notices(self) -> None:
        specs = build_specs(["IA00000001"])
        self.assertEqual(len(specs), 1)
        self.assertEqual(specs[0].source_id, "pop_merimee")
        self.assertEqual(specs[0].scope, "orne_pilote_phase5")
        self.assertTrue(specs[0].request_url.endswith("/IA00000001"))
