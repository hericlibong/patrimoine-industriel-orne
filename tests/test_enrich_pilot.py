"""Tests du bloc d'enrichissement des sites pilotes."""

import uuid
from pathlib import Path
from unittest import TestCase

from patrimoine_orne.classify.sectors import load_classifications, load_pop_manifest_sample
from patrimoine_orne.enrich.pilot import (
    build_enriched_corpus,
    load_mh_records,
    load_palissy_records,
    load_yaml,
)


ROOT = Path(__file__).parents[1]


class PilotEnrichmentTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus, cls.report = build_enriched_corpus(
            load_yaml(ROOT / "config" / "echantillon_pilote.yml"),
            load_yaml(ROOT / "config" / "enrichissement_pilote.yml"),
            load_classifications(ROOT / "config" / "classifications.yml"),
            load_pop_manifest_sample(ROOT / "reports" / "audits" / "phase5_pop_manifest.json"),
            load_palissy_records(ROOT / "reports" / "audits" / "phase5_palissy_manifest.json"),
            load_mh_records(
                ROOT / "reports" / "audits" / "phase2_extraction_samples_manifest.json"
            ),
        )

    def test_all_sites_have_unique_v4_ids(self) -> None:
        identifiers = [uuid.UUID(site["site_id"]) for site in self.corpus["sites"]]
        self.assertEqual(len(identifiers), 30)
        self.assertEqual(len(set(identifiers)), 30)
        self.assertTrue(all(identifier.version == 4 for identifier in identifiers))

    def test_activities_are_classified(self) -> None:
        activities = [
            activity for site in self.corpus["sites"] for activity in site["activites"]
        ]
        self.assertEqual(len(activities), 47)
        self.assertTrue(all(activity["activite_code"] for activity in activities))
        self.assertTrue(all(activity["secteur_code"] for activity in activities))

    def test_reconciliations_and_objects_are_explicit(self) -> None:
        self.assertEqual(self.report["counts"]["protections_mh_confirmees"], 6)
        self.assertEqual(self.report["counts"]["rapprochements_mh_rejetes"], 1)
        self.assertEqual(self.report["counts"]["objets_palissy_recenses"], 31)
        self.assertTrue(
            all(
                item["statut_rapprochement"] == "a_verifier"
                for item in self.corpus["objets_techniques"]
            )
        )

    def test_current_state_does_not_reuse_old_inventory_as_current(self) -> None:
        self.assertEqual(
            self.report["counts"]["sites_avec_source_recente_situation_actuelle"], 4
        )
        self.assertEqual(self.report["counts"]["sites_situation_actuelle_inconnue"], 26)
        self.assertTrue(self.report["checks_passed"], self.report["errors"])
