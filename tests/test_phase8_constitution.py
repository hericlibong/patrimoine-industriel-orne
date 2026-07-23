"""Contrôles des livrables de constitution du corpus en phase 8."""

import csv
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_official_corpus_enumeration_is_complete() -> None:
    manifest = json.loads(
        (ROOT / "reports" / "audits" / "phase8_enumeration_corpus.json").read_text(
            encoding="utf-8"
        )
    )
    references = manifest["references"]
    exclusions = [
        row
        for row in manifest["search_result_audit"]
        if row["status"] == "excluded"
    ]

    assert len(references) == len(set(references)) == 319
    assert manifest["search_result_count"] == 320
    assert exclusions[0]["reference"] == "IA61000851"
    assert all(manifest["checks"].values())


def test_lot1_is_non_pilot_and_reviewed() -> None:
    lot = yaml.safe_load((ROOT / "config" / "phase8_lot1.yml").read_text(encoding="utf-8"))
    pilot = yaml.safe_load(
        (ROOT / "config" / "echantillon_pilote.yml").read_text(encoding="utf-8")
    )
    assessment = json.loads(
        (ROOT / "reports" / "quality" / "phase8_lot1_evaluation.json").read_text(
            encoding="utf-8"
        )
    )

    pilot_references = {row["ia_reference"] for row in pilot["sites"]}
    assert len(lot["references"]) == len(set(lot["references"])) == 50
    assert set(lot["references"]).isdisjoint(pilot_references)
    assert assessment["record_count"] == 50
    assert assessment["classification"]["denominations"]["coverage_percent"] == 100.0
    assert assessment["unresolved_review_count"] == 0
    assert assessment["lot_canonical_site_count"] == 50
    assert assessment["canonical_site_count"] is None


def test_reference_csv_matches_manifest() -> None:
    manifest = json.loads(
        (ROOT / "reports" / "audits" / "phase8_enumeration_corpus.json").read_text(
            encoding="utf-8"
        )
    )
    with (ROOT / "reports" / "audits" / "phase8_references_ia.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        references = [row["reference"] for row in csv.DictReader(stream)]
    assert references == manifest["references"]


def test_common_corpus_80_summary_and_csv() -> None:
    summary = json.loads(
        (ROOT / "reports" / "quality" / "phase8_corpus_80_resume.json").read_text(
            encoding="utf-8"
        )
    )
    with (ROOT / "reports" / "quality" / "phase8_corpus_80.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        rows = list(csv.DictReader(stream))

    assert summary["counts"]["dossiers"] == 80
    assert summary["counts"]["pilot"] == 30
    assert summary["counts"]["lot1"] == 50
    assert summary["counts"]["activites"] == 109
    assert summary["counts"]["rapprochements_a_verifier"] == 0
    assert all(summary["checks"].values())
    assert len(rows) == 80
    assert len({row["dossier_reference"] for row in rows}) == 80
