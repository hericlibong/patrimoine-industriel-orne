"""Calcule le contexte territorial des 30 sites pilotes."""

from __future__ import annotations

import argparse
import json
import math
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from pyproj import Transformer


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def local_xy(point: Sequence[float], origin: Sequence[float]) -> tuple[float, float]:
    lon, lat = point[:2]
    lon0, lat0 = origin[:2]
    return (
        (lon - lon0) * 111_320 * math.cos(math.radians(lat0)),
        (lat - lat0) * 111_320,
    )


def point_segment_distance(
    point: Sequence[float], start: Sequence[float], end: Sequence[float]
) -> float:
    px, py = local_xy(point, point)
    ax, ay = local_xy(start, point)
    bx, by = local_xy(end, point)
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(ax - px, ay - py)
    ratio = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + ratio * dx), py - (ay + ratio * dy))


def point_in_ring(point: Sequence[float], ring: Sequence[Sequence[float]]) -> bool:
    x, y = point[:2]
    inside = False
    previous = ring[-1]
    for current in ring:
        x1, y1 = previous[:2]
        x2, y2 = current[:2]
        if (y1 > y) != (y2 > y):
            crossing = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if x < crossing:
                inside = not inside
        previous = current
    return inside


def line_distance(point: Sequence[float], coordinates: Sequence[Sequence[float]]) -> float:
    if len(coordinates) == 1:
        return math.hypot(*local_xy(coordinates[0], point))
    return min(
        point_segment_distance(point, start, end)
        for start, end in zip(coordinates, coordinates[1:])
    )


def polygon_distance(point: Sequence[float], rings: Sequence[Sequence[Sequence[float]]]) -> float:
    if rings and point_in_ring(point, rings[0]):
        return 0.0
    return min(line_distance(point, ring) for ring in rings if ring)


def geometry_distance(point: Sequence[float], geometry: Mapping[str, Any]) -> float:
    kind = geometry.get("type")
    coordinates = geometry.get("coordinates") or []
    if kind == "Point":
        return math.hypot(*local_xy(coordinates, point))
    if kind == "MultiPoint":
        return min(math.hypot(*local_xy(item, point)) for item in coordinates)
    if kind == "LineString":
        return line_distance(point, coordinates)
    if kind == "MultiLineString":
        return min(line_distance(point, item) for item in coordinates)
    if kind == "Polygon":
        return polygon_distance(point, coordinates)
    if kind == "MultiPolygon":
        return min(polygon_distance(point, item) for item in coordinates)
    raise ValueError(f"géométrie non prise en charge : {kind!r}")


def nearest_geojson_feature(
    point: Sequence[float], payload: Mapping[str, Any]
) -> tuple[Mapping[str, Any] | None, float | None]:
    candidates = []
    for feature in payload.get("features", []):
        geometry = feature.get("geometry")
        if geometry:
            candidates.append((geometry_distance(point, geometry), feature))
    if not candidates:
        return None, None
    distance, feature = min(candidates, key=lambda item: item[0])
    return feature, round(distance, 1)


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_coordinate_text(value: str) -> list[list[float]]:
    return [
        [float(part) for part in pair.split(",")[:2]]
        for pair in value.strip().split()
        if pair.strip()
    ]


def parse_brgm_features(path: Path) -> list[dict[str, Any]]:
    root = ET.parse(path).getroot()
    features = []
    for member in (item for item in root.iter() if _local_name(item.tag) == "featureMember"):
        entity = next(iter(member), None)
        if entity is None:
            continue
        properties: dict[str, Any] = {}
        geometry = None
        for child in entity:
            name = _local_name(child.tag)
            point = next((item for item in child.iter() if _local_name(item.tag) == "Point"), None)
            polygon = next(
                (item for item in child.iter() if _local_name(item.tag) == "Polygon"), None
            )
            if point is not None:
                coordinate = next(
                    (item for item in point.iter() if _local_name(item.tag) == "coordinates"),
                    None,
                )
                if coordinate is not None and coordinate.text:
                    geometry = {"type": "Point", "coordinates": parse_coordinate_text(coordinate.text)[0]}
            elif polygon is not None:
                rings = []
                for coordinate in (
                    item for item in polygon.iter() if _local_name(item.tag) == "coordinates"
                ):
                    if coordinate.text:
                        rings.append(parse_coordinate_text(coordinate.text))
                if rings:
                    geometry = {"type": "Polygon", "coordinates": rings}
            elif len(child) == 0:
                properties[name] = child.text.strip() if child.text else None
        features.append(
            {
                "id": entity.attrib.get("fid"),
                "geometry": geometry,
                "properties": properties,
            }
        )
    return features


