import csv
import json
import uuid
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_canonical_summary_establishes_318_sites() -> None:
    summary = json.loads(
        (
            ROOT / "reports" / "quality" / "phase8_corpus_canonique_resume.json"
        ).read_text(encoding="utf-8")
    )

    assert summary["source_dossier_count"] == 319
    assert summary["canonical_site_count"] == 318
    assert summary["counts"]["sites_avec_activites_productives"] == 314
    assert summary["counts"]["sites_composants_non_productifs"] == 4
    assert summary["counts"]["activites"] == 403
    assert summary["counts"]["rapprochements_rejetes"] == 7
    # 5 relations structurelles de la phase 8, plus 18 relations de production
    # extraites des textes de notices en phase 10.A.1.
    assert summary["counts"]["relations_sites_validees"] == 23
    assert all(summary["checks"].values())


def test_site_id_registry_is_complete_unique_and_uuid4() -> None:
    registry = yaml.safe_load(
        (ROOT / "config" / "phase8_site_ids.yml").read_text(encoding="utf-8")
    )
    values = list(registry["site_ids"].values())

    assert len(values) == len(set(values)) == 318
    assert all(uuid.UUID(value).version == 4 for value in values)
    assert "IA61001399" not in registry["site_ids"]
    assert len(registry["relation_ids"]) == 23


def test_pilot_site_ids_are_preserved() -> None:
    corpus = json.loads(
        (ROOT / "data" / "interim" / "phase8_corpus_319.json").read_text(
            encoding="utf-8"
        )
    )
    registry = yaml.safe_load(
        (ROOT / "config" / "phase8_site_ids.yml").read_text(encoding="utf-8")
    )
    pilot_records = [
        record
        for record in corpus["dossiers"]
        if record["origine"] == "pilote_30"
    ]

    assert len(pilot_records) == 29
    assert all(
        registry["site_ids"][record["dossier_reference"]] == record["site_id"]
        for record in pilot_records
    )


def test_canonical_csv_and_review_files_are_complete() -> None:
    def rows(name: str) -> list[dict[str, str]]:
        with (ROOT / "reports" / "quality" / name).open(
            encoding="utf-8", newline=""
        ) as stream:
            return list(csv.DictReader(stream))

    sites = rows("phase8_corpus_canonique.csv")
    references = [row["dossier_reference"] for row in sites]
    assert len(sites) == len(set(references)) == 318
    assert "IA61001399" not in references

    relations = rows("phase8_relations_sites.csv")
    assert len(relations) == 23
    assert all(row["statut_validation_code"] == "valide" for row in relations)

    review = rows("phase8_revue_canoniques.csv")
    # 15 décisions de la phase 8, plus 18 relations de production ajoutées
    # en phase 10.A.1.
    assert len(review) == 33
    assert sum(row["type_decision"] == "rapprochement" for row in review) == 7
    assert sum(row["type_decision"] == "activite_precisee" for row in review) == 2
