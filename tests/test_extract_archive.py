"""Tests de l'archivage des données brutes."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from zipfile import ZipFile

from patrimoine_orne.extract.archive import create_sample_archive, verify_sample_archive
from patrimoine_orne.extract.metadata import (
    create_retrieval_metadata,
    metadata_sidecar_path,
    write_metadata_sidecar,
)


class SampleArchiveTests(TestCase):
    def setUp(self) -> None:
        self.temp_directory = TemporaryDirectory()
        self.addCleanup(self.temp_directory.cleanup)
        self.root = Path(self.temp_directory.name)
        raw_directory = self.root / "data/raw/source/2026/2026-07-20"
        raw_directory.mkdir(parents=True)
        self.data_file = raw_directory / "source__resource__orne__20260720T000000Z.json"
        self.data_file.write_text('{"id": 1}\n', encoding="utf-8")
        metadata = create_retrieval_metadata(
            data_file=self.data_file,
            source_id="source",
            resource_id="resource",
            scope="orne",
            retrieved_at=datetime(2026, 7, 20, tzinfo=timezone.utc),
            source_page_url="https://example.test/source",
            request_url="https://example.test/data",
            final_url="https://example.test/data",
            http_status=200,
            content_type="application/json; charset=utf-8",
            format="json",
            license="test",
            extractor="test",
            extractor_version="1.0",
        )
        self.metadata_file = write_metadata_sidecar(self.data_file, metadata)
        manifest = {
            "schema_version": "1.0",
            "generated_at": "2026-07-20T00:00:00Z",
            "sources": {
                "source": [
                    {
                        "data_file": self.data_file.relative_to(self.root).as_posix(),
                        "metadata_file": self.metadata_file.relative_to(self.root).as_posix(),
                        "sha256": metadata["sha256"],
                    }
                ]
            },
        }
        self.manifest_path = self.root / "reports/manifest.json"
        self.manifest_path.parent.mkdir(parents=True)
        self.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    def test_archive_is_created_and_verified(self) -> None:
        archive = self.root / "data/archive/test.zip"
        descriptor = self.root / "reports/archive.json"
        result = create_sample_archive(
            manifest_path=self.manifest_path.relative_to(self.root),
            archive_path=archive,
            descriptor_path=descriptor,
            project_root=self.root,
        )
        verify_sample_archive(archive, descriptor)
        self.assertEqual(result["raw_file_count"], 1)
        self.assertEqual(result["metadata_file_count"], 1)
        self.assertEqual(result["zip_entry_count"], 4)
        self.assertTrue(archive.with_suffix(".zip.sha256").is_file())

        with ZipFile(archive) as zipped:
            names = zipped.namelist()
        self.assertIn("ARCHIVE_MANIFEST.json", names)
        self.assertIn(self.data_file.relative_to(self.root).as_posix(), names)

    def test_archive_is_not_overwritten(self) -> None:
        archive = self.root / "data/archive/test.zip"
        descriptor = self.root / "reports/archive.json"
        arguments = {
            "manifest_path": self.manifest_path.relative_to(self.root),
            "archive_path": archive,
            "descriptor_path": descriptor,
            "project_root": self.root,
        }
        create_sample_archive(**arguments)
        with self.assertRaises(FileExistsError):
            create_sample_archive(**arguments)