def proximity_class(distance: float | None, limits: Sequence[tuple[float, str]]) -> str:
    if distance is None:
        return "hors_rayon_de_recherche"
    for limit, label in limits:
        if distance <= limit:
            return label
    return "hors_rayon_de_recherche"


def _manifest_index(manifest: Mapping[str, Any]) -> dict[tuple[str, str], Path]:
    return {
        (
            str(item["observations"]["reference"]),
            str(item["observations"]["layer"]),
        ): Path(item["data_file"])
        for item in manifest["items"]
    }


def _selected_properties(feature: Mapping[str, Any] | None, names: Iterable[str]) -> dict[str, Any]:
    properties = feature.get("properties", {}) if feature else {}
    return {name: properties.get(name) for name in names}


def build_context(
    locations: Mapping[str, Any], manifest: Mapping[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    index = _manifest_index(manifest)
    transformer = Transformer.from_crs(2154, 4326, always_xy=True)
    errors: list[str] = []
    results = []
    crs_differences = []

    for location in locations["locations"]:
        reference = str(location["reference_ia"])
        point = location["geometrie_reference"]["point_wgs84"]
        x, y = location["geometrie_reference"]["point_lambert93"]
        transformed = transformer.transform(x, y)
        crs_difference = geometry_distance(point, {"type": "Point", "coordinates": transformed})
        crs_differences.append(crs_difference)

        geojson_results: dict[str, tuple[Mapping[str, Any] | None, float | None]] = {}
        for layer in ("hydrographie", "forets", "rail"):
            payload = load_json(index[(reference, layer)])
            geojson_results[layer] = nearest_geojson_feature(point, payload)

        hydro_feature, hydro_distance = geojson_results["hydrographie"]
        forest_feature, forest_distance = geojson_results["forets"]
        rail_feature, rail_distance = geojson_results["rail"]

        brgm_features = {
            layer: parse_brgm_features(index[(reference, layer)])
            for layer in ("lithologie", "mines", "gites")
        }
        lithology_candidates = [
            feature
            for feature in brgm_features["lithologie"]
            if feature.get("geometry")
            and geometry_distance(point, feature["geometry"]) == 0
        ]
        lithology = lithology_candidates[0] if lithology_candidates else None
        if lithology is None:
            errors.append(f"{reference} : lithologie non déterminée")

        mineral_candidates = []
        for layer in ("mines", "gites"):
            for feature in brgm_features[layer]:
                if feature.get("geometry"):
                    mineral_candidates.append(
                        (geometry_distance(point, feature["geometry"]), layer, feature)
                    )
        if mineral_candidates:
            mineral_distance, mineral_layer, mineral_feature = min(
                mineral_candidates, key=lambda item: item[0]
            )
            mineral_distance = round(mineral_distance, 1)
        else:
            mineral_distance, mineral_layer, mineral_feature = None, None, None

        results.append(
            {
                "site_id": location["site_id"],
                "reference_ia": reference,
                "point_wgs84": point,
                "systemes_coordonnees": {
                    "travail": "EPSG:2154",
                    "echange_web": "EPSG:4326",
                    "ecart_transformation_m": round(crs_difference, 3),
                    "statut": "coherent" if crs_difference <= 1 else "a_verifier",
                },
                "cours_eau": {
                    "distance_m": hydro_distance,
                    "classe_proximite": proximity_class(
                        hydro_distance,
                        (
                            (25, "moins_25_m"),
                            (100, "moins_100_m"),
                            (500, "moins_500_m"),
                            (2500, "moins_2500_m"),
                        ),
                    ),
                    "objet": _selected_properties(
                        hydro_feature,
                        ("cleabs", "nature", "etat_de_l_objet", "origine", "cpx_toponyme_de_cours_d_eau"),
                    ),
                    "source": "BD TOPO V3 2026-06-15",
                    "relation_historique": "non_etablie_par_la_seule_proximite",
                },
                "foret": {
                    "distance_m": forest_distance,
                    "dans_formation_vegetale": forest_distance == 0,
                    "classe_proximite": proximity_class(
                        forest_distance,
                        (
                            (0, "dans_formation"),
                            (100, "moins_100_m"),
                            (500, "moins_500_m"),
                            (2500, "moins_2500_m"),
                        ),
                    ),
                    "objet": _selected_properties(forest_feature, ("id", "code_tfv", "tfv", "tfv_g11", "essence")),
                    "source": "BD Forêt v2 2006-2019",
                    "relation_historique": "non_etablie_par_la_seule_proximite",
                },
                "geologie": {
                    "lithologie": _selected_properties(lithology, ("CODE_GEOL", "DESCR", "TYPE")),
                    "source": "BRGM LITHO_1M_SIMPLIFIEE",
                    "echelle": "1:1 000 000",
                    "usage": "contexte_general_non_preuve_d_approvisionnement",
                },
                "ressource_minerale": {
                    "distance_m": mineral_distance,
                    "classe_proximite": proximity_class(
                        mineral_distance,
                        ((1000, "moins_1_km"), (5000, "moins_5_km"), (10000, "moins_10_km")),
                    ),
                    "type_source": mineral_layer,
                    "objet": _selected_properties(
                        mineral_feature,
                        ("id_unique", "identifiant", "nom_site", "nom_gite", "substance", "c_substance"),
                    ),
                    "source": "BRGM MINES_PT et GITES_PT",
                    "relation_historique": "non_etablie_par_la_seule_proximite",
                },
                "rail": {
                    "distance_m": rail_distance,
                    "classe_proximite": proximity_class(
                        rail_distance,
                        (
                            (100, "moins_100_m"),
                            (500, "moins_500_m"),
                            (2000, "moins_2_km"),
                            (5000, "moins_5_km"),
                        ),
                    ),
                    "objet": _selected_properties(
                        rail_feature,
                        ("cleabs", "nature", "etat_de_l_objet", "date_d_apparition", "usage"),
                    ),
                    "source": "BD TOPO V3 2026-06-15",
                    "couverture_historique": "non_exhaustive",
                    "relation_historique": "non_etablie_par_la_seule_proximite",
                },
            }
        )

    def class_counts(key: str) -> dict[str, int]:
        return dict(sorted(Counter(item[key]["classe_proximite"] for item in results).items()))

    report = {
        "schema_version": "1.0",
        "date_controle": "2026-07-22",
        "checks_passed": not errors,
        "errors": errors,
        "counts": {
            "sites": len(results),
            "lithologies_renseignees": sum(bool(item["geologie"]["lithologie"]) for item in results),
            "sites_avec_indice_mineral_dans_10_km": sum(
                item["ressource_minerale"]["classe_proximite"]
                != "hors_rayon_de_recherche"
                for item in results
            ),
            "systemes_coordonnees_coherents": sum(
                item["systemes_coordonnees"]["statut"] == "coherent" for item in results
            ),
        },
        "proximites": {
            "cours_eau": class_counts("cours_eau"),
            "foret": class_counts("foret"),
            "ressource_minerale": class_counts("ressource_minerale"),
            "rail": class_counts("rail"),
        },
        "crs": {
            "travail": "EPSG:2154",
            "echange_web": "EPSG:4326",
            "ecart_maximum_transformation_m": round(max(crs_differences), 3),
        },
        "interpretation": "Les proximités sont des indices spatiaux, jamais des causes historiques prouvées.",
    }
    output = {
        "schema_version": "1.0",
        "date_controle": "2026-07-22",
        "sources": manifest["layers"],
        "seuils": {
            "cours_eau_m": [25, 100, 500, 2500],
            "foret_m": [0, 100, 500, 2500],
            "ressource_minerale_m": [1000, 5000, 10000],
            "rail_m": [100, 500, 2000, 5000],
        },
        "sites": results,
    }
    return output, report


def write_json(value: Mapping[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--locations",
        type=Path,
        default=Path("data/pilot/localisations_pilote_phase6.json"),
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("reports/audits/phase6_contexte_manifest.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/pilot/contexte_territorial_phase6.json"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/quality/phase6_contexte_territorial.json"),
    )
    args = parser.parse_args()
    output, report = build_context(load_json(args.locations), load_json(args.manifest))
    write_json(output, args.output)
    write_json(report, args.report)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    if not report["checks_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
