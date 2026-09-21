"""T1 du filtre temporel — établir les époques de chaque lieu.

Un lieu appartient à une époque lorsqu'au moins un événement daté de sa
chronologie a son **intervalle propre** qui chevauche cette époque. L'intervalle
est celui que la source donne à l'événement : « 1949 » vaut 1949-1949, « vers
1920 » vaut 1915-1925, « 19e siècle » vaut 1801-1900.

Deux interdits structurent ce calcul, et deux contrôles les vérifient :

- **Aucun lien entre deux événements.** Un lieu documenté en 1700 puis en 1900
  n'appartient pas aux époques intermédiaires. La règle de l'intervalle
  première-dernière date, proposée puis refusée le 21 septembre 2026, fabriquait
  une continuité absente de la source.
- **Aucune année inventée.** Les événements dont une borne est ouverte —
  « après 1920 », « avant 1900 » — sont écartés du calcul. Les ancrer sur 1921
  ou 1899 inventerait une année que la source ne donne pas. Ils restent
  intégralement dans la chronologie du lieu et continuent d'être lisibles.

Ce module ne modifie aucune donnée : il lit les exports du corpus et imprime un
rapport JSON. Il sort en code 1 si un contrôle échoue.

Décisions : `docs/phase10_filtre_temporel.md`, version 3.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

RACINE = Path(__file__).resolve().parent.parent
DEFAULT_CHRONOLOGIE = RACINE / "data" / "exports" / "chronologie_sites_v1.csv"
DEFAULT_SITES = RACINE / "data" / "exports" / "sites_corpus_complet_v1.csv"
DEFAULT_CLASSIFICATIONS = RACINE / "config" / "classifications.yml"
DEFAULT_SORTIE = RACINE / "data" / "interim" / "epoques_lieux_v1.json"

# « Depuis 2001 » est retirée du filtre par décision du 21 septembre 2026 : un
# seul lieu la porte, pour un seul événement de toute la chronologie. Elle reste
# dans le vocabulaire contrôlé, d'où l'exclusion par code plutôt que par retrait.
EPOQUE_ECARTEE = "periode_contemporaine"

# Effectifs arrêtés avec le porteur dans la version 3 du document de décision.
# Un écart ici n'est pas une régression à corriger dans l'assertion : c'est un
# changement de corpus à justifier.
ATTENDUS = {
    "lieux_total": 318,
    "lieux_dates": 314,
    "evenements_retenus": 2243,
    "evenements_bornes_ouvertes": 117,
    "par_epoque": {
        "avant_1789": 67,
        "revolution_premiere_industrialisation": 176,
        "industrialisation_rail_vapeur": 258,
        "guerres_entre_deux_guerres": 168,
        "modernisation_apres_guerre": 154,
        "mutations_reconversions": 103,
    },
}


def lire_epoques(chemin: Path = DEFAULT_CLASSIFICATIONS) -> list[dict]:
    """Les époques du filtre, dans l'ordre du vocabulaire contrôlé."""
    vocabulaire = yaml.safe_load(chemin.read_text(encoding="utf-8"))
    epoques = []
    for code, entree in vocabulaire["periodes_historiques"].items():
        if code == EPOQUE_ECARTEE:
            continue
        epoques.append(
            {
                "code": code,
                "libelle": entree["libelle"],
                # Une borne nulle dans le registre signifie « pas de limite de ce
                # côté » : « Avant 1789 » n'a pas de début.
                "debut": entree["debut_annee"],
                "fin": entree["fin_annee"],
            }
        )
    return epoques


def annee(valeur: str | None) -> int | None:
    """L'année d'une date d'export, qui est au format AAAA-MM-JJ."""
    trouve = re.match(r"^(\d{4})", (valeur or "").strip())
    return int(trouve.group(1)) if trouve else None


def intervalle_evenement(ligne: dict) -> tuple[int, int] | None:
    """L'intervalle propre d'un événement, ou None si une borne est ouverte.

    Rendre None est ici le comportement correct et non un échec : un événement
    que la source situe seulement « après 1920 » n'appartient à aucune époque.
    """
    debut, fin = annee(ligne["date_min"]), annee(ligne["date_max"])
    if debut is None or fin is None:
        return None
    return (debut, fin)


def epoques_chevauchees(bornes: tuple[int, int], epoques: list[dict]) -> list[str]:
    """Les époques que traverse un intervalle, et elles seules."""
    debut, fin = bornes
    return [
        epoque["code"]
        for epoque in epoques
        if (epoque["fin"] is None or debut <= epoque["fin"])
        and (epoque["debut"] is None or fin >= epoque["debut"])
    ]


