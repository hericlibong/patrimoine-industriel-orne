import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_remaining_manifest_is_complete() -> None:
    manifest = json.loads(
        (ROOT / "reports" / "audits" / "phase8_remaining_pop_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    rows = manifest["sources"]["pop_merimee"]
    references = [row["observations"]["reference"] for row in rows]

    assert manifest["status"] == "complete"
    assert manifest["retrieved_count"] == len(rows) == 240
    assert manifest["remaining_count"] == 0
    assert len(references) == len(set(references)) == 240


def test_corpus_319_summary_is_complete_and_harmonized() -> None:
    summary = json.loads(
        (ROOT / "reports" / "quality" / "phase8_corpus_319_resume.json").read_text(
            encoding="utf-8"
        )
    )

    assert summary["counts"]["dossiers_officiels"] == 319
    assert summary["counts"]["pilotes_officiels"] == 29
    assert summary["counts"]["premiers_dossiers"] == 50
    assert summary["counts"]["dossiers_restants_traites"] == 240
    assert summary["classifications"]["couverture_resolue_pourcent"] == 100.0
    assert summary["classifications"]["termes_inconnus"] == {}
    assert all(summary["checks"].values())
    assert summary["canonical_site_count"] is None


def test_corpus_319_csv_contains_every_official_reference_once() -> None:
    enumeration = json.loads(
        (ROOT / "reports" / "audits" / "phase8_enumeration_corpus.json").read_text(
            encoding="utf-8"
        )
    )
    with (ROOT / "reports" / "quality" / "phase8_corpus_319.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        rows = list(csv.DictReader(stream))
    references = [row["dossier_reference"] for row in rows]

    assert len(rows) == len(set(references)) == 319
    assert set(references) == set(enumeration["references"])
    assert "IA00061060" not in references


def test_review_files_have_the_detected_cases() -> None:
    def rows(name: str) -> list[dict[str, str]]:
        with (ROOT / "reports" / "quality" / name).open(
            encoding="utf-8", newline=""
        ) as stream:
            return list(csv.DictReader(stream))

    assert len(rows("phase8_corpus_319_rapprochements.csv")) == 7
    assert rows("phase8_corpus_319_separations.csv")[0]["dossier_reference"] == "IA61001399"
    anomalies = rows("phase8_corpus_319_anomalies.csv")
    assert any(row["dossier_reference"] == "IA00061060" for row in anomalies)
    assert sum(row["type"] == "composant_non_productif_a_relier" for row in anomalies) == 4
