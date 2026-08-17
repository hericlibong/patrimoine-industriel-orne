import json
from pathlib import Path

from patrimoine_orne.export.chronologie_v1 import resoudre_date, type_evenement, MOTIFS_DATE
import re

ROOT = Path(__file__).resolve().parents[1]


def rapport() -> dict:
    return json.loads(
        (ROOT / "reports" / "quality" / "phase10_chronologie_sites.json").read_text(
            encoding="utf-8"
        )
    )


def match(code: str, texte: str) -> re.Match[str]:
    motif = dict(MOTIFS_DATE)[code]
    trouve = re.search(motif, texte, re.IGNORECASE)
    assert trouve is not None
    return trouve


def test_chronologie_produite_et_validee() -> None:
    donnees = rapport()
    assert donnees["checks_passed"] is True
    assert donnees["counts"]["notices_lues"] == 314
    assert donnees["counts"]["evenements"] == donnees["counts"]["lignes_en_base"]
    assert donnees["counts"]["evenements_ecartes_par_revue"] == 11


def test_une_date_imprecise_reste_un_intervalle() -> None:
    minimum, maximum, precision = resoudre_date("vers_annee", match("vers_annee", "vers 1850"))
    assert (minimum, maximum, precision) == ("1845-01-01", "1855-12-31", "vers_annee")


def test_une_borne_ouverte_reste_nulle() -> None:
    minimum, maximum, precision = resoudre_date("apres", match("apres", "après 1945"))
    assert minimum == "1946-01-01"
    assert maximum == ""
    assert precision == "apres"


def test_reconstruire_n_est_pas_construire() -> None:
    assert type_evenement("reconstruite en 1880 par Benjamin Bohin") == "reconstruction"
    assert type_evenement("Tissage construit en 1877") == "creation"


def test_une_fermentation_n_est_pas_une_fermeture() -> None:
    assert type_evenement("installation de cuves de fermentation") != "cessation"


def test_un_texte_source_absurde_est_refuse() -> None:
    from patrimoine_orne.export.corpus_complet_v1 import textes_sources_absurdes

    corpus = {
        "sites": [
            {"reference_ia": "IA_JETON", "historique_source": "$26"},
            {"reference_ia": "IA_BALISE", "historique_source": "<div>"},
            {"reference_ia": "IA_VIDE", "historique_source": "null"},
            {
                "reference_ia": "IA_VRAI",
                "historique_source": "Moulin attesté en 1809, converti vers 1840.",
            },
        ]
    }
    assert textes_sources_absurdes(corpus) == {"IA_JETON", "IA_BALISE", "IA_VIDE"}


def test_les_historiques_repares_sont_dans_le_corpus() -> None:
    import duckdb

    base = ROOT / "data" / "processed" / "patrimoine_orne_corpus_complet_v1.duckdb"
    if not base.exists():
        return
    connection = duckdb.connect(str(base), read_only=True)
    longueurs = dict(
        connection.execute(
            "select reference_ia, length(historique_source) from recits_sites"
            " where reference_ia in ('IA00060969', 'IA00061153')"
        ).fetchall()
    )
    connection.close()
    assert longueurs["IA00060969"] > 1000
    assert longueurs["IA00061153"] > 1000
