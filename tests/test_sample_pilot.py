"""Tests de composition du premier bloc de la phase 5."""

from pathlib import Path
from unittest import TestCase

from patrimoine_orne.sample.pilot import build_composition_report, load_yaml


ROOT = Path(__file__).parents[1]


class PilotSampleTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sample = load_yaml(ROOT / "config" / "echantillon_pilote.yml")
        cls.classifications = load_yaml(ROOT / "config" / "classifications.yml")
        cls.report = build_composition_report(cls.sample, cls.classifications)

    def test_composition_passes_all_quotas(self) -> None:
        self.assertTrue(self.report["checks_passed"], self.report["errors"])
        self.assertEqual(self.report["selected_count"], 30)
        self.assertEqual(self.report["unique_references"], 30)

    def test_each_zone_has_five_sites(self) -> None:
        self.assertEqual(len(self.report["counts"]["zones"]), 6)
        self.assertEqual(set(self.report["counts"]["zones"].values()), {5})

    def test_hard_and_protected_cases_are_present(self) -> None:
        self.assertGreaterEqual(
            self.report["counts"]["localisation_difficulty"]["difficile"], 5
        )
        self.assertGreaterEqual(
            self.report["counts"]["protection_signals"]["protege_mh_identifie"], 5
        )
        self.assertIn("disparu", self.report["counts"]["conservation_source_signals"])
        self.assertIn("vestiges", self.report["counts"]["conservation_source_signals"])

    def test_controlled_vocabularies_are_used(self) -> None:
        self.assertTrue(
            set(self.report["counts"]["sectors"]).issubset(self.classifications["secteurs"])
        )
        self.assertTrue(
            set(self.report["counts"]["periods"]).issubset(
                self.classifications["periodes_historiques"]
            )
        )
        self.assertTrue(
            set(self.report["counts"]["conservation_source_signals"]).issubset(
                self.classifications["conservation"]
            )
        )
