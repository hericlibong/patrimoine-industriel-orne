"""Archive les sources complémentaires nécessaires aux 318 sites canoniques."""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping
from urllib.parse import urlencode

from patrimoine_orne.extract.http import RetrievalResult, RetrievalSpec, retrieve
from patrimoine_orne.extract.pilot import current_git_commit, result_manifest
from patrimoine_orne.extract.samples import CASIAS_WFS, _wfs_filter


EXTRACTOR_VERSION = "0.1.0"
DEFAULT_MANIFEST = Path("reports/audits/phase8_enrichissement_sources_manifest.json")
POP_ADVANCED_API = "https://api.pop.culture.gouv.fr/search/advanced"


def validate_pop_page(source: str) -> Callable[[Path], dict[str, Any]]:
    def validator(path: Path) -> dict[str, Any]:
        payload = json.loads(path.read_text(encoding="utf-8"))
        hits = payload.get("hits")
        if not isinstance(hits, list):
            raise ValueError(f"page {source} sans liste de résultats")
        records = [row.get("_source", {}) for row in hits]
        outside = [row.get("REF") for row in records if "61" not in str(row.get("DPT"))]
        if outside:
            raise ValueError(f"page {source} contenant des notices hors Orne")
        return {
            "source": source,
            "total_count": int(payload.get("total", 0)),
            "result_count": len(records),
            "references": [str(row.get("REF")) for row in records],
        }

    return validator


def validate_casias_full(path: Path) -> dict[str, Any]:
    root = ET.parse(path).getroot()
    features = [
        node for node in root.iter() if node.tag.endswith("drealnorm_casias_s_r28")
    ]
    records = [
        {child.tag.rsplit("}", 1)[-1]: child.text or "" for child in feature}
        for feature in features
    ]
    if not records or any(row.get("code_depar") != "61" for row in records):
        raise ValueError("extraction CASIAS complète invalide ou hors Orne")
    references = [row.get("code_inven") or row.get("code_metie") for row in records]
    if len(references) != len(set(references)):
        raise ValueError("l'extraction CASIAS contient des identifiants dupliqués")
    return {
        "result_count": len(records),
        "with_coordinates": sum(bool(row.get("x_wgs84")) for row in records),
        "without_coordinates": sum(not row.get("x_wgs84") for row in records),
    }


def _pop_spec(
    *,
    source_id: str,
    source_name: str,
    base: str,
    offset: int,
    limit: int,
) -> RetrievalSpec:
    body = {
        "bases": [base],
        "crits": [
            {
                "crits": [
                    {
                        "base": base,
                        "fields": "DPT",
                        "operator": "*",
                        "value": "61",
                    }
                ]
            }
        ],
        "size": limit,
        "from": offset,
    }
    return RetrievalSpec(
        source_id=source_id,
        resource_id=f"orne_page_{offset:04d}",
        scope="orne_phase8_complet",
        source_page_url="https://pop.culture.gouv.fr/donnees-ouvertes",
        request_url=POP_ADVANCED_API,
        format="json",
        license="Licence Ouverte 2.0 ; médias selon leurs droits propres",
        query=body,
        notes=(f"Extraction départementale complète {source_name}.",),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        validator=validate_pop_page(source_name),
        method="POST",
        body=json.dumps(body, ensure_ascii=False).encode("utf-8"),
    )


def _retrieve_pop_pages(
    *,
    source_id: str,
    source_name: str,
    base: str,
    timestamp: datetime,
    raw_root: Path,
) -> list[RetrievalResult]:
    limit = 500
    results = []
    offset = 0
    total = None
    while total is None or offset < total:
        spec = _pop_spec(
            source_id=source_id,
            source_name=source_name,
            base=base,
            offset=offset,
            limit=limit,
        )
        result = retrieve(
            spec,
            retrieved_at=timestamp,
            raw_root=raw_root,
            extractor="patrimoine_orne.extract.full_enrichment",
            extractor_version=EXTRACTOR_VERSION,
            git_commit=current_git_commit(),
            max_bytes=20 * 1024 * 1024,
        )
        results.append(result)
        total = int(result.observations["total_count"])
        offset += limit
    observed = sum(result.observations["result_count"] for result in results)
    if observed != total:
        raise ValueError(f"{source_name}: {observed} notices archivées sur {total}")
    return results


def extract_full_sources(
    *,
    raw_root: Path = Path("data/raw"),
    manifest_path: Path = DEFAULT_MANIFEST,
) -> dict[str, Any]:
    timestamp = datetime.now(timezone.utc).replace(microsecond=0)
    mh_results = _retrieve_pop_pages(
        source_id="monuments_historiques_data_culture",
        source_name="monuments_historiques",
        base="merimee",
        timestamp=timestamp,
        raw_root=raw_root,
    )
    palissy_results = _retrieve_pop_pages(
        source_id="pop_palissy",
        source_name="palissy",
        base="palissy",
        timestamp=timestamp,
        raw_root=raw_root,
    )
    casias_query = {
        "SERVICE": "WFS",
        "VERSION": "2.0.0",
        "REQUEST": "GetFeature",
        "TYPENAMES": "ms:drealnorm_casias_s_r28",
        "COUNT": 5000,
        "FILTER": _wfs_filter(("PropertyIsEqualTo", "code_depar", "61")),
    }
    casias_spec = RetrievalSpec(
        source_id="casias",
        resource_id="wfs_orne_complet",
        scope="orne_phase8_complet",
        source_page_url=(
            "https://www.data.gouv.fr/datasets/"
            "carte-des-anciens-sites-industriels-et-activites-de-services-casias-normandie"
        ),
        request_url=f"{CASIAS_WFS}&{urlencode(casias_query)}",
        format="gml",
        license="Licence Ouverte 2.0",
        query=casias_query,
        notes=(
            "Corpus départemental utilisé uniquement pour recoupement et élargissement.",
            "Une coordonnée CASIAS ne vaut pas localisation patrimoniale précise.",
        ),
        validator=validate_casias_full,
    )
    casias_result = retrieve(
        casias_spec,
        retrieved_at=timestamp,
        raw_root=raw_root,
        extractor="patrimoine_orne.extract.full_enrichment",
        extractor_version=EXTRACTOR_VERSION,
        git_commit=current_git_commit(),
        max_bytes=50 * 1024 * 1024,
    )
    manifest = {
        "schema_version": "1.0",
        "generated_at": timestamp.isoformat().replace("+00:00", "Z"),
        "status": "complete",
        "sources": {
            "monuments_historiques": [
                result_manifest(result) for result in mh_results
            ],
            "pop_palissy": [result_manifest(result) for result in palissy_results],
            "casias": [result_manifest(casias_result)],
        },
        "counts": {
            "monuments_historiques": sum(
                result.observations["result_count"] for result in mh_results
            ),
            "pop_palissy": sum(
                result.observations["result_count"] for result in palissy_results
            ),
            "casias": casias_result.observations["result_count"],
        },
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def load_culture_records(
    manifest: Mapping[str, Any], source: str
) -> list[dict[str, Any]]:
    records = []
    for row in manifest["sources"][source]:
        payload = json.loads(Path(row["data_file"]).read_text(encoding="utf-8"))
        records.extend(dict(item["_source"]) for item in payload["hits"])
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-root", type=Path, default=Path("data/raw"))
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    manifest = extract_full_sources(
        raw_root=args.raw_root, manifest_path=args.manifest
    )
    print(json.dumps(manifest["counts"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
