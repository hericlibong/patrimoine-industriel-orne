"""Tests des calculs du contexte territorial."""

from patrimoine_orne.geocode.territorial_context import (
    geometry_distance,
    point_in_ring,
    proximity_class,
)


def test_line_and_polygon_distances() -> None:
    point = [0.0, 48.5]
    line = {"type": "LineString", "coordinates": [[-0.01, 48.5], [0.01, 48.5]]}
    polygon = {
        "type": "Polygon",
        "coordinates": [[[-0.01, 48.49], [0.01, 48.49], [0.01, 48.51], [-0.01, 48.51], [-0.01, 48.49]]],
    }
    assert geometry_distance(point, line) == 0
    assert geometry_distance(point, polygon) == 0
    assert point_in_ring(point, polygon["coordinates"][0])


def test_proximity_class_preserves_search_limit() -> None:
    limits = ((100, "proche"), (500, "environnant"))
    assert proximity_class(80, limits) == "proche"
    assert proximity_class(300, limits) == "environnant"
    assert proximity_class(None, limits) == "hors_rayon_de_recherche"
    assert proximity_class(900, limits) == "hors_rayon_de_recherche"

