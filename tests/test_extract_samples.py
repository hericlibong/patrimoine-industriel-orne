"""Tests des validateurs utilisés par les extractions d'échantillons."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from patrimoine_orne.extract.samples import (
    validate_casias_xml,
    validate_inventaire_index,
    validate_mh_json,
    validate_palissy_json,
    validate_pop_notice,
)


class SampleValidatorsTests(TestCase):
    def setUp(self) -> None:
        self.temp_directory = TemporaryDirectory()
        self.addCleanup(self.temp_directory.cleanup)
        self.path = Path(self.temp_directory.name) / "sample"

    def test_inventaire_challenge_is_rejected(self) -> None:
        self.path.write_bytes(b"IA00060965 THUMBNAILFRAME.HTM haphash")
        with self.assertRaises(ValueError):
            validate_inventaire_index("IA00060965")(self.path)

    def test_pop_notice_reports_links(self) -> None:
        self.path.write_bytes(
            b"IA00060965 inventaire-patrimoine.normandie.fr www2.culture.gouv.fr"
        )
        observations = validate_pop_notice("IA00060965")(self.path)
        self.assertTrue(observations["has_inventaire_link"])
        self.assertTrue(observations["has_static_dossier_link"])

    def test_palissy_references_and_link_are_measured(self) -> None:
        payload = {
            "total_count": 2,
            "results": [
                {"reference": "PM61000916", "reference_a_une_notice_merimee_mh": "PA1"},
                {"reference": "PM61000814", "reference_a_une_notice_merimee_mh": None},
            ],
        }
        self.path.write_text(json.dumps(payload), encoding="utf-8")
        observations = validate_palissy_json(self.path)
        self.assertEqual(observations["result_count"], 2)
        self.assertEqual(observations["with_merimee_reference"], 1)

    def test_mh_wrong_department_is_rejected(self) -> None:
        payload = {
            "total_count": 1,
            "results": [{"reference": "PA1", "departement_en_lettres": "Calvados"}],
        }
        self.path.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaises(ValueError):
            validate_mh_json(self.path)

    def test_mh_department_list_is_accepted(self) -> None:
        payload = {
            "total_count": 1,
            "results": [
                {
                    "reference": "PA1",
                    "departement_en_lettres": ["Orne"],
                    "coordonnees_au_format_wgs84": {"lon": 0.1, "lat": 48.5},
                }
            ],
        }
        self.path.write_text(json.dumps(payload), encoding="utf-8")
        observations = validate_mh_json(self.path)
        self.assertEqual(observations["with_coordinates"], 1)

    def test_casias_localized_sample_is_measured(self) -> None:
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <wfs:FeatureCollection xmlns:wfs="http://www.opengis.net/wfs/2.0"
          xmlns:ms="http://mapserver.gis.umn.edu/mapserver">
          <wfs:member><ms:drealnorm_casias_s_r28>
            <ms:code_depar>61</ms:code_depar><ms:code_inven>BNO1</ms:code_inven>
            <ms:nom_etabli>Forge</ms:nom_etabli><ms:x_wgs84>-0.5</ms:x_wgs84>
          </ms:drealnorm_casias_s_r28></wfs:member>
        </wfs:FeatureCollection>"""
        self.path.write_text(xml, encoding="utf-8")
        observations = validate_casias_xml(True)(self.path)
        self.assertEqual(observations["result_count"], 1)
        self.assertEqual(observations["with_coordinates"], 1)
