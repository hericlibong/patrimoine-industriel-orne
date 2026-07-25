from pathlib import Path

import duckdb

from patrimoine_orne.export.medias_v1 import (
    MEDIA_FIELDS,
    inventory_report,
    load_corpus,
    media_rows,
    write_csv,
    write_database,
)


ROOT = Path(__file__).parents[1]
CORPUS_PATH = ROOT / "data" / "processed" / "corpus_complet_v1.json"


def test_media_inventory_covers_all_sites_without_downloading_images() -> None:
    corpus = load_corpus(CORPUS_PATH)
    rows, without_media, duplicates = media_rows(corpus)

    assert len(rows) == 1900
    assert len(without_media) == 2
    assert duplicates == []
    assert {row["site_id"] for row in rows} | {
        row["site_id"] for row in without_media
    } == {site["site_id"] for site in corpus["sites"]}
    assert all(row["chemin_local"] is None for row in rows)
    assert all(row["fichier_sha256"] is None for row in rows)


def test_media_rows_preserve_metadata_and_default_to_non_public_use() -> None:
    rows, _, _ = media_rows(load_corpus(CORPUS_PATH))

    for row in rows:
        assert set(row) == set(MEDIA_FIELDS)
        assert row["media_reference"]
        assert row["url_media"].startswith("https://pop.culture.gouv.fr/notice/memoire/")
        assert row["url_notice_source"].startswith(
            "https://pop.culture.gouv.fr/notice/merimee/"
        )
        assert row["selection_media_code"] == "non_evalue"
        assert row["statut_droits_code"] == "inconnus"
        assert row["statut_autorisation_code"] == "non_demandee"
        assert row["usage_media_code"] == "metadonnees_seulement"


def test_html_archives_are_used_when_json_metadata_is_unavailable() -> None:
    rows, _, _ = media_rows(load_corpus(CORPUS_PATH))
    html_rows = [
        row
        for row in rows
        if row["metadonnees_source"].get("extraction_format")
        == "html_notice_archivee"
    ]

    assert len(html_rows) == 117
    assert all(row["url_fichier_source"].startswith("https://popcorn-") for row in html_rows)
    assert all(row["legende_source"] is None for row in html_rows)


def test_database_and_parquet_keep_media_site_relations(tmp_path: Path) -> None:
    corpus = load_corpus(CORPUS_PATH)
    rows, _, _ = media_rows(corpus)
    csv_path = tmp_path / "medias.csv"
    parquet_path = tmp_path / "medias.parquet"
    database_path = tmp_path / "media.duckdb"
    write_csv(csv_path, rows)
    connection = duckdb.connect(str(database_path))
    connection.execute("CREATE TABLE sites (site_id VARCHAR)")
    connection.executemany(
        "INSERT INTO sites VALUES (?)", [(site["site_id"],) for site in corpus["sites"]]
    )
    connection.close()

    count = write_database(database_path, csv_path, parquet_path)

    connection = duckdb.connect(str(database_path), read_only=True)
    try:
        assert count == 1900
        assert connection.execute("SELECT count(*) FROM medias").fetchone()[0] == 1900
        assert connection.execute(
            "SELECT count(*) FROM medias WHERE site_id NOT IN (SELECT site_id FROM sites)"
        ).fetchone()[0] == 0
        assert connection.execute(
            f"SELECT count(*) FROM read_parquet('{parquet_path.as_posix()}')"
        ).fetchone()[0] == 1900
    finally:
        connection.close()


def test_inventory_report_is_valid() -> None:
    corpus = load_corpus(CORPUS_PATH)
    rows, without_media, duplicates = media_rows(corpus)
    report = inventory_report(corpus, rows, without_media, duplicates, 1900)

    assert report["decision"] == "medias_sites_v1_valide"
    assert report["sites_avec_media"] == 316
    assert report["sites_sans_media_exploitable"] == 2
    assert report["references_medias_uniques"] == 1888
    assert report["doublons_techniques_supprimes"] == 0
    assert report["erreurs"] == []
