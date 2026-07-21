"""Tests des règles de qualité du troisième bloc de la phase 4."""

import json
from pathlib import Path
from unittest import TestCase

from patrimoine_orne.classify.current_state import load_mh_sample
from patrimoine_orne.classify.quality import (
    build_final_validation_report,
    build_reproducibility_report,
    canonical_fingerprint,
    classify_geographic_precision,
    classify_reliability,
    decide_generic_value,
    validate_published_classifications,
    validate_quality_classifications,
)
from patrimoine_orne.classify.sectors import load_classifications, load_pop_manifest_sample
from patrimoine_orne.model.validation import (
    ALLOWED_GEOGRAPHIC_PRECISION_CODES,
    ALLOWED_RELIABILITY_CODES,
)


ROOT = Path(__file__).parents[1]
CONFIG_PATH = ROOT / "config" / "classifications.yml"
MANIFEST_PATH = ROOT / "reports" / "audits" / "phase2_extraction_samples_manifest.json"
MH_SAMPLE_PATH = (
    ROOT
    / "data"
    / "raw"
    / "monuments_historiques_data_culture"
    / "2026"
    / "2026-07-20"
    / "monuments_historiques_data_culture__candidats_industriels__orne__20260720T072951Z.json"
)


class QualityClassificationTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_classifications(CONFIG_PATH)

    def test_configuration_is_consistent(self) -> None:
        self.assertEqual(validate_quality_classifications(self.config), [])
        self.assertNotIn("centre_commune", self.config["precision_geographique"])
        self.assertNotIn("non_localise", self.config["precision_geographique"])
        self.assertEqual(set(self.config["fiabilite"]), {"forte", "moyenne", "faible"})
        self.assertEqual(
            set(self.config["precision_geographique"]),
            ALLOWED_GEOGRAPHIC_PRECISION_CODES,
        )
        self.assertEqual(set(self.config["fiabilite"]), ALLOWED_RELIABILITY_CODES)
        self.assertEqual(validate_published_classifications(self.config), [])
        self.assertEqual(str(self.config["version"]), "1.1")
        self.assertEqual(self.config["status"], "phase5_enrichissement")

    def test_precision_does_not_confuse_evidence_and_method(self) -> None:
        self.assertEqual(
            classify_geographic_precision("parcelle", verified=True, config=self.config),
            "parcelle_verifiee",
        )
        self.assertEqual(
            classify_geographic_precision("adresse", verified=False, config=self.config),
            "point_adresse",
        )
        with self.assertRaises(ValueError):
            classify_geographic_precision("adresse", verified=True, config=self.config)

    def test_reliability_grid_is_deterministic(self) -> None:
        strong = classify_reliability(
            direct_evidence=True,
            independent_concordant_sources=1,
            target_unambiguous=True,
            unresolved_contradiction=False,
            interpretation_required=False,
        )
        medium = classify_reliability(
            direct_evidence=False,
            independent_concordant_sources=2,
            target_unambiguous=True,
            unresolved_contradiction=False,
            interpretation_required=True,
        )
        weak = classify_reliability(
            direct_evidence=True,
            independent_concordant_sources=2,
            target_unambiguous=False,
            unresolved_contradiction=False,
            interpretation_required=False,
        )
        self.assertEqual((strong, medium, weak), ("forte", "moyenne", "faible"))

    def test_other_requires_a_documented_positive_value(self) -> None:
        with self.assertRaises(ValueError):
            decide_generic_value(
                applicable=True,
                checked=True,
                documented_unrepresented_value=True,
                source_label="production spéciale",
            )
        result = decide_generic_value(
            applicable=True,
            checked=True,
            documented_unrepresented_value=True,
            source_label="production spéciale",
            justification="aucun code existant ne convient",
            human_validated=True,
        )
        self.assertEqual(result, {"code": "autre", "statut_valeur_code": "renseignee"})

    def test_unknown_requires_an_applicable_checked_question(self) -> None:
        unknown = decide_generic_value(
            applicable=True,
            checked=True,
            documented_unrepresented_value=False,
        )
        missing = decide_generic_value(
            applicable=True,
            checked=False,
            documented_unrepresented_value=False,
        )
        not_applicable = decide_generic_value(
            applicable=False,
            checked=True,
            documented_unrepresented_value=False,
        )
        self.assertEqual(unknown["code"], "inconnu")
        self.assertEqual(missing, {"code": None, "statut_valeur_code": "non_renseignee_source"})
        self.assertEqual(not_applicable, {"code": None, "statut_valeur_code": "non_applicable"})

    def test_canonical_fingerprint_ignores_dictionary_order(self) -> None:
        self.assertEqual(
            canonical_fingerprint({"a": 1, "b": 2}),
            canonical_fingerprint({"b": 2, "a": 1}),
        )

    def test_real_sample_classifications_are_reproducible(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        report = build_reproducibility_report(
            load_pop_manifest_sample(MANIFEST_PATH),
            load_mh_sample(MH_SAMPLE_PATH),
            manifest,
            self.config,
        )
        self.assertTrue(report["all_reproducible"])
        self.assertTrue(all(report["reproducibility_checks"].values()))
        self.assertEqual(report["validation_errors"], {
            "secteurs": [],
            "situation_actuelle": [],
            "qualite": [],
        })

    def test_final_phase4_registry_is_publishable(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        report = build_final_validation_report(
            load_pop_manifest_sample(MANIFEST_PATH),
            load_mh_sample(MH_SAMPLE_PATH),
            manifest,
            self.config,
        )
        self.assertTrue(report["all_valid"])
        self.assertEqual(report["published_version"], "1.1")
        self.assertEqual(report["published_code_count"], 174)
        self.assertEqual(report["validation_errors"], [])