def calculer(
    chronologie: Path = DEFAULT_CHRONOLOGIE,
    classifications: Path = DEFAULT_CLASSIFICATIONS,
) -> dict:
    """Les époques de chaque lieu, plus la trace de ce qui a été écarté."""
    epoques = lire_epoques(classifications)
    lignes = list(csv.DictReader(chronologie.open(encoding="utf-8")))

    par_lieu: dict[str, set[str]] = defaultdict(set)
    justifications: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    ecartes: list[dict] = []

    for ligne in lignes:
        reference = ligne["reference_ia"]
        bornes = intervalle_evenement(ligne)
        if bornes is None:
            ecartes.append(
                {
                    "ref": reference,
                    "precision": ligne["precision_code"].strip(),
                    "texte": ligne["texte_source"].strip(),
                }
            )
            continue
        for code in epoques_chevauchees(bornes, epoques):
            par_lieu[reference].add(code)
            justifications[reference][code].append(ligne["texte_source"].strip())

    return {
        "epoques": epoques,
        "par_lieu": {ref: sorted(codes) for ref, codes in par_lieu.items()},
        "justifications": justifications,
        "evenements_total": len(lignes),
        "evenements_retenus": len(lignes) - len(ecartes),
        "ecartes": ecartes,
    }


def repartir(calcul: dict, sites: Path = DEFAULT_SITES) -> dict:
    """Les décomptes par époque, par ensemble et par métier."""
    sys.path.insert(0, str(RACINE / "tools"))
    import generer_vue_reference as vue  # noqa: PLC0415

    lignes = {r["reference_ia"]: r for r in csv.DictReader(sites.open(encoding="utf-8"))}
    par_lieu = calcul["par_lieu"]
    codes = [e["code"] for e in calcul["epoques"]]

    # Le rattachement aux ensembles est calculé par le générateur de la vue ;
    # le réimplémenter ici créerait une seconde vérité sur le même découpage.
    tous = [s["code"] for s in vue.construire()["departement"]["systemes"]]
    vue.SYSTEMES_DETAILLES = tuple(tous)
    donnees = vue.construire()

    par_epoque = {c: sum(1 for v in par_lieu.values() if c in v) for c in codes}

    par_ensemble = {}
    for code, detail in donnees["detail"].items():
        refs = {s["ref"] for s in detail["sites"]}
        par_ensemble[code] = {
            "lieux": len(refs),
            "dates": len(refs & set(par_lieu)),
            "epoques": {
                c: sum(1 for r in refs if c in par_lieu.get(r, ())) for c in codes
            },
        }

    def secteurs(ligne: dict) -> list[str]:
        return [x.strip() for x in (ligne["secteurs_codes"] or "").split("|") if x.strip()]

    metiers = sorted({s for ligne in lignes.values() for s in secteurs(ligne)})
    par_metier = {}
    for metier in metiers:
        concernes = {r for r, ligne in lignes.items() if metier in secteurs(ligne)}
        par_metier[metier] = {
            "lieux": len(concernes),
            "epoques": {
                c: sum(1 for r in concernes if c in par_lieu.get(r, ())) for c in codes
            },
        }

    sans_date = [
        {"ref": r, "nom": ligne["nom_principal"], "commune": ligne["communes_source"]}
        for r, ligne in sorted(lignes.items())
        if r not in par_lieu
    ]
    en_ensemble = {s["ref"] for d in donnees["detail"].values() for s in d["sites"]}

    return {
        "lieux_total": len(lignes),
        "lieux_dates": len(par_lieu),
        "par_epoque": par_epoque,
        "par_ensemble": par_ensemble,
        "par_metier": par_metier,
        "sans_date": sans_date,
        "sans_date_en_ensemble": [s["ref"] for s in sans_date if s["ref"] in en_ensemble],
        "couples_vides": [
            {"ensemble": code, "epoque": c}
            for code, bilan in par_ensemble.items()
            for c in codes
            if bilan["epoques"][c] == 0
        ],
        "trajectoires": {
            str(n): sum(1 for v in par_lieu.values() if len(v) == n)
            for n in range(1, len(codes) + 1)
        },
    }


def _troue(epoques: list[str], codes: list[str]) -> bool:
    """Vrai si le lieu saute au moins une époque entre deux qu'il occupe.

    Un tel lieu est la preuve que le calcul n'a pas comblé le silence de la
    source : la règle de l'intervalle, refusée le 21 septembre 2026, aurait
    rempli ce trou.
    """
    rangs = sorted(codes.index(c) for c in epoques)
    return bool(rangs) and rangs[-1] - rangs[0] + 1 > len(rangs)


