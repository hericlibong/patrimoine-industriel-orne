"""Tests de la structure commune des 80 dossiers."""

from patrimoine_orne.transform.corpus_80 import find_match_candidates, flat_rows


def _record(reference: str, origin: str, address: str = "") -> dict:
    return {
        "dossier_reference": reference,
        "origine": origin,
        "insee_source": ["61001"],
        "adresses_source": [address] if address else [],
        "lieux_dits_source": [],
        "dossier_url": f"https://example.test/{reference}",
        "longitude_source": None,
        "latitude_source": None,
    }


def test_same_normalised_address_is_only_a_candidate() -> None:
    records = [
        _record("IA00000001", "pilote_30", "Rue du Moulin, 2"),
        _record("IA00000002", "phase8_lot1_50", "rue du moulin 2"),
    ]
    candidates = find_match_candidates(records)
    assert len(candidates) == 1
    assert candidates[0]["motifs"] == "meme_adresse_normalisee"
    assert candidates[0]["decision"] == "a_verifier"


def test_distinct_records_are_not_merged() -> None:
    records = [
        _record("IA00000001", "pilote_30", "Rue A"),
        _record("IA00000002", "phase8_lot1_50", "Rue B"),
    ]
    assert find_match_candidates(records) == []


def test_flat_export_preserves_origin_and_nullable_site_id() -> None:
    corpus = {
        "dossiers": [
            {
                **_record("IA00000001", "phase8_lot1_50"),
                "statut_traitement": "structure_classee_a_enrichir",
                "statut_site": "site_provisoire_lot1_valide",
                "site_id": None,
                "titre_source": "moulin",
                "communes_source": ["Alençon"],
                "denominations_source": ["moulin à farine"],
                "activites": [{"activite_code": "mouture_cereales"}],
                "secteurs_codes": ["agroalimentaire"],
                "installations_codes": ["moulin"],
                "periodes_activite_codes": [],
                "periodes_source_codes": ["industrialisation_rail_vapeur"],
                "localisation_statut_code": "non_localise",
                "decision_rapprochement": "aucun_rapprochement_requis_a_ce_stade",
            }
        ]
    }
    row = flat_rows(corpus)[0]
    assert row["origine"] == "phase8_lot1_50"
    assert row["site_id"] is None
    assert row["activites_codes"] == "mouture_cereales"
