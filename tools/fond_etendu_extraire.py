"""Prolonge le fond géographique de la carte départementale au-delà de l'Orne (phase 10.E).

Correction du 19 novembre 2026 : le relief, les rivières et les forêts de la carte seule
s'arrêtaient sur une emprise rectangulaire visible à l'écran. Ce script interroge les mêmes
sources, sur une emprise plus large, pour que le fond couvre toute la surface affichée :

- RGE ALTI (service d'altimétrie IGN) : la grille est prolongée au même pas (0,0075°) et
  calée sur la grille existante. Les altitudes déjà extraites sont reprises telles quelles ;
  seuls les points nouveaux sont demandés. Rien n'est étiré ni extrapolé.
- BD TOPO V3 (WFS) : cours d'eau d'ordre 4 et plus, forêts publiques, hors de l'emprise
  déjà couverte.

Les réponses brutes sont archivées dans data/raw/ign_fond_etendu/ (non versionné), avec un
.metadata.json voisin. La sortie est prototype/edition/fond_etendu.js (window.FOND).
La carte seule et ses données (prototype/recherche/carte_donnees.js) ne sont pas modifiées.

    python tools/fond_etendu_extraire.py
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
CARTE = RACINE / "prototype" / "recherche" / "carte_donnees.js"
SORTIE = RACINE / "prototype" / "edition" / "fond_etendu.js"
BRUT = RACINE / "data" / "raw" / "ign_fond_etendu"
WFS = "https://data.geopf.fr/wfs/ows"
ALTI = "https://data.geopf.fr/altimetrie/1.0/calcul/alti/rest/elevation.json"
ANCIENNE = (-0.98, 48.10, 1.07, 49.05)  # emprise de la carte seule
# cases ajoutées de chaque côté de la grille existante : ouest, est, nord, sud
AJOUT = {"o": 156, "e": 98, "n": 53, "s": 67}
LOT = 150
FILS = 6
JOUR = dt.datetime.now(dt.UTC).date().isoformat()


def lire(url: str) -> bytes:
    for essai in range(6):
        try:
            with urllib.request.urlopen(url, timeout=120) as rep:
                return rep.read()
        except OSError:
            if essai == 5:
                raise
            time.sleep(5 * (essai + 1))
    raise AssertionError


def archiver(nom: str, contenu: object, source: str, url: str) -> None:
    BRUT.mkdir(parents=True, exist_ok=True)
    chemin = BRUT / f"{JOUR}_{nom}.json"
    if chemin.exists():  # data/raw n'est jamais écrasé
        chemin = BRUT / f"{JOUR}_{nom}_{int(time.time())}.json"
    chemin.write_text(json.dumps(contenu, ensure_ascii=False), encoding="utf-8")
    meta = {"source": source, "url": url, "date": JOUR,
            "sha256": hashlib.sha256(chemin.read_bytes()).hexdigest(),
            "licence": "Licence ouverte Etalab 2.0"}
    chemin.with_suffix(".metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False),
                                                    encoding="utf-8")


def simplifier(points: list, tol: float) -> list:
    """Douglas-Peucker, coordonnées arrondies à 5 décimales (identique à la carte seule)."""
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
    t, c = geom["type"], geom["coordinates"]
    if t == "LineString":
        return [c]
    if t in ("MultiLineString", "Polygon"):
        return c
    if t == "MultiPolygon":
        return [a for poly in c for a in poly]
    return []


def dans_ancienne(geom: dict) -> bool:
    """Vrai si un sommet tombe dans l'emprise déjà couverte : l'entité y est déjà."""
    x0, y0, x1, y1 = ANCIENNE
    return any(x0 <= p[0] <= x1 and y0 <= p[1] <= y1 for ligne in lignes(geom) for p in ligne)


def wfs(couche: str, filtre: str, page: int = 1000) -> list[dict]:
    entites: list[dict] = []
    debut = 0
    while True:
        params = {"SERVICE": "WFS", "VERSION": "2.0.0", "REQUEST": "GetFeature",
                  "OUTPUTFORMAT": "application/json", "TYPENAMES": f"BDTOPO_V3:{couche}",
                  "COUNT": str(page), "STARTINDEX": str(debut), "CQL_FILTER": filtre}
        lot = json.loads(lire(WFS + "?" + urllib.parse.urlencode(params)))["features"]
        entites += lot
        print(f"  {couche} : {len(entites)}", file=sys.stderr, flush=True)
        if len(lot) < page:
            break
        debut += page
    archiver(couche, entites, f"IGN BD TOPO V3 — {couche} (WFS Géoplateforme)", WFS)
    return entites


def relief(ancien: dict) -> dict:
    p = ancien["pas"]
    x0 = round(ancien["x0"] - AJOUT["o"] * p, 6)
    y1 = round(ancien["y1"] + AJOUT["n"] * p, 6)
    nx = ancien["nx"] + AJOUT["o"] + AJOUT["e"]
    ny = ancien["ny"] + AJOUT["n"] + AJOUT["s"]
    z: list[float | None] = [None] * (nx * ny)
    for j in range(ancien["ny"]):  # reprise de la grille existante, case pour case
        for i in range(ancien["nx"]):
            z[(j + AJOUT["n"]) * nx + i + AJOUT["o"]] = ancien["z"][j * ancien["nx"] + i]
    manque = [k for k, v in enumerate(z) if v is None]
    lots = [manque[k: k + LOT] for k in range(0, len(manque), LOT)]
    print(f"relief : {nx}×{ny}, {len(manque)} points à demander en {len(lots)} lots",
          file=sys.stderr, flush=True)

    def demander(lot: list[int]) -> tuple[list[int], str]:
        url = (f"{ALTI}?lon={'|'.join(f'{x0 + (k % nx) * p:.5f}' for k in lot)}"
               f"&lat={'|'.join(f'{y1 - (k // nx) * p:.5f}' for k in lot)}"
               "&resource=ign_rge_alti_wld&zonly=true")
        return lot, lire(url).decode("utf-8")

    brut = []
    with ThreadPoolExecutor(FILS) as ex:
        for n, (lot, corps) in enumerate(ex.map(demander, lots), 1):
            brut.append(corps)
            for k, v in zip(lot, json.loads(corps)["elevations"]):
                z[k] = round(max(v, -50), 1)
            if n % 50 == 0:
                print(f"  lots : {n}/{len(lots)}", file=sys.stderr, flush=True)
    archiver("altitudes", {"x0": x0, "y1": y1, "pas": p, "nx": nx, "ny": ny, "lots": brut},
             "IGN Géoplateforme — altimétrie, ressource ign_rge_alti_wld", ALTI)
    assert all(v is not None for v in z)
    return {"x0": x0, "y1": y1, "pas": p, "nx": nx, "ny": ny, "z": z}


def main() -> None:
    ancien = json.loads(CARTE.read_text(encoding="utf-8")[len("window.CARTE = "):].rstrip()
                        .rstrip(";"))
    r = relief(ancien["relief"])
    p = r["pas"]
    emprise = (r["x0"], r["y1"] - (r["ny"] - 1) * p, r["x0"] + (r["nx"] - 1) * p, r["y1"])
    cql = f"BBOX(geometrie,{emprise[1]},{emprise[0]},{emprise[3]},{emprise[2]})"

    rivieres = []
    for f in wfs("troncon_hydrographique", f"{cql} AND numero_d_ordre>'3' AND fictif=false"):
        pr = f["properties"]
        try:
            ordre = int(pr.get("numero_d_ordre") or 0)
        except ValueError:
            continue
        if ordre < 4 or not f["geometry"] or dans_ancienne(f["geometry"]):
            continue
        for ligne in lignes(f["geometry"]):
            pts = simplifier(ligne, 0.00025)
            if len(pts) >= 2:
                rivieres.append({"nom": pr.get("cpx_toponyme_de_cours_d_eau"), "ordre": ordre,
                                 "pts": pts})

    forets = []
    for f in wfs("foret_publique", cql):
        if not f["geometry"] or dans_ancienne(f["geometry"]):
            continue
        forets.append({"nom": f["properties"].get("toponyme"),
                       "nature": f["properties"].get("nature"),
                       "anneaux": [simplifier(a, 0.0006) for a in lignes(f["geometry"])]})

    sortie = {"emprise": emprise, "relief": r, "rivieres": rivieres, "forets": forets,
              "note": "Fond prolongé autour de l'Orne ; s'ajoute à carte_donnees.js sans le "
                      "remplacer. Relief repris case pour case à l'intérieur de l'ancienne "
                      "emprise."}
    SORTIE.write_text("window.FOND = " + json.dumps(sortie, ensure_ascii=False) + ";\n",
                      encoding="utf-8")
    print(json.dumps({"sortie": str(SORTIE), "octets": SORTIE.stat().st_size,
                      "relief": f"{r['nx']}x{r['ny']}", "emprise": emprise,
                      "rivieres": len(rivieres), "forets": len(forets)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
