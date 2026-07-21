"""Validation finale du corpus pilote de la phase 5."""

from __future__ import annotations

import argparse
import csv
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

import yaml


REVIEW_COLUMNS = (
    "personne",
    "reference",
    "nombre_de_phases",
    "activites_codes",
    "secteurs_codes",
    "installations_codes",
    "mode_chronologique",
    "conservation_code",
    "usages_actuels",
    "accessibilite_code",
    "fiabilite_code",
    "statut_protection",
    "commentaire",
)


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manual_reviews(
    corpus: Mapping[str, Any], review_config: Mapping[str, Any]
) -> list[str]:
    references = {str(site["reference_ia"]) for site in corpus["sites"]}
    reviews = review_config["fiches"]
    review_references = [str(review["reference"]) for review in reviews]
    errors: list[str] = []
    if len(reviews) != 30 or set(review_references) != references:
        errors.append("le contrôle manuel ne couvre pas exactement les 30 fiches")
    if len(review_references) != len(set(review_references)):
        errors.append("une fiche possède plusieurs contrôles manuels")
    required = {
        "identite",
        "commune",
        "activites",
        "chronologie",
        "situation_actuelle",
        "provenance",
        "decision",
    }
    for review in reviews:
        missing = sorted(field for field in required if not review.get(field))
        if missing:
            errors.append(f"{review['reference']} : contrôles absents {missing}")
        if not str(review.get("decision", "")).startswith("retenue"):
            errors.append(f"{review['reference']} : décision de pilote non validée")
    return errors


def validate_provenance(corpus: Mapping[str, Any]) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    counts = {
        "sites_avec_notice_principale": 0,
        "sites_avec_source_commune_actuelle": 0,
        "activites_avec_source": 0,
        "situations_actuelles_renseignees_avec_source": 0,
        "protections_avec_source": 0,
        "objets_avec_source": 0,
    }
    for site in corpus["sites"]:
        reference = str(site["reference_ia"])
        sources = site.get("sources", [])
        if any(
            source.get("source_id") == "pop_merimee"
            and source.get("reference") == reference
            and source.get("role") == "notice_principale"
            for source in sources
        ):
            counts["sites_avec_notice_principale"] += 1
        else:
            errors.append(f"{reference} : notice principale sans provenance")
        if any(
            source.get("source_id") == "api_geo"
            and source.get("reference") == site.get("commune_actuelle_code_insee")
            for source in sources
        ):
            counts["sites_avec_source_commune_actuelle"] += 1
        else:
            errors.append(f"{reference} : commune actuelle sans provenance")

        for activity in site.get("activites", []):
            if activity.get("source_id") and activity.get("reference_source"):
                counts["activites_avec_source"] += 1
            else:
                errors.append(
                    f"{reference} : activité {activity.get('libelle_source')} sans source"
                )

        state = site["situation_actuelle"]
        has_information = (
            state.get("conservation_code") != "inconnu"
            or state.get("accessibilite_code") != "inconnu"
            or state.get("usages") != ["inconnu"]
        )
        if has_information:
            if state.get("source_url") and state.get("source_id"):
                counts["situations_actuelles_renseignees_avec_source"] += 1
            else:
                errors.append(f"{reference} : situation actuelle renseignée sans source")
        elif not state.get("note"):
            errors.append(f"{reference} : situation inconnue sans justification")

        protection = site.get("protection_mh_reference")
        if protection:
            if any(
                source.get("reference") == protection
                and source.get("role") == "protection_confirmee"
                for source in sources
            ):
                counts["protections_avec_source"] += 1
            else:
                errors.append(f"{reference} : protection {protection} sans source")

    for item in corpus.get("objets_techniques", []):
        if item.get("source_id") == "pop_palissy" and item.get("reference_palissy"):
            counts["objets_avec_source"] += 1
        else:
            errors.append("objet technique sans référence Palissy")
    return errors, counts


