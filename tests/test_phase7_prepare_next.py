"""Contrôles des livrables de préparation de la suite."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_internal_map_is_validated() -> None:
    validation = json.loads(
        (ROOT / "reports" / "maps" / "carte_pilote_interne_validation.json").read_text(
            encoding="utf-8"
        )
    )
    output = ROOT / validation["output"]

    assert validation["checks_passed"] is True
    assert validation["site_count"] == 30
    assert validation["alert_count"] == 9
    assert sum(validation["category_counts"].values()) == 30
    assert output.is_file() and output.stat().st_size > 100_000


def test_full_extraction_evaluation_is_conservative() -> None:
    evaluation = json.loads(
        (
            ROOT
            / "reports"
            / "quality"
            / "phase7_evaluation_extraction_complete.json"
        ).read_text(encoding="utf-8")
    )

    assert evaluation["decision"] == "go_par_lots"
    assert evaluation["official_corpus"]["announced_records"] == 319
    assert evaluation["recommended_first_batch"] == 50
    assert evaluation["readiness"]["structured_pop_parser"] is True
    assert evaluation["readiness"]["reference_enumerator"] is False
    assert evaluation["full_ocr_recommended"] is False


def test_decision_documents_exist() -> None:
    required = [
        "docs/estimation_charge_corpus_complet.md",
        "docs/recits_soutenus_donnees.md",
        "docs/recommandation_application.md",
        "reports/maps/README.md",
        "reports/quality/phase7_preparation_suite.md",
    ]

    assert all((ROOT / path).is_file() for path in required)
