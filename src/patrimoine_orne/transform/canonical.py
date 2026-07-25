"""Applique la revue canonique au corpus source complet de la phase 8."""

from __future__ import annotations

import argparse
import csv
import json
import uuid
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from patrimoine_orne.transform.corpus_80 import flat_rows


DEFAULT_CORPUS = Path("data/interim/phase8_corpus_319.json")
DEFAULT_DECISIONS = Path("config/phase8_decisions_canoniques.yml")
DEFAULT_IDS = Path("config/phase8_site_ids.yml")
DEFAULT_OUTPUT = Path("data/processed/corpus_canonique_phase8_v1.json")
DEFAULT_SUMMARY = Path("reports/quality/phase8_corpus_canonique_resume.json")
DEFAULT_CSV = Path("reports/quality/phase8_corpus_canonique.csv")
DEFAULT_RELATIONS = Path("reports/quality/phase8_relations_sites.csv")
DEFAULT_REVIEW = Path("reports/quality/phase8_revue_canoniques.csv")
DEFAULT_REPORT = Path("reports/quality/phase8_corpus_canonique.md")


def _pair_key(values: Sequence[str]) -> str:
    return "__".join(sorted(str(value) for value in values))


def _validate_uuid4(value: str) -> None:
    parsed = uuid.UUID(value)
    if parsed.version != 4 or str(parsed) != value:
        raise ValueError(f"identifiant non conforme à UUID v4 : {value}")


def load_or_create_ids(
    records: Sequence[Mapping[str, Any]],
    relations: Sequence[Mapping[str, Any]],
    *,
    excluded_reference: str,
    path: Path,
) -> dict[str, Any]:
    canonical = [
        record for record in records if record["dossier_reference"] != excluded_reference
    ]
    expected_references = {record["dossier_reference"] for record in canonical}
    expected_relations = {
        f"{row['source_reference']}__{row['type_relation_code']}__{row['target_reference']}"
        for row in relations
    }
    if path.exists():
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    else:
        site_ids = {}
        for record in canonical:
            site_ids[record["dossier_reference"]] = record.get("site_id") or str(
                uuid.uuid4()
            )
        relation_ids = {key: str(uuid.uuid4()) for key in sorted(expected_relations)}
        payload = {
            "version": "1.0",
            "generated_at": date.today().isoformat(),
            "excluded_source_references": [excluded_reference],
            "site_ids": dict(sorted(site_ids.items())),
            "relation_ids": relation_ids,
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )

    if set(payload["site_ids"]) != expected_references:
        raise ValueError("le registre des site_id ne couvre pas exactement les sites canoniques")
    if set(payload["relation_ids"]) != expected_relations:
        raise ValueError("le registre des relations ne correspond pas aux décisions")
    all_ids = [*payload["site_ids"].values(), *payload["relation_ids"].values()]
    for value in all_ids:
        _validate_uuid4(str(value))
    if len(all_ids) != len(set(all_ids)):
        raise ValueError("le registre contient des UUID dupliqués")
    for record in canonical:
        existing = record.get("site_id")
        if existing and payload["site_ids"][record["dossier_reference"]] != existing:
            raise ValueError("un site_id du pilote a été modifié")
    return payload


def _apply_activity_overrides(
    record: dict[str, Any], decision: Mapping[str, Any]
) -> None:
    removed_code = str(decision["supprimer_code"])
    removed = [
        activity
        for activity in record["activites"]
        if activity["activite_code"] == removed_code
    ]
    if len(removed) != 1:
        raise ValueError(
            f"{record['dossier_reference']}: activité générique absente ou dupliquée"
        )
    record["activites"] = [
        activity
        for activity in record["activites"]
        if activity["activite_code"] != removed_code
    ]
    template = removed[0]
    order = max((activity["ordre"] for activity in record["activites"]), default=0)
    for addition in decision["ajouter"]:
        order += 1
        activity = deepcopy(template)
        activity.update(
            {
                "ordre": order,
                "libelle_source": addition["libelle_source"],
                "activite_code": addition["activite_code"],
                "secteur_code": addition["secteur_code"],
                "installation_code": addition["installation_code"],
                "note": addition["note"],
                "fiabilite_code": "forte",
            }
        )
        record["activites"].append(activity)
    record["secteurs_codes"] = sorted(
        {activity["secteur_code"] for activity in record["activites"]}
    )
    record["installations_codes"] = sorted(
        {activity["installation_code"] for activity in record["activites"]}
    )


