"""Contrôles du bloc documentaire de la phase 7."""

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_source_registry_is_complete() -> None:
    registry = yaml.safe_load((ROOT / "config" / "sources.yml").read_text(encoding="utf-8"))
    sources = registry["sources"]

    assert str(registry["version"]) == "1.1"
    assert len(sources) == 21
    assert len({source["id"] for source in sources}) == len(sources)
    for source in sources:
        for field in ("data_license", "media_rights", "attribution", "rights_url"):
            assert source.get(field), f"{source['id']}: champ {field} manquant"


def test_current_observations_use_distinct_sources() -> None:
    enrichment = yaml.safe_load(
        (ROOT / "config" / "enrichissement_pilote.yml").read_text(encoding="utf-8")
    )
    observations = enrichment["situation_actuelle"]["exceptions"]

    assert observations["IA00060938"]["source_id"] == "edf_rabodanges"
    assert observations["IA00061155"]["source_id"] == "bohin"
    assert observations["IA00061029"]["source_id"] == "archives_orne"
    assert observations["IA00061008"]["source_id"] == "departement_orne"


def test_final_classification_registry_is_published() -> None:
    registry = yaml.safe_load(
        (ROOT / "config" / "classifications.yml").read_text(encoding="utf-8")
    )

    assert registry["version"] == "1.2"
    assert registry["status"] == "socle_v1"
    assert set(registry["methodes_periodes"]) == {
        "chronologie_phase",
        "siecles_source_site",
        "situation_actuelle_documentee",
    }


def test_anomaly_register_and_required_documents_exist() -> None:
    anomalies = json.loads(
        (ROOT / "reports" / "quality" / "phase7_anomalies_restantes.json").read_text(
            encoding="utf-8"
        )
    )
    assert len(anomalies["open_items"]) == 8
    assert len(anomalies["resolved_items"]) == 5

    required = [
        "docs/dictionnaire_donnees.md",
        "docs/registre_sources.md",
        "docs/limites_editoriales.md",
        "docs/licences_droits_images.md",
        "reports/quality/phase7_rapport_qualite.md",
        "reports/quality/phase7_anomalies_restantes.md",
    ]
    assert all((ROOT / path).is_file() for path in required)
