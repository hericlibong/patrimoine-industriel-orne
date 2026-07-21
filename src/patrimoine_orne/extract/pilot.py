"""Extraction des notices POP nécessaires à l'enrichissement du pilote."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .http import RetrievalResult, RetrievalSpec, retrieve
from .samples import POP_BASE, validate_pop_notice


EXTRACTOR_VERSION = "0.1.0"


def load_references(sample_path: Path) -> list[str]:
    sample = yaml.safe_load(sample_path.read_text(encoding="utf-8"))
    references = [str(site["ia_reference"]) for site in sample["sites"]]
    if len(references) != len(set(references)):
        raise ValueError("l'échantillon contient des références IA dupliquées")
    return references


def build_specs(references: list[str]) -> list[RetrievalSpec]:
    return [
        RetrievalSpec(
            source_id="pop_merimee",
            resource_id=reference,
            scope="orne_pilote_phase5",
            source_page_url="https://pop.culture.gouv.fr/donnees-ouvertes",
            request_url=f"{POP_BASE}/{reference}",
            format="html",
            license="Licence Ouverte 2.0 sauf mention contraire ; © Région Normandie",
            notes=(
                "Notice de l'Inventaire général diffusée dans la base Mérimée de POP.",
                "Extraction du corpus pilote de la phase 5.",
            ),
            validator=validate_pop_notice(reference),
        )
        for reference in references
    ]


def current_git_commit() -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def result_manifest(result: RetrievalResult) -> dict[str, Any]:
    return {
        "data_file": _relative(result.data_file),
        "metadata_file": _relative(result.metadata_file),
        "file_size_bytes": result.metadata["file_size_bytes"],
        "sha256": result.metadata["sha256"],
        "observations": result.observations,
    }


def extract_pilot_notices(
    *,
    sample_path: Path = Path("config/echantillon_pilote.yml"),
    raw_root: Path = Path("data/raw"),
    manifest_path: Path = Path("reports/audits/phase5_pop_manifest.json"),
    retrieved_at: datetime | None = None,
) -> dict[str, Any]:
    timestamp = retrieved_at or datetime.now(timezone.utc).replace(microsecond=0)
    references = load_references(sample_path)
    results = [
        retrieve(
            spec,
            retrieved_at=timestamp,
            raw_root=raw_root,
            extractor="patrimoine_orne.extract.pilot",
            extractor_version=EXTRACTOR_VERSION,
            git_commit=current_git_commit(),
        )
        for spec in build_specs(references)
    ]
    manifest = {
        "schema_version": "1.0",
        "generated_at": timestamp.isoformat().replace("+00:00", "Z"),
        "sample_file": sample_path.as_posix(),
        "reference_count": len(references),
        "sources": {"pop_merimee": [result_manifest(result) for result in results]},
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", type=Path, default=Path("config/echantillon_pilote.yml"))
    parser.add_argument("--raw-root", type=Path, default=Path("data/raw"))
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("reports/audits/phase5_pop_manifest.json"),
    )
    args = parser.parse_args()
    manifest = extract_pilot_notices(
        sample_path=args.sample,
        raw_root=args.raw_root,
        manifest_path=args.manifest,
    )
    print(json.dumps({"pop_merimee": manifest["reference_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
