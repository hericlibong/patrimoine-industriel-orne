import csv
import json
from pathlib import Path

from patrimoine_orne.export.corpus_complet_v1 import stable_uuid


ROOT = Path(__file__).resolve().parents[1]


def load_report(name: str) -> dict:
    return json.loads(
        (ROOT / "reports" / "quality" / name).read_text(encoding="utf-8")
    )


def test_corpus_complet_v1_is_validated() -> None:
    report = load_report("phase8_validation_corpus_complet.json")
    assert report["checks_passed"] is True
    assert report["decision"] == "corpus_complet_v1_valide"
    assert report["counts"]["dossiers_sources"] == 319
    assert report["counts"]["sites"] == 318
    assert report["counts"]["activites"] == 403
    assert report["counts"]["sites_csv"] == 318
    assert report["counts"]["sites_parquet"] == 318
    assert report["counts"]["sites_geojson"] == 318


def test_final_indicators_keep_unknown_values_explicit() -> None:
    indicators = load_report("phase8_indicateurs_corpus_complet.json")
    assert indicators["population"]["sites_canoniques"] == 318
    assert indicators["chronologie"]["sites_avec_periode_source"] == 318
    assert indicators["chronologie"]["activites_avec_periode_datee"] == 42
    assert indicators["situation_actuelle"]["conservation"]["inconnu"] == 315
    assert indicators["situation_actuelle"]["accessibilite"]["inconnu"] == 316
    assert indicators["localisation"]["sites_localises"] == 318
    assert sum(indicators["localisation"]["precision"].values()) == 318


def test_remaining_anomalies_are_non_blocking() -> None:
    path = ROOT / "reports" / "quality" / "phase8_anomalies_restantes.csv"
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert rows
    assert {row["bloquant"] for row in rows} == {"non"}
    assert {row["code"] for row in rows} >= {
        "situation_actuelle_inconnue",
        "point_approximatif",
        "activite_sans_chronologie_directe",
    }


def test_activity_identifier_is_stable() -> None:
    first = stable_uuid("activite", "site-1", 1)
    assert first == stable_uuid("activite", "site-1", 1)
    assert first != stable_uuid("activite", "site-1", 2)
