"""Archivage vérifiable des données brutes référencées par un manifeste."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from .metadata import sha256_file, verify_data_file

ARCHIVE_SCHEMA_VERSION = "1.0"
INTERNAL_MANIFEST_NAME = "ARCHIVE_MANIFEST.json"


def _project_path(project_root: Path, relative_path: str) -> Path:
    path = (project_root / relative_path).resolve()
    root = project_root.resolve()
    if root not in path.parents and path != root:
        raise ValueError(f"chemin hors du projet : {relative_path}")
    return path


def _zip_info(name: str, timestamp: tuple[int, int, int, int, int, int]) -> ZipInfo:
    info = ZipInfo(name, date_time=timestamp)
    info.compress_type = ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    return info


def _archive_timestamp(manifest: Mapping[str, Any]) -> tuple[int, int, int, int, int, int]:
    generated_at = datetime.fromisoformat(manifest["generated_at"].replace("Z", "+00:00"))
    return (
        generated_at.year,
        generated_at.month,
        generated_at.day,
        generated_at.hour,
        generated_at.minute,
        generated_at.second,
    )


def build_archive_inventory(
    manifest: Mapping[str, Any],
    *,
    project_root: Path,
) -> list[dict[str, Any]]:
    """Vérifie et décrit les couples fichier brut/métadonnées du manifeste."""
    entries = []
    archive_names: set[str] = set()
    for source, rows in manifest["sources"].items():
        for row in rows:
            data_file = _project_path(project_root, row["data_file"])
            metadata_file = _project_path(project_root, row["metadata_file"])
            metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
            verify_data_file(data_file, metadata)
            if sha256_file(data_file) != row["sha256"]:
                raise ValueError(f"hash du manifeste différent : {row['data_file']}")

            data_name = Path(row["data_file"]).as_posix()
            metadata_name = Path(row["metadata_file"]).as_posix()
            for name in (data_name, metadata_name):
                if name in archive_names:
                    raise ValueError(f"entrée d'archive dupliquée : {name}")
                archive_names.add(name)

            entries.append(
                {
                    "source_id": source,
                    "data_file": data_name,
                    "data_size_bytes": data_file.stat().st_size,
                    "data_sha256": sha256_file(data_file),
                    "metadata_file": metadata_name,
                    "metadata_size_bytes": metadata_file.stat().st_size,
                    "metadata_sha256": sha256_file(metadata_file),
                }
            )
    return sorted(entries, key=lambda item: (item["source_id"], item["data_file"]))


def create_sample_archive(
    *,
    manifest_path: Path,
    archive_path: Path,
    descriptor_path: Path,
    project_root: Path = Path.cwd(),
) -> dict[str, Any]:
    """Crée une archive déterministe et son descripteur versionnable."""
    if archive_path.exists():
        raise FileExistsError(archive_path)
    manifest_full_path = _project_path(project_root, manifest_path.as_posix())
    manifest = json.loads(manifest_full_path.read_text(encoding="utf-8"))
    inventory = build_archive_inventory(manifest, project_root=project_root)
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = _archive_timestamp(manifest)
    internal_manifest = {
        "schema_version": ARCHIVE_SCHEMA_VERSION,
        "source_manifest": manifest_path.as_posix(),
        "source_manifest_sha256": sha256_file(manifest_full_path),
        "raw_file_count": len(inventory),
        "archived_file_count": len(inventory) * 2,
        "entries": inventory,
    }
    internal_payload = (
        json.dumps(internal_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")

    with ZipFile(archive_path, "x") as archive:
        archive.writestr(_zip_info(INTERNAL_MANIFEST_NAME, timestamp), internal_payload)
        archive.writestr(
            _zip_info(manifest_path.as_posix(), timestamp),
            manifest_full_path.read_bytes(),
        )
        for entry in inventory:
            for field in ("data_file", "metadata_file"):
                name = entry[field]
                archive.writestr(
                    _zip_info(name, timestamp),
                    _project_path(project_root, name).read_bytes(),
                )

    checksum = sha256_file(archive_path)
    checksum_path = archive_path.with_suffix(f"{archive_path.suffix}.sha256")
    checksum_path.write_text(f"{checksum}  {archive_path.name}\n", encoding="ascii")
    descriptor = {
        "schema_version": ARCHIVE_SCHEMA_VERSION,
        "archive_file": archive_path.as_posix(),
        "archive_size_bytes": archive_path.stat().st_size,
        "archive_sha256": checksum,
        "checksum_file": checksum_path.as_posix(),
        "zip_entry_count": len(inventory) * 2 + 2,
        "raw_file_count": len(inventory),
        "metadata_file_count": len(inventory),
        "source_manifest": manifest_path.as_posix(),
        "source_manifest_sha256": sha256_file(manifest_full_path),
        "sources": {
            source: sum(entry["source_id"] == source for entry in inventory)
            for source in sorted({entry["source_id"] for entry in inventory})
        },
    }
    descriptor_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor_path.write_text(
        json.dumps(descriptor, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return descriptor


def verify_sample_archive(
    archive_path: Path,
    descriptor_path: Path,
) -> None:
    """Vérifie l'empreinte, le nombre d'entrées et le manifeste interne."""
    descriptor = json.loads(descriptor_path.read_text(encoding="utf-8"))
    if sha256_file(archive_path) != descriptor["archive_sha256"]:
        raise ValueError("empreinte de l'archive différente du descripteur")
    with ZipFile(archive_path, "r") as archive:
        if len(archive.infolist()) != descriptor["zip_entry_count"]:
            raise ValueError("nombre d'entrées différent du descripteur")
        internal = json.loads(archive.read(INTERNAL_MANIFEST_NAME))
        if internal["raw_file_count"] != descriptor["raw_file_count"]:
            raise ValueError("nombre de fichiers bruts différent du descripteur")
        bad_files = archive.testzip()
        if bad_files:
            raise ValueError(f"entrée ZIP corrompue : {bad_files}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("reports/audits/phase2_extraction_samples_manifest.json"),
    )
    parser.add_argument(
        "--archive",
        type=Path,
        default=Path("data/archive/phase2_extractions_tests_2026-07-20.zip"),
    )
    parser.add_argument(
        "--descriptor",
        type=Path,
        default=Path("reports/audits/phase2_archive_descriptor.json"),
    )
    args = parser.parse_args()
    descriptor = create_sample_archive(
        manifest_path=args.manifest,
        archive_path=args.archive,
        descriptor_path=args.descriptor,
    )
    verify_sample_archive(args.archive, args.descriptor)
    print(json.dumps(descriptor, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
