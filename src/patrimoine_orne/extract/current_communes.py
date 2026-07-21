"""Archive le référentiel officiel des communes actuelles de l'Orne."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from .http import RetrievalSpec, retrieve
from .pilot import EXTRACTOR_VERSION, current_git_commit, result_manifest


API_URL = "https://geo.api.gouv.fr/communes"
EXPECTED_MERGED_COMMUNES = {
    "61007": "Athis-Val de Rouvre",
    "61153": "Écouché-les-Vallées",
    "61194": "Monts-sur-Orne",
    "61230": "Longny les Villages",
    "61339": "Putanges-le-Lac",
    "61474": "Gouffern en Auge",
}


def validate_current_communes(path: Path) -> dict[str, Any]:
    records = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(records, list) or len(records) < 300:
        raise ValueError("référentiel communal de l'Orne incomplet")
    by_code = {str(record["code"]): str(record["nom"]) for record in records}
    if any(record.get("codeDepartement") != "61" for record in records):
        raise ValueError("le référentiel contient une commune hors de l'Orne")
    mismatches = {
        code: {"attendu": name, "recu": by_code.get(code)}
        for code, name in EXPECTED_MERGED_COMMUNES.items()
        if by_code.get(code) != name
    }
    if mismatches:
        raise ValueError(f"communes nouvelles inattendues : {mismatches}")
    return {
        "result_count": len(records),
        "department": "61",
        "merged_communes_verified": EXPECTED_MERGED_COMMUNES,
    }


def build_spec() -> RetrievalSpec:
    query = {
        "codeDepartement": "61",
        "fields": "nom,code,codeDepartement",
        "format": "json",
    }
    return RetrievalSpec(
        source_id="api_geo",
        resource_id="communes_actuelles_orne",
        scope="orne_phase5",
        source_page_url="https://geo.api.gouv.fr/decoupage-administratif/communes",
        request_url=f"{API_URL}?{urlencode(query)}",
        format="json",
        license="Licence Ouverte 2.0",
        query=query,
        notes=("Référentiel des communes actuelles utilisé pour les fusions de communes.",),
        validator=validate_current_communes,
    )


def extract_current_communes(
    *,
    raw_root: Path = Path("data/raw"),
    manifest_path: Path = Path("reports/audits/phase5_communes_manifest.json"),
    retrieved_at: datetime | None = None,
) -> dict[str, Any]:
    timestamp = retrieved_at or datetime.now(timezone.utc).replace(microsecond=0)
    result = retrieve(
        build_spec(),
        retrieved_at=timestamp,
        raw_root=raw_root,
        extractor="patrimoine_orne.extract.current_communes",
        extractor_version=EXTRACTOR_VERSION,
        git_commit=current_git_commit(),
    )
    manifest = {
        "schema_version": "1.0",
        "generated_at": timestamp.isoformat().replace("+00:00", "Z"),
        "sources": {"api_geo": [result_manifest(result)]},
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-root", type=Path, default=Path("data/raw"))
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("reports/audits/phase5_communes_manifest.json"),
    )
    args = parser.parse_args()
    manifest = extract_current_communes(raw_root=args.raw_root, manifest_path=args.manifest)
    observations = manifest["sources"]["api_geo"][0]["observations"]
    print(json.dumps(observations, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