def controler(calcul: dict, bilan: dict) -> tuple[dict, list[str]]:
    """Les cinq contrôles de T1. Un seul faux suffit à refuser la production."""
    ecarts: list[str] = []
    codes = [e["code"] for e in calcul["epoques"]]

    # 1. Les effectifs sont ceux arrêtés avec le porteur.
    effectifs = (
        bilan["lieux_total"] == ATTENDUS["lieux_total"]
        and bilan["lieux_dates"] == ATTENDUS["lieux_dates"]
        and calcul["evenements_retenus"] == ATTENDUS["evenements_retenus"]
        and len(calcul["ecartes"]) == ATTENDUS["evenements_bornes_ouvertes"]
        and bilan["par_epoque"] == ATTENDUS["par_epoque"]
    )
    if not effectifs:
        ecarts.append(
            f"effectifs : {bilan['lieux_dates']}/{bilan['lieux_total']} lieux datés, "
            f"{calcul['evenements_retenus']} événements retenus, "
            f"{len(calcul['ecartes'])} écartés, par époque {bilan['par_epoque']}"
        )

    # 2. Chaque époque attribuée s'appuie sur au moins un événement nommable.
    justifiees = all(
        calcul["justifications"][ref].get(code)
        for ref, epoques in calcul["par_lieu"].items()
        for code in epoques
    )
    if not justifiees:
        ecarts.append("une époque est attribuée sans événement qui la justifie")

    # 3. Aucune époque intermédiaire n'est ajoutée entre deux faits.
    #
    #    Comparer le résultat à lui-même ne prouverait rien. Le contrôle compare
    #    donc au **résultat qu'aurait donné la règle refusée** — celle de
    #    l'intervalle entre la première et la dernière date. Cette règle produit
    #    toujours un ensemble d'époques contigu ; la nôtre laisse des trous
    #    partout où la source se tait. Si les deux coïncidaient partout, c'est
    #    que nous aurions reconstitué la continuité que nous refusons.
    trous = [ref for ref, e in calcul["par_lieu"].items() if _troue(e, codes)]
    sans_pont = bool(trous)
    if not sans_pont:
        ecarts.append(
            "aucun lieu ne présente de trou entre deux époques : le calcul a "
            "reconstitué une continuité entre des faits distincts"
        )

    # 4. Aucune année n'est inventée : tout événement écarté l'est bien pour
    #    borne ouverte, et aucun n'a contribué à une époque.
    aucune_annee_inventee = all(
        e["precision"] in {"avant", "apres"} for e in calcul["ecartes"]
    )
    if not aucune_annee_inventee:
        mauvais = {e["precision"] for e in calcul["ecartes"]} - {"avant", "apres"}
        ecarts.append(f"événements écartés pour un autre motif que la borne ouverte : {mauvais}")

    # 5. Les événements écartés restent affichables : ils portent un texte source.
    ecartes_lisibles = all(e["texte"] for e in calcul["ecartes"])
    if not ecartes_lisibles:
        ecarts.append("un événement écarté n'a plus de texte source affichable")

    controles = {
        "effectifs_conformes": effectifs,
        "epoques_justifiees": justifiees,
        "aucun_pont_entre_deux_faits": sans_pont,
        "aucune_annee_inventee": aucune_annee_inventee,
        "evenements_ecartes_toujours_lisibles": ecartes_lisibles,
        "toutes_les_epoques_servent": all(bilan["par_epoque"][c] > 0 for c in codes),
    }
    return controles, ecarts


def main() -> None:
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument("--sortie", type=Path, default=DEFAULT_SORTIE)
    parseur.add_argument("--sans-ecrire", action="store_true")
    arguments = parseur.parse_args()

    calcul = calculer()
    bilan = repartir(calcul)
    controles, ecarts = controler(calcul, bilan)
    reussi = all(controles.values())

    if reussi and not arguments.sans_ecrire:
        arguments.sortie.parent.mkdir(parents=True, exist_ok=True)
        arguments.sortie.write_text(
            json.dumps(
                {
                    "epoques": calcul["epoques"],
                    "par_lieu": calcul["par_lieu"],
                    "par_ensemble": {
                        code: sorted(
                            c for c, n in bilan["par_ensemble"][code]["epoques"].items() if n
                        )
                        for code in bilan["par_ensemble"]
                    },
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    rapport = {
        "controles": controles,
        "checks_passed": reussi,
        "ecarts": ecarts,
        "lieux_total": bilan["lieux_total"],
        "lieux_dates": bilan["lieux_dates"],
        "lieux_sans_date": [s["ref"] for s in bilan["sans_date"]],
        "lieux_sans_date_en_ensemble": bilan["sans_date_en_ensemble"],
        "evenements_total": calcul["evenements_total"],
        "evenements_retenus": calcul["evenements_retenus"],
        "evenements_ecartes_borne_ouverte": len(calcul["ecartes"]),
        "par_epoque": bilan["par_epoque"],
        "par_ensemble": {
            code: bilan["par_ensemble"][code]["epoques"] for code in bilan["par_ensemble"]
        },
        "par_metier": {m: bilan["par_metier"][m]["epoques"] for m in bilan["par_metier"]},
        "couples_ensemble_epoque_vides": bilan["couples_vides"],
        "trajectoires": bilan["trajectoires"],
        "lieux_avec_un_trou_entre_deux_epoques": len(
            [r for r, e in calcul["par_lieu"].items() if _troue(e, [x["code"] for x in calcul["epoques"]])]
        ),
        "sortie": None if arguments.sans_ecrire else str(arguments.sortie),
    }
    print(json.dumps(rapport, ensure_ascii=False, indent=2))
    if not reussi:
        sys.exit(1)


if __name__ == "__main__":
    main()
