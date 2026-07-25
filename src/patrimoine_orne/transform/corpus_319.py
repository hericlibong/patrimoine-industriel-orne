"""Construit le corpus commun des 319 dossiers officiels de l'Inventaire."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Sequence

from patrimoine_orne.classify.sectors import (
    classify_pop_records,
    load_classifications,
    load_pop_manifest_sample,
)
from patrimoine_orne.extract.corpus import load_lot_records
from patrimoine_orne.transform.corpus_80 import (
    _manifest_paths,
    find_match_candidates,
    flat_rows,
    project_lot1,
    project_pilot,
)


DEFAULT_ENUMERATION = Path("reports/audits/phase8_enumeration_corpus.json")
DEFAULT_PILOT_CORPUS = Path("data/processed/corpus_pilote_socle_v1.json")
DEFAULT_PILOT_MANIFEST = Path("reports/audits/phase5_pop_manifest.json")
DEFAULT_FIRST_MANIFEST = Path("reports/audits/phase8_lot1_pop_manifest.json")
DEFAULT_REMAINING_MANIFEST = Path("reports/audits/phase8_remaining_pop_manifest.json")
DEFAULT_OUTPUT = Path("data/interim/phase8_corpus_319.json")
DEFAULT_SUMMARY = Path("reports/quality/phase8_corpus_319_resume.json")
DEFAULT_CSV = Path("reports/quality/phase8_corpus_319.csv")
DEFAULT_MATCHES = Path("reports/quality/phase8_corpus_319_rapprochements.csv")
DEFAULT_SPLITS = Path("reports/quality/phase8_corpus_319_separations.csv")
DEFAULT_ANOMALIES = Path("reports/quality/phase8_corpus_319_anomalies.csv")
DEFAULT_CLASSIFICATION = Path("reports/quality/phase8_classification_corpus_319.json")
DEFAULT_REPORT = Path("reports/quality/phase8_corpus_319.md")


def _objects_by_reference(
    pilot_corpus: Mapping[str, Any],
) -> dict[str, list[Mapping[str, Any]]]:
    result: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for item in pilot_corpus.get("objets_techniques", []):
        result[str(item["site_candidat_reference"])].append(item)
    return result


def _split_candidates(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for record in records:
        reasons = []
        if record.get("type_dossier_source") == "dossier collectif":
            reasons.append("dossier_collectif")
        if len(set(record["communes_source"])) > 1:
            reasons.append("plusieurs_communes")
        if len(set(record["insee_source"])) > 1:
            reasons.append("plusieurs_codes_insee")
        if reasons:
            rows.append(
                {
                    "dossier_reference": record["dossier_reference"],
                    "titre_source": record.get("titre_source"),
                    "motifs": " | ".join(reasons),
                    "communes_source": " | ".join(record["communes_source"]),
                    "insee_source": " | ".join(record["insee_source"]),
                    "decision": "a_verifier",
                }
            )
    return rows


def _anomalies(
    records: Sequence[Mapping[str, Any]], supplemental_references: Sequence[str]
) -> list[dict[str, Any]]:
    rows = [
        {
            "dossier_reference": reference,
            "type": "pilote_hors_enumeration_officielle",
            "gravite": "information",
            "traitement": "conserve_hors_corpus_principal",
        }
        for reference in supplemental_references
    ]
    for record in records:
        reference = record["dossier_reference"]
        if record.get("type_dossier_source") == "dossier collectif":
            rows.append(
                {
                    "dossier_reference": reference,
                    "type": "dossier_collectif_a_decomposer",
                    "gravite": "revue_requise",
                    "traitement": "ne_pas_compter_comme_site_unique",
                }
            )
        if not record["activites"] and record["composants_non_productifs_source"]:
            rows.append(
                {
                    "dossier_reference": reference,
                    "type": "composant_non_productif_a_relier",
                    "gravite": "revue_requise",
                    "traitement": "relier_au_site_industriel_sans_fusion",
                }
            )
        if any(
            activity["activite_code"] == "activite_industrielle_indeterminee"
            for activity in record["activites"]
        ):
            rows.append(
                {
                    "dossier_reference": reference,
                    "type": "activite_generique_a_preciser",
                    "gravite": "revue_requise",
                    "traitement": "consulter_historique_source",
                }
            )
        if record["longitude_source"] is None or record["latitude_source"] is None:
            rows.append(
                {
                    "dossier_reference": reference,
                    "type": "coordonnees_source_absentes",
                    "gravite": "qualite",
                    "traitement": "conserver_non_localise_jusqua_geocodage",
                }
            )
    return rows


def build_corpus_319(
    *,
    official_references: Sequence[str],
    pilot_corpus: Mapping[str, Any],
    pilot_notices: Sequence[Mapping[str, Any]],
    first_records: Sequence[Mapping[str, Any]],
    remaining_records: Sequence[Mapping[str, Any]],
    pilot_paths: Mapping[str, str],
    first_paths: Mapping[str, str],
    remaining_paths: Mapping[str, str],
    classifications: Mapping[str, Any],
) -> dict[str, Any]:
    official = set(official_references)
    if len(official_references) != len(official) or len(official) != 319:
        raise ValueError("le corpus officiel doit contenir 319 références uniques")

    pilot_sites = {str(site["reference_ia"]): site for site in pilot_corpus["sites"]}
    pilot_notice_map = {str(notice["REF"]): notice for notice in pilot_notices}
    first_map = {str(notice["REF"]): notice for notice in first_records}
    remaining_map = {str(notice["REF"]): notice for notice in remaining_records}
    official_pilot = set(pilot_sites) & official
    supplemental = sorted(set(pilot_sites) - official)
    if supplemental != ["IA00061060"]:
        raise ValueError(f"pilotes hors énumération inattendus : {supplemental}")
    covered = official_pilot | set(first_map) | set(remaining_map)
    if covered != official:
        missing = sorted(official - covered)
        extra = sorted(covered - official)
        raise ValueError(f"couverture officielle incorrecte ; absents={missing}, hors_corpus={extra}")
    if any(
        left & right
        for left, right in (
            (official_pilot, set(first_map)),
            (official_pilot, set(remaining_map)),
            (set(first_map), set(remaining_map)),
        )
    ):
        raise ValueError("les trois ensembles officiels se recouvrent")

    objects = _objects_by_reference(pilot_corpus)
    records = []
    for reference in sorted(official_pilot):
        record = project_pilot(
            pilot_sites[reference],
            pilot_notice_map[reference],
            raw_path=pilot_paths[reference],
            objects=objects.get(reference, []),
            classifications_version=str(classifications["version"]),
        )
        record["type_dossier_source"] = pilot_notice_map[reference].get("DOSS")
        record["composants_non_productifs_source"] = []
        records.append(record)
    for reference in sorted(first_map):
        notice = first_map[reference]
        record = project_lot1(
            notice,
            raw_path=first_paths[reference],
            classifications=classifications,
        )
        record["type_dossier_source"] = notice.get("DOSS")
        records.append(record)
    for reference in sorted(remaining_map):
        notice = remaining_map[reference]
        is_collective = notice.get("DOSS") == "dossier collectif"
        record = project_lot1(
            notice,
            raw_path=remaining_paths[reference],
            classifications=classifications,
            origin="phase8_restant_officiel",
            site_status=(
                "dossier_collectif_a_decomposer"
                if is_collective
                else "site_provisoire_a_verifier"
            ),
        )
        record["type_dossier_source"] = notice.get("DOSS")
        if not record["activites"] and record["composants_non_productifs_source"]:
            record["statut_site"] = "composant_industriel_non_productif_a_relier"
            record["decision_rapprochement"] = "relation_site_a_etablir"
        if is_collective:
            record["nombre_sites_provisoire"] = None
            record["decision_rapprochement"] = "separation_a_verifier"
        records.append(record)

    matches = find_match_candidates(records)
    matched = {
        reference
        for row in matches
        for reference in (row["reference_1"], row["reference_2"])
    }
    for record in records:
        if record["dossier_reference"] in matched:
            record["decision_rapprochement"] = "candidat_a_verifier"
    splits = _split_candidates(records)
    split_references = {row["dossier_reference"] for row in splits}
    for record in records:
        if record["dossier_reference"] in split_references:
            record["decision_rapprochement"] = "separation_a_verifier"

    references = [record["dossier_reference"] for record in records]
    if len(records) != 319 or set(references) != official:
        raise ValueError("la projection finale ne concorde pas avec les 319 références")
    record_shapes = {tuple(sorted(record)) for record in records}
    if len(record_shapes) != 1:
        raise ValueError("la structure harmonisée des dossiers n'est pas uniforme")
    return {
        "schema_version": "1.0",
        "corpus_version": "phase8_319_dossiers_officiels_v1",
        "generated_at": date.today().isoformat(),
        "status": "corpus_source_complet_non_canonique",
        "classifications_version": str(classifications["version"]),
        "counts": {
            "dossiers_officiels": 319,
            "pilotes_officiels": len(official_pilot),
            "premiers_dossiers": len(first_map),
            "dossiers_restants_traites": len(remaining_map),
            "references_uniques": len(set(references)),
            "activites": sum(len(record["activites"]) for record in records),
            "dossiers_multi_activites": sum(
                len(record["activites"]) > 1 for record in records
            ),
            "dossiers_multi_secteurs": sum(
                len(record["secteurs_codes"]) > 1 for record in records
            ),
            "dossiers_composants_non_productifs": sum(
                not record["activites"] and bool(record["composants_non_productifs_source"])
                for record in records
            ),
            "rapprochements_a_verifier": len(matches),
            "separations_a_verifier": len(splits),
            "site_ids_attribues": sum(record["site_id"] is not None for record in records),
        },
        "canonical_site_count": None,
        "canonical_count_status": "en_attente_revue_rapprochements_separations",
        "dossiers_pilotes_hors_corpus_principal": supplemental,
        "rapprochements_candidats": matches,
        "separations_candidates": splits,
        "dossiers": records,
    }


def build_summary(
    corpus: Mapping[str, Any],
    classification_report: Mapping[str, Any],
    anomalies: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    records = corpus["dossiers"]
    return {
        "schema_version": "1.0",
        "generated_at": corpus["generated_at"],
        "corpus_version": corpus["corpus_version"],
        "counts": corpus["counts"],
        "classifications": {
            "version": corpus["classifications_version"],
            "denominations_total": classification_report["denominations"]["total"],
            "denominations_resolues": classification_report["denominations"]["resolved"],
            "couverture_resolue_pourcent": classification_report["denominations"][
                "resolved_percent"
            ],
            "termes_inconnus": classification_report["denominations"]["unknown_terms"],
        },
        "checks": {
            "expected_319_dossiers": len(records) == 319,
            "unique_references": len({row["dossier_reference"] for row in records}) == 319,
            "official_pilot_29": sum(row["origine"] == "pilote_30" for row in records)
            == 29,
            "first_50": sum(row["origine"] == "phase8_lot1_50" for row in records)
            == 50,
            "remaining_240": sum(
                row["origine"] == "phase8_restant_officiel" for row in records
            )
            == 240,
            "all_have_source": all(row["sources"] for row in records),
            "all_have_classified_content": all(
                row["activites"] or row["composants_non_productifs_source"]
                for row in records
            ),
            "all_terms_resolved": not classification_report["denominations"][
                "unknown_terms"
            ],
            "uniform_record_structure": len({tuple(sorted(row)) for row in records}) == 1,
        },
        "anomaly_count": len(anomalies),
        "canonical_site_count": None,
        "next_step": "revoir_les_rapprochements_et_separations_puis_attribuer_les_site_id",
    }


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(fields))
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(
    corpus: Mapping[str, Any],
    classification_report: Mapping[str, Any],
    *,
    output: Path,
    summary: Path,
    csv_path: Path,
    matches: Path,
    splits: Path,
    anomalies_path: Path,
    classification_path: Path,
    report_path: Path,
) -> dict[str, Any]:
    anomaly_rows = _anomalies(
        corpus["dossiers"], corpus["dossiers_pilotes_hors_corpus_principal"]
    )
    summary_payload = build_summary(corpus, classification_report, anomaly_rows)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(corpus, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    for path, payload in (
        (summary, summary_payload),
        (classification_path, classification_report),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    rows = flat_rows(corpus)
    for row, record in zip(rows, corpus["dossiers"], strict=True):
        row["type_dossier_source"] = record["type_dossier_source"]
        row["composants_non_productifs_source"] = " | ".join(
            item["libelle_source"]
            for item in record["composants_non_productifs_source"]
        )
    _write_csv(csv_path, rows, list(rows[0]))
    _write_csv(
        matches,
        corpus["rapprochements_candidats"],
        ["reference_1", "reference_2", "origines", "motifs", "distance_m", "decision"],
    )
    _write_csv(
        splits,
        corpus["separations_candidates"],
        [
            "dossier_reference",
            "titre_source",
            "motifs",
            "communes_source",
            "insee_source",
            "decision",
        ],
    )
    _write_csv(
        anomalies_path,
        anomaly_rows,
        ["dossier_reference", "type", "gravite", "traitement"],
    )
    counts = corpus["counts"]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "\n".join(
            [
                "# Phase 8 — Corpus commun des 319 dossiers",
                "",
                "## Résultat",
                "",
                "Les 319 références officielles sont désormais présentes dans un format commun.",
                "Ce total décrit des dossiers sources, pas encore le nombre définitif de sites.",
                "",
                f"- {counts['activites']} activités structurées ;",
                f"- {counts['dossiers_multi_activites']} dossiers multi-activités ;",
                f"- {counts['dossiers_multi_secteurs']} dossiers multi-secteurs ;",
                f"- {counts['dossiers_composants_non_productifs']} dossiers décrivent un "
                "composant non productif à relier à un site industriel ;",
                f"- {counts['rapprochements_a_verifier']} paires à rapprocher ou écarter ;",
                f"- {counts['separations_a_verifier']} dossiers à examiner pour une séparation ;",
                "- 100 % des dénominations sont soit classées comme activité, soit identifiées "
                "comme composant non productif.",
                "",
                "## Correction de périmètre",
                "",
                "`IA00061060`, présent dans les 30 pilotes, n'appartient pas à l'énumération "
                "officielle actuelle. Il reste conservé dans le corpus pilote enrichi, mais n'est "
                "pas compté parmi les 319 dossiers officiels. Il a donc fallu traiter 240, et non "
                "239, références officielles restantes.",
                "",
                "## Limite actuelle",
                "",
                "Aucun rapprochement ni découpage n'est appliqué automatiquement. Le nombre de "
                "sites canoniques restera inconnu jusqu'à la revue des deux files dédiées.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return summary_payload


def load_and_build(args: argparse.Namespace) -> dict[str, Any]:
    enumeration = json.loads(args.enumeration.read_text(encoding="utf-8"))
    pilot_corpus = json.loads(args.pilot_corpus.read_text(encoding="utf-8"))
    pilot_manifest = json.loads(args.pilot_manifest.read_text(encoding="utf-8"))
    first_manifest = json.loads(args.first_manifest.read_text(encoding="utf-8"))
    remaining_manifest = json.loads(args.remaining_manifest.read_text(encoding="utf-8"))
    classifications = load_classifications(args.classifications)
    pilot_notices = load_pop_manifest_sample(args.pilot_manifest)
    first_records = load_lot_records(first_manifest)
    remaining_records = load_lot_records(remaining_manifest)
    corpus = build_corpus_319(
        official_references=enumeration["references"],
        pilot_corpus=pilot_corpus,
        pilot_notices=pilot_notices,
        first_records=first_records,
        remaining_records=remaining_records,
        pilot_paths=_manifest_paths(pilot_manifest),
        first_paths=_manifest_paths(first_manifest),
        remaining_paths=_manifest_paths(remaining_manifest),
        classifications=classifications,
    )
    official_notice_map = {
        str(notice["REF"]): notice
        for notice in [*pilot_notices, *first_records, *remaining_records]
        if str(notice["REF"]) in set(enumeration["references"])
    }
    classification_report = classify_pop_records(
        [official_notice_map[reference] for reference in enumeration["references"]],
        classifications,
    )
    return write_outputs(
        corpus,
        classification_report,
        output=args.output,
        summary=args.summary,
        csv_path=args.csv,
        matches=args.matches,
        splits=args.splits,
        anomalies_path=args.anomalies,
        classification_path=args.classification_report,
        report_path=args.report,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--enumeration", type=Path, default=DEFAULT_ENUMERATION)
    parser.add_argument("--pilot-corpus", type=Path, default=DEFAULT_PILOT_CORPUS)
    parser.add_argument("--pilot-manifest", type=Path, default=DEFAULT_PILOT_MANIFEST)
    parser.add_argument("--first-manifest", type=Path, default=DEFAULT_FIRST_MANIFEST)
    parser.add_argument("--remaining-manifest", type=Path, default=DEFAULT_REMAINING_MANIFEST)
    parser.add_argument("--classifications", type=Path, default=Path("config/classifications.yml"))
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--matches", type=Path, default=DEFAULT_MATCHES)
    parser.add_argument("--splits", type=Path, default=DEFAULT_SPLITS)
    parser.add_argument("--anomalies", type=Path, default=DEFAULT_ANOMALIES)
    parser.add_argument(
        "--classification-report", type=Path, default=DEFAULT_CLASSIFICATION
    )
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    arguments = parser.parse_args()
    print(json.dumps(load_and_build(arguments), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
