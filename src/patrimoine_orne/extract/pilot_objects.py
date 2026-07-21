"""Extraction des objets Palissy associés au complexe de Varenne."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from .http import RetrievalSpec, retrieve
from .pilot import EXTRACTOR_VERSION, current_git_commit, result_manifest
from .samples import PALISSY_API


PALISSY_REFERENCES = ("PM61000916",) + tuple(
    f"PM610008{number:02d}" for number in range(13, 43)
)


def validate_palissy_collection(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    results = payload.get("results", [])
    references = sorted(str(record.get("reference")) for record in results)
    expected = sorted(PALISSY_REFERENCES)
    if references != expected:
        missing = sorted(set(expected) - set(references))
        unexpected = sorted(set(references) - set(expected))
        raise ValueError(
            f"collection Palissy incomplète : manquantes={missing}, inattendues={unexpected}"
        )
    return {
        "total_count": payload.get("total_count"),
        "result_count": len(results),
        "references": references,
        "with_merimee_reference": sum(
            bool(record.get("reference_a_une_notice_merimee_mh")) for record in results
        ),
    }


def build_spec() -> RetrievalSpec:
    where = "reference in (" + ",".join(f'\"{ref}\"' for ref in PALISSY_REFERENCES) + ")"
    query = {"where": where, "order_by": "reference", "limit": 100}
    return RetrievalSpec(
        source_id="pop_palissy",
        resource_id="collection_metallurgique_varenne",
        scope="orne_pilote_phase5",
        source_page_url="https://pop.culture.gouv.fr/notice/palissy/PM61000916",
        request_url=f"{PALISSY_API}?{urlencode(query)}",
        format="json",
        license="Licence Ouverte 2.0 ; médias selon leurs droits propres",
        query=query,
        notes=(
            "Ensemble PM61000916 et ses trente parties constituantes.",
            "Le rattachement au site pilote IA00060965 reste à vérifier.",
        ),
        validator=validate_palissy_collection,
    )


def extract_pilot_objects(
    *,
    raw_root: Path = Path("data/raw"),
    manifest_path: Path = Path("reports/audits/phase5_palissy_manifest.json"),
    retrieved_at: datetime | None = None,
) -> dict[str, Any]:
    timestamp = retrieved_at or datetime.now(timezone.utc).replace(microsecond=0)
    result = retrieve(
        build_spec(),
        retrieved_at=timestamp,
        raw_root=raw_root,
        extractor="patrimoine_orne.extract.pilot_objects",
        extractor_version=EXTRACTOR_VERSION,
        git_commit=current_git_commit(),
    )
    manifest = {
        "schema_version": "1.0",
        "generated_at": timestamp.isoformat().replace("+00:00", "Z"),
        "reference_count": len(PALISSY_REFERENCES),
        "sources": {"pop_palissy": [result_manifest(result)]},
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
        default=Path("reports/audits/phase5_palissy_manifest.json"),
    )
    args = parser.parse_args()
    manifest = extract_pilot_objects(raw_root=args.raw_root, manifest_path=args.manifest)
    print(json.dumps({"pop_palissy": manifest["reference_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
