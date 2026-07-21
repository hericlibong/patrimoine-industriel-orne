"""Tests des classifications sectorielles du premier bloc de la phase 4."""

from pathlib import Path
from unittest import TestCase

from patrimoine_orne.classify.sectors import (
    classify_denomination,
    classify_energy_terms,
    classify_pop_records,
    load_classifications,
    validate_classifications,
)


CONFIG_PATH = Path(__file__).parents[1] / "config" / "classifications.yml"


class SectorClassificationTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_classifications(CONFIG_PATH)

    def test_configuration_is_consistent(self) -> None:
        self.assertEqual(validate_classifications(self.config), [])
        self.assertNotIn("activite_mixte", self.config["secteurs"])

    def test_activity_and_installation_are_distinct(self) -> None:
        mill = classify_denomination("moulin à farine", self.config)
        flour_mill = classify_denomination("minoterie", self.config)
        self.assertEqual(mill["activite_code"], "mouture_cereales")
        self.assertEqual(flour_mill["activite_code"], "mouture_cereales")
        self.assertEqual(mill["installation_code"], "moulin")
        self.assertEqual(flour_mill["installation_code"], "minoterie")

    def test_unknown_label_is_not_silently_guessed(self) -> None:
        self.assertIsNone(classify_denomination("atelier industriel ambigu", self.config))

    def test_energy_role_and_equipment_are_separated(self) -> None:
        result = classify_energy_terms(
            [
                "énergie hydraulique",
                "produite sur place",
                "roue hydraulique verticale",
            ],
            self.config,
        )
        self.assertEqual(result["energies"], ["hydraulique"])
        self.assertEqual(result["roles"], ["produite_sur_place"])
        self.assertEqual(result["hors_energie"], ["equipement_technique"])
        self.assertEqual(result["inconnus"], [])

    def test_phase2_sample_denominations_are_covered(self) -> None:
        records = [
            {
                "REF": "IA00060965",
                "DENO": ["affinerie", "moulin à blé"],
                "ENER": ["énergie hydraulique", "produite sur place"],
            },
            {"REF": "IA00061095", "DENO": ["briqueterie"], "ENER": []},
            {
                "REF": "IA00060938",
                "DENO": ["centrale hydroélectrique"],
                "ENER": ["énergie hydraulique", "produite sur place"],
            },
            {"REF": "IA00061190", "DENO": ["filature"], "ENER": []},
            {"REF": "IA00061038", "DENO": ["filature"], "ENER": []},
            {"REF": "IA00061008", "DENO": ["usine d'extraction"], "ENER": []},
            {
                "REF": "IA00061113",
                "DENO": ["laminoir", "usine de quincaillerie"],
                "ENER": [],
            },
            {"REF": "IA00061091", "DENO": ["moulin à farine"], "ENER": []},
            {
                "REF": "IA00061082",
                "DENO": ["moulin à farine", "moulin à huile"],
                "ENER": [],
            },
            {"REF": "IA00061147", "DENO": ["cartonnerie"], "ENER": []},
        ]
        report = classify_pop_records(records, self.config)
        self.assertEqual(report["denominations"]["total"], 13)
        self.assertEqual(report["denominations"]["coverage_percent"], 100.0)
        self.assertEqual(report["denominations"]["unknown_terms"], {})
        self.assertEqual(report["multi_sector_references"], ["IA00060965"])
        self.assertEqual(
            report["multi_activity_references"],
            ["IA00060965", "IA00061082", "IA00061113"],
        )
