"""Inventorie les métadonnées des médias liés au corpus complet V1."""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
from urllib.parse import unquote
from collections import Counter
from collections.abc import Mapping, Sequence
from datetime import date
from pathlib import Path
from typing import Any

import duckdb

from patrimoine_orne.export.corpus_complet_v1 import stable_uuid


DEFAULT_CORPUS = Path("data/processed/corpus_complet_v1.json")
DEFAULT_DATABASE = Path("data/processed/patrimoine_orne_corpus_complet_v1.duckdb")
DEFAULT_CSV = Path("data/exports/medias_sites_v1.csv")
DEFAULT_PARQUET = Path("data/exports/medias_sites_v1.parquet")
DEFAULT_WITHOUT_MEDIA = Path("reports/quality/phase9_notices_sans_media.csv")
DEFAULT_REPORT = Path("reports/quality/phase9_medias_sites_inventaire.json")
DEFAULT_REPORT_MARKDOWN = Path("reports/quality/phase9_medias_sites_inventaire.md")

MEDIA_FIELDS = (
    "media_site_id",
    "media_id",
    "site_id",
    "reference_ia",
    "source_id",
    "media_reference",
    "type_media_code",
    "url_media",
    "url_fichier_source",
    "url_notice_source",
    "legende_source",
    "auteur_source",
    "credit_source",
    "mention_droits_source",
    "image_principale_source",
    "metadonnees_source",
    "selection_media_code",
    "statut_droits_code",
    "statut_autorisation_code",
    "usage_media_code",
    "licence_nom",
    "licence_url",
    "preuve_droits_url",
    "autorisation_demandee_le",
    "autorisation_repondue_le",
    "autorisation_expire_le",
    "conditions_autorisation",
    "date_consultation",
    "chemin_local",
    "fichier_sha256",
)

JSON_FIELDS = {"metadonnees_source"}


