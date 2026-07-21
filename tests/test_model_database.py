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
PHASE3_CASES_PATH = Path(__file__).parent / "fixtures" / "phase3_validation_cases.sql"


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
            self.connection.execute(
                "SELECT schema_version FROM schema_metadata"
            ).fetchone()[0],
            "1.1.0",
        )
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
                "propositions_rapprochement",
                "objets_techniques",
                "geometries",
                "exploitants",
                "exploitations",
                "relations_sites",
                "identifiants_externes",
                "etats_actuels_courants",
                "usages_actuels",
                "usages_actuels_courants",
            }.issubset(names)
        )

    def test_current_state_is_assembled_dimension_by_dimension(self) -> None:
        row = self.connection.execute(
            """
            SELECT conservation_code, usages_actuels_codes, accessibilite_code,
                   conservation_verifiee_le, accessibilite_verifiee_le
            FROM etats_actuels_courants
            WHERE site_id = '10000000-0000-4000-8000-000000000001'
            """
        ).fetchone()
        self.assertEqual(
            row[:3],
            ("partiellement_conserve", ["logement"], "prive_non_visible"),
        )
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

    def test_match_proposal_uses_canonical_pair_order(self) -> None:
        self.connection.execute(
            """
            INSERT INTO propositions_rapprochement (
                site_a_id, site_b_id, methode_code, statut_decision_code,
                fiabilite_code
            ) VALUES (
                '10000000-0000-4000-8000-000000000002',
                '10000000-0000-4000-8000-000000000001',
                'test', 'a_verifier', 'faible'
            )
            """
        )
        self.assertIn("RAPPROCHEMENT_NON_CANONIQUE", self.issue_codes())

    def test_confirmed_match_requires_effective_fusion(self) -> None:
        self.connection.execute(
            """
            INSERT INTO propositions_rapprochement (
                site_a_id, site_b_id, methode_code, statut_decision_code,
                site_canonique_id, date_decision, fiabilite_code
            ) VALUES (
                '10000000-0000-4000-8000-000000000001',
                '10000000-0000-4000-8000-000000000002',
                'test', 'confirme_meme_site',
                '10000000-0000-4000-8000-000000000001',
                DATE '2026-07-20', 'forte'
            )
            """
        )
        self.assertIn("RAPPROCHEMENT_CONFIRME_SANS_FUSION", self.issue_codes())

    def test_current_observation_must_contain_information(self) -> None:
        self.connection.execute(
            """
            INSERT INTO etats_actuels (
                site_id, date_verification, methode_verification_code,
                fiabilite_code, version_numero
            ) VALUES (
                '10000000-0000-4000-8000-000000000002', DATE '2026-07-21',
                'test', 'forte', 2
            )
            """
        )
        self.assertIn("ETAT_ACTUEL_SANS_INFORMATION", self.issue_codes())

    def test_only_one_current_use_can_be_principal(self) -> None:
        self.connection.execute(
            """
            INSERT INTO usages_actuels (
                etat_actuel_id, usage_code, principal
            ) VALUES (
                '30000000-0000-4000-8000-000000000001',
                'commerce_services', true
            )
            """
        )
        self.assertIn("PLUSIEURS_USAGES_PRINCIPAUX", self.issue_codes())

    def test_unknown_use_cannot_coexist_with_known_use(self) -> None:
        self.connection.execute(
            """
            INSERT INTO usages_actuels (
                etat_actuel_id, usage_code, principal
            ) VALUES (
                '30000000-0000-4000-8000-000000000001', 'inconnu', false
            )
            """
        )
        self.assertIn("USAGES_ACTUELS_INCOMPATIBLES", self.issue_codes())

    def test_one_notice_can_contain_several_protection_measures(self) -> None:
        self.connection.execute(
            """
            INSERT INTO protections (
                site_id, type_protection_code, reference_protection,
                portee_code, date_verification
            ) VALUES
                (
                    '10000000-0000-4000-8000-000000000001', 'classe_mh',
                    'PA-TEST-MULTIPLE', 'partielle', DATE '2026-07-21'
                ),
                (
                    '10000000-0000-4000-8000-000000000001', 'inscrit_mh',
                    'PA-TEST-MULTIPLE', 'partielle', DATE '2026-07-21'
                )
            """
        )
        count = self.connection.execute(
            "SELECT count(*) FROM protections WHERE reference_protection = 'PA-TEST-MULTIPLE'"
        ).fetchone()[0]
        self.assertEqual(count, 2)


