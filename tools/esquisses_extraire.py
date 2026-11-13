"""Prépare les données des esquisses de direction artistique (phase 10.E).

Lit les données déjà embarquées dans la vue de référence (aucune donnée
nouvelle sur les lieux) et y ajoute une grille d'altitude IGN (RGE ALTI, service
d'altimétrie de la Géoplateforme) pour la Risle et Crulai. La réponse brute du
service est archivée dans data/raw/ign_altimetrie_esquisses/ (non versionné) ;
la grille dérivée est écrite dans prototype/esquisses/donnees.js.

    python tools/esquisses_extraire.py
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
SOURCE = RACINE / "prototype" / "vue_reference" / "index.html"
SORTIE = RACINE / "prototype" / "esquisses" / "donnees.js"
BRUT = RACINE / "data" / "raw" / "ign_altimetrie_esquisses"
URL = "https://data.geopf.fr/altimetrie/1.0/calcul/alti/rest/elevation.json"
PAS = 0.004  # degrés, environ 300 m en latitude
MARGE = 0.03
LOT = 120


def lire_donnees() -> dict:
    for ligne in SOURCE.read_text(encoding="utf-8").splitlines():
        if ligne.startswith("const D = "):
            return json.loads(ligne[len("const D = ") :].rstrip(";"))
    raise SystemExit("Données de la vue de référence introuvables")


def emprise(ensemble: dict) -> tuple[float, float, float, float]:
    pts = [p for e in ensemble["eau"] for p in e["points"]]
    pts += [(s["lon"], s["lat"]) for s in ensemble["sites"] if s.get("lon") is not None]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs) - MARGE, min(ys) - MARGE, max(xs) + MARGE, max(ys) + MARGE


def altitudes(code: str, bbox: tuple[float, float, float, float]) -> dict:
    x0, y0, x1, y1 = bbox
    nx = int((x1 - x0) / PAS) + 1
    ny = int((y1 - y0) / PAS) + 1
    pts = [(x0 + i * PAS, y1 - j * PAS) for j in range(ny) for i in range(nx)]
    valeurs: list[float] = []
    brut = []
    for k in range(0, len(pts), LOT):
        lot = pts[k : k + LOT]
        url = (
            f"{URL}?lon={'|'.join(f'{p[0]:.5f}' for p in lot)}"
            f"&lat={'|'.join(f'{p[1]:.5f}' for p in lot)}"
            "&resource=ign_rge_alti_wld&zonly=true"
        )
        with urllib.request.urlopen(url, timeout=60) as rep:
            corps = rep.read()
        brut.append(corps.decode("utf-8"))
        valeurs += json.loads(corps)["elevations"]
    BRUT.mkdir(parents=True, exist_ok=True)
    jour = dt.date.today().isoformat()
    chemin = BRUT / f"{jour}_{code}.json"
    chemin.write_text(json.dumps({"bbox": bbox, "pas": PAS, "lots": brut}), encoding="utf-8")
    meta = {
        "source": "IGN Géoplateforme — altimétrie, ressource ign_rge_alti_wld",
        "url": URL,
        "date": jour,
        "sha256": hashlib.sha256(chemin.read_bytes()).hexdigest(),
        "licence": "Licence ouverte Etalab 2.0",
    }
    chemin.with_suffix(".metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return {"x0": x0, "y1": y1, "pas": PAS, "nx": nx, "ny": ny,
            "z": [round(v, 1) for v in valeurs]}


def main() -> None:
    d = lire_donnees()
    sortie = {"epoques": d["epoques"], "libelles": d["libelles"], "ensembles": {}}
    for code in ("risle", "crulai"):
        ens = d["detail"][code]
        meta = next(s for s in d["departement"]["systemes"] if s["code"] == code)
        sortie["ensembles"][code] = {
            "nom": meta["nom"],
            "nomDeTravail": meta.get("nomDeTravail"),
            "presentation": meta.get("presentationCourte"),
            "sites": ens["sites"],
            "liens": ens["liens"],
            "chronologie": ens["chronologie"],
            "eau": ens["eau"],
            "resume": ens["resume"],
            "communes": ens["sol"]["communes"],
            "bourgs": ens.get("reperes", {}).get("bourgs", []),
            "relief": altitudes(code, emprise(ens)),
        }
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(
        "window.DONNEES = " + json.dumps(sortie, ensure_ascii=False) + ";\n", encoding="utf-8"
    )
    print(json.dumps({"sortie": str(SORTIE), "octets": SORTIE.stat().st_size}))


if __name__ == "__main__":
    main()
