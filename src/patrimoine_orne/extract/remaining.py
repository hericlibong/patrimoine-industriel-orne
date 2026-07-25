"""Récupère de manière reprenable les dossiers POP restant à traiter en phase 8."""

from __future__ import annotations

import argparse
import json
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from patrimoine_orne.extract.corpus import build_lot_specs
from patrimoine_orne.extract.http import retrieve
from patrimoine_orne.extract.pilot import current_git_commit, result_manifest


EXTRACTOR_VERSION = "0.1.0"
DEFAULT_ENUMERATION = Path("reports/audits/phase8_enumeration_corpus.json")
DEFAULT_PILOT = Path("config/echantillon_pilote.yml")
DEFAULT_FIRST_GROUP = Path("config/phase8_lot1.yml")
DEFAULT_MANIFEST = Path("reports/audits/phase8_remaining_pop_manifest.json")


def remaining_references(
    enumeration: Mapping[str, Any],
    pilot: Mapping[str, Any],
    first_group: Mapping[str, Any],
) -> list[str]:
    """Calcule les références officielles non encore couvertes par les 80 dossiers."""
    all_references = [str(value) for value in enumeration["references"]]
    pilot_references = [str(row["ia_reference"]) for row in pilot["sites"]]
    first_references = [str(value) for value in first_group["references"]]
    used = set(pilot_references) | set(first_references)
    remaining = [reference for reference in all_references if reference not in used]
    if len(all_references) != 319 or len(set(all_references)) != 319:
        raise ValueError("l'énumération ne contient pas 319 références uniques")
    if set(pilot_references) & set(first_references):
        raise ValueError("les pilotes et les 50 premiers dossiers se recouvrent")
    expected_remaining = 319 - len(set(all_references) & used)
    if len(remaining) != expected_remaining or len(set(remaining)) != expected_remaining:
        raise ValueError(
            f"{len(remaining)} références restantes au lieu de {expected_remaining}"
        )
    return remaining


def load_remaining_references(
    enumeration_path: Path = DEFAULT_ENUMERATION,
    pilot_path: Path = DEFAULT_PILOT,
    first_group_path: Path = DEFAULT_FIRST_GROUP,
) -> list[str]:
    enumeration = json.loads(enumeration_path.read_text(encoding="utf-8"))
    pilot = yaml.safe_load(pilot_path.read_text(encoding="utf-8"))
    first_group = yaml.safe_load(first_group_path.read_text(encoding="utf-8"))
    return remaining_references(enumeration, pilot, first_group)


def _write_manifest(path: Path, manifest: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _new_manifest(references: Sequence[str], timestamp: datetime) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "generated_at": timestamp.isoformat().replace("+00:00", "Z"),
        "status": "in_progress",
        "reference_count": len(references),
        "retrieved_count": 0,
        "remaining_count": len(references),
        "expected_references": list(references),
        "sources": {"pop_merimee": []},
    }


def _load_or_create_manifest(
    path: Path, references: Sequence[str], timestamp: datetime
) -> dict[str, Any]:
    if not path.exists():
        return _new_manifest(references, timestamp)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("expected_references") != list(references):
        raise ValueError("le manifeste existant ne correspond plus aux références attendues")
    completed = [
        str(row["observations"]["reference"])
        for row in manifest["sources"]["pop_merimee"]
    ]
    if len(completed) != len(set(completed)):
        raise ValueError("le manifeste reprenable contient des références dupliquées")
    if not set(completed) <= set(references):
        raise ValueError("le manifeste reprenable contient une référence inattendue")
    return manifest


def extract_remaining(
    references: Sequence[str],
    *,
    raw_root: Path,
    manifest_path: Path,
) -> dict[str, Any]:
    """Télécharge les notices manquantes et enregistre un point de reprise après chacune."""
    timestamp = datetime.now(timezone.utc).replace(microsecond=0)
    manifest = _load_or_create_manifest(manifest_path, references, timestamp)
    rows = manifest["sources"]["pop_merimee"]
    completed = {str(row["observations"]["reference"]) for row in rows}
    if completed == set(references) and manifest.get("status") == "complete":
        return manifest

    specs = [
        replace(
            spec,
            scope="orne_phase8_restant",
            notes=(
                "Notice structurée de l'Inventaire général diffusée par l'API POP.",
                "Phase 8, dossiers restant après le corpus commun de 80.",
            ),
        )
        for spec in build_lot_specs(references, lot=2)
    ]
    for spec in specs:
        if spec.resource_id in completed:
            continue
        result = retrieve(
            spec,
            raw_root=raw_root,
            extractor="patrimoine_orne.extract.remaining",
            extractor_version=EXTRACTOR_VERSION,
            git_commit=current_git_commit(),
        )
        rows.append(result_manifest(result))
        completed.add(spec.resource_id)
        manifest["retrieved_count"] = len(completed)
        manifest["remaining_count"] = len(references) - len(completed)
        _write_manifest(manifest_path, manifest)

    observed = {
        str(row["observations"]["reference"])
        for row in manifest["sources"]["pop_merimee"]
    }
    if observed != set(references):
        raise ValueError("l'extraction s'est terminée avec un corpus incomplet")
    manifest["status"] = "complete"
    manifest["retrieved_count"] = len(observed)
    manifest["remaining_count"] = 0
    manifest["completed_at"] = (
        datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    )
    _write_manifest(manifest_path, manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--enumeration", type=Path, default=DEFAULT_ENUMERATION)
    parser.add_argument("--pilot", type=Path, default=DEFAULT_PILOT)
    parser.add_argument("--first-group", type=Path, default=DEFAULT_FIRST_GROUP)
    parser.add_argument("--raw-root", type=Path, default=Path("data/raw"))
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    references = load_remaining_references(
        args.enumeration, args.pilot, args.first_group
    )
    manifest = extract_remaining(
        references, raw_root=args.raw_root, manifest_path=args.manifest
    )
    print(
        json.dumps(
            {
                "status": manifest["status"],
                "retrieved_count": manifest["retrieved_count"],
                "remaining_count": manifest["remaining_count"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