class Phase3ValidationCasesTests(TestCase):
    def setUp(self) -> None:
        try:
            self.connection = connect_database()
        except RuntimeError as error:
            self.skipTest(str(error))
        self.addCleanup(self.connection.close)
        initialize_database(self.connection)
        execute_sql_file(self.connection, SEED_PATH)
        execute_sql_file(self.connection, PHASE3_CASES_PATH)
        self.assertEqual(validate_database(self.connection), [])

    def test_simple_site(self) -> None:
        site_id = "10000000-0000-4000-8000-000000000004"
        counts = self.connection.execute(
            """
            SELECT
                (SELECT count(*) FROM activites WHERE site_id = ?),
                (SELECT count(*) FROM etats_actuels WHERE site_id = ?),
                (SELECT count(*) FROM geometries
                 WHERE site_id = ? AND geometrie_reference),
                (SELECT count(*) FROM mentions_sources
                 WHERE entite_type_code = 'sites' AND entite_id = ?)
            """,
            [site_id, site_id, site_id, site_id],
        ).fetchone()
        self.assertEqual(counts, (1, 1, 1, 1))

    def test_multi_activity_site(self) -> None:
        activities = self.connection.execute(
            """
            SELECT activite_code, debut_min, fin_max
            FROM activites
            WHERE site_id = '10000000-0000-4000-8000-000000000001'
            ORDER BY debut_min
            """
        ).fetchall()
        self.assertEqual([row[0] for row in activities], ["forge", "moulin_farines"])
        self.assertLess(activities[0][2], activities[1][1])

    def test_reconverted_site(self) -> None:
        activity = self.connection.execute(
            """
            SELECT activite_code, fin_max
            FROM activites
            WHERE site_id = '10000000-0000-4000-8000-000000000005'
            """
        ).fetchone()
        current_state = self.connection.execute(
            """
            SELECT conservation_code, usages_actuels_codes, accessibilite_code
            FROM etats_actuels_courants
            WHERE site_id = '10000000-0000-4000-8000-000000000005'
            """
        ).fetchone()
        self.assertEqual(activity[0], "filature")
        self.assertEqual(str(activity[1]), "1960-12-31")
        self.assertEqual(
            current_state,
            ("conserve", ["culture_musee", "tourisme_visite"], "visitable"),
        )

    def test_disappeared_site_without_fake_geometry(self) -> None:
        result = self.connection.execute(
            """
            SELECT courant.conservation_code, count(geometrie.geometrie_id)
            FROM etats_actuels_courants AS courant
            LEFT JOIN geometries AS geometrie ON geometrie.site_id = courant.site_id
            WHERE courant.site_id = '10000000-0000-4000-8000-000000000003'
            GROUP BY courant.conservation_code
            """
        ).fetchone()
        self.assertEqual(result, ("disparu", 0))

    def test_uncertain_match_remains_two_sites(self) -> None:
        proposal = self.connection.execute(
            """
            SELECT proposition.statut_decision_code,
                   proposition.site_canonique_id,
                   site_a.statut_corpus_code,
                   site_b.statut_corpus_code,
                   site_a.decision_inclusion_code,
                   site_b.decision_inclusion_code
            FROM propositions_rapprochement AS proposition
            JOIN sites AS site_a ON site_a.site_id = proposition.site_a_id
            JOIN sites AS site_b ON site_b.site_id = proposition.site_b_id
            WHERE proposition.proposition_rapprochement_id =
                'a0000000-0000-4000-8000-000000000001'
            """
        ).fetchone()
        self.assertEqual(
            proposal,
            ("a_verifier", None, "candidat", "candidat", "a_verifier", "a_verifier"),
        )
        candidate_count = self.connection.execute(
            """
            SELECT count(*) FROM sites
            WHERE site_id IN (
                '10000000-0000-4000-8000-000000000006',
                '10000000-0000-4000-8000-000000000007'
            )
            """
        ).fetchone()[0]
        self.assertEqual(candidate_count, 2)