def validate_double_sample(
    corpus: Mapping[str, Any], review_config: Mapping[str, Any]
) -> list[str]:
    references = {str(site["reference_ia"]) for site in corpus["sites"]}
    double = review_config["double_classement"]
    simple = [str(item["reference"]) for item in double["sous_echantillon"]["simples"]]
    ambiguous = [
        str(item["reference"]) for item in double["sous_echantillon"]["ambigus"]
    ]
    errors: list[str] = []
    if len(simple) != 3 or len(ambiguous) != 3:
        errors.append("le double classement doit contenir trois cas simples et trois ambigus")
    if len(set(simple + ambiguous)) != 6:
        errors.append("le sous-échantillon de double classement contient un doublon")
    if not set(simple + ambiguous).issubset(references):
        errors.append("le double classement référence un site absent du pilote")
    return errors


def write_review_templates(review_config: Mapping[str, Any], directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    double = review_config["double_classement"]["sous_echantillon"]
    references = [item["reference"] for item in double["simples"] + double["ambigus"]]
    for label in ("a", "b"):
        path = directory / f"classement_{label}.csv"
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=REVIEW_COLUMNS)
            writer.writeheader()
            for reference in references:
                row = {column: "" for column in REVIEW_COLUMNS}
                row["personne"] = label.upper()
                row["reference"] = reference
                writer.writerow(row)


def build_validation_report(
    corpus: Mapping[str, Any], review_config: Mapping[str, Any]
) -> dict[str, Any]:
    manual_errors = validate_manual_reviews(corpus, review_config)
    provenance_errors, provenance_counts = validate_provenance(corpus)
    sample_errors = validate_double_sample(corpus, review_config)
    errors = manual_errors + provenance_errors + sample_errors
    double_status = str(review_config["double_classement"]["statut"])
    return {
        "schema_version": "1.0",
        "date_controle": str(review_config["date_controle"]),
        "corpus_checks_passed": not errors,
        "phase5_complete": not errors,
        "double_classement_status": double_status,
        "errors": errors,
        "counts": {
            "sites": len(corpus["sites"]),
            "fiches_controlees_manuellement": len(review_config["fiches"]),
            "sites_double_classement_prepares": 6,
            "activites": sum(len(site["activites"]) for site in corpus["sites"]),
            "objets_techniques": len(corpus.get("objets_techniques", [])),
            "anomalies": len(corpus.get("anomalies", [])),
            **provenance_counts,
        },
        "blocking_items": [],
        "accepted_limitations": [
            "la reproductibilité entre deux lecteurs humains n'est pas mesurée",
            "quelques classifications interprétatives pourront être révisées",
        ],
    }


def build_v1_corpus(
    corpus: Mapping[str, Any], report: Mapping[str, Any]
) -> dict[str, Any]:
    result = deepcopy(corpus)
    result["schema_version"] = "1.0"
    result["corpus_version"] = "1.0"
    result["status"] = "phase5_validee" if report["phase5_complete"] else "invalide"
    result["validation"] = {
        "date": report["date_controle"],
        "controle_manuel_30_fiches": True,
        "provenance_complete": report["corpus_checks_passed"],
        "double_classement_humain": report["double_classement_status"],
    }
    return result


def write_json(value: Mapping[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--corpus", type=Path, default=Path("data/interim/phase5_pilot_enriched.json")
    )
    parser.add_argument(
        "--reviews", type=Path, default=Path("config/validation_pilote.yml")
    )
    parser.add_argument(
        "--output", type=Path, default=Path("data/pilot/corpus_pilote_v1.json")
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/quality/phase5_validation_finale.json"),
    )
    parser.add_argument(
        "--review-directory", type=Path, default=Path("data/review/phase5")
    )
    args = parser.parse_args()
    corpus = load_json(args.corpus)
    review_config = load_yaml(args.reviews)
    report = build_validation_report(corpus, review_config)
    write_json(build_v1_corpus(corpus, report), args.output)
    write_json(report, args.report)
    write_review_templates(review_config, args.review_directory)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    if not report["corpus_checks_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
