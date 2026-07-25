"""Produit une revue éditoriale factuelle, sans sélectionner de récit final."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from datetime import date
from pathlib import Path
from typing import Any

import duckdb


DEFAULT_RECITS = Path("data/exports/recits_sites_v1.csv")
DEFAULT_MEDIAS = Path("data/exports/medias_sites_v1.csv")
DEFAULT_DATABASE = Path("data/processed/patrimoine_orne_corpus_complet_v1.duckdb")
DEFAULT_CSV = Path("data/exports/revue_editoriale_sites_v1.csv")
DEFAULT_PARQUET = Path("data/exports/revue_editoriale_sites_v1.parquet")
DEFAULT_REPORT = Path("reports/quality/phase9_revue_editoriale.json")
DEFAULT_REPORT_MARKDOWN = Path("reports/quality/phase9_revue_editoriale.md")

FIELDS = (
    "site_id",
    "reference_ia",
    "nom_site",
    "historique_present",
    "historique_longueur_caracteres",
    "description_presente",
    "description_longueur_caracteres",
    "siecles_nombre",
    "periodes_documentaires_nombre",
    "periodes_activite_nombre",
    "activites_successives_nombre",
    "richesse_historique_score",
    "richesse_historique_code",
    "chronologie_disponible",
    "medias_nombre",
    "medias_credits_nombre",
    "medias_legendes_nombre",
    "medias_marques_principaux_nombre",
    "media_principal_candidat_reference",
    "media_principal_candidat_url",
    "media_principal_candidat_statut_code",
    "richesse_iconographique_score",
    "richesse_iconographique_code",
    "combinaison_editoriale_code",
    "besoin_recherche_historique",
    "besoin_recherche_visuelle",
    "besoin_recherche_complementaire",
    "motifs_recherche",
    "statut_revue_code",
)

JSON_FIELDS = {"motifs_recherche"}


def _optional(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _json(value: str | None) -> list[Any]:
    if not value:
        return []
    parsed = json.loads(value)
    return parsed if isinstance(parsed, list) else []


def load_recits(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows = []
        for raw in csv.DictReader(stream):
            row = dict(raw)
            for field in (
                "siecles_source",
                "periodes_source_codes",
                "periodes_activite_codes",
                "activites_successives",
            ):
                row[field] = _json(row.get(field))
            rows.append(row)
    return rows


def load_medias(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows = []
        for raw in csv.DictReader(stream):
            row = dict(raw)
            row["image_principale_source"] = (
                str(row["image_principale_source"]).casefold() == "true"
            )
            rows.append(row)
    return rows


def history_score(
    history: str | None,
    description: str | None,
    centuries: Sequence[Any],
    source_periods: Sequence[Any],
    activity_periods: Sequence[Any],
    activities: Sequence[Any],
) -> int:
    return (
        (2 if history else 0)
        + (1 if description else 0)
        + (1 if centuries else 0)
        + (1 if source_periods or activity_periods else 0)
        + (1 if len(activities) > 1 else 0)
    )


def history_label(score: int) -> str:
    if score >= 5:
        return "forte"
    if score >= 3:
        return "moyenne"
    if score:
        return "faible"
    return "absente"


def icon_score(media: Sequence[Mapping[str, Any]]) -> int:
    if not media:
        return 0
    credits = sum(bool(_optional(row.get("credit_source"))) for row in media)
    captions = sum(bool(_optional(row.get("legende_source"))) for row in media)
    main = sum(bool(row.get("image_principale_source")) for row in media)
    return min(5, 1 + min(2, credits) + (1 if captions else 0) + (1 if main else 0))


def icon_label(score: int) -> str:
    if score >= 4:
        return "forte"
    if score >= 2:
        return "moyenne"
    if score:
        return "faible"
    return "absente"


def main_candidate(media: Sequence[Mapping[str, Any]]) -> Mapping[str, Any] | None:
    usable = [row for row in media if _optional(row.get("credit_source"))]
    if not usable:
        return None
    return sorted(
        usable,
        key=lambda row: (
            not bool(row.get("image_principale_source")),
            not bool(_optional(row.get("legende_source"))),
            str(row["media_reference"]),
        ),
    )[0]


def build_rows(
    recits: Sequence[Mapping[str, Any]], medias: Sequence[Mapping[str, Any]]
) -> list[dict[str, Any]]:
    media_by_site: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for media in medias:
        media_by_site[str(media["site_id"])].append(media)

    rows = []
    for recit in sorted(recits, key=lambda row: str(row["reference_ia"])):
        history = _optional(recit.get("historique_source"))
        description = _optional(recit.get("description_source"))
        centuries = recit["siecles_source"]
        source_periods = recit["periodes_source_codes"]
        activity_periods = recit["periodes_activite_codes"]
        activities = recit["activites_successives"]
        linked_media = media_by_site[str(recit["site_id"])]
        historical = history_score(
            history, description, centuries, source_periods, activity_periods, activities
        )
        icons = icon_score(linked_media)
        chronology = bool(source_periods or activity_periods or centuries)
        candidate = main_candidate(linked_media)
        motifs = []
        if not history:
            motifs.append("historique_source_absent")
        if not chronology:
            motifs.append("reperes_chronologiques_absents")
        if not linked_media:
            motifs.append("media_absent")
        elif candidate is None:
            motifs.append("media_sans_credit_exploitable")
        needs_history = not history or not chronology
        needs_visual = not linked_media or candidate is None
        combined = (
            "pret_a_examiner"
            if historical >= 3 and chronology and candidate is not None
            else "matiere_partielle"
        )
        rows.append(
            {
                "site_id": recit["site_id"],
                "reference_ia": recit["reference_ia"],
                "nom_site": recit["nom_site"],
                "historique_present": bool(history),
                "historique_longueur_caracteres": len(history or ""),
                "description_presente": bool(description),
                "description_longueur_caracteres": len(description or ""),
                "siecles_nombre": len(centuries),
                "periodes_documentaires_nombre": len(source_periods),
                "periodes_activite_nombre": len(activity_periods),
                "activites_successives_nombre": len(activities),
                "richesse_historique_score": historical,
                "richesse_historique_code": history_label(historical),
                "chronologie_disponible": chronology,
                "medias_nombre": len(linked_media),
                "medias_credits_nombre": sum(
                    bool(_optional(media.get("credit_source"))) for media in linked_media
                ),
                "medias_legendes_nombre": sum(
                    bool(_optional(media.get("legende_source"))) for media in linked_media
                ),
                "medias_marques_principaux_nombre": sum(
                    bool(media.get("image_principale_source")) for media in linked_media
                ),
                "media_principal_candidat_reference": (
                    candidate["media_reference"] if candidate else None
                ),
                "media_principal_candidat_url": candidate["url_media"] if candidate else None,
                "media_principal_candidat_statut_code": (
                    "a_revoir" if candidate else "aucun_candidat"
                ),
                "richesse_iconographique_score": icons,
                "richesse_iconographique_code": icon_label(icons),
                "combinaison_editoriale_code": combined,
                "besoin_recherche_historique": needs_history,
                "besoin_recherche_visuelle": needs_visual,
                "besoin_recherche_complementaire": needs_history or needs_visual,
                "motifs_recherche": motifs,
                "statut_revue_code": "a_examiner",
            }
        )
    return rows


def serialized(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        field: (
            json.dumps(row[field], ensure_ascii=False, sort_keys=True)
            if field in JSON_FIELDS
            else row[field]
        )
        for field in FIELDS
    }


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(serialized(row) for row in rows)


def write_database(database: Path, csv_path: Path, parquet_path: Path) -> int:
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    connection = duckdb.connect(str(database), read_only=False)
    try:
        connection.execute("BEGIN TRANSACTION")
        connection.execute("DROP TABLE IF EXISTS revue_editoriale_sites")
        escaped = csv_path.resolve().as_posix().replace("'", "''")
        connection.execute(
            "CREATE TABLE revue_editoriale_sites AS "
            f"SELECT * FROM read_csv_auto('{escaped}')"
        )
        count = int(connection.execute("SELECT count(*) FROM revue_editoriale_sites").fetchone()[0])
        missing = int(
            connection.execute(
                "SELECT count(*) FROM sites WHERE site_id NOT IN "
                "(SELECT site_id FROM revue_editoriale_sites)"
            ).fetchone()[0]
        )
        if count != 318 or missing:
            raise ValueError(f"revue editoriale invalide : {count} lignes, {missing} sites manquants")
        connection.execute("COMMIT")
        target = parquet_path.resolve().as_posix().replace("'", "''")
        connection.execute(
            f"COPY revue_editoriale_sites TO '{target}' (FORMAT PARQUET, COMPRESSION ZSTD)"
        )
        return count
    except Exception:
        try:
            connection.execute("ROLLBACK")
        except duckdb.Error:
            pass
        raise
    finally:
        connection.close()


def report(rows: Sequence[Mapping[str, Any]], database_count: int) -> dict[str, Any]:
    histories = Counter(str(row["richesse_historique_code"]) for row in rows)
    icons = Counter(str(row["richesse_iconographique_code"]) for row in rows)
    combined = sum(row["combinaison_editoriale_code"] == "pret_a_examiner" for row in rows)
    errors = []
    if len(rows) != 318 or database_count != len(rows):
        errors.append("effectif de la revue editoriale invalide")
    if any(row["statut_revue_code"] != "a_examiner" for row in rows):
        errors.append("un site est selectionne automatiquement")
    if any(
        row["media_principal_candidat_statut_code"] == "valide"
        for row in rows
    ):
        errors.append("une image principale est validee automatiquement")
    return {
        "schema_version": "1.0",
        "date_validation": date.today().isoformat(),
        "sites": len(rows),
        "richesse_historique": dict(sorted(histories.items())),
        "richesse_iconographique": dict(sorted(icons.items())),
        "chronologie_disponible": sum(bool(row["chronologie_disponible"]) for row in rows),
        "sites_combinant_histoire_chronologie_medias": combined,
        "candidats_image_principale_a_revoir": sum(
            row["media_principal_candidat_statut_code"] == "a_revoir" for row in rows
        ),
        "recherche_historique_necessaire": sum(
            bool(row["besoin_recherche_historique"]) for row in rows
        ),
        "recherche_visuelle_necessaire": sum(
            bool(row["besoin_recherche_visuelle"]) for row in rows
        ),
        "recherche_complementaire_necessaire": sum(
            bool(row["besoin_recherche_complementaire"]) for row in rows
        ),
        "lignes_duckdb": database_count,
        "erreurs": errors,
        "decision": "revue_editoriale_v1_validee" if not errors else "validation_echouee",
    }


def write_reports(json_path: Path, markdown_path: Path, data: Mapping[str, Any]) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(
        "\n".join(
            [
                "# Revue éditoriale des sites V1",
                "",
                f"Date : {data['date_validation']}",
                "",
                "Cette revue mesure la matière disponible ; elle ne choisit ni récit final ni image publiée.",
                "",
                "## Résultats",
                "",
                f"- sites : **{data['sites']}** ;",
                f"- chronologie disponible : **{data['chronologie_disponible']}** ;",
                f"- sites combinant histoire, chronologie et média candidat : **{data['sites_combinant_histoire_chronologie_medias']}** ;",
                f"- candidats image principale à revoir : **{data['candidats_image_principale_a_revoir']}** ;",
                f"- recherche historique nécessaire : **{data['recherche_historique_necessaire']}** ;",
                f"- recherche visuelle nécessaire : **{data['recherche_visuelle_necessaire']}** ;",
                f"- recherche complémentaire nécessaire : **{data['recherche_complementaire_necessaire']}**.",
                "",
                "## Règles",
                "",
                "- une image candidate est un repère technique, jamais une autorisation de publication ;",
                "- les scores décrivent seulement la couverture documentaire ;",
                "- tous les sites restent au statut `a_examiner`.",
                "",
                f"Décision : **{data['decision']}**.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def produce(
    recits_path: Path = DEFAULT_RECITS,
    medias_path: Path = DEFAULT_MEDIAS,
    database: Path = DEFAULT_DATABASE,
    csv_path: Path = DEFAULT_CSV,
    parquet_path: Path = DEFAULT_PARQUET,
    report_path: Path = DEFAULT_REPORT,
    report_markdown_path: Path = DEFAULT_REPORT_MARKDOWN,
) -> dict[str, Any]:
    rows = build_rows(load_recits(recits_path), load_medias(medias_path))
    write_csv(csv_path, rows)
    database_count = write_database(database, csv_path, parquet_path)
    result = report(rows, database_count)
    write_reports(report_path, report_markdown_path, result)
    if result["erreurs"]:
        raise ValueError("; ".join(result["erreurs"]))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recits", type=Path, default=DEFAULT_RECITS)
    parser.add_argument("--medias", type=Path, default=DEFAULT_MEDIAS)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    args = parser.parse_args()
    print(json.dumps(produce(args.recits, args.medias, args.database), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
