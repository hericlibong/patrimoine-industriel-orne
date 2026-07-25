import json
from pathlib import Path

import yaml

from patrimoine_orne.extract.remaining import load_remaining_references, remaining_references


ROOT = Path(__file__).resolve().parents[1]


def test_remaining_references_cover_the_official_corpus() -> None:
    references = load_remaining_references(
        ROOT / "reports" / "audits" / "phase8_enumeration_corpus.json",
        ROOT / "config" / "echantillon_pilote.yml",
        ROOT / "config" / "phase8_lot1.yml",
    )
    enumeration = json.loads(
        (ROOT / "reports" / "audits" / "phase8_enumeration_corpus.json").read_text(
            encoding="utf-8"
        )
    )
    pilot = yaml.safe_load(
        (ROOT / "config" / "echantillon_pilote.yml").read_text(encoding="utf-8")
    )
    first_group = yaml.safe_load(
        (ROOT / "config" / "phase8_lot1.yml").read_text(encoding="utf-8")
    )
    used = {row["ia_reference"] for row in pilot["sites"]} | set(
        first_group["references"]
    )

    assert len(references) == len(set(references)) == 240
    assert set(references).isdisjoint(used)
    assert set(references) | (used & set(enumeration["references"])) == set(
        enumeration["references"]
    )
    assert used - set(enumeration["references"]) == {"IA00061060"}


def test_remaining_references_rejects_incomplete_enumeration() -> None:
    enumeration = {"references": [f"IA{index:08d}" for index in range(318)]}
    pilot = {"sites": [{"ia_reference": f"IA{index:08d}"} for index in range(30)]}
    first_group = {"references": [f"IA{index:08d}" for index in range(30, 80)]}

    try:
        remaining_references(enumeration, pilot, first_group)
    except ValueError as error:
        assert "319" in str(error)
    else:
        raise AssertionError("une énumération incomplète doit être refusée")
