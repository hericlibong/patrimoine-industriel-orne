"""Prépare les données légères du prototype statique de la phase 10."""

from __future__ import annotations

import csv
import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROTOTYPE = ROOT / "prototype" / "phase10"
DATA_DIR = PROTOTYPE / "data"
ASSET_DIR = PROTOTYPE / "assets"
SITES_GEOJSON = ROOT / "data" / "exports" / "sites_corpus_complet_v1.geojson"
ACTIVITIES_CSV = ROOT / "data" / "exports" / "activites_corpus_complet_v1.csv"
COMMUNES_GEOJSON = (
    ROOT
    / "data"
    / "raw"
    / "api_geo"
    / "2026"
    / "2026-07-22"
    / "communes_orne_contours.geojson"
)


FEATURED = {
    "IA00060969": {
        "slug": "oze-moulinex",
        "image": "oze-1987.jpg",
        "eyebrow": "Un lieu, plusieurs vies",
        "summary": "Du moulin d'Ozé à la filature, puis à Moulinex.",
    },
    "IA00061086": {
        "slug": "abadie",
        "image": "abadie-1988.jpg",
        "eyebrow": "Lire un paysage industriel",
        "summary": "Une usine à papier inscrite entre bourg, rivière et champs.",
    },
    "IA00061155": {
        "slug": "bohin",
        "image": "bohin-1982.jpg",
        "eyebrow": "Continuité et situation actuelle",
        "summary": "Un moulin devenu site métallurgique, toujours documenté aujourd'hui.",
    },
}


def iter_positions(value: Any):
    if (
        isinstance(value, list)
        and len(value) >= 2
        and isinstance(value[0], (int, float))
        and isinstance(value[1], (int, float))
    ):
        yield float(value[0]), float(value[1])
        return
    if isinstance(value, list):
        for item in value:
            yield from iter_positions(item)


def split_codes(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split("|") if part.strip()]


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)

    communes = json.loads(COMMUNES_GEOJSON.read_text(encoding="utf-8"))
    positions = [
        position
        for feature in communes["features"]
        for position in iter_positions(feature["geometry"]["coordinates"])
    ]
    longitudes = [position[0] for position in positions]
    latitudes = [position[1] for position in positions]
    min_lon, max_lon = min(longitudes), max(longitudes)
    min_lat, max_lat = min(latitudes), max(latitudes)

    activities_by_site: dict[str, list[dict[str, Any]]] = defaultdict(list)
    with ACTIVITIES_CSV.open(encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            activities_by_site[row["site_id"]].append(
                {
                    "order": int(row["ordre"]),
                    "sector": row["secteur_code"],
                    "code": row["activite_code"],
                    "label": row["libelle_source"],
                    "start": row["debut_texte_source"] or None,
                    "end": row["fin_texte_source"] or None,
                    "periods": split_codes(row["periodes_codes"]),
                    "reliability": row["fiabilite_code"],
                }
            )

    sites_geojson = json.loads(SITES_GEOJSON.read_text(encoding="utf-8"))
    output_sites: list[dict[str, Any]] = []
    for feature in sites_geojson["features"]:
        props = feature["properties"]
        longitude, latitude = feature["geometry"]["coordinates"]
        reference = props["reference_ia"]
        activities = sorted(
            activities_by_site[props["site_id"]], key=lambda item: item["order"]
        )
        featured = FEATURED.get(reference)
        output_sites.append(
            {
                "id": props["site_id"],
                "reference": reference,
                "name": props["nom_principal"],
                "commune": props["communes_source"],
                "address": props["adresses_source"],
                "placeName": props["lieux_dits_source"],
                "sectors": split_codes(props["secteurs_codes"]),
                "activityCount": int(props["nombre_activites"]),
                "activities": activities,
                "situationDocumented": bool(props["situation_actuelle_documentee"]),
                "conservation": props["conservation_code"],
                "uses": split_codes(props["usages_actuels_codes"]),
                "accessibility": props["accessibilite_code"],
                "precision": props["precision_geographique_code"],
                "waterProximity": props["proximite_cours_eau_code"],
                "sourceUrl": props["source_principale_url"],
                "x": round((longitude - min_lon) / (max_lon - min_lon) * 100, 4),
                "y": round((max_lat - latitude) / (max_lat - min_lat) * 100, 4),
                "featured": featured,
            }
        )

    output_sites.sort(key=lambda item: (item["commune"], item["name"]))
    payload = {
        "version": "prototype-phase10-v1",
        "generatedAt": "2026-07-27",
        "counts": {
            "sites": len(output_sites),
            "activities": sum(len(site["activities"]) for site in output_sites),
            "datedActivities": sum(
                1
                for site in output_sites
                for activity in site["activities"]
                if activity["periods"]
            ),
            "documentedCurrentSituations": sum(
                1 for site in output_sites if site["situationDocumented"]
            ),
        },
        "sites": output_sites,
    }
    (DATA_DIR / "sites.json").write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    design_assets = ROOT / "docs" / "design" / "phase10"
    for source_name, target_name in {
        "reference_paysage_orne.jpg": "paysage-orne.jpg",
        "reference_oze_1987.jpg": "oze-1987.jpg",
        "reference_abadie_vue_aerienne.jpg": "abadie-1988.jpg",
        "reference_bohin_1982.jpg": "bohin-1982.jpg",
    }.items():
        shutil.copy2(design_assets / source_name, ASSET_DIR / target_name)

    print(
        json.dumps(
            {
                "output": str((DATA_DIR / "sites.json").relative_to(ROOT)),
                **payload["counts"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
