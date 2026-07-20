"""Tests de l'évaluation de qualité des échantillons."""

from __future__ import annotations

import json
from unittest import TestCase

from patrimoine_orne.validate.sample_quality import (
    completeness_profile,
    coordinate_profile,
    extract_pop_notice,
    identifier_profile,
    inspect_encoding,
)


class SampleQualityTests(TestCase):
    def test_pop_notice_is_extracted_from_next_f_payload(self) -> None:
        chunk = '1:{"notice":{"REF":"IA1","TICO":"forge","COM":["Test"]}}'
        pushed = json.dumps([1, chunk], ensure_ascii=False)
        html = f"<html><script>self.__next_f.push({pushed})</script></html>"
        notice = extract_pop_notice(html, "IA1")
        self.assertEqual(notice["TICO"], "forge")

    def test_completeness_treats_empty_collections_as_missing(self) -> None:
        records = [{"id": "A", "name": []}, {"id": "B", "name": ["Forge"]}]
        profile = completeness_profile(records, ("id", "name"))
        self.assertEqual(profile["priority_fields"]["name"]["filled"], 1)
        self.assertEqual(profile["priority_fields"]["name"]["missing"], 1)

    def test_identifier_duplicates_are_reported(self) -> None:
        records = [{"id": "A"}, {"id": "A"}, {"id": "B"}, {"id": ""}]
        profile = identifier_profile(records, ("id",))
        self.assertEqual(profile["id"]["filled"], 3)
        self.assertEqual(profile["id"]["value_count"], 3)
        self.assertEqual(profile["id"]["unique"], 2)
        self.assertEqual(profile["id"]["duplicate_values"], ["A"])

    def test_identifier_lists_are_flattened(self) -> None:
        records = [{"insee": ["61001"]}, {"insee": ["61001", "61002"]}]
        profile = identifier_profile(records, ("insee",))
        self.assertEqual(profile["insee"]["filled"], 2)
        self.assertEqual(profile["insee"]["value_count"], 3)
        self.assertEqual(profile["insee"]["duplicate_values"], ["61001"])

    def test_coordinates_distinguish_missing_and_invalid(self) -> None:
        records = [
            {"lon": "-0.5", "lat": "48.7"},
            {"lon": "", "lat": ""},
            {"lon": "999", "lat": "48.7"},
        ]
        profile = coordinate_profile(
            records,
            lambda row: (row.get("lon"), row.get("lat")),
        )
        self.assertEqual(profile["present"], 2)
        self.assertEqual(profile["valid_wgs84"], 1)
        self.assertEqual(profile["within_broad_orne_envelope"], 1)
        self.assertEqual(profile["invalid_row_indexes"], [2])

    def test_declared_utf8_is_decoded_strictly(self) -> None:
        profile = inspect_encoding("énergie".encode(), "text/plain; charset=utf-8")
        self.assertEqual(profile["decoded_as"], "utf-8")
        self.assertTrue(profile["strict_decode"])
