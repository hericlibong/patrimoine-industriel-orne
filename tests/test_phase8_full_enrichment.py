import pytest

from patrimoine_orne.enrich.full_corpus import (
    apply_casias_review,
    build_locations,
    reconcile_mh,
    token_set_ratio,
)
from patrimoine_orne.extract.full_territorial_context import build_specs
from patrimoine_orne.geocode.full_territorial_context import (
    _feature_index,
    _nearest_indexed,
)


def _site(reference: str = "IA00000001") -> dict:
    return {
        "site_id": "site-1",
        "dossier_reference": reference,
        "nom_principal": "forge de la Roche",
        "titre_source": "ancienne forge",
        "adresses_source": [],
        "lieux_dits_source": ["Roche (La)"],
        "insee_source": ["61001"],
        "longitude_source": 0.1,
        "latitude_source": 48.5,
        "localisation_detail": None,
        "objets_techniques": [],
    }


def test_mh_requires_an_explicit_ia_reference() -> None:
    sites = [_site()]
    rows, links = reconcile_mh(
        sites,
        [
            {"REF": "PA00000001", "RENV": ["IA00000001"], "TICO": "Forge"},
            {"REF": "PA00000002", "TICO": "Forge dans la même commune"},
        ],
    )
    assert len(rows) == 1
    assert links == {"PA00000001": "IA00000001"}
    assert sites[0]["protections_mh"][0]["fiabilite_code"] == "forte"


def test_manual_casias_review_must_cover_every_candidate() -> None:
    sites = [_site()]
    records = [
        {
            "code_inven": "BNO1",
            "nom_etabli": "FORGE DE LA ROCHE",
            "url_fiche": "https://example.test/BNO1",
        }
    ]
    ambiguities = [
        {
            "reference_source": "BNO1",
            "site_candidat_reference": "IA00000001",
            "score_texte": 90,
            "distance_m": 120,
            "decision": "non_rattache_a_verifier",
        }
    ]
    confirmed = []
    counts = apply_casias_review(
        sites,
        records,
        confirmed,
        ambiguities,
        {"confirmer": ["BNO1"], "rejeter": [], "maintenir_ambigu": []},
    )
    assert counts["confirme_apres_revue"] == 1
    assert confirmed[0]["statut"] == "recoupement_confirme_apres_revue"
    with pytest.raises(ValueError, match="ne couvrent pas"):
        apply_casias_review(
            sites,
            records,
            [],
            ambiguities,
            {"confirmer": [], "rejeter": [], "maintenir_ambigu": []},
        )


def test_locations_keep_pop_points_approximate() -> None:
    locations, duplicates = build_locations([_site()])
    row = locations["locations"][0]
    assert row["precision_geographique_code"] == "point_approximatif"
    assert row["methode_localisation_code"] == "coordonnees_source"
    assert row["point_lambert93"] is not None
    assert duplicates == []


def test_tiled_extraction_builds_three_ign_and_three_brgm_specs() -> None:
    locations = {
        "locations": [
            {
                "reference_ia": "IA00000001",
                "point_wgs84": [0.1, 48.5],
            }
        ]
    }
    specs = build_specs(locations)
    assert len(specs) == 6
    assert sum(spec.source_id == "brgm" for spec in specs) == 3


def test_indexed_nearest_feature() -> None:
    payload = {
        "features": [
            {
                "properties": {"name": "far"},
                "geometry": {"type": "Point", "coordinates": [0.5, 48.5]},
            },
            {
                "properties": {"name": "near"},
                "geometry": {"type": "Point", "coordinates": [0.1001, 48.5]},
            },
        ]
    }
    feature, distance = _nearest_indexed([0.1, 48.5], _feature_index(payload))
    assert feature["properties"]["name"] == "near"
    assert distance < 10


def test_token_overlap_is_deterministic() -> None:
    assert token_set_ratio("forge de la roche", "ancienne forge roche") > 50
    assert token_set_ratio("", "forge") == 0
