"""Prépare le fond géographique de l'essai « carte seule » (phase 10.E, recherche artistique).

Sources, toutes IGN Géoplateforme, Licence ouverte Etalab 2.0 :
- BD TOPO V3 (service WFS) : cours d'eau, forêts publiques, communes de l'Orne ;
- RGE ALTI (service d'altimétrie) : grille d'altitude du département.

Les réponses brutes sont archivées dans data/raw/ign_carte_seule/ (non versionné), avec
un .metadata.json voisin. Les géométries sont simplifiées et écrites dans
prototype/recherche/carte_donnees.js. Les lieux et ensembles viennent des esquisses.

    python tools/carte_seule_extraire.py
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
ESQUISSES = RACINE / "prototype" / "esquisses" / "donnees.js"
SORTIE = RACINE / "prototype" / "recherche" / "carte_donnees.js"
BRUT = RACINE / "data" / "raw" / "ign_carte_seule"
WFS = "https://data.geopf.fr/wfs/ows"
ALTI = "https://data.geopf.fr/altimetrie/1.0/calcul/alti/rest/elevation.json"
BBOX = (-0.98, 48.10, 1.07, 49.05)  # Orne et ses abords
PAS_ALTI = 0.0075
LOT_ALTI = 150
JOUR = dt.datetime.now(dt.UTC).date().isoformat()


def lire(url: str) -> bytes:
    for essai in range(5):
        try:
            with urllib.request.urlopen(url, timeout=120) as rep:
                return rep.read()
        except OSError:
            if essai == 4:
                raise
            time.sleep(5 * (essai + 1))
    raise AssertionError


def archiver(nom: str, contenu: object, source: str, url: str) -> None:
    BRUT.mkdir(parents=True, exist_ok=True)
    chemin = BRUT / f"{JOUR}_{nom}.json"
    chemin.write_text(json.dumps(contenu, ensure_ascii=False), encoding="utf-8")
    meta = {
        "source": source,
        "url": url,
        "date": JOUR,
        "sha256": hashlib.sha256(chemin.read_bytes()).hexdigest(),
        "licence": "Licence ouverte Etalab 2.0",
    }
    chemin.with_suffix(".metadata.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def wfs(couche: str, filtre: str | None = None, page: int = 1000) -> list[dict]:
    entites: list[dict] = []
    debut = 0
    while True:
        params = {
            "SERVICE": "WFS", "VERSION": "2.0.0", "REQUEST": "GetFeature",
            "OUTPUTFORMAT": "application/json", "TYPENAMES": f"BDTOPO_V3:{couche}",
            "COUNT": str(page), "STARTINDEX": str(debut),
        }
        if filtre:
            params["CQL_FILTER"] = filtre
        else:
            params["BBOX"] = ",".join(str(v) for v in BBOX) + ",EPSG:4326"
        lot = json.loads(lire(WFS + "?" + urllib.parse.urlencode(params)))["features"]
        entites += lot
        if len(lot) < page:
            break
        debut += page
    archiver(couche, entites, f"IGN BD TOPO V3 — {couche} (WFS Géoplateforme)", WFS)
    return entites


def simplifier(points: list, tol: float) -> list:
    """Douglas-Peucker, coordonnées arrondies à 5 décimales. Un anneau fermé est coupé en deux."""
    if len(points) > 4 and points[0][:2] == points[-1][:2]:
        m = len(points) // 2
        return simplifier(points[: m + 1], tol)[:-1] + simplifier(points[m:], tol)
    if len(points) < 3:
        return [[round(p[0], 5), round(p[1], 5)] for p in points]
    garde = [False] * len(points)
    garde[0] = garde[-1] = True
    pile = [(0, len(points) - 1)]
    while pile:
        a, b = pile.pop()
        (x1, y1), (x2, y2) = points[a][:2], points[b][:2]
        dx, dy = x2 - x1, y2 - y1
        norme = (dx * dx + dy * dy) ** 0.5 or 1e-12
        imax, dmax = a, 0.0
        for i in range(a + 1, b):
            d = abs(dy * points[i][0] - dx * points[i][1] + x2 * y1 - y2 * x1) / norme
            if d > dmax:
                imax, dmax = i, d
        if dmax > tol:
            garde[imax] = True
            pile += [(a, imax), (imax, b)]
    return [[round(p[0], 5), round(p[1], 5)] for p, g in zip(points, garde) if g]


def lignes(geom: dict) -> list:
    if geom["type"] == "LineString":
        return [geom["coordinates"]]
    if geom["type"] == "MultiLineString":
        return geom["coordinates"]
    if geom["type"] == "Polygon":
        return geom["coordinates"]
    if geom["type"] == "MultiPolygon":
        return [anneau for poly in geom["coordinates"] for anneau in poly]
    return []


def centre(geom: dict) -> tuple[float, float]:
    anneau = max(lignes(geom), key=len)
    aire = cx = cy = 0.0
    for (x0, y0), (x1, y1) in zip(anneau, anneau[1:]):
        f = x0 * y1 - x1 * y0
        aire += f
        cx += (x0 + x1) * f
        cy += (y0 + y1) * f
    return round(cx / (3 * aire), 5), round(cy / (3 * aire), 5)


def altitudes() -> dict:
    x0, y0, x1, y1 = BBOX
    nx = int((x1 - x0) / PAS_ALTI) + 1
    ny = int((y1 - y0) / PAS_ALTI) + 1
    pts = [(x0 + i * PAS_ALTI, y1 - j * PAS_ALTI) for j in range(ny) for i in range(nx)]
    valeurs: list[float] = []
    brut = []
    for k in range(0, len(pts), LOT_ALTI):
        lot = pts[k : k + LOT_ALTI]
        url = (
            f"{ALTI}?lon={'|'.join(f'{p[0]:.5f}' for p in lot)}"
            f"&lat={'|'.join(f'{p[1]:.5f}' for p in lot)}"
            "&resource=ign_rge_alti_wld&zonly=true"
        )
        corps = lire(url)
        brut.append(corps.decode("utf-8"))
        valeurs += json.loads(corps)["elevations"]
    archiver("altitudes", {"bbox": BBOX, "pas": PAS_ALTI, "lots": brut},
             "IGN Géoplateforme — altimétrie, ressource ign_rge_alti_wld", ALTI)
    return {"x0": x0, "y1": y1, "pas": PAS_ALTI, "nx": nx, "ny": ny,
            "z": [round(max(v, -50), 1) for v in valeurs]}


def relief_existant() -> dict | None:
    """Réutilise la grille déjà extraite le même jour plutôt que de réinterroger l'IGN."""
    if not SORTIE.exists():
        return None
    ancien = json.loads(SORTIE.read_text(encoding="utf-8")[len("window.CARTE = "):].rstrip()
                        .rstrip(";"))
    r = ancien.get("relief")
    return r if r and r.get("pas") == PAS_ALTI else None


