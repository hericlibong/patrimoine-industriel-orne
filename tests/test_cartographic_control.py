"""Tests du contrôle cartographique du pilote."""

from pyproj import Transformer

from patrimoine_orne.geocode.cartographic_control import (
    polygon_area_m2,
    ring_is_closed,
    ring_self_intersects,
)


def test_polygon_helpers_detect_closed_and_crossed_rings() -> None:
    square = [[0, 48.5], [0.01, 48.5], [0.01, 48.51], [0, 48.51], [0, 48.5]]
    crossed = [[0, 48.5], [0.01, 48.51], [0, 48.51], [0.01, 48.5], [0, 48.5]]

    assert ring_is_closed(square)
    assert not ring_self_intersects(square)
    assert ring_self_intersects(crossed)


def test_projected_polygon_area_is_positive() -> None:
    transformer = Transformer.from_crs(4326, 2154, always_xy=True)
    square = [[0, 48.5], [0.001, 48.5], [0.001, 48.501], [0, 48.501], [0, 48.5]]

    assert polygon_area_m2(square, transformer) > 0
