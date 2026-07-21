"""Tests de préparation des requêtes géographiques du pilote."""

from patrimoine_orne.extract.pilot_geography import build_specs, sufficient_address_query


def test_unique_pop_address_is_reformatted() -> None:
    record = {
        "REF": "IA1",
        "ADRS": "Poulet Malassis (place) 19",
        "COM": ["Alençon"],
        "INSEE": ["61001"],
        "POP_COORDONNEES": {"lon": 0.08, "lat": 48.43},
    }
    assert sufficient_address_query(record) == "19 place Poulet Malassis Alençon"
    specs, rejected = build_specs([record])
    assert [item.source_id for item in specs] == ["ban", "cadastre"]
    assert rejected == []


def test_street_or_number_range_is_not_geocoded() -> None:
    base = {
        "REF": "IA1",
        "COM": ["Alençon"],
        "INSEE": ["61001"],
        "POP_COORDONNEES": {"lon": 0.08, "lat": 48.43},
    }
    assert sufficient_address_query({**base, "ADRS": "Touque (rue de la)"}) is None
    assert sufficient_address_query({**base, "ADRS": "Ancinnes (route d') 4 à 22"}) is None

