"""Tests de l'énumération et du premier lot de la phase 8."""

from patrimoine_orne.extract.corpus import (
    build_lot_assessment,
    enumerate_corpus,
    select_systematic_lot,
)


def _notice(reference: str, dossier_type: str = "dossier individuel") -> dict:
    return {
        "REF": reference,
        "ETUD": ["patrimoine industriel (patrimoine industriel de l’Orne)"],
        "DOSS": dossier_type,
        "TICO": "moulin",
    }


def _config(expected: int) -> dict:
    return {
        "corpus_source": {"announced_records": expected, "presentation_reference": "IA61000851"},
        "enumeration": {
            "method": "test",
            "api_url": "https://example.test",
            "expected_study": "patrimoine industriel (patrimoine industriel de l’Orne)",
            "expected_search_count": expected + 1,
            "excluded_search_results": [
                {"reference": "IA61000851", "reason": "notice_de_presentation_non_site"}
            ],
        },
    }


def test_enumeration_excludes_only_presentation_and_keeps_collective_dossier() -> None:
    config = _config(2)

    def searcher(_: dict) -> list[dict]:
        return [
            _notice("IA00000001"),
            _notice("IA61000851", "présentation de l'aire d'étude"),
            _notice("IA61001399", "dossier collectif"),
        ]

    result = enumerate_corpus(config, searcher=searcher)
    assert result["references"] == ["IA00000001", "IA61001399"]
    assert result["eligible_count"] == 2
    assert result["excluded_search_result_count"] == 1
    assert all(result["checks"].values())


def test_systematic_lot_excludes_pilot_and_covers_range() -> None:
    references = [f"IA{number:08d}" for number in range(1, 21)]
    selected = select_systematic_lot(references, ["IA00000010"], 5)
    assert len(selected) == 5
    assert "IA00000010" not in selected
    assert selected == sorted(selected)
    assert int(selected[-1][2:]) - int(selected[0][2:]) > 10


def test_manual_decision_resolves_multi_sector_review() -> None:
    classifications = {
        "activites_detaillees": {
            "metal": {"libelle": "Métal", "secteur_code": "metallurgie"},
            "grain": {"libelle": "Grain", "secteur_code": "agroalimentaire"},
        },
        "correspondances_sources": [
            {"terme": "forge", "activite_code": "metal", "installation_code": "usine"},
            {"terme": "moulin", "activite_code": "grain", "installation_code": "moulin"},
        ],
        "correspondances_energies_sources": [],
        "termes_hors_energie": [],
    }
    records = [{"REF": "IA00000001", "DENO": ["forge", "moulin"]}]
    decisions = {
        "decisions": {
            "IA00000001": {
                "decision": "conserver_un_site_activites_successives",
                "justification": "conversion documentée",
            }
        }
    }
    result = build_lot_assessment(records, classifications, decisions)
    assert result["lot_review_complete"] is True
    assert result["lot_canonical_site_count"] == 1
    assert result["review_queue"][0]["decision"] == "conserver_un_site_activites_successives"
