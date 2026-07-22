"""Énumère le corpus officiel et prépare des lots POP reproductibles."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence
from urllib.request import Request, urlopen

import yaml

from patrimoine_orne.classify.sectors import (
    classify_denomination,
    classify_pop_records,
    load_classifications,
)
from patrimoine_orne.extract.http import RetrievalResult, RetrievalSpec, retrieve
from patrimoine_orne.extract.pilot import current_git_commit, result_manifest


EXTRACTOR_VERSION = "0.1.0"
DEFAULT_CONFIG = Path("config/corpus_phase8.yml")
DEFAULT_PILOT = Path("config/echantillon_pilote.yml")
POP_API_BASE = "https://api.pop.culture.gouv.fr"


def _as_list(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [str(item) for item in value if item not in (None, "")]
    return [str(value)]


def load_config(path: Path = DEFAULT_CONFIG) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def fetch_pop_search(config: Mapping[str, Any], *, timeout: int = 60) -> list[dict[str, Any]]:
    """Interroge l'API avancée POP sur le libellé exact de l'étude."""
    enumeration = config["enumeration"]
    body = {
        "bases": ["merimee"],
        "crits": [
            {
                "crits": [
                    {
                        "base": "merimee",
                        "fields": "ETUD",
                        "operator": "*",
                        "value": "patrimoine industriel de l’Orne",
                    }
                ]
            }
        ],
        "size": 500,
        "from": 0,
    }
    request = Request(
        enumeration["api_url"],
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={
            "User-Agent": "PatrimoineIndustrielOrne/0.3 (+datajournalisme)",
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8", errors="strict"))
    if payload.get("total") != len(payload.get("hits", [])):
        raise ValueError("la réponse POP est tronquée ou incohérente")
    return [dict(row["_source"]) for row in payload["hits"]]


def enumerate_corpus(
    config: Mapping[str, Any],
    *,
    searcher: Callable[[Mapping[str, Any]], list[dict[str, Any]]] = fetch_pop_search,
) -> dict[str, Any]:
    """Énumère et valide les 319 références attendues."""
    enumeration = config["enumeration"]
    records = searcher(config)
    if len(records) != enumeration["expected_search_count"]:
        raise ValueError("le total de la recherche POP a changé")
    expected_exclusions = {
        row["reference"]: row["reason"]
        for row in enumeration["excluded_search_results"]
    }
    audits = []
    for notice in records:
        reference = str(notice.get("REF", ""))
        if not re.fullmatch(r"IA\d{8}", reference):
            raise ValueError(f"référence IA invalide dans la réponse POP : {reference!r}")
        if enumeration["expected_study"] not in _as_list(notice.get("ETUD")):
            raise ValueError(f"cadre d'étude inattendu pour {reference}")
        reason = expected_exclusions.get(reference)
        audits.append(
            {
                "reference": reference,
                "status": "excluded" if reason else "eligible",
                "reason": reason,
                "title": notice.get("TICO"),
                "dossier_type": notice.get("DOSS"),
                "communes": _as_list(notice.get("COM")),
                "insee": _as_list(notice.get("INSEE")),
                "dossier_url": notice.get("DOSURL"),
            }
        )
    audits.sort(key=lambda row: row["reference"])
    references = [row["reference"] for row in audits if row["status"] == "eligible"]
    if len(references) != len(set(references)):
        raise ValueError("références IA éligibles dupliquées")
    expected = config["corpus_source"]["announced_records"]
    if len(references) != expected:
        excluded = [
            (row["reference"], row.get("reason"))
            for row in audits
            if row["status"] == "excluded"
        ]
        raise ValueError(
            f"{len(references)} références éligibles au lieu des {expected} attendues ; "
            f"résultats exclus : {excluded}"
        )
    observed_exclusions = {
        row["reference"]: row["reason"]
        for row in audits
        if row["status"] == "excluded"
    }
    if observed_exclusions != expected_exclusions:
        raise ValueError(
            "les exclusions observées ne correspondent pas aux exclusions documentées"
        )

    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "official_source": config["corpus_source"],
        "method": enumeration["method"],
        "search_result_count": len(records),
        "eligible_count": len(references),
        "excluded_search_result_count": len(audits) - len(references),
        "references": references,
        "search_result_audit": audits,
        "checks": {
            "unique": len(references) == len(set(references)),
            "official_total_matches": len(references) == expected,
            "presentation_exclusion_matches": True,
        },
    }


def load_pilot_references(path: Path = DEFAULT_PILOT) -> list[str]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return [str(row["ia_reference"]) for row in payload["sites"]]


def select_systematic_lot(
    references: Sequence[str], excluded: Sequence[str], size: int
) -> list[str]:
    """Sélectionne un lot réparti sur la liste triée, sans prétention statistique."""
    pool = sorted(set(references) - set(excluded))
    if size <= 0 or size > len(pool):
        raise ValueError("taille de lot incompatible avec le nombre de références disponibles")
    indexes = [math.floor((index + 0.5) * len(pool) / size) for index in range(size)]
    selected = [pool[index] for index in indexes]
    if len(selected) != len(set(selected)):
        raise ValueError("la sélection systématique a produit un doublon")
    return selected


def write_enumeration_outputs(
    manifest: Mapping[str, Any],
    *,
    json_path: Path,
    csv_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["reference", "title", "communes", "insee", "dossier_url"])
        writer.writeheader()
        for row in manifest["search_result_audit"]:
            if row["status"] != "eligible":
                continue
            writer.writerow(
                {
                    "reference": row["reference"],
                    "title": row.get("title"),
                    "communes": " | ".join(row.get("communes", [])),
                    "insee": " | ".join(row.get("insee", [])),
                    "dossier_url": row.get("dossier_url"),
                }
            )


def write_lot_config(
    references: Sequence[str], path: Path, enumeration_manifest: Path
) -> None:
    payload = {
        "version": "1.0",
        "lot": 1,
        "nature": "premier_lot_non_pilote_de_calibrage",
        "selection": "systematique_sur_references_triees",
        "enumeration_manifest": enumeration_manifest.as_posix(),
        "reference_count": len(references),
        "references": list(references),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )


def validate_pop_api_notice(reference: str) -> Callable[[Path], dict[str, Any]]:
    def validator(path: Path) -> dict[str, Any]:
        notice = json.loads(path.read_text(encoding="utf-8"))
        if notice.get("REF") != reference:
            raise ValueError(f"référence POP inattendue : {notice.get('REF')!r}")
        return {"reference": reference, "field_count": len(notice)}

    return validator


def build_lot_specs(references: Sequence[str], lot: int) -> list[RetrievalSpec]:
    return [
        RetrievalSpec(
            source_id="pop_merimee",
            resource_id=reference,
            scope=f"orne_phase8_lot{lot:02d}",
            source_page_url="https://pop.culture.gouv.fr/donnees-ouvertes",
            request_url=f"{POP_API_BASE}/notices/merimee/{reference}",
            format="json",
            license="Licence Ouverte 2.0 sauf mention contraire ; © Région Normandie",
            notes=(
                "Notice structurée de l'Inventaire général diffusée par l'API POP.",
                f"Phase 8, lot {lot:02d} non pilote.",
            ),
            headers={"Accept": "application/json"},
            validator=validate_pop_api_notice(reference),
        )
        for reference in references
    ]


def extract_lot(
    references: Sequence[str],
    *,
    lot: int,
    raw_root: Path,
    manifest_path: Path,
) -> dict[str, Any]:
    timestamp = datetime.now(timezone.utc).replace(microsecond=0)
    results: list[RetrievalResult] = []
    for spec in build_lot_specs(references, lot):
        results.append(
            retrieve(
                spec,
                retrieved_at=timestamp,
                raw_root=raw_root,
                extractor="patrimoine_orne.extract.corpus",
                extractor_version=EXTRACTOR_VERSION,
                git_commit=current_git_commit(),
            )
        )
    manifest = {
        "schema_version": "1.0",
        "generated_at": timestamp.isoformat().replace("+00:00", "Z"),
        "lot": lot,
        "reference_count": len(references),
        "sources": {"pop_merimee": [result_manifest(result) for result in results]},
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def load_lot_records(manifest: Mapping[str, Any]) -> list[dict[str, Any]]:
    records = []
    for row in manifest["sources"]["pop_merimee"]:
        notice = json.loads(Path(row["data_file"]).read_text(encoding="utf-8"))
        if notice.get("REF") != row["observations"]["reference"]:
            raise ValueError("le manifeste et la notice POP ne concordent pas")
        records.append(notice)
    return records


def build_lot_assessment(
    records: Sequence[Mapping[str, Any]],
    classifications: Mapping[str, Any],
    decisions: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Produit un diagnostic, sans fusionner ni séparer automatiquement."""
    classification_report = classify_pop_records(records, classifications)
    review_rows = []
    preliminary_rows = []
    keys: dict[tuple[str, str], list[str]] = {}
    for record in records:
        reference = str(record["REF"])
        denominations = _as_list(record.get("DENO"))
        classified = [
            item
            for denomination in denominations
            if (item := classify_denomination(denomination, classifications)) is not None
        ]
        unknown = [
            denomination
            for denomination in denominations
            if classify_denomination(denomination, classifications) is None
        ]
        communes = _as_list(record.get("COM"))
        insee = _as_list(record.get("INSEE"))
        addresses = _as_list(record.get("ADRS"))
        reasons = []
        if unknown:
            reasons.append("denomination_non_classee")
        if len(set(communes)) > 1 or len(set(insee)) > 1:
            reasons.append("emprises_distinctes_possibles")
        if len({item["secteur_code"] for item in classified}) > 1:
            reasons.append("site_multi_secteurs_a_confirmer")
        if not record.get("POP_COORDONNEES") and not record.get("COOR"):
            reasons.append("localisation_structuree_absente")
        key = ((insee[0] if len(insee) == 1 else ""), (addresses[0].casefold() if len(addresses) == 1 else ""))
        if all(key):
            keys.setdefault(key, []).append(reference)
        preliminary_rows.append(
            {
                "dossier_reference": reference,
                "statut": "un_site_presume_a_verifier",
                "titre_source": record.get("TICO"),
                "communes_source": " | ".join(communes),
                "insee_source": " | ".join(insee),
                "adresses_source": " | ".join(addresses),
                "denominations_source": " | ".join(denominations),
                "activites_codes": " | ".join(sorted({item["activite_code"] for item in classified})),
                "secteurs_codes": " | ".join(sorted({item["secteur_code"] for item in classified})),
                "installations_codes": " | ".join(sorted({item["installation_code"] for item in classified})),
                "scle_source": " | ".join(_as_list(record.get("SCLE"))),
                "dossier_url": record.get("DOSURL"),
            }
        )
        if reasons:
            review_rows.append(
                {
                    "dossier_reference": reference,
                    "motifs": " | ".join(reasons),
                    "decision": "a_verifier",
                    "commentaire": "",
                }
            )

    merge_groups = [refs for refs in keys.values() if len(refs) > 1]
    for refs in merge_groups:
        for reference in refs:
            row = next(
                (item for item in review_rows if item["dossier_reference"] == reference),
                None,
            )
            if row is None:
                row = {
                    "dossier_reference": reference,
                    "motifs": "rapprochement_possible_meme_adresse",
                    "decision": "a_verifier",
                    "commentaire": "",
                }
                review_rows.append(row)
            elif "rapprochement_possible_meme_adresse" not in row["motifs"]:
                row["motifs"] += " | rapprochement_possible_meme_adresse"

    decision_rows = (decisions or {}).get("decisions", {})
    known_references = {str(record["REF"]) for record in records}
    unknown_decisions = set(decision_rows) - known_references
    if unknown_decisions:
        raise ValueError(f"décisions hors du lot : {sorted(unknown_decisions)}")
    for row in review_rows:
        decision = decision_rows.get(row["dossier_reference"])
        if decision:
            row["decision"] = decision["decision"]
            row["commentaire"] = decision["justification"]
    unresolved = [row for row in review_rows if row["decision"] == "a_verifier"]

    return {
        "schema_version": "1.0",
        "record_count": len(records),
        "classification": classification_report,
        "preliminary_sites": preliminary_rows,
        "review_queue": sorted(review_rows, key=lambda row: row["dossier_reference"]),
        "unresolved_review_count": len(unresolved),
        "lot_review_complete": not unresolved,
        "lot_canonical_site_count": len(records) if not unresolved and not merge_groups else None,
        "possible_merge_groups": merge_groups,
        "canonical_site_count": None,
        "canonical_count_status": "inconnu_avant_revue_complete",
    }


