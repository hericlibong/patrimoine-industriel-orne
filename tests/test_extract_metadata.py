"""Tests des métadonnées de récupération."""

import json
from datetime import datetime, timezone
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import TestCase

from patrimoine_orne.extract.metadata import (
    create_retrieval_metadata,
    metadata_sidecar_path,
    validate_metadata,
    verify_data_file,
    write_metadata_sidecar,
)


class MetadataTests(TestCase):
    def setUp(self) -> None:
        self.temp_directory = TemporaryDirectory()
        self.addCleanup(self.temp_directory.cleanup)
        self.data_file = (
            Path(self.temp_directory.name) / "source__resource__orne__20260720T090000Z.csv"
        )
        self.data_file.write_bytes(b"id;nom\n1;Forge\n")

    def make_metadata(self) -> dict[str, object]:
        return create_retrieval_metadata(
            data_file=self.data_file,
            source_id="source",
            resource_id="resource",
            scope="orne",
            retrieved_at=datetime(2026, 7, 20, 9, tzinfo=timezone.utc),
            source_page_url="https://example.test/source",
            request_url="https://example.test/export.csv?departement=61",
            final_url="https://example.test/export.csv?departement=61",
            http_status=200,
            content_type="text/csv",
            format="csv",
            license="Licence Ouverte 2.0",
            extractor="patrimoine_orne.extract.example",
            extractor_version="0.1.0",
            git_commit="abc1234",
            query={"departement": "61"},
        )

    def test_metadata_matches_data_file(self) -> None:
        metadata = self.make_metadata()
        validate_metadata(metadata)
        verify_data_file(self.data_file, metadata)
        self.assertEqual(metadata["file_size_bytes"], self.data_file.stat().st_size)
        self.assertEqual(len(str(metadata["sha256"])), 64)

    def test_sidecar_is_valid_utf8_json(self) -> None:
        metadata = self.make_metadata()
        sidecar = write_metadata_sidecar(self.data_file, metadata)
        self.assertEqual(sidecar, metadata_sidecar_path(self.data_file))
        self.assertEqual(json.loads(sidecar.read_text(encoding="utf-8")), metadata)

    def test_sidecar_is_not_overwritten_by_default(self) -> None:
        metadata = self.make_metadata()
        write_metadata_sidecar(self.data_file, metadata)
        with self.assertRaises(FileExistsError):
            write_metadata_sidecar(self.data_file, metadata)

    def test_modified_data_file_is_detected(self) -> None:
        metadata = self.make_metadata()
        self.data_file.write_bytes(b"contenu modifie")
        with self.assertRaises(ValueError):
            verify_data_file(self.data_file, metadata)

    def test_missing_required_field_is_rejected(self) -> None:
        metadata = self.make_metadata()
        del metadata["source_id"]
        with self.assertRaises(ValueError):
            validate_metadata(metadata)
