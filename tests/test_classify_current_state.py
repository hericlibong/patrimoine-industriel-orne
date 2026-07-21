"""Tests des classifications du deuxième bloc de la phase 4."""

from pathlib import Path
from unittest import TestCase

from patrimoine_orne.classify.current_state import (
    classify_conservation_term,
    parse_protection_label,
    period_codes_for_interval,
    validate_current_state_classifications,
)
from patrimoine_orne.classify.sectors import load_classifications


CONFIG_PATH = Path(__file__).parents[1] / "config" / "classifications.yml"


class CurrentStateClassificationTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_classifications(CONFIG_PATH)

    def test_configuration_is_consistent(self) -> None:
        self.assertEqual(validate_current_state_classifications(self.config), [])
        self.assertNotIn("usage_mixte", self.config["usages_actuels"])

    def test_period_boundaries_are_inclusive(self) -> None:
        self.assertEqual(
            period_codes_for_interval(1840, 1860, self.config),
            [
                "revolution_premiere_industrialisation",
                "industrialisation_rail_vapeur",
            ],
        )
        self.assertEqual(
            period_codes_for_interval(2001, 2001, self.config),
            ["periode_contemporaine"],
        )
        self.assertEqual(period_codes_for_interval(None, None, self.config), [])

    def test_desaffecte_is_not_a_conservation_state(self) -> None:
        self.assertEqual(
            classify_conservation_term("établissement industriel désaffecté", self.config),
            {"hors_conservation": "statut_activite"},
        )
        self.assertEqual(
            classify_conservation_term("vestiges", self.config),
            {"conservation_code": "vestiges"},
        )

    def test_protection_type_and_scope_are_separate(self) -> None:
        measures = parse_protection_label(
            "classé MH partiellement ; inscrit MH partiellement ; protection partielle",
            self.config,
        )
        self.assertEqual(
            measures,
            [
                {"type_protection_code": "classe_mh", "portee_code": "partielle"},
                {"type_protection_code": "inscrit_mh", "portee_code": "partielle"},
            ],
        )

    def test_unspecified_protection_scope_remains_unknown(self) -> None:
        self.assertEqual(
            parse_protection_label("1980/01/01 : classé MH", self.config),
            [{"type_protection_code": "classe_mh", "portee_code": "inconnue"}],
        )
