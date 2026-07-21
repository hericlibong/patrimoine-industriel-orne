"""Tests de préparation des extractions du contexte territorial."""

from patrimoine_orne.extract.territorial_context import bbox_around, build_specs


def test_bbox_contains_origin() -> None:
    west, south, east, north = bbox_around([0.1, 48.5], 1000)
    assert west < 0.1 < east
    assert south < 48.5 < north


def test_one_site_builds_six_requests() -> None:
    locations = {
        "locations": [
            {
                "reference_ia": "IA1",
                "geometrie_reference": {"point_wgs84": [0.1, 48.5]},
            }
        ]
    }
    specs = build_specs(locations)
    assert len(specs) == 6
    assert {spec.validator.__name__ for spec in specs} == {"validator"}
    assert any("troncon_hydrographique" in spec.request_url for spec in specs)
    assert any("LITHO_1M_SIMPLIFIEE" in spec.request_url for spec in specs)

