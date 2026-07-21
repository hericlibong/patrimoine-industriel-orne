"""Tests de qualification géographique du pilote."""

from patrimoine_orne.geocode.pilot import (
    cadastral_reference_matches,
    haversine_metres,
    parse_lambert_point,
    parse_lambert_polygon,
    parse_pop_wgs_polygon,
    valid_wgs84,
)


def test_pop_coordinate_parsers() -> None:
    assert parse_lambert_point("0484694;6818662") == [484694.0, 6818662.0]
    assert parse_lambert_polygon("1;2/3;4/5;6/1;2") == [
        [1.0, 2.0],
        [3.0, 4.0],
        [5.0, 6.0],
        [1.0, 2.0],
    ]
    assert parse_pop_wgs_polygon(
        {"coordinates": [[48.4, 0.1], [48.5, 0.2], [48.6, 0.3], [48.4, 0.1]]}
    ) == [[0.1, 48.4], [0.2, 48.5], [0.3, 48.6], [0.1, 48.4]]


def test_wgs_envelope_and_distance() -> None:
    assert valid_wgs84([0.1, 48.5])
    assert not valid_wgs84([2.3, 48.5])
    assert haversine_metres([0.1, 48.5], [0.1, 48.5]) == 0


def test_cadastral_reference_comparison_accepts_lists_and_ranges() -> None:
    assert cadastral_reference_matches("0B", "0032", ["1980 B 32"])
    assert cadastral_reference_matches("ZR", "0033", ["1987 ZR 30 A 33"])
    assert not cadastral_reference_matches("AI", "1032", ["1980 AI 986"])
