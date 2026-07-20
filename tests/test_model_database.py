"""Tests du schema DuckDB et de ses validations transversales."""

from pathlib import Path
from unittest import TestCase

import duckdb

from patrimoine_orne.model import (
    connect_database,
    initialize_database,
    validate_database,
)
from patrimoine_orne.model.database import execute_sql_file


SEED_PATH = Path(__file__).parent / "fixtures" / "model_seed.sql"


class ModelDatabaseTests(TestCase):
    def setUp(self) -> None:
        try:
            self.connection = connect_database()
        except RuntimeError as error:
            self.skipTest(str(error))
        self.addCleanup(self.connection.close)
        initialize_database(self.connection)
        execute_sql_file(self.connection, SEED_PATH)

    def issue_codes(self) -> set[str]:
        return {issue.code for issue in validate_database(self.connection)}

    def test_seed_respects_all_model_rules(self) -> None:
        self.assertEqual(validate_database(self.connection), [])
        self.assertEqual(
            self.connection.execute("SELECT count(*) FROM sites").fetchone()[0],
            3,
        )

    def test_expected_tables_and_views_exist(self) -> None:
        names = {
            row[0]
            for row in self.connection.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'main'"
            ).fetchall()
        }
        self.assertTrue(
            {
                "sites",
                "activites",
                "etats_actuels",
                "sources",
                "mentions_sources",
                "protections",
                "objets_techniques",
                "geometries",
                "exploitants",
                "exploitations",
                "relations_sites",
                "identifiants_externes",
                "etats_actuels_courants",
            }.issubset(names)
        )

    def test_current_state_is_assembled_dimension_by_dimension(self) -> None:
        row = self.connection.execute(
            """
            SELECT conservation_code, usage_actuel_code, accessibilite_code,
                   conservation_verifiee_le, accessibilite_verifiee_le
            FROM etats_actuels_courants
            WHERE site_id = '10000000-0000-4000-8000-000000000001'
            """
        ).fetchone()
        self.assertEqual(row[:3], ("partiel", "habitation", "prive_non_visitable"))
        self.assertEqual(str(row[3]), "2025-07-20")
        self.assertEqual(str(row[4]), "2026-07-20")

    def test_sql_constraints_reject_structural_errors(self) -> None:
        with self.assertRaises(duckdb.ConstraintException):
            self.connection.execute(
                """
                INSERT INTO relations_sites (
                    site_source_id, site_cible_id, type_relation_code,
                    statut_validation_code, fiabilite_code
                ) VALUES (?, ?, 'depend_de', 'confirmee', 'forte')
                """,
                [
                    "10000000-0000-4000-8000-000000000001",
                    "10000000-0000-4000-8000-000000000001",
                ],
            )
        with self.assertRaises(duckdb.ConstraintException):
            self.connection.execute(
                """
                INSERT INTO protections (
                    site_id, objet_technique_id, type_protection_code,
                    reference_protection, date_verification
                ) VALUES (?, ?, 'inscrit_mh', 'TEST-INVALIDE', DATE '2026-07-20')
                """,
                [
                    "10000000-0000-4000-8000-000000000001",
                    "50000000-0000-4000-8000-000000000001",
                ],
            )
        with self.assertRaises(duckdb.ConstraintException):
            self.connection.execute(
                """
                INSERT INTO activites (
                    site_id, activite_code, debut_min, debut_max, fiabilite_code
                ) VALUES (?, 'test', DATE '1900-12-31', DATE '1900-01-01', 'forte')
                """,
                ["10000000-0000-4000-8000-000000000001"],
            )

    def test_generic_target_must_exist(self) -> None:
        self.connection.execute(
            """
            INSERT INTO mentions_sources (
                source_id, date_consultation, entite_type_code, entite_id,
                statut_valeur_code, nature_information_code, fiabilite_code
            ) VALUES (
                'test_inventaire', current_timestamp, 'sites',
                'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
                'a_verifier', 'sourcee', 'faible'
            )
            """
        )
        self.assertIn("CIBLE_ABSENTE", self.issue_codes())

    def test_mentioned_field_must_exist(self) -> None:
        self.connection.execute(
            """
            INSERT INTO mentions_sources (
                source_id, date_consultation, entite_type_code, entite_id,
                champ_cible, statut_valeur_code, nature_information_code,
                fiabilite_code
            ) VALUES (
                'test_inventaire', current_timestamp, 'sites',
                '10000000-0000-4000-8000-000000000001',
                'champ_inexistant', 'a_verifier', 'sourcee', 'faible'
            )
            """
        )
        self.assertIn("CHAMP_CIBLE_INCONNU", self.issue_codes())

    def test_included_site_requirements_are_validated(self) -> None:
        self.connection.execute(
            """
            INSERT INTO sites (
                site_id, nom_principal, statut_corpus_code,
                decision_inclusion_code, fiabilite_code
            ) VALUES (
                'aaaaaaaa-0000-4aaa-8aaa-aaaaaaaaaaaa', 'Site incomplet',
                'candidat', 'inclus', 'faible'
            )
            """
        )
        codes = self.issue_codes()
        self.assertIn("SITE_INCLUS_SANS_COMMUNE", codes)
        self.assertIn("SITE_INCLUS_SANS_ACTIVITE", codes)
        self.assertIn("SITE_INCLUS_SANS_SOURCE", codes)

    def test_only_one_reference_geometry_per_usage_is_allowed(self) -> None:
        self.connection.execute(
            """
            INSERT INTO geometries (
                site_id, geom, type_geometrie_code, precision_geographique_code,
                methode_localisation_code, geometrie_reference, usage_code,
                fiabilite_code
            ) VALUES (
                '10000000-0000-4000-8000-000000000001',
                ST_Point(450001, 6850001), 'point_site', 'adresse',
                'geocodage', true, 'affichage', 'moyenne'
            )
            """
        )
        self.assertIn("PLUSIEURS_GEOMETRIES_REFERENCE", self.issue_codes())