def main() -> None:
    texte = ESQUISSES.read_text(encoding="utf-8")
    esquisses = json.loads(texte[len("window.DONNEES = "):].rstrip().rstrip(";"))
    dep = esquisses["departement"]

    # Tronçons de rivière : l'ordre de Strahler (numero_d_ordre) donne l'épaisseur du trait.
    bbox_cql = f"BBOX(geometrie,{BBOX[1]},{BBOX[0]},{BBOX[3]},{BBOX[2]})"
    rivieres = []
    for f in wfs("troncon_hydrographique",
                 f"{bbox_cql} AND numero_d_ordre>'2' AND fictif=false"):
        p = f["properties"]
        try:
            ordre = int(p.get("numero_d_ordre") or 0)
        except ValueError:
            continue
        if ordre < 3 or not f["geometry"]:
            continue
        for ligne in lignes(f["geometry"]):
            pts = simplifier(ligne, 0.00025)
            if len(pts) >= 2:
                rivieres.append({"nom": p.get("cpx_toponyme_de_cours_d_eau"), "ordre": ordre,
                                 "pts": pts})

    forets = []
    for f in wfs("foret_publique"):
        if not f["geometry"]:
            continue
        forets.append({"nom": f["properties"].get("toponyme"),
                       "nature": f["properties"].get("nature"),
                       "anneaux": [simplifier(a, 0.0006) for a in lignes(f["geometry"])]})

    villes = []
    for f in wfs("commune", "code_insee_du_departement='61'"):
        p = f["properties"]
        if (p.get("population") or 0) >= 2000:
            lon, lat = centre(f["geometry"])
            villes.append({"nom": p["nom_officiel"], "pop": p["population"],
                           "prefecture": p["chef_lieu_de_departement"],
                           "sousPrefecture": p["chef_lieu_d_arrondissement"],
                           "lon": lon, "lat": lat})

    sortie = {
        "contour": dep["contour"],
        "ensembles": [{k: e[k] for k in ("code", "nom", "nbSites", "lon", "lat")}
                      for e in dep["ensembles"]],
        "autresLieux": [{k: s[k] for k in ("nom", "lon", "lat", "secteurs")}
                        for s in dep["autresLieux"]],
        "lieuxEnsembles": [
            {"nom": s["nom"], "lon": s["lon"], "lat": s["lat"], "ensemble": code}
            for code, ens in esquisses["ensembles"].items()
            for s in ens["sites"] if s.get("lon") is not None
        ],
        "nbLieux": dep["nbLieux"],
        "rivieres": rivieres,
        "forets": forets,
        "villes": sorted(villes, key=lambda v: -v["pop"]),
        "relief": relief_existant() or altitudes(),
    }
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text("window.CARTE = " + json.dumps(sortie, ensure_ascii=False) + ";\n",
                      encoding="utf-8")
    print(json.dumps({"sortie": str(SORTIE), "octets": SORTIE.stat().st_size,
                      "rivieres": len(rivieres), "forets": len(forets),
                      "villes": len(villes)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
