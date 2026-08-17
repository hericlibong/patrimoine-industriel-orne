"""Fabrique la vue de référence de la phase 10.D.

Un seul fichier HTML autonome, sans serveur ni dépendance : on l'ouvre dans un
navigateur et il fonctionne. Toutes les données sont incluses dans la page et
viennent du corpus validé.

La vue porte trois niveaux et rien d'autre : le département, la vallée de la
Risle, puis un site. Les données de Crulai sont embarquées elles aussi, non pour
construire un second écran, mais pour vérifier que la même forme tient sur un
système pauvre.

    python tools/generer_vue_reference.py

Le script échoue si les effectifs calculés ne correspondent pas au registre des
systèmes : une vue de référence bâtie sur des chiffres faux ne vaut rien.
"""

from __future__ import annotations

import glob
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import duckdb
import yaml


RACINE = Path(__file__).resolve().parents[1]
BASE = RACINE / "data" / "processed" / "patrimoine_orne_corpus_complet_v1.duckdb"
REGISTRE = RACINE / "config" / "phase10_systemes.yml"
COMMUNES = (
    RACINE / "data" / "raw" / "api_geo" / "2026" / "2026-07-22" / "communes_orne_contours.geojson"
)
CLASSIFICATIONS = RACINE / "config" / "classifications.yml"
GABARIT = Path(__file__).resolve().parent / "vue_reference_gabarit.html"
SORTIE = RACINE / "prototype" / "vue_reference" / "index.html"

SEUIL_REGROUPEMENT_M = 3000
MARGE_DEGRES = 0.02

# Systèmes détaillés dans la vue : celui qu'on lit, et celui qui sert de contrôle.
SYSTEMES_DETAILLES = ("risle", "crulai")


# --------------------------------------------------------------------------
# Regroupement des sites
# --------------------------------------------------------------------------