def write_assessment(assessment: Mapping[str, Any], report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(assessment, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    for key, filename, fieldnames in (
        (
            "preliminary_sites",
            "phase8_lot1_sites_candidats.csv",
            [
                "dossier_reference",
                "statut",
                "titre_source",
                "communes_source",
                "insee_source",
                "adresses_source",
                "denominations_source",
                "activites_codes",
                "secteurs_codes",
                "installations_codes",
                "scle_source",
                "dossier_url",
            ],
        ),
        (
            "review_queue",
            "phase8_lot1_file_revue.csv",
            ["dossier_reference", "motifs", "decision", "commentaire"],
        ),
    ):
        output = report_path.with_name(filename)
        with output.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(assessment[key])


def prepare_lot1(args: argparse.Namespace) -> dict[str, Any]:
    config = load_config(args.config)
    enumeration = enumerate_corpus(config)
    write_enumeration_outputs(
        enumeration, json_path=args.enumeration_manifest, csv_path=args.references_csv
    )
    selected = select_systematic_lot(
        enumeration["references"],
        load_pilot_references(args.pilot),
        config["batches"]["first_new_batch_size"],
    )
    write_lot_config(selected, args.lot_config, args.enumeration_manifest)
    lot_manifest = extract_lot(
        selected, lot=1, raw_root=args.raw_root, manifest_path=args.lot_manifest
    )
    assessment = build_lot_assessment(
        load_lot_records(lot_manifest),
        load_classifications(args.classifications),
        yaml.safe_load(args.lot_decisions.read_text(encoding="utf-8"))
        if args.lot_decisions.exists()
        else None,
    )
    write_assessment(assessment, args.assessment)
    return {
        "enumerated": enumeration["eligible_count"],
        "excluded_search_results": enumeration["excluded_search_result_count"],
        "lot1_extracted": lot_manifest["reference_count"],
        "lot1_review_queue": len(assessment["review_queue"]),
        "canonical_site_count": assessment["canonical_site_count"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--pilot", type=Path, default=DEFAULT_PILOT)
    parser.add_argument("--classifications", type=Path, default=Path("config/classifications.yml"))
    parser.add_argument("--raw-root", type=Path, default=Path("data/raw"))
    parser.add_argument("--enumeration-manifest", type=Path, default=Path("reports/audits/phase8_enumeration_corpus.json"))
    parser.add_argument("--references-csv", type=Path, default=Path("reports/audits/phase8_references_ia.csv"))
    parser.add_argument("--lot-config", type=Path, default=Path("config/phase8_lot1.yml"))
    parser.add_argument("--lot-decisions", type=Path, default=Path("config/phase8_lot1_decisions.yml"))
    parser.add_argument("--lot-manifest", type=Path, default=Path("reports/audits/phase8_lot1_pop_manifest.json"))
    parser.add_argument("--assessment", type=Path, default=Path("reports/quality/phase8_lot1_evaluation.json"))
    args = parser.parse_args()
    print(json.dumps(prepare_lot1(args), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