def load_corpus(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        values = [str(item).strip() for item in value if str(item).strip()]
        return " | ".join(values) or None
    original = str(value)
    return original if original.strip() else None


def _consultation_date(site: Mapping[str, Any], corpus: Mapping[str, Any]) -> str:
    match = re.search(r"20\d{2}-\d{2}-\d{2}", str(site.get("notice_brute") or ""))
    if match:
        return match.group(0)
    match = re.search(r"20\d{2}-\d{2}-\d{2}", str(corpus.get("generated_at") or ""))
    return match.group(0) if match else date.today().isoformat()


ASSET_URL_RE = re.compile(
    r"(https://popcorn-prd-perf-assets\.s3\.gra\.io\.cloud\.ovh\.net/"
    r"memoire/(?P<reference>IVR[^/]+)/[^&\"'\s<>]+?\.(?:JPG|JPEG|PNG|TIFF))",
    flags=re.IGNORECASE,
)


def _html_media_notice(raw: str) -> dict[str, Any] | None:
    decoded = unquote(html.unescape(raw))
    entries_by_reference: dict[str, dict[str, Any]] = {}
    for match in ASSET_URL_RE.finditer(decoded):
        reference = match.group("reference")
        entries_by_reference.setdefault(
            reference,
            {
                "ref": reference,
                "url": match.group(1),
                "extraction_format": "html_notice_archivee",
            },
        )
    return {"MEMOIRE": list(entries_by_reference.values())} if entries_by_reference else None


def _raw_notice(site: Mapping[str, Any]) -> tuple[dict[str, Any] | None, str]:
    raw_path = Path(str(site.get("notice_brute") or ""))
    if not raw_path.is_file():
        return None, "notice_brute_introuvable"
    try:
        raw = raw_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None, "notice_brute_illisible"
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        html_notice = _html_media_notice(raw)
        return (
            (html_notice, "notice_html_archivee")
            if html_notice
            else (None, "notice_brute_illisible")
        )
    return (value, "ok") if isinstance(value, dict) else (None, "notice_brute_invalide")


def _media_entries(notice: Mapping[str, Any] | None) -> list[dict[str, Any]]:
    if not notice:
        return []
    value = notice.get("MEMOIRE") or []
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        return []
    return [dict(item) for item in value if isinstance(item, Mapping)]


def _first_media_value(entry: Mapping[str, Any], names: Sequence[str]) -> str | None:
    normalized = {str(key).casefold(): value for key, value in entry.items()}
    for name in names:
        value = _text(normalized.get(name.casefold()))
        if value is not None:
            return value
    return None


def _media_notice_url(reference: str) -> str:
    return f"https://pop.culture.gouv.fr/notice/memoire/{reference}"


def _source_notice_url(site: Mapping[str, Any]) -> str:
    return f"https://pop.culture.gouv.fr/notice/merimee/{site['dossier_reference']}"


def _technical_key(site_id: str, entry: Mapping[str, Any]) -> str:
    return json.dumps(
        {"site_id": site_id, "entry": entry}, ensure_ascii=False, sort_keys=True
    )


def media_rows(
    corpus: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    without_media: list[dict[str, Any]] = []
    duplicate_rows: list[dict[str, Any]] = []
    for site in sorted(corpus["sites"], key=lambda item: item["dossier_reference"]):
        notice, notice_status = _raw_notice(site)
        entries = _media_entries(notice)
        valid_entries = [entry for entry in entries if _text(entry.get("ref"))]
        if not valid_entries:
            if notice is None:
                reason = notice_status
            elif entries:
                reason = "media_sans_reference_exploitable"
            else:
                reason = "aucun_media_dans_la_notice"
            without_media.append(
                {
                    "site_id": site["site_id"],
                    "reference_ia": site["dossier_reference"],
                    "nom_site": site["nom_principal"],
                    "motif": reason,
                }
            )
            continue

        seen: set[str] = set()
        reference_variants: Counter[str] = Counter()
        for entry in valid_entries:
            reference = _text(entry.get("ref"))
            assert reference is not None
            key = _technical_key(site["site_id"], entry)
            if key in seen:
                duplicate_rows.append(
                    {
                        "site_id": site["site_id"],
                        "reference_ia": site["dossier_reference"],
                        "media_reference": reference,
                        "motif": "metadonnees_strictement_identiques",
                    }
                )
                continue
            seen.add(key)
            reference_variants[reference] += 1
            suffix = "" if reference_variants[reference] == 1 else str(reference_variants[reference])
            raw_url = _text(entry.get("url"))
            credit = _first_media_value(entry, ("copy", "credit", "credits"))
            rights = _first_media_value(
                entry, ("droits", "rights", "copyright", "copy")
            )
            rows.append(
                {
                    "media_site_id": stable_uuid(
                        "media_site", site["site_id"], "pop_memoire", reference, suffix
                    ),
                    "media_id": stable_uuid("media", "pop_memoire", reference),
                    "site_id": site["site_id"],
                    "reference_ia": site["dossier_reference"],
                    "source_id": "pop_memoire",
                    "media_reference": reference,
                    "type_media_code": "image_non_qualifiee",
                    "url_media": _media_notice_url(reference),
                    "url_fichier_source": raw_url,
                    "url_notice_source": _source_notice_url(site),
                    "legende_source": _first_media_value(
                        entry, ("name", "legende", "legend", "titre", "title")
                    ),
                    "auteur_source": _first_media_value(
                        entry, ("auteur", "author", "creator", "photographe")
                    ),
                    "credit_source": credit,
                    "mention_droits_source": rights,
                    "image_principale_source": str(entry.get("marq") or "") == "1",
                    "metadonnees_source": entry,
                    "selection_media_code": "non_evalue",
                    "statut_droits_code": "inconnus",
                    "statut_autorisation_code": "non_demandee",
                    "usage_media_code": "metadonnees_seulement",
                    "licence_nom": None,
                    "licence_url": None,
                    "preuve_droits_url": None,
                    "autorisation_demandee_le": None,
                    "autorisation_repondue_le": None,
                    "autorisation_expire_le": None,
                    "conditions_autorisation": None,
                    "date_consultation": _consultation_date(site, corpus),
                    "chemin_local": None,
                    "fichier_sha256": None,
                }
            )
    return rows, without_media, duplicate_rows


def _serialized_row(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        field: (
            json.dumps(row[field], ensure_ascii=False, sort_keys=True)
            if field in JSON_FIELDS
            else row[field]
        )
        for field in MEDIA_FIELDS
    }


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=MEDIA_FIELDS)
        writer.writeheader()
        writer.writerows(_serialized_row(row) for row in rows)


def write_without_media(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ("site_id", "reference_ia", "nom_site", "motif")
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_database(
    path: Path, csv_path: Path, parquet_path: Path
) -> int:
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    connection = duckdb.connect(str(path), read_only=False)
    try:
        connection.execute("BEGIN TRANSACTION")
        connection.execute("DROP TABLE IF EXISTS medias")
        escaped_csv = csv_path.resolve().as_posix().replace("'", "''")
        connection.execute(
            f"CREATE TABLE medias AS SELECT * FROM read_csv_auto('{escaped_csv}')"
        )
        unknown_sites = int(
            connection.execute(
                """
                SELECT count(*) FROM medias
                WHERE site_id NOT IN (SELECT site_id FROM sites)
                """
            ).fetchone()[0]
        )
        duplicate_ids = int(
            connection.execute(
                """
                SELECT count(*) FROM (
                    SELECT media_site_id FROM medias
                    GROUP BY media_site_id HAVING count(*) > 1
                )
                """
            ).fetchone()[0]
        )
        if unknown_sites or duplicate_ids:
            raise ValueError(
                f"Table medias invalide : {unknown_sites} site_id inconnus, "
                f"{duplicate_ids} media_site_id dupliqués."
            )
        connection.execute("COMMIT")
        escaped_path = parquet_path.resolve().as_posix().replace("'", "''")
        connection.execute(
            f"COPY medias TO '{escaped_path}' (FORMAT PARQUET, COMPRESSION ZSTD)"
        )
        return int(connection.execute("SELECT count(*) FROM medias").fetchone()[0])
    except Exception:
        try:
            connection.execute("ROLLBACK")
        except duckdb.Error:
            pass
        raise
    finally:
        connection.close()


def inventory_report(
    corpus: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
    without_media: Sequence[Mapping[str, Any]],
    duplicates: Sequence[Mapping[str, Any]],
    database_count: int,
) -> dict[str, Any]:
    sites_with_media = {row["site_id"] for row in rows}
    corpus_ids = {site["site_id"] for site in corpus["sites"]}
    errors = []
    if len(corpus_ids) != 318:
        errors.append("le corpus source ne contient pas 318 sites")
    if len(sites_with_media) + len(without_media) != len(corpus_ids):
        errors.append("la couverture sites avec ou sans média est incohérente")
    if any(row["site_id"] not in corpus_ids for row in rows):
        errors.append("un média est relié à un site absent du corpus")
    if database_count != len(rows):
        errors.append("le nombre de lignes DuckDB diffère de l'export média")
    reference_counts = Counter(
        (row["source_id"], row["media_reference"]) for row in rows
    )
    return {
        "schema_version": "1.0",
        "date_validation": date.today().isoformat(),
        "sites_corpus": len(corpus_ids),
        "sites_avec_media": len(sites_with_media),
        "sites_sans_media_exploitable": len(without_media),
        "medias_inventories": len(rows),
        "references_medias_uniques": len(
            {(row["source_id"], row["media_reference"]) for row in rows}
        ),
        "references_reutilisees_entre_relations": sum(
            count > 1 for count in reference_counts.values()
        ),
        "relations_avec_reference_reutilisee": sum(
            count for count in reference_counts.values() if count > 1
        ),
        "doublons_techniques_supprimes": len(duplicates),
        "medias_extraits_depuis_archive_html": sum(
            row["metadonnees_source"].get("extraction_format")
            == "html_notice_archivee"
            for row in rows
        ),
        "medias_avec_legende": sum(bool(row["legende_source"]) for row in rows),
        "medias_avec_auteur": sum(bool(row["auteur_source"]) for row in rows),
        "medias_avec_credit": sum(bool(row["credit_source"]) for row in rows),
        "medias_avec_mention_droits": sum(
            bool(row["mention_droits_source"]) for row in rows
        ),
        "medias_marques_principaux": sum(
            bool(row["image_principale_source"]) for row in rows
        ),
        "lignes_duckdb": database_count,
        "erreurs": errors,
        "decision": "medias_sites_v1_valide" if not errors else "validation_echouee",
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
                "# Inventaire des médias — `medias_sites` V1",
                "",
                f"Date : {report['date_validation']}",
                "",
                "## Résultats",
                "",
                f"- sites du corpus : **{report['sites_corpus']}** ;",
                f"- sites avec au moins un média : **{report['sites_avec_media']}** ;",
                (
                    "- sites sans média exploitable : "
                    f"**{report['sites_sans_media_exploitable']}** ;"
                ),
                f"- relations média-site conservées : **{report['medias_inventories']}** ;",
                (
                    "- références médias uniques : "
                    f"**{report['references_medias_uniques']}** ;"
                ),
                (
                    "- références réutilisées entre plusieurs relations : "
                    f"**{report['references_reutilisees_entre_relations']}** ;"
                ),
                (
                    "- médias extraits depuis une archive HTML : "
                    f"**{report['medias_extraits_depuis_archive_html']}** ;"
                ),
                (
                    "- doublons techniques strictement identiques supprimés : "
                    f"**{report['doublons_techniques_supprimes']}** ;"
                ),
                f"- légendes disponibles : **{report['medias_avec_legende']}** ;",
                f"- auteurs explicitement indiqués : **{report['medias_avec_auteur']}** ;",
                f"- crédits disponibles : **{report['medias_avec_credit']}** ;",
                (
                    "- mentions de droits disponibles : "
                    f"**{report['medias_avec_mention_droits']}** ;"
                ),
                (
                    "- médias marqués principaux dans la notice : "
                    f"**{report['medias_marques_principaux']}**."
                ),
                "",
                "## Méthode et limites",
                "",
                "- l'inventaire utilise les métadonnées `MEMOIRE` présentes dans les "
                "notices POP archivées ;",
                "- l'URL du média mène à sa notice POP ; le chemin de fichier brut est "
                "conservé séparément ;",
                "- aucun fichier image n'est téléchargé ou versionné ;",
                "- les doublons ne sont supprimés que lorsque toutes leurs métadonnées "
                "sources sont identiques ;",
                "- une même référence peut être reliée à plusieurs sites : ces relations "
                "sont conservées ;",
                "- les statuts de droits restent à `inconnus` et les usages à "
                "`metadonnees_seulement` jusqu'au bloc suivant.",
                "",
                f"Décision : **{report['decision']}**.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def produce(
    corpus_path: Path = DEFAULT_CORPUS,
    database_path: Path = DEFAULT_DATABASE,
    csv_path: Path = DEFAULT_CSV,
    parquet_path: Path = DEFAULT_PARQUET,
    without_media_path: Path = DEFAULT_WITHOUT_MEDIA,
    report_path: Path = DEFAULT_REPORT,
    report_markdown_path: Path = DEFAULT_REPORT_MARKDOWN,
) -> dict[str, Any]:
    corpus = load_corpus(corpus_path)
    rows, without_media, duplicates = media_rows(corpus)
    write_csv(csv_path, rows)
    write_without_media(without_media_path, without_media)
    database_count = write_database(database_path, csv_path, parquet_path)
    report = inventory_report(corpus, rows, without_media, duplicates, database_count)
    write_reports(report_path, report_markdown_path, report)
    if report["erreurs"]:
        raise ValueError("; ".join(report["erreurs"]))
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--parquet", type=Path, default=DEFAULT_PARQUET)
    parser.add_argument("--without-media", type=Path, default=DEFAULT_WITHOUT_MEDIA)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument(
        "--report-markdown", type=Path, default=DEFAULT_REPORT_MARKDOWN
    )
    args = parser.parse_args()
    report = produce(
        corpus_path=args.corpus,
        database_path=args.database,
        csv_path=args.csv,
        parquet_path=args.parquet,
        without_media_path=args.without_media,
        report_path=args.report,
        report_markdown_path=args.report_markdown,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
