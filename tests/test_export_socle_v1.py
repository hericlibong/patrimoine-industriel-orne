"""Tests de consolidation et d'export du socle V1."""

from patrimoine_orne.export.socle_v1 import (
    consolidate_corpus,
    flat_rows,
    stable_uuid,
)


def test_stable_uuid_is_reproducible() -> None:
    assert stable_uuid("site", "IA1") == stable_uuid("site", "IA1")
    assert stable_uuid("site", "IA1") != stable_uuid("site", "IA2")


def test_consolidation_keeps_conservative_precision() -> None:
    corpus = {
        "corpus_version": "1.0",
        "classifications_version": "1.1",
        "validation": {},
        "objets_techniques": [],
        "anomalies": [],
        "sites": [
            {
                "site_id": "00000000-0000-0000-0000-000000000001",
                "reference_ia": "IA1",
                "statut_corpus_code": "rapproche",
            }
        ],
    }
    locations = {
        "locations": [
            {
                "reference_ia": "IA1",
                "geometrie_reference": {},
                "controle_humain_cartographique": "a_realiser",
            }
        ]
    }
    context = {"sites": [{"reference_ia": "IA1"}]}
    control = {"cas_sensibles": []}

    result = consolidate_corpus(corpus, locations, context, control)
    site = result["sites"][0]

    assert site["statut_corpus_code"] == "cartographiable"
    assert (
        site["localisation"]["geometrie_reference"]["precision_geographique_code"]
        == "point_approximatif"
    )
    assert site["localisation"]["controle_humain_cartographique"] == (
        "controle_coherent_approximatif"
    )


def test_flat_rows_preserve_one_row_per_site() -> None:
    site = {
        "site_id": "00000000-0000-0000-0000-000000000001",
        "reference_ia": "IA1",
        "nom_principal": "Site test",
        "commune_actuelle_code_insee": "61001",
        "commune_actuelle_nom": "Commune",
        "commune_historique_nom": "Commune",
        "lieu_dit": None,
        "historique_source": "Historique",
        "protection_mh_reference": None,
        "activites": [
            {
                "secteur_code": "metal",
                "activite_code": "forge",
                "libelle_source": "forge",
            }
        ],
        "situation_actuelle": {
            "conservation_code": "inconnu",
            "usages": ["inconnu"],
            "accessibilite_code": "inconnu",
            "date_verification": "2026-07-22",
        },
        "sources": [
            {"role": "notice_principale", "url": "https://example.test/IA1"}
        ],
        "localisation": {
            "statut_localisation_code": "geometrie_approximative",
            "geometrie_reference": {
                "point_wgs84": [0.1, 48.5],
                "point_lambert93": [500000, 6800000],
            },
            "emprise_source": None,
            "parcelles_actuelles_candidates": [
                {"idu": "61001000AA0001", "reference_source_concordante": False}
            ],
        },
        "controle_cartographique": {"motifs": []},
        "contexte_territorial": {
            "cours_eau": {"distance_m": 10, "classe_proximite": "moins_25_m"},
            "foret": {"distance_m": 20, "classe_proximite": "moins_100_m"},
            "geologie": {"lithologie": {"DESCR": "schiste"}},
            "ressource_minerale": {
                "distance_m": 500,
                "classe_proximite": "moins_1_km",
            },
            "rail": {"distance_m": 2000, "classe_proximite": "moins_2_km"},
        },
    }

    rows = flat_rows({"sites": [site]})

    assert len(rows) == 1
    assert rows[0]["site_id"] == site["site_id"]
    assert rows[0]["secteurs_codes"] == "metal"
    assert rows[0]["longitude"] == 0.1
