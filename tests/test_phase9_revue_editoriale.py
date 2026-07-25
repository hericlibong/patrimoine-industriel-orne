from patrimoine_orne.export.revue_editoriale_v1 import (
    DEFAULT_MEDIAS,
    DEFAULT_RECITS,
    build_rows,
    load_medias,
    load_recits,
    report,
)


def test_editorial_review_covers_all_sites_without_selection() -> None:
    rows = build_rows(load_recits(DEFAULT_RECITS), load_medias(DEFAULT_MEDIAS))

    assert len(rows) == 318
    assert {row["statut_revue_code"] for row in rows} == {"a_examiner"}
    assert all(
        row["media_principal_candidat_statut_code"] != "valide" for row in rows
    )
    assert sum(row["chronologie_disponible"] for row in rows) == 318


def test_editorial_review_reports_documentary_gaps() -> None:
    rows = build_rows(load_recits(DEFAULT_RECITS), load_medias(DEFAULT_MEDIAS))
    result = report(rows, database_count=len(rows))

    assert result["sites_combinant_histoire_chronologie_medias"] == 284
    assert result["recherche_historique_necessaire"] == 4
    assert result["recherche_visuelle_necessaire"] == 31
    assert result["erreurs"] == []
