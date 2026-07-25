"""Qualifie prudemment les droits et usages des métadonnées médias V1."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from collections.abc import Mapping, Sequence
from datetime import date
from pathlib import Path
from typing import Any

import duckdb

from patrimoine_orne.export.corpus_complet_v1 import stable_uuid
from patrimoine_orne.export.medias_v1 import (
    DEFAULT_CSV as DEFAULT_MEDIA_CSV,
    DEFAULT_DATABASE,
    DEFAULT_PARQUET as DEFAULT_MEDIA_PARQUET,
    MEDIA_FIELDS,
    write_csv,
    write_database,
)


DEFAULT_REGISTRY = Path("data/exports/registre_autorisations_medias_v1.csv")
DEFAULT_REPORT = Path("reports/quality/phase9_droits_medias.json")
DEFAULT_REPORT_MARKDOWN = Path("reports/quality/phase9_droits_medias.md")
POP_CGU_URL = "https://pop.culture.gouv.fr/conditions-generales-utilisation"
POP_OPEN_DATA_URL = "https://pop.culture.gouv.fr/donnees-ouvertes"
POP_CONTACT = "pop@culture.gouv.fr"

REGISTRY_FIELDS = (
    "demande_autorisation_id",
    "media_id",
    "source_id",
    "media_reference",
    "site_ids",
    "references_ia",
    "statut_droits_code",
    "statut_autorisation_code",
    "publication_publique_code",
    "contact_propose",
    "credit_a_conserver",
    "motif_demande",
    "preuve_droits_url",
    "demande_envoyee_le",
    "reponse_recue_le",
    "autorisation_expire_le",
    "conditions_reponse",
    "notes",
)

REGISTRY_JSON_FIELDS = {"site_ids", "references_ia"}


def _text(value: Any) -> str | None:
    if value is None:
        return None
    original = str(value)
    return original if original.strip() else None


def load_media_rows(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows = []
        for raw in csv.DictReader(stream):
            row = dict(raw)
            row["image_principale_source"] = (
                str(row["image_principale_source"]).casefold() == "true"
            )
            row["metadonnees_source"] = json.loads(row["metadonnees_source"])
            for field in MEDIA_FIELDS:
                if field not in {"image_principale_source", "metadonnees_source"}:
                    row[field] = _text(row.get(field))
            rows.append(row)
    return rows


def qualify_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    qualified = []
    for raw in rows:
        row = dict(raw)
        has_credit = bool(_text(row.get("credit_source")))
        if has_credit:
            row["statut_droits_code"] = "protege"
            row["usage_media_code"] = "prototype_prive"
            row["conditions_autorisation"] = (
                "Aperçu distant crédité admis seulement dans un prototype privé ; "
                "publication publique interdite sans autorisation documentée."
            )
        else:
            row["statut_droits_code"] = "inconnus"
            row["usage_media_code"] = "reference_interne"
            row["conditions_autorisation"] = (
                "Référence interne seulement ; crédit et droits à confirmer avant "
                "tout aperçu ou publication."
            )
        row["statut_autorisation_code"] = "a_demander"
        row["licence_nom"] = None
        row["licence_url"] = None
        row["preuve_droits_url"] = POP_CGU_URL
        qualified.append(row)
    return qualified


def authorization_registry(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_media: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        by_media[str(row["media_id"])].append(row)
    registry = []
    for media_id, relations in sorted(by_media.items()):
        first = relations[0]
        credit = _text(first.get("credit_source"))
        needs_credit_completion = credit is None
        registry.append(
            {
                "demande_autorisation_id": stable_uuid(
                    "demande_autorisation_media", media_id
                ),
                "media_id": media_id,
                "source_id": first["source_id"],
                "media_reference": first["media_reference"],
                "site_ids": sorted({str(row["site_id"]) for row in relations}),
                "references_ia": sorted(
                    {str(row["reference_ia"]) for row in relations}
                ),
                "statut_droits_code": first["statut_droits_code"],
                "statut_autorisation_code": "a_demander",
                "publication_publique_code": "non_autorisee",
                "contact_propose": POP_CONTACT,
                "credit_a_conserver": (
                    credit
                    if credit is not None
                    else "À confirmer — POP / Mémoire et référence du média à conserver"
                ),
                "motif_demande": (
                    "Autorisation de publication publique à demander ; "
                    "réutilisation visuelle non déduite de la seule consultation POP."
                ),
                "preuve_droits_url": POP_CGU_URL,
                "demande_envoyee_le": None,
                "reponse_recue_le": None,
                "autorisation_expire_le": None,
                "conditions_reponse": None,
                "notes": (
                    "Crédit à compléter avant toute publication."
                    if needs_credit_completion
                    else None
                ),
            }
        )
    return registry


def _serialize(row: Mapping[str, Any], json_fields: set[str], fields: Sequence[str]) -> dict[str, Any]:
    return {
        field: (
            json.dumps(row[field], ensure_ascii=False, sort_keys=True)
            if field in json_fields
            else row[field]
        )
        for field in fields
    }


def write_registry(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=REGISTRY_FIELDS)
        writer.writeheader()
        writer.writerows(
            _serialize(row, REGISTRY_JSON_FIELDS, REGISTRY_FIELDS) for row in rows
        )


def write_registry_database(path: Path, registry_path: Path) -> int:
    connection = duckdb.connect(str(path), read_only=False)
    try:
        connection.execute("BEGIN TRANSACTION")
        connection.execute("DROP TABLE IF EXISTS demandes_autorisation_medias")
        escaped_path = registry_path.resolve().as_posix().replace("'", "''")
        connection.execute(
            "CREATE TABLE demandes_autorisation_medias AS "
            f"SELECT * FROM read_csv_auto('{escaped_path}')"
        )
        connection.execute("COMMIT")
        return int(
            connection.execute(
                "SELECT count(*) FROM demandes_autorisation_medias"
            ).fetchone()[0]
        )
    except Exception:
        try:
            connection.execute("ROLLBACK")
        except duckdb.Error:
            pass
        raise
    finally:
        connection.close()


def quality_report(
    rows: Sequence[Mapping[str, Any]], registry: Sequence[Mapping[str, Any]], registry_count: int
) -> dict[str, Any]:
    rights = defaultdict(int)
    usages = defaultdict(int)
    for row in rows:
        rights[str(row["statut_droits_code"])] += 1
        usages[str(row["usage_media_code"])] += 1
    errors = []
    if len(rows) != 1900:
        errors.append(f"{len(rows)} médias au lieu de 1900")
    if any(row["statut_autorisation_code"] != "a_demander" for row in rows):
        errors.append("un média ne possède pas le statut d'autorisation prudent")
    if any(row["usage_media_code"] == "publication_autorisee" for row in rows):
        errors.append("un média est déclaré publiable sans autorisation")
    if registry_count != len(registry):
        errors.append("le registre DuckDB diffère du registre CSV")
    return {
        "schema_version": "1.0",
        "date_validation": date.today().isoformat(),
        "medias": len(rows),
        "statuts_droits": dict(sorted(rights.items())),
        "usages_actuels": dict(sorted(usages.items())),
        "publication_autorisee": 0,
        "medias_necessitant_autorisation": len(rows),
        "medias_droits_inconnus": rights["inconnus"],
        "medias_droits_proteges": rights["protege"],
        "registre_demandes": len(registry),
        "registre_demandes_duckdb": registry_count,
        "credits_sources_a_conserver": sum(
            bool(_text(row.get("credit_source"))) for row in rows
        ),
        "credits_a_completer": sum(
            not bool(_text(row.get("credit_source"))) for row in rows
        ),
        "erreurs": errors,
        "decision": "droits_medias_v1_valides" if not errors else "validation_echouee",
    }


def write_reports(
    json_path: Path, markdown_path: Path, report: Mapping[str, Any]
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        "\n".join(
            [
                "# Qualification des droits et usages des médias V1",
                "",
                f"Date : {report['date_validation']}",
                "",
                "## Décision d'usage",
                "",
                "| Niveau | Règle appliquée |",
                "|---|---|",
                "| Consultation interne | Métadonnées, liens et crédits seulement pour les 1 900 médias. |",
                "| Prototype privé | Aperçu distant crédité seulement pour les médias avec crédit source ; aucune copie locale. |",
                "| Publication publique | Aucune image autorisée par défaut ; autorisation ou licence documentée requise. |",
                "",
                "## Résultats",
                "",
                f"- médias avec droits explicitement protégés : **{report['medias_droits_proteges']}** ;",
                f"- médias aux droits inconnus : **{report['medias_droits_inconnus']}** ;",
                f"- médias nécessitant une autorisation avant publication : **{report['medias_necessitant_autorisation']}** ;",
                f"- médias publiables automatiquement : **{report['publication_autorisee']}** ;",
                f"- crédits sources à conserver : **{report['credits_sources_a_conserver']}** ;",
                f"- crédits à compléter : **{report['credits_a_completer']}** ;",
                f"- lignes du registre de demandes : **{report['registre_demandes']}**.",
                "",
                "## Sources et limites",
                "",
                "- POP distingue les données descriptives des images, qui peuvent être "
                "soumises aux droits de tiers ;",
                "- le registre prépare les demandes mais n'envoie aucun message ;",
                "- aucun média n'est téléchargé ni versionné ;",
                "- cette qualification organise le travail éditorial et ne remplace pas "
                "une analyse juridique d'un cas particulier.",
                "",
                f"Références : {POP_CGU_URL} ; {POP_OPEN_DATA_URL}.",
                "",
                f"Décision : **{report['decision']}**.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def produce(
    media_csv: Path = DEFAULT_MEDIA_CSV,
    database: Path = DEFAULT_DATABASE,
    media_parquet: Path = DEFAULT_MEDIA_PARQUET,
    registry_path: Path = DEFAULT_REGISTRY,
    report_path: Path = DEFAULT_REPORT,
    report_markdown_path: Path = DEFAULT_REPORT_MARKDOWN,
) -> dict[str, Any]:
    qualified = qualify_rows(load_media_rows(media_csv))
    write_csv(media_csv, qualified)
    media_count = write_database(database, media_csv, media_parquet)
    if media_count != len(qualified):
        raise ValueError("la table medias ne contient pas tous les médias qualifiés")
    registry = authorization_registry(qualified)
    write_registry(registry_path, registry)
    registry_count = write_registry_database(database, registry_path)
    report = quality_report(qualified, registry, registry_count)
    write_reports(report_path, report_markdown_path, report)
    if report["erreurs"]:
        raise ValueError("; ".join(report["erreurs"]))
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--media-csv", type=Path, default=DEFAULT_MEDIA_CSV)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--media-parquet", type=Path, default=DEFAULT_MEDIA_PARQUET)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--report-markdown", type=Path, default=DEFAULT_REPORT_MARKDOWN)
    args = parser.parse_args()
    report = produce(
        media_csv=args.media_csv,
        database=args.database,
        media_parquet=args.media_parquet,
        registry_path=args.registry,
        report_path=args.report,
        report_markdown_path=args.report_markdown,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
