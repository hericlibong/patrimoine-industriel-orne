"""Produit la table éditoriale des récits de sites à partir du corpus complet V1."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from datetime import date
from pathlib import Path
from typing import Any

import duckdb


DEFAULT_CORPUS = Path("data/processed/corpus_complet_v1.json")
DEFAULT_DATABASE = Path("data/processed/patrimoine_orne_corpus_complet_v1.duckdb")
DEFAULT_CSV = Path("data/exports/recits_sites_v1.csv")
DEFAULT_PARQUET = Path("data/exports/recits_sites_v1.parquet")
DEFAULT_REPORT = Path("reports/quality/phase9_recits_sites_couverture.json")
DEFAULT_REPORT_MARKDOWN = Path("reports/quality/phase9_recits_sites_couverture.md")

RECIT_FIELDS = (
    "site_id",
    "reference_ia",
    "titre_source",
    "nom_site",
    "historique_source",
    "historique_source_statut_code",
    "historique_source_sha256",
    "description_source",
    "description_source_statut_code",
    "description_source_sha256",
    "siecles_source",
    "periodes_source_codes",
    "periodes_activite_codes",
    "activites_successives",
    "source_id",
    "source_reference",
    "source_url",
    "date_consultation_source",
    "references_sources",
    "resume_documentaire",
    "resume_documentaire_statut_code",
    "resume_documentaire_sources",
    "resume_documentaire_auteur",
    "resume_documentaire_valide_le",
    "note_journalistique",
    "note_journalistique_statut_code",
    "note_journalistique_auteur",
    "selection_texte_code",
    "besoin_recherche_complementaire",
    "notes_editoriales",
)

JSON_FIELDS = {
    "siecles_source",
    "periodes_source_codes",
    "periodes_activite_codes",
    "activites_successives",
    "references_sources",
    "resume_documentaire_sources",
}


def load_corpus(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _text(value: Any) -> str | None:
    if value is None:
        return None
    original = str(value)
    return original if original.strip() else None


def sha256_text(value: str | None) -> str | None:
    if value is None:
        return None
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def source_status(value: str | None) -> str:
    return "renseigne" if value is not None else "absent_source"


def _consultation_date(site: Mapping[str, Any], corpus: Mapping[str, Any]) -> str:
    raw_path = str(site.get("notice_brute") or "")
    match = re.search(r"20\d{2}-\d{2}-\d{2}", raw_path)
    if match:
        return match.group(0)
    generated_at = str(corpus.get("generated_at") or "")
    match = re.search(r"20\d{2}-\d{2}-\d{2}", generated_at)
    return match.group(0) if match else date.today().isoformat()


def _primary_source(site: Mapping[str, Any]) -> dict[str, Any]:
    sources = list(site.get("sources") or [])
    if not sources:
        return {
            "source_id": "pop_merimee",
            "reference": site["dossier_reference"],
            "url": site.get("dossier_url"),
        }
    return next(
        (source for source in sources if source.get("role") == "notice_principale"),
        sources[0],
    )


def recit_rows(corpus: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for site in sorted(corpus["sites"], key=lambda item: item["dossier_reference"]):
        history = _text(site.get("historique_source"))
        description = _text(site.get("description_source"))
        primary_source = _primary_source(site)
        rows.append(
            {
                "site_id": site["site_id"],
                "reference_ia": site["dossier_reference"],
                "titre_source": _text(site.get("titre_source")),
                "nom_site": site["nom_principal"],
                "historique_source": history,
                "historique_source_statut_code": source_status(history),
                "historique_source_sha256": sha256_text(history),
                "description_source": description,
                "description_source_statut_code": source_status(description),
                "description_source_sha256": sha256_text(description),
                "siecles_source": list(site.get("siecles_source") or []),
                "periodes_source_codes": list(site.get("periodes_source_codes") or []),
                "periodes_activite_codes": list(
                    site.get("periodes_activite_codes") or []
                ),
                "activites_successives": list(site.get("activites") or []),
                "source_id": primary_source.get("source_id") or "pop_merimee",
                "source_reference": (
                    primary_source.get("reference") or site["dossier_reference"]
                ),
                "source_url": (
                    primary_source.get("url")
                    or site.get("dossier_url")
                    or f"https://pop.culture.gouv.fr/notice/merimee/"
                    f"{site['dossier_reference']}"
                ),
                "date_consultation_source": _consultation_date(site, corpus),
                "references_sources": list(site.get("sources") or []),
                "resume_documentaire": None,
                "resume_documentaire_statut_code": "non_produit",
                "resume_documentaire_sources": [],
                "resume_documentaire_auteur": None,
                "resume_documentaire_valide_le": None,
                "note_journalistique": None,
                "note_journalistique_statut_code": "non_produite",
                "note_journalistique_auteur": None,
                "selection_texte_code": "non_evalue",
                "besoin_recherche_complementaire": False,
                "notes_editoriales": None,
            }
        )
    return rows


def _serialized_row(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        field: (
            json.dumps(row[field], ensure_ascii=False, sort_keys=True)
            if field in JSON_FIELDS
            else row[field]
        )
        for field in RECIT_FIELDS
    }


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=RECIT_FIELDS)
        writer.writeheader()
        writer.writerows(_serialized_row(row) for row in rows)


def write_database(
    path: Path, rows: Sequence[Mapping[str, Any]], parquet_path: Path
) -> int:
    serialized = [_serialized_row(row) for row in rows]
    path.parent.mkdir(parents=True, exist_ok=True)
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    connection = duckdb.connect(str(path), read_only=False)
    try:
        site_count = int(connection.execute("SELECT count(*) FROM sites").fetchone()[0])
        if site_count != len(rows):
            raise ValueError(
                f"Le DuckDB contient {site_count} sites mais {len(rows)} récits."
            )
        connection.execute("BEGIN TRANSACTION")
        connection.execute("DROP TABLE IF EXISTS recits_sites")
        definitions = []
        for field in RECIT_FIELDS:
            kind = "BOOLEAN" if field == "besoin_recherche_complementaire" else "VARCHAR"
            definitions.append(f'"{field}" {kind}')
        connection.execute(f"CREATE TABLE recits_sites ({', '.join(definitions)})")
        placeholders = ", ".join("?" for _ in RECIT_FIELDS)
        connection.executemany(
            f"INSERT INTO recits_sites VALUES ({placeholders})",
            [[row[field] for field in RECIT_FIELDS] for row in serialized],
        )
        mismatch_count = int(
            connection.execute(
                """
                SELECT count(*)
                FROM (
                    SELECT site_id FROM sites
                    EXCEPT
                    SELECT site_id FROM recits_sites
                )
                """
            ).fetchone()[0]
        )
        extra_count = int(
            connection.execute(
                """
                SELECT count(*)
                FROM (
                    SELECT site_id FROM recits_sites
                    EXCEPT
                    SELECT site_id FROM sites
                )
                """
            ).fetchone()[0]
        )
        duplicate_count = int(
            connection.execute(
                """
                SELECT count(*)
                FROM (
                    SELECT site_id FROM recits_sites
                    GROUP BY site_id HAVING count(*) <> 1
                )
                """
            ).fetchone()[0]
        )
        if mismatch_count or extra_count or duplicate_count:
            raise ValueError(
                "Concordance des identifiants invalide : "
                f"{mismatch_count} manquants, {extra_count} supplémentaires, "
                f"{duplicate_count} dupliqués."
            )
        connection.execute("COMMIT")
        escaped_path = parquet_path.resolve().as_posix().replace("'", "''")
        connection.execute(
            f"COPY recits_sites TO '{escaped_path}' "
            "(FORMAT PARQUET, COMPRESSION ZSTD)"
        )
        return int(
            connection.execute("SELECT count(*) FROM recits_sites").fetchone()[0]
        )
    except Exception:
        try:
            connection.execute("ROLLBACK")
        except duckdb.Error:
            pass
        raise
    finally:
        connection.close()


def coverage_report(
    corpus: Mapping[str, Any], rows: Sequence[Mapping[str, Any]], database_count: int
) -> dict[str, Any]:
    history_count = sum(
        row["historique_source_statut_code"] == "renseigne" for row in rows
    )
    description_count = sum(
        row["description_source_statut_code"] == "renseigne" for row in rows
    )
    both_count = sum(
        row["historique_source_statut_code"] == "renseigne"
        and row["description_source_statut_code"] == "renseigne"
        for row in rows
    )
    neither_count = sum(
        row["historique_source_statut_code"] == "absent_source"
        and row["description_source_statut_code"] == "absent_source"
        for row in rows
    )
    corpus_ids = {site["site_id"] for site in corpus["sites"]}
    recit_ids = {row["site_id"] for row in rows}
    errors = []
    if len(rows) != 318:
        errors.append(f"{len(rows)} récits au lieu de 318")
    if corpus_ids != recit_ids:
        errors.append("les identifiants des récits diffèrent de ceux du corpus")
    if database_count != len(rows):
        errors.append("le nombre de lignes DuckDB diffère du nombre de récits")
    for row in rows:
        for field in ("historique_source", "description_source"):
            expected = sha256_text(row[field])
            if row[f"{field}_sha256"] != expected:
                errors.append(f"empreinte invalide pour {row['reference_ia']}:{field}")
    return {
        "schema_version": "1.0",
        "date_validation": date.today().isoformat(),
        "sites_corpus": len(corpus["sites"]),
        "lignes_recits_sites": len(rows),
        "lignes_duckdb": database_count,
        "identifiants_concordants": corpus_ids == recit_ids,
        "couverture": {
            "historique_renseigne": history_count,
            "historique_absent_source": len(rows) - history_count,
            "historique_couverture_pourcent": round(history_count * 100 / len(rows), 1),
            "description_renseignee": description_count,
            "description_absente_source": len(rows) - description_count,
            "description_couverture_pourcent": round(
                description_count * 100 / len(rows), 1
            ),
            "historique_et_description": both_count,
            "historique_seul": history_count - both_count,
            "description_seule": description_count - both_count,
            "ni_historique_ni_description": neither_count,
        },
        "erreurs": errors,
        "decision": "recits_sites_v1_valide" if not errors else "validation_echouee",
    }


def write_reports(
    json_path: Path, markdown_path: Path, report: Mapping[str, Any]
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    coverage = report["couverture"]
    markdown_path.write_text(
        "\n".join(
            [
                "# Couverture de la matière historique — `recits_sites` V1",
                "",
                f"Date : {report['date_validation']}",
                "",
                "## Résultats",
                "",
                f"- sites et lignes éditoriales : **{report['lignes_recits_sites']}** ;",
                (
                    "- historiques renseignés : "
                    f"**{coverage['historique_renseigne']}** "
                    f"({coverage['historique_couverture_pourcent']} %) ;"
                ),
                (
                    "- historiques explicitement absents : "
                    f"**{coverage['historique_absent_source']}** ;"
                ),
                (
                    "- descriptions renseignées : "
                    f"**{coverage['description_renseignee']}** "
                    f"({coverage['description_couverture_pourcent']} %) ;"
                ),
                (
                    "- descriptions explicitement absentes : "
                    f"**{coverage['description_absente_source']}** ;"
                ),
                (
                    "- sites avec historique et description : "
                    f"**{coverage['historique_et_description']}** ;"
                ),
                (
                    "- sites sans historique ni description : "
                    f"**{coverage['ni_historique_ni_description']}**."
                ),
                "",
                "## Contrôles",
                "",
                "- les 318 identifiants correspondent exactement à la table `sites` ;",
                "- les textes sources conservent une empreinte SHA-256 ;",
                "- les siècles, périodes, activités successives et références sont "
                "conservés ;",
                "- une absence reste vide et reçoit le statut `absent_source` ;",
                "- les champs de résumé et de texte journalistique sont initialisés "
                "sans contenu.",
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
    report_path: Path = DEFAULT_REPORT,
    report_markdown_path: Path = DEFAULT_REPORT_MARKDOWN,
) -> dict[str, Any]:
    corpus = load_corpus(corpus_path)
    rows = recit_rows(corpus)
    write_csv(csv_path, rows)
    database_count = write_database(database_path, rows, parquet_path)
    report = coverage_report(corpus, rows, database_count)
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
        report_path=args.report,
        report_markdown_path=args.report_markdown,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
