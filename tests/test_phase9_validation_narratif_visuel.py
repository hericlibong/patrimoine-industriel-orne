from patrimoine_orne.export.validate_narratif_visuel_v1 import (
    DEFAULT_CORPUS,
    DEFAULT_DATABASE,
    DEFAULT_MEDIAS,
    DEFAULT_RECITS,
    DEFAULT_REVIEW,
    validate,
)


def test_narrative_and_visual_foundation_is_consistent() -> None:
    result = validate(
        DEFAULT_CORPUS,
        DEFAULT_RECITS,
        DEFAULT_MEDIAS,
        DEFAULT_REVIEW,
        DEFAULT_DATABASE,
    )

    assert result["erreurs"] == []
    assert result["decision"] == "socle_narratif_visuel_v1_approuve"
    assert result["textes_sources"] == {
        "historiques_attendus": 314,
        "historiques_conserves": 314,
        "descriptions_attendues": 257,
        "descriptions_conservees": 257,
    }
    assert result["medias"]["avec_provenance_et_statut"] == 1900
    assert result["medias"]["publication_automatique"] == 0
