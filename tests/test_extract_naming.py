"""Tests des conventions de nommage des extractions."""

from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import TestCase

from patrimoine_orne.extract.naming import (
    build_raw_filename,
    build_raw_path,
    normalise_extension,
    normalise_token,
)


class NamingTests(TestCase):
    def test_normalise_accents_and_spaces(self) -> None:
        self.assertEqual(
            normalise_token("Forges de Varenne", field="resource"),
            "forges_de_varenne",
        )

    def test_build_filename_converts_time_to_utc(self) -> None:
        retrieved_at = datetime(2026, 7, 20, 11, 30, 12, tzinfo=timezone(timedelta(hours=2)))
        filename = build_raw_filename(
            source_id="monuments_historiques_data_culture",
            resource_id="Immeubles protégés",
            scope="Orne",
            retrieved_at=retrieved_at,
            extension=".json",
        )
        self.assertEqual(
            filename,
            "monuments_historiques_data_culture__immeubles_proteges__orne__20260720T093012Z.json",
        )

    def test_build_path_uses_utc_retrieval_date(self) -> None:
        retrieved_at = datetime(2026, 7, 20, 9, 30, 12, tzinfo=timezone.utc)
        path = build_raw_path(
            source_id="casias",
            resource_id="wfs_normandie",
            scope="departement_61",
            retrieved_at=retrieved_at,
            extension="gml",
        )
        self.assertEqual(
            path,
            Path(
                "data/raw/casias/2026/2026-07-20/"
                "casias__wfs_normandie__departement_61__20260720T093012Z.gml"
            ),
        )

    def test_composite_extension_is_allowed(self) -> None:
        self.assertEqual(normalise_extension(".csv.gz"), "csv.gz")

    def test_path_traversal_extension_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            normalise_extension("../csv")

    def test_naive_datetime_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            build_raw_filename(
                source_id="casias",
                resource_id="export",
                scope="orne",
                retrieved_at=datetime(2026, 7, 20),
                extension="csv",
            )
