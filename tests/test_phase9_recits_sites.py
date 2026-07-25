import json
from pathlib import Path

import duckdb

from patrimoine_orne.export.editorial_v1 import (
    RECIT_FIELDS,
    _text,
    coverage_report,
    load_corpus,
    recit_rows,
    sha256_text,
    write_database,
)


ROOT = Path(__file__).parents[1]
CORPUS_PATH = ROOT / "data" / "processed" / "corpus_complet_v1.json"


def test_recits_sites_cover_the_complete_corpus() -> None:
    corpus = load_corpus(CORPUS_PATH)
    rows = recit_rows(corpus)

    assert len(rows) == 318
    assert {row["site_id"] for row in rows} == {
        site["site_id"] for site in corpus["sites"]
    }
    assert sum(row["historique_source"] is not None for row in rows) == 314
    assert sum(row["description_source"] is not None for row in rows) == 257


def test_source_absences_and_hashes_are_explicit() -> None:
    rows = recit_rows(load_corpus(CORPUS_PATH))

    for row in rows:
        for field in ("historique_source", "description_source"):
            expected_status = "renseigne" if row[field] is not None else "absent_source"
            assert row[f"{field}_statut_code"] == expected_status
            assert row[f"{field}_sha256"] == sha256_text(row[field])

    assert _text("  texte source  ") == "  texte source  "
    assert _text("   ") is None


def test_periods_activities_and_sources_are_preserved() -> None:
    corpus = load_corpus(CORPUS_PATH)
    source_by_id = {site["site_id"]: site for site in corpus["sites"]}

    for row in recit_rows(corpus):
        site = source_by_id[row["site_id"]]
        assert row["siecles_source"] == site["siecles_source"]
        assert row["periodes_source_codes"] == site["periodes_source_codes"]
        assert row["periodes_activite_codes"] == site["periodes_activite_codes"]
        assert row["activites_successives"] == site["activites"]
        assert row["references_sources"] == site["sources"]


def test_database_and_parquet_keep_one_row_per_site(tmp_path: Path) -> None:
    corpus = load_corpus(CORPUS_PATH)
    rows = recit_rows(corpus)
    database = tmp_path / "editorial.duckdb"
    parquet = tmp_path / "recits.parquet"
    connection = duckdb.connect(str(database))
    connection.execute("CREATE TABLE sites (site_id VARCHAR)")
    connection.executemany(
        "INSERT INTO sites VALUES (?)", [(row["site_id"],) for row in rows]
    )
    connection.close()

    count = write_database(database, rows, parquet)

    connection = duckdb.connect(str(database), read_only=True)
    try:
        assert count == 318
        assert connection.execute("SELECT count(*) FROM recits_sites").fetchone()[0] == 318
        assert {
            row[0] for row in connection.execute("SELECT site_id FROM sites").fetchall()
        } == {
            row[0]
            for row in connection.execute("SELECT site_id FROM recits_sites").fetchall()
        }
        assert connection.execute(
            f"SELECT count(*) FROM read_parquet('{parquet.as_posix()}')"
        ).fetchone()[0] == 318
    finally:
        connection.close()


def test_coverage_report_validates_the_expected_counts() -> None:
    corpus = load_corpus(CORPUS_PATH)
    rows = recit_rows(corpus)
    report = coverage_report(corpus, rows, 318)

    assert report["decision"] == "recits_sites_v1_valide"
    assert report["couverture"] == {
        "historique_renseigne": 314,
        "historique_absent_source": 4,
        "historique_couverture_pourcent": 98.7,
        "description_renseignee": 257,
        "description_absente_source": 61,
        "description_couverture_pourcent": 80.8,
        "historique_et_description": 256,
        "historique_seul": 58,
        "description_seule": 1,
        "ni_historique_ni_description": 3,
    }
    assert report["erreurs"] == []
    assert len(RECIT_FIELDS) == len(set(RECIT_FIELDS))


def test_generated_recits_exports_are_validated() -> None:
    report_path = ROOT / "reports" / "quality" / "phase9_recits_sites_couverture.json"
    if not report_path.exists():
        return

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["decision"] == "recits_sites_v1_valide"
    assert report["lignes_recits_sites"] == 318
