"""Tests de la validation finale du pilote."""

from copy import deepcopy
from pathlib import Path
from unittest import TestCase

from patrimoine_orne.validate.pilot_phase5 import (
    build_validation_report,
    build_v1_corpus,
    load_json,
    load_yaml,
)


ROOT = Path(__file__).parents[1]


class PilotPhase5ValidationTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus = load_json(ROOT / "data" / "interim" / "phase5_pilot_enriched.json")
        cls.reviews = load_yaml(ROOT / "config" / "validation_pilote.yml")
        cls.report = build_validation_report(cls.corpus, cls.reviews)

    def test_manual_review_covers_all_sites(self) -> None:
        self.assertEqual(cls_count := self.report["counts"]["fiches_controlees_manuellement"], 30)
        self.assertEqual(cls_count, self.report["counts"]["sites"])

    def test_important_information_has_provenance(self) -> None:
        counts = self.report["counts"]
        self.assertEqual(counts["sites_avec_notice_principale"], 30)
        self.assertEqual(counts["sites_avec_source_commune_actuelle"], 30)
        self.assertEqual(counts["activites_avec_source"], 47)
        self.assertEqual(counts["situations_actuelles_renseignees_avec_source"], 4)
        self.assertEqual(counts["protections_avec_source"], 6)
        self.assertEqual(counts["objets_avec_source"], 31)
        self.assertTrue(self.report["corpus_checks_passed"], self.report["errors"])

    def test_phase_is_complete_without_optional_double_review(self) -> None:
        self.assertTrue(self.report["phase5_complete"])
        self.assertEqual(self.report["blocking_items"], [])
        self.assertEqual(len(self.report["accepted_limitations"]), 2)
        v1 = build_v1_corpus(self.corpus, self.report)
        self.assertEqual(v1["status"], "phase5_validee")
        self.assertEqual(
            v1["validation"]["double_classement_humain"], "reporte_hors_phase5"
        )

    def test_missing_activity_source_is_detected(self) -> None:
        corpus = deepcopy(self.corpus)
        corpus["sites"][0]["activites"][0]["source_id"] = None
        report = build_validation_report(corpus, self.reviews)
        self.assertFalse(report["corpus_checks_passed"])
        self.assertTrue(any("activité" in error for error in report["errors"]))
