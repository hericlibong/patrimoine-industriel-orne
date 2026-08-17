"""Fabrique l'écran de référence sur la vallée de la Risle.

Un seul fichier HTML autonome, sans serveur ni dépendance : on l'ouvre dans un
navigateur et il fonctionne. Toutes les données sont issues du corpus et
incluses dans la page.

Ce n'est pas une maquette. Les 43 sites, leurs liens, leurs dates et le tracé de
la rivière viennent des mêmes fichiers que la publication future.
"""

from __future__ import annotations

import glob
import json
import math
from collections import defaultdict
from pathlib import Path

import duckdb


RACINE = Path(__file__).resolve().parents[1]
BASE = RACINE / "data" / "processed" / "patrimoine_orne_corpus_complet_v1.duckdb"
GABARIT = Path(__file__).resolve().parent / "ecran_risle_gabarit.html"
SORTIE = RACINE / "prototype" / "risle" / "index.html"

LIEN_A_3_KM = 3000
MARGE_DEGRES = 0.02


def ensemble_risle(connection: duckdb.DuckDBPyConnection) -> list[str]:
    """Le plus grand regroupement de sites à moins de 3 km de proche en proche."""
    lignes = connection.execute(
        "select reference_ia, x_lambert93, y_lambert93 from sites"
        " where x_lambert93 is not null"
    ).fetchall()
    parent = list(range(len(lignes)))

    def racine(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    for i in range(len(lignes)):
        for j in range(i + 1, len(lignes)):
            distance = math.hypot(
                lignes[i][1] - lignes[j][1], lignes[i][2] - lignes[j][2]
            )
            if distance < LIEN_A_3_KM:
                a, b = racine(i), racine(j)
                if a != b:
                    parent[b] = a

    groupes: dict[int, list[str]] = defaultdict(list)
    for index, ligne in enumerate(lignes):
        groupes[racine(index)].append(ligne[0])
    return sorted(max(groupes.values(), key=len))


def sites_du_groupe(
    connection: duckdb.DuckDBPyConnection, references: list[str]
) -> list[dict]:
    marques = ",".join(f"'{reference}'" for reference in references)
    lignes = connection.execute(
        f"""
        select s.reference_ia, s.nom_principal, s.communes_source,
               s.lieux_dits_source, s.longitude, s.latitude, s.secteurs_codes,
               s.nombre_activites, s.distance_cours_eau_m,
               s.precision_geographique_code, s.conservation_code,
               s.accessibilite_code, s.source_principale_url,
               r.historique_source
        from sites s
        left join recits_sites r on r.site_id = s.site_id
        where s.reference_ia in ({marques})
        order by s.communes_source, s.reference_ia
        """
    ).fetchall()
    return [
        {
            "ref": ligne[0],
            "nom": ligne[1],
            "commune": ligne[2],
            "lieuDit": ligne[3] or "",
            "lon": ligne[4],
            "lat": ligne[5],
            "secteurs": [s.strip() for s in (ligne[6] or "").split("|") if s.strip()],
            "nbActivites": ligne[7],
            "eau": ligne[8],
            "precision": ligne[9],
            "conservation": ligne[10],
            "acces": ligne[11],
            "url": ligne[12],
            "histoire": ligne[13] or "",
        }
        for ligne in lignes
    ]


def liens_du_groupe(
    connection: duckdb.DuckDBPyConnection, references: list[str]
) -> list[dict]:
    marques = ",".join(f"'{reference}'" for reference in references)
    lignes = connection.execute(
        f"""
        select source_reference, target_reference, type_relation_code,
               fiabilite_code, justification
        from relations_sites
        where source_reference in ({marques})
           or target_reference in ({marques})
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


def chronologie_du_groupe(
    connection: duckdb.DuckDBPyConnection, references: list[str]
) -> dict[str, list[dict]]:
    marques = ",".join(f"'{reference}'" for reference in references)
    lignes = connection.execute(
        f"""
        select reference_ia, type_evenement, date_min, date_max,
               precision_code, texte_source, phrase_source
        from chronologie_sites
        where reference_ia in ({marques})
        order by reference_ia, coalesce(date_min, date_max)
        """
    ).fetchall()
    par_site: dict[str, list[dict]] = defaultdict(list)
    for ligne in lignes:
        par_site[ligne[0]].append(
            {
                "type": ligne[1],
                "min": str(ligne[2]) if ligne[2] else "",
                "max": str(ligne[3]) if ligne[3] else "",
                "precision": ligne[4],
                "texte": ligne[5],
                "phrase": ligne[6],
            }
        )
    return dict(par_site)


def riviere(sites: list[dict]) -> list[list[list[float]]]:
    """Tronçons hydrographiques traversant l'emprise, simplifiés."""
    lons = [site["lon"] for site in sites]
    lats = [site["lat"] for site in sites]
    boite = (
        min(lons) - MARGE_DEGRES,
        max(lons) + MARGE_DEGRES,
        min(lats) - MARGE_DEGRES,
        max(lats) + MARGE_DEGRES,
    )
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
            cle = element["properties"]["cleabs"]
            troncons[cle] = [
                [round(x, 5), round(y, 5)] for x, y in points[:: max(1, len(points) // 12)]
            ]
    return list(troncons.values())


def construire() -> dict:
    connection = duckdb.connect(str(BASE), read_only=True)
    references = ensemble_risle(connection)
    sites = sites_du_groupe(connection, references)
    donnees = {
        "sites": sites,
        "liens": liens_du_groupe(connection, references),
        "chronologie": chronologie_du_groupe(connection, references),
        "riviere": riviere(sites),
    }
    connection.close()
    return donnees


def main() -> None:
    donnees = construire()
    gabarit = GABARIT.read_text(encoding="utf-8")
    charge = json.dumps(donnees, ensure_ascii=False, separators=(",", ":"))
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(gabarit.replace("__DONNEES__", charge), encoding="utf-8")
    print(f"sites: {len(donnees['sites'])}")
    print(f"liens: {len(donnees['liens'])}")
    print(f"evenements: {sum(len(v) for v in donnees['chronologie'].values())}")
    print(f"troncons de riviere: {len(donnees['riviere'])}")
    print(f"ecrit: {SORTIE}")
    print(f"poids: {SORTIE.stat().st_size // 1024} Ko")


if __name__ == "__main__":
    main()