def build_canonical_corpus(
    corpus: Mapping[str, Any],
    decisions: Mapping[str, Any],
    ids: Mapping[str, Any],
) -> dict[str, Any]:
    records = deepcopy(corpus["dossiers"])
    by_reference = {record["dossier_reference"]: record for record in records}
    source_pairs = {
        _pair_key((row["reference_1"], row["reference_2"]))
        for row in corpus["rapprochements_candidats"]
    }
    decision_pairs = {
        _pair_key(row["references"]) for row in decisions["rapprochements"]
    }
    if source_pairs != decision_pairs:
        raise ValueError("les décisions ne couvrent pas exactement les rapprochements proposés")
    if any(
        row["decision"] != "rejete_sites_distincts"
        for row in decisions["rapprochements"]
    ):
        raise ValueError("une fusion inattendue exige une procédure de choix du site canonique")

    rejected_by_reference: dict[str, list[str]] = {}
    for row in decisions["rapprochements"]:
        first, second = row["references"]
        rejected_by_reference.setdefault(first, []).append(second)
        rejected_by_reference.setdefault(second, []).append(first)
    for reference, others in rejected_by_reference.items():
        by_reference[reference]["decision_rapprochement"] = "rejete_sites_distincts"
        by_reference[reference]["rapprochements_rejetes_avec"] = sorted(others)
    for record in records:
        record.setdefault("rapprochements_rejetes_avec", [])

    for reference, decision in decisions["activites_a_preciser"].items():
        _apply_activity_overrides(by_reference[reference], decision)

    excluded_reference = decisions["dossier_collectif"]["reference"]
    excluded = by_reference[excluded_reference]
    canonical_records = [
        record for record in records if record["dossier_reference"] != excluded_reference
    ]
    for record in canonical_records:
        reference = record["dossier_reference"]
        record["site_id"] = ids["site_ids"][reference]
        record["statut_site"] = (
            "site_canonique_composant_non_productif"
            if not record["activites"]
            else "site_canonique_phase8"
        )
        record["decision_inclusion_code"] = "inclus"
        record["statut_traitement"] = "canonise_phase8"

    relations = []
    for row in decisions["relations_sites"]:
        key = (
            f"{row['source_reference']}__{row['type_relation_code']}__"
            f"{row['target_reference']}"
        )
        relations.append(
            {
                "relation_site_id": ids["relation_ids"][key],
                "site_source_id": ids["site_ids"][row["source_reference"]],
                "site_cible_id": ids["site_ids"][row["target_reference"]],
                "source_reference": row["source_reference"],
                "target_reference": row["target_reference"],
                "type_relation_code": row["type_relation_code"],
                "statut_validation_code": "valide",
                "fiabilite_code": row["fiabilite_code"],
                "justification": row["justification"],
            }
        )

    if len(canonical_records) != 318:
        raise ValueError("le corpus canonique doit contenir 318 sites")
    if len({record["site_id"] for record in canonical_records}) != 318:
        raise ValueError("les site_id canoniques ne sont pas uniques")
    if any(
        activity["activite_code"] == "activite_industrielle_indeterminee"
        for record in canonical_records
        for activity in record["activites"]
    ):
        raise ValueError("une activité industrielle indéterminée subsiste")
    return {
        "schema_version": "1.0",
        "corpus_version": "phase8_canonique_v1",
        "generated_at": date.today().isoformat(),
        "status": "corpus_canonique_technique",
        "classifications_version": corpus["classifications_version"],
        "source_dossier_count": 319,
        "canonical_site_count": 318,
        "counts": {
            "sites": len(canonical_records),
            "sites_avec_activites_productives": sum(
                bool(record["activites"]) for record in canonical_records
            ),
            "sites_composants_non_productifs": sum(
                not record["activites"] for record in canonical_records
            ),
            "activites": sum(len(record["activites"]) for record in canonical_records),
            "rapprochements_rejetes": len(decisions["rapprochements"]),
            "relations_sites_validees": len(relations),
            "dossiers_sources_hors_decompte": 1,
        },
        "dossiers_sources_hors_decompte": [
            {
                "dossier_reference": excluded_reference,
                "titre_source": excluded["titre_source"],
                "decision": decisions["dossier_collectif"]["decision"],
                "nature": decisions["dossier_collectif"]["nature"],
                "justification": decisions["dossier_collectif"]["justification"],
            }
        ],
        "relations_sites": relations,
        "sites": canonical_records,
    }


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(fields))
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(
    canonical: Mapping[str, Any],
    decisions: Mapping[str, Any],
    *,
    output: Path,
    summary: Path,
    csv_path: Path,
    relations_path: Path,
    review_path: Path,
    report_path: Path,
) -> dict[str, Any]:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(canonical, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    summary_payload = {
        "schema_version": "1.0",
        "generated_at": canonical["generated_at"],
        "corpus_version": canonical["corpus_version"],
        "source_dossier_count": canonical["source_dossier_count"],
        "canonical_site_count": canonical["canonical_site_count"],
        "counts": canonical["counts"],
        "checks": {
            "source_319": canonical["source_dossier_count"] == 319,
            "canonical_318": canonical["canonical_site_count"] == 318,
            "unique_site_ids": len(
                {record["site_id"] for record in canonical["sites"]}
            )
            == 318,
            "all_uuid4": all(
                uuid.UUID(record["site_id"]).version == 4
                for record in canonical["sites"]
            ),
            "no_unknown_activity": all(
                activity["activite_code"] != "activite_industrielle_indeterminee"
                for record in canonical["sites"]
                for activity in record["activites"]
            ),
            "all_match_candidates_decided": canonical["counts"][
                "rapprochements_rejetes"
            ]
            == 7,
            "collective_source_excluded_from_site_count": len(
                canonical["dossiers_sources_hors_decompte"]
            )
            == 1,
        },
        "next_step": "enrichir_et_localiser_les_318_sites_canoniques",
    }
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(
        json.dumps(summary_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    site_rows = flat_rows({"dossiers": canonical["sites"]})
    _write_csv(csv_path, site_rows, list(site_rows[0]))
    _write_csv(
        relations_path,
        canonical["relations_sites"],
        [
            "relation_site_id",
            "site_source_id",
            "site_cible_id",
            "source_reference",
            "target_reference",
            "type_relation_code",
            "statut_validation_code",
            "fiabilite_code",
            "justification",
        ],
    )
    review_rows = [
        {
            "type_decision": "rapprochement",
            "references": " | ".join(row["references"]),
            "decision": row["decision"],
            "justification": row["justification"],
        }
        for row in decisions["rapprochements"]
    ]
    review_rows.append(
        {
            "type_decision": "dossier_collectif",
            "references": decisions["dossier_collectif"]["reference"],
            "decision": decisions["dossier_collectif"]["decision"],
            "justification": decisions["dossier_collectif"]["justification"],
        }
    )
    review_rows.extend(
        {
            "type_decision": "relation_site",
            "references": f"{row['source_reference']} → {row['target_reference']}",
            "decision": row["type_relation_code"],
            "justification": row["justification"],
        }
        for row in decisions["relations_sites"]
    )
    review_rows.extend(
        {
            "type_decision": "activite_precisee",
            "references": reference,
            "decision": "activites_historiques_structurees",
            "justification": " | ".join(
                addition["libelle_source"] for addition in row["ajouter"]
            ),
        }
        for reference, row in decisions["activites_a_preciser"].items()
    )
    _write_csv(
        review_path,
        review_rows,
        ["type_decision", "references", "decision", "justification"],
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "\n".join(
            [
                "# Phase 8 — Revue canonique",
                "",
                "## Résultat",
                "",
                "**Le corpus principal contient 318 sites canoniques.**",
                "",
                "Le passage de 319 dossiers sources à 318 sites s'explique uniquement par "
                "le dossier collectif `IA61001399`, qui est une synthèse sans emprise. Les "
                "quinze dossiers individuels de fromageries sont déjà présents.",
                "",
                "- les 7 rapprochements automatiques sont rejetés comme sites distincts ;",
                "- 5 relations entre sites sont validées ;",
                "- les 4 cités ouvrières restent des emprises distinctes reliées aux mines ;",
                "- les activités des deux moulins génériques sont précisées depuis leur "
                "historique ;",
                f"- {canonical['counts']['activites']} activités sont désormais structurées ;",
                "- les 318 sites possèdent un UUID v4 stable.",
                "",
                "Ce nombre est un décompte technique du corpus de l'Inventaire. Il ne comprend "
                "pas encore les éventuels sites supplémentaires qui pourraient être ajoutés "
                "par CASIAS, les archives ou d'autres sources.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return summary_payload


def load_and_build(args: argparse.Namespace) -> dict[str, Any]:
    corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
    decisions = yaml.safe_load(args.decisions.read_text(encoding="utf-8"))
    ids = load_or_create_ids(
        corpus["dossiers"],
        decisions["relations_sites"],
        excluded_reference=decisions["dossier_collectif"]["reference"],
        path=args.ids,
    )
    canonical = build_canonical_corpus(corpus, decisions, ids)
    return write_outputs(
        canonical,
        decisions,
        output=args.output,
        summary=args.summary,
        csv_path=args.csv,
        relations_path=args.relations,
        review_path=args.review,
        report_path=args.report,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--decisions", type=Path, default=DEFAULT_DECISIONS)
    parser.add_argument("--ids", type=Path, default=DEFAULT_IDS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--relations", type=Path, default=DEFAULT_RELATIONS)
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    arguments = parser.parse_args()
    print(json.dumps(load_and_build(arguments), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