def groupes_par_proximite(lignes: list[tuple]) -> list[list[int]]:
    """Regroupe les indices des sites distants de moins du seuil, de proche en proche."""
    parent = list(range(len(lignes)))

    def racine(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    for i in range(len(lignes)):
        for j in range(i + 1, len(lignes)):
            distance = math.hypot(lignes[i][1] - lignes[j][1], lignes[i][2] - lignes[j][2])
            if distance < SEUIL_REGROUPEMENT_M:
                a, b = racine(i), racine(j)
                if a != b:
                    parent[b] = a

    groupes: dict[int, list[int]] = defaultdict(list)
    for index in range(len(lignes)):
        groupes[racine(index)].append(index)
    return sorted(groupes.values(), key=len, reverse=True)


def rattacher_systemes(
    groupes: list[list[int]], lignes: list[tuple], registre: dict
) -> tuple[dict[str, list[int]], list[str]]:
    """Associe chaque système du registre au groupe calculé qui contient sa commune d'ancrage.

    L'ancrage par commune est nécessaire : quatre systèmes partagent leur
    effectif avec un autre, le rang seul ne les distingue donc pas.
    """
    par_code: dict[str, list[int]] = {}
    ecarts: list[str] = []
    deja_pris: set[int] = set()

    for systeme in registre["systemes"]:
        candidats = [
            (rang, groupe)
            for rang, groupe in enumerate(groupes)
            if rang not in deja_pris
            and any(lignes[i][3] == systeme["commune_ancrage"] for i in groupe)
        ]
        if not candidats:
            ecarts.append(f"{systeme['code']} : aucun groupe ne contient {systeme['commune_ancrage']}")
            continue
        rang, groupe = max(candidats, key=lambda couple: len(couple[1]))
        deja_pris.add(rang)
        par_code[systeme["code"]] = groupe
        if len(groupe) != systeme["sites_attendus"]:
            ecarts.append(
                f"{systeme['code']} : {len(groupe)} sites calculés"
                f" contre {systeme['sites_attendus']} attendus"
            )
    return par_code, ecarts


# --------------------------------------------------------------------------
# Lecture du corpus
# --------------------------------------------------------------------------


def nom_court(nom: str | None) -> str:
    """Version abrégée du nom, pour les listes et les libellés de liens.

    Les noms de l'Inventaire cumulent l'état ancien et l'état actuel — « tréfilerie
    Boisthorel, actuellement usine de transformation des métaux dite Tréfimétaux ».
    Le nom entier reste affiché dans la fiche du site ; seules les listes sont
    abrégées, faute de quoi elles deviennent illisibles.
    """
    if not nom:
        return "site sans nom"
    abrege = nom.split(",")[0].strip()
    if len(abrege) > 46:
        coupe = abrege[:46].rsplit(" ", 1)[0]
        return coupe + "…"
    return abrege


def lire_sites(connection: duckdb.DuckDBPyConnection) -> list[dict]:
    lignes = connection.execute(
        """
        select s.reference_ia, s.nom_principal, s.communes_source, s.lieux_dits_source,
               s.longitude, s.latitude, s.secteurs_codes, s.nombre_activites,
               s.distance_cours_eau_m, s.precision_geographique_code,
               s.conservation_code, s.source_principale_url, r.historique_source
        from sites s
        left join recits_sites r on r.site_id = s.site_id
        where s.longitude is not null
        order by s.communes_source, s.reference_ia
        """
    ).fetchall()
    return [
        {
            "ref": ligne[0],
            "nom": ligne[1],
            "nomCourt": nom_court(ligne[1]),
            "commune": ligne[2],
            "lieuDit": ligne[3] or "",
            "lon": ligne[4],
            "lat": ligne[5],
            "secteurs": [code.strip() for code in (ligne[6] or "").split("|") if code.strip()],
            "nbActivites": ligne[7],
            "eau": ligne[8],
            "precision": ligne[9],
            "conservation": ligne[10],
            "url": ligne[11],
            "histoire": ligne[12] or "",
        }
        for ligne in lignes
    ]


def lire_liens(connection: duckdb.DuckDBPyConnection, references: set[str]) -> list[dict]:
    lignes = connection.execute(
        """
        select source_reference, target_reference, type_relation_code,
               fiabilite_code, justification
        from relations_sites
        """
    ).fetchall()
    return [
        {
            "de": ligne[0],
            "vers": ligne[1],
            "type": ligne[2],
            "fiabilite": ligne[3],
            "phrase": ligne[4],
        }
        for ligne in lignes
        if ligne[0] in references and ligne[1] in references
    ]


def lire_chronologie(
    connection: duckdb.DuckDBPyConnection, references: set[str]
) -> dict[str, list[dict]]:
    lignes = connection.execute(
        """
        select reference_ia, type_evenement, date_min, date_max,
               precision_code, texte_source
        from chronologie_sites
        order by reference_ia, coalesce(date_min, date_max)
        """
    ).fetchall()
    par_site: dict[str, list[dict]] = defaultdict(list)
    for ligne in lignes:
        if ligne[0] not in references:
            continue
        par_site[ligne[0]].append(
            {
                "type": ligne[1],
                "min": ligne[2].year if ligne[2] else None,
                "max": ligne[3].year if ligne[3] else None,
                "precision": ligne[4],
                "texte": ligne[5],
            }
        )
    return dict(par_site)


# --------------------------------------------------------------------------
# Fond de carte
# --------------------------------------------------------------------------


def contour_departement() -> list[list[list[float]]]:
    """Frontière extérieure de l'Orne, déduite des contours communaux.

    Une arête partagée par deux communes est intérieure ; une arête vue une
    seule fois appartient à la frontière du département. Les arêtes retenues
    sont ensuite chaînées en boucles fermées.
    """
    donnees = json.loads(COMMUNES.read_text(encoding="utf-8"))
    compte: Counter = Counter()

    def anneaux(geometrie: dict) -> list[list]:
        if geometrie["type"] == "Polygon":
            return geometrie["coordinates"]
        return [anneau for partie in geometrie["coordinates"] for anneau in partie]

    for element in donnees["features"]:
        for anneau in anneaux(element["geometry"]):
            points = [(round(x, 6), round(y, 6)) for x, y in anneau]
            for depart, arrivee in zip(points, points[1:]):
                if depart != arrivee:
                    compte[tuple(sorted((depart, arrivee)))] += 1

    frontiere = [arete for arete, nombre in compte.items() if nombre == 1]

    voisins: dict[tuple, list[tuple]] = defaultdict(list)
    for depart, arrivee in frontiere:
        voisins[depart].append(arrivee)
        voisins[arrivee].append(depart)

    vues: set[tuple] = set()
    boucles: list[list[list[float]]] = []
    for depart, arrivee in frontiere:
        if (depart, arrivee) in vues:
            continue
        chaine = [depart, arrivee]
        vues.add((depart, arrivee))
        vues.add((arrivee, depart))
        courant, precedent = arrivee, depart
        while True:
            suite = [point for point in voisins[courant] if point != precedent]
            suite = [point for point in suite if (courant, point) not in vues]
            if not suite:
                break
            suivant = suite[0]
            vues.add((courant, suivant))
            vues.add((suivant, courant))
            chaine.append(suivant)
            precedent, courant = courant, suivant
            if suivant == chaine[0]:
                break
        if len(chaine) > 40:
            boucles.append([[x, y] for x, y in alleger(chaine, 400)])
    return boucles


def alleger(points: list, maximum: int) -> list:
    """Échantillonne une ligne en gardant ses extrémités."""
    if len(points) <= maximum:
        return points
    pas = math.ceil(len(points) / maximum)
    retenus = points[::pas]
    if retenus[-1] != points[-1]:
        retenus.append(points[-1])
    return retenus


def hydrographie(
    sites: list[dict], boite: tuple[float, float, float, float], maximum: int
) -> list[list[list[float]]]:
    """Cours d'eau qui longent réellement les sites du système.

    Le fond hydrographique complet noie les usines sous un chevelu de ruisseaux
    sans rapport avec elles. Seuls sont conservés les tronçons passant à moins
    d'environ deux kilomètres d'un site : ce sont ceux qui expliquent quelque
    chose de l'implantation.
    """
    proche_degres = 0.022  # ~2 km aux latitudes de l'Orne
    troncons: dict[str, list[list[float]]] = {}
    motif = str(RACINE / "data" / "raw" / "hydrographie" / "**" / "*.geojson")
    for fichier in glob.glob(motif, recursive=True):
        try:
            donnees = json.loads(Path(fichier).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for element in donnees.get("features", []):
            if element["geometry"]["type"] != "LineString":
                continue
            points = [coord[:2] for coord in element["geometry"]["coordinates"]]
            dedans = [
                point
                for point in points
                if boite[0] <= point[0] <= boite[1] and boite[2] <= point[1] <= boite[3]
            ]
            if len(dedans) < 2:
                continue
            longe = any(
                abs(point[0] - site["lon"]) < proche_degres
                and abs(point[1] - site["lat"]) < proche_degres
                for point in dedans[:: max(1, len(dedans) // 20)]
                for site in sites
            )
            if not longe:
                continue
            cle = element["properties"]["cleabs"]
            troncons[cle] = [
                [round(x, 5), round(y, 5)] for x, y in alleger(points, maximum)
            ]
    return list(troncons.values())


def emprise(sites: list[dict], marge: float = MARGE_DEGRES) -> tuple[float, float, float, float]:
    lons = [site["lon"] for site in sites]
    lats = [site["lat"] for site in sites]
    return (min(lons) - marge, max(lons) + marge, min(lats) - marge, max(lats) + marge)


# --------------------------------------------------------------------------
# Construction du paquet
# --------------------------------------------------------------------------


def resume_systeme(sites: list[dict], liens: list[dict], chronologie: dict) -> dict:
    """Chiffres calculés depuis les données, sans aucune phrase rédigée.

    Les textes éditoriaux des systèmes relèvent de la phase 10.F. Cette vue
    n'affiche donc que ce qui se déduit du corpus, et le dit.
    """
    metiers = Counter(secteur for site in sites for secteur in site["secteurs"])
    communes = sorted({site["commune"] for site in sites})
    annees = [
        evenement["min"]
        for site in sites
        for evenement in chronologie.get(site["ref"], [])
        if evenement["min"]
    ]
    distances = sorted(site["eau"] for site in sites if site["eau"] is not None)
    mediane = distances[len(distances) // 2] if distances else None
    return {
        "communes": communes,
        "metiers": metiers.most_common(),
        "premiereAnnee": min(annees) if annees else None,
        "derniereAnnee": max(annees) if annees else None,
        "nbEvenements": sum(len(chronologie.get(site["ref"], [])) for site in sites),
        "nbLiens": len(liens),
        "medianeEau": mediane,
    }


def construire() -> dict:
    registre = yaml.safe_load(REGISTRE.read_text(encoding="utf-8"))
    connection = duckdb.connect(str(BASE), read_only=True)

    lignes = connection.execute(
        "select reference_ia, x_lambert93, y_lambert93, communes_source from sites"
        " where x_lambert93 is not null"
    ).fetchall()
    groupes = groupes_par_proximite(lignes)
    par_code, ecarts = rattacher_systemes(groupes, lignes, registre)

    tous_les_sites = {site["ref"]: site for site in lire_sites(connection)}
    references_par_systeme = {
        code: [lignes[i][0] for i in indices] for code, indices in par_code.items()
    }
    dans_un_systeme = {
        reference for references in references_par_systeme.values() for reference in references
    }

    systemes = []
    for definition in registre["systemes"]:
        code = definition["code"]
        references = references_par_systeme.get(code, [])
        sites = [tous_les_sites[reference] for reference in references if reference in tous_les_sites]
        if not sites:
            continue
        metiers = Counter(secteur for site in sites for secteur in site["secteurs"])
        systemes.append(
            {
                "code": code,
                "nom": definition["nom"],
                "nomDeTravail": definition["nom_de_travail"],
                "nbSites": len(sites),
                "lon": sum(site["lon"] for site in sites) / len(sites),
                "lat": sum(site["lat"] for site in sites) / len(sites),
                "communePrincipale": Counter(
                    site["commune"] for site in sites
                ).most_common(1)[0][0],
                "metiers": dict(metiers),
                "sitesParMetier": {
                    secteur: sum(1 for site in sites if secteur in site["secteurs"])
                    for secteur in metiers
                },
            }
        )

    detail = {}
    for code in SYSTEMES_DETAILLES:
        references = set(references_par_systeme.get(code, []))
        sites = [tous_les_sites[reference] for reference in sorted(references)]
        liens = lire_liens(connection, references)
        chronologie = lire_chronologie(connection, references)
        detail[code] = {
            "sites": sites,
            "liens": liens,
            "chronologie": chronologie,
            "eau": hydrographie(sites, emprise(sites), 14),
            "resume": resume_systeme(sites, liens, chronologie),
        }

    autres = [
        {
            "ref": site["ref"],
            "nom": site["nom"],
            "lon": site["lon"],
            "lat": site["lat"],
            "commune": site["commune"],
            "secteurs": site["secteurs"],
        }
        for reference, site in tous_les_sites.items()
        if reference not in dans_un_systeme
    ]

    connection.close()

    return {
        "departement": {
            "contour": contour_departement(),
            "systemes": systemes,
            "autresSites": autres,
            "nbSites": len(tous_les_sites),
        },
        "detail": detail,
        "ecarts": ecarts,
        "libelles": libelles_du_vocabulaire(),
    }


def libelles_du_vocabulaire() -> dict[str, dict[str, str]]:
    """Libellés lisibles issus du vocabulaire contrôlé versionné.

    Rien n'est reformulé ici : l'interface affiche les libellés déjà arrêtés en
    phase 4, pour qu'un même code ne porte jamais deux noms selon l'écran.
    """
    vocabulaire = yaml.safe_load(CLASSIFICATIONS.read_text(encoding="utf-8"))

    def extraire(rubrique: str) -> dict[str, str]:
        entrees = vocabulaire.get(rubrique, {})
        return {
            code: valeur["libelle"]
            for code, valeur in entrees.items()
            if isinstance(valeur, dict) and "libelle" in valeur
        }

    return {
        "metiers": extraire("secteurs"),
        "precision": extraire("precision_geographique"),
        "conservation": extraire("conservation"),
        "fiabilite": extraire("fiabilite"),
        "evenements": LIBELLES_EVENEMENTS,
    }


# La typologie des événements datés a été arrêtée en phase 10.A.2 dans le module
# d'extraction, mais elle n'a jamais été versée au vocabulaire contrôlé de la
# phase 4. Ces libellés la rendent lisible à l'écran ; leur place définitive est
# dans `config/classifications.yml`, hors du périmètre du bloc en cours.
LIBELLES_EVENEMENTS = {
    "creation": "création",
    "attestation": "attestation",
    "reconstruction": "reconstruction",
    "agrandissement": "agrandissement",
    "equipement": "équipement",
    "acquisition": "acquisition",
    "conversion": "conversion",
    "destruction": "destruction",
    "reglementation": "réglementation",
    "exploitation": "exploitation",
    "production": "production",
    "emploi": "emploi",
}


def main() -> None:
    donnees = construire()

    total_systemes = sum(systeme["nbSites"] for systeme in donnees["departement"]["systemes"])
    controles = {
        "douze_systemes_identifies": len(donnees["departement"]["systemes"]) == 12,
        "effectif_des_systemes": total_systemes == 172,
        "autres_sites": len(donnees["departement"]["autresSites"]) == 146,
        "aucun_ecart_de_rattachement": not donnees["ecarts"],
        "contour_departemental_trouve": bool(donnees["departement"]["contour"]),
    }

    gabarit = GABARIT.read_text(encoding="utf-8")
    charge = json.dumps(donnees, ensure_ascii=False, separators=(",", ":"))
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(gabarit.replace("__DONNEES__", charge), encoding="utf-8")

    rapport = {
        "controles": controles,
        "checks_passed": all(controles.values()),
        "ecarts": donnees["ecarts"],
        "systemes": len(donnees["departement"]["systemes"]),
        "sites_en_systeme": total_systemes,
        "autres_sites": len(donnees["departement"]["autresSites"]),
        "risle_sites": len(donnees["detail"]["risle"]["sites"]),
        "risle_liens": len(donnees["detail"]["risle"]["liens"]),
        "crulai_sites": len(donnees["detail"]["crulai"]["sites"]),
        "crulai_liens": len(donnees["detail"]["crulai"]["liens"]),
        "poids_ko": SORTIE.stat().st_size // 1024,
        "sortie": str(SORTIE.relative_to(RACINE)),
    }
    print(json.dumps(rapport, ensure_ascii=False, indent=2))
    if not rapport["checks_passed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
