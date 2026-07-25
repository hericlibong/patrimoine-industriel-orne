"""Valide le socle narratif et visuel V1 sans produire de contenu éditorial."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

import duckdb


DEFAULT_CORPUS = Path("data/processed/corpus_complet_v1.json")
DEFAULT_RECITS = Path("data/exports/recits_sites_v1.csv")
DEFAULT_MEDIAS = Path("data/exports/medias_sites_v1.csv")
DEFAULT_REVIEW = Path("data/exports/revue_editoriale_sites_v1.csv")
DEFAULT_DATABASE = Path("data/processed/patrimoine_orne_corpus_complet_v1.duckdb")
DEFAULT_REPORT = Path("reports/quality/phase9_validation_narratif_visuel.json")
DEFAULT_REPORT_MARKDOWN = Path("reports/quality/phase9_validation_narratif_visuel.md")


def optional(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def text_hash(value: str | None) -> str | None:
    return hashlib.sha256(value.encode("utf-8")).hexdigest() if value else None


def validate(
    corpus_path: Path,
    recits_path: Path,
    medias_path: Path,
    review_path: Path,
    database_path: Path,
) -> dict[str, Any]:
    corpus = json.loads(corpus_path.read_text(encoding="utf-8"))
    source_sites = {site["site_id"]: site for site in corpus["sites"]}
    recits = load_csv(recits_path)
    medias = load_csv(medias_path)
    review = load_csv(review_path)
    source_ids = set(source_sites)
    recit_ids = {row["site_id"] for row in recits}
    review_ids = {row["site_id"] for row in review}
    media_ids = {row["site_id"] for row in medias}
    errors: list[str] = []

    if len(source_ids) != 318:
        errors.append(f"corpus source : {len(source_ids)} sites au lieu de 318")
    if len(recits) != 318 or recit_ids != source_ids:
        errors.append("concordance entre corpus et récits invalide")
    if len(review) != 318 or review_ids != source_ids:
        errors.append("concordance entre corpus et revue éditoriale invalide")
    if media_ids - source_ids:
        errors.append("un média est relié à un site absent du corpus")

    histories_expected = 0
    histories_preserved = 0
    descriptions_expected = 0
    descriptions_preserved = 0
    for recit in recits:
        source = source_sites.get(recit["site_id"])
        if source is None:
            continue
        for field, expected_counter, preserved_counter in (
            ("historique_source", "history", "history"),
            ("description_source", "description", "description"),
        ):
            value = optional(source.get(field))
            if value:
                if expected_counter == "history":
                    histories_expected += 1
                else:
                    descriptions_expected += 1
                if (
                    optional(recit.get(field)) == value
                    and recit.get(f"{field}_sha256") == text_hash(value)
                ):
                    if preserved_counter == "history":
                        histories_preserved += 1
                    else:
                        descriptions_preserved += 1
                else:
                    errors.append(f"texte source perdu ou modifié : {recit['reference_ia']}:{field}")

    required_media = (
        "media_id",
        "site_id",
        "reference_ia",
        "source_id",
        "media_reference",
        "url_media",
        "url_notice_source",
        "statut_droits_code",
        "statut_autorisation_code",
        "usage_media_code",
    )
    media_without_provenance = sum(
        any(not optional(row.get(field)) for field in required_media) for row in medias
    )
    invalid_rights = sum(
        row.get("statut_droits_code") not in {"protege", "inconnus"} for row in medias
    )
    public_media = sum(
        row.get("usage_media_code") == "publication_autorisee" for row in medias
    )
    invalid_review = sum(
        row.get("statut_revue_code") != "a_examiner" for row in review
    )
    if media_without_provenance:
        errors.append(f"{media_without_provenance} médias sans provenance complète")
    if invalid_rights:
        errors.append(f"{invalid_rights} médias sans statut de droits valide")
    if public_media:
        errors.append(f"{public_media} médias publiables sans validation de phase")
    if invalid_review:
        errors.append(f"{invalid_review} décisions éditoriales automatiques détectées")

    connection = duckdb.connect(str(database_path), read_only=True)
    try:
        tables = {
            name: int(connection.execute(f"SELECT count(*) FROM {name}").fetchone()[0])
            for name in ("sites", "recits_sites", "medias", "revue_editoriale_sites")
        }
    finally:
        connection.close()
    if tables != {"sites": 318, "recits_sites": 318, "medias": 1900, "revue_editoriale_sites": 318}:
        errors.append(f"effectifs DuckDB inattendus : {tables}")

    rights = Counter(row["statut_droits_code"] for row in medias)
    return {
        "schema_version": "1.0",
        "date_validation": date.today().isoformat(),
        "effectifs": {
            "sites": len(source_ids),
            "recits": len(recits),
            "medias": len(medias),
            "revues_editoriales": len(review),
            "duckdb": tables,
        },
        "textes_sources": {
            "historiques_attendus": histories_expected,
            "historiques_conserves": histories_preserved,
            "descriptions_attendues": descriptions_expected,
            "descriptions_conservees": descriptions_preserved,
        },
        "medias": {
            "avec_provenance_et_statut": len(medias) - media_without_provenance,
            "sans_provenance_complete": media_without_provenance,
            "droits": dict(sorted(rights.items())),
            "publication_automatique": public_media,
        },
        "relecture_editoriale": {
            "sites_a_examiner": len(review) - invalid_review,
            "decisions_automatiques": invalid_review,
        },
        "erreurs": errors,
        "decision": "socle_narratif_visuel_v1_approuve" if not errors else "validation_echouee",
    }


def write_reports(json_path: Path, markdown_path: Path, result: dict[str, Any]) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    texts = result["textes_sources"]
    media = result["medias"]
    markdown_path.write_text(
        "\n".join(
            [
                "# Validation du socle narratif et visuel V1",
                "",
                f"Date : {result['date_validation']}",
                "",
                "## Contrôles",
                "",
                f"- sites, récits et revues éditoriales : **{result['effectifs']['sites']}** chacun ;",
                f"- historiques sources conservés : **{texts['historiques_conserves']} / {texts['historiques_attendus']}** ;",
                f"- descriptions sources conservées : **{texts['descriptions_conservees']} / {texts['descriptions_attendues']}** ;",
                f"- médias avec provenance et statut : **{media['avec_provenance_et_statut']} / {result['effectifs']['medias']}** ;",
                f"- médias publiables automatiquement : **{media['publication_automatique']}** ;",
                f"- décisions éditoriales automatiques : **{result['relecture_editoriale']['decisions_automatiques']}**.",
                "",
                "## Décision",
                "",
                "Le socle conserve les textes sources disponibles, relie les médias à leur provenance "
                "et maintient les décisions de récit et de publication sous contrôle humain.",
                "",
                f"Décision : **{result['decision']}**.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--recits", type=Path, default=DEFAULT_RECITS)
    parser.add_argument("--medias", type=Path, default=DEFAULT_MEDIAS)
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--report-markdown", type=Path, default=DEFAULT_REPORT_MARKDOWN)
    args = parser.parse_args()
    result = validate(args.corpus, args.recits, args.medias, args.review, args.database)
    write_reports(args.report, args.report_markdown, result)
    if result["erreurs"]:
        raise SystemExit("; ".join(result["erreurs"]))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
