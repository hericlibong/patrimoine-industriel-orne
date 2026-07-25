"""Calcule le contexte territorial des 318 sites à partir des tuiles archivées."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping

from pyproj import Transformer

from patrimoine_orne.geocode.territorial_context import (
    geometry_distance,
    parse_brgm_features,
    proximity_class,
)


DEFAULT_LOCATIONS = Path("data/processed/localisations_corpus_phase8_v1.json")
DEFAULT_MANIFEST = Path("reports/audits/phase8_contexte_territorial_manifest.json")
DEFAULT_OUTPUT = Path("data/processed/contexte_territorial_phase8_v1.json")
DEFAULT_REPORT = Path("reports/quality/phase8_contexte_territorial.json")
DEFAULT_CORPUS = Path("data/processed/corpus_enrichi_phase8_v1.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _selected_properties(
    feature: Mapping[str, Any] | None, names: Iterable[str]
) -> dict[str, Any]:
    properties = feature.get("properties", {}) if feature else {}
    return {name: properties.get(name) for name in names}


def _indexes(
    manifest: Mapping[str, Any],
) -> tuple[dict[tuple[str, str], Path], dict[str, Path]]:
    tiled = {}
    brgm = {}
    for item in manifest["items"]:
        source = str(item["source_id"])
        path = Path(item["data_file"])
        observations = item["observations"]
        if source == "brgm":
            brgm[str(observations["layer"])] = path
            continue
        for reference in observations["references"]:
            tiled[(str(reference), str(observations["layer"]))] = path
    return tiled, brgm


def _coordinate_pairs(value: Any) -> Iterable[tuple[float, float]]:
    if (
        isinstance(value, list)
        and len(value) >= 2
        and isinstance(value[0], (int, float))
        and isinstance(value[1], (int, float))
    ):
        yield float(value[0]), float(value[1])
    elif isinstance(value, list):
        for item in value:
            yield from _coordinate_pairs(item)


def _feature_index(
    payload: Mapping[str, Any],
) -> list[tuple[tuple[float, float, float, float], Mapping[str, Any]]]:
    rows = []
    for feature in payload.get("features", []):
        geometry = feature.get("geometry")
        points = list(_coordinate_pairs(geometry.get("coordinates"))) if geometry else []
        if not points:
            continue
        lon_values = [point[0] for point in points]
        lat_values = [point[1] for point in points]
        rows.append(
            (
                (
                    min(lon_values),
                    min(lat_values),
                    max(lon_values),
                    max(lat_values),
                ),
                feature,
            )
        )
    return rows


def _bbox_lower_distance(
    point: list[float], bbox: tuple[float, float, float, float]
) -> float:
    lon, lat = point
    lon_delta = max(bbox[0] - lon, 0, lon - bbox[2])
    lat_delta = max(bbox[1] - lat, 0, lat - bbox[3])
    return math.hypot(
        lon_delta * 111_320 * math.cos(math.radians(lat)),
        lat_delta * 111_320,
    )


def _nearest_indexed(
    point: list[float],
    index: list[tuple[tuple[float, float, float, float], Mapping[str, Any]]],
) -> tuple[Mapping[str, Any] | None, float | None]:
    ordered = sorted(
        ((_bbox_lower_distance(point, bbox), feature) for bbox, feature in index),
        key=lambda item: item[0],
    )
    best_feature = None
    best_distance = float("inf")
    for lower_bound, feature in ordered:
        if lower_bound > best_distance:
            break
        distance = geometry_distance(point, feature["geometry"])
        if distance < best_distance:
            best_feature, best_distance = feature, distance
    if best_feature is None:
        return None, None
    return best_feature, round(best_distance, 1)


def build_full_context(
    locations: Mapping[str, Any], manifest: Mapping[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    tiled_index, brgm_index = _indexes(manifest)
    geojson_cache: dict[Path, Mapping[str, Any]] = {}
    feature_index_cache: dict[
        Path, list[tuple[tuple[float, float, float, float], Mapping[str, Any]]]
    ] = {}
    brgm_features = {
        layer: parse_brgm_features(brgm_index[layer])
        for layer in ("lithologie", "mines", "gites")
    }
    transformer = Transformer.from_crs(2154, 4326, always_xy=True)
    results = []
    errors = []
    crs_differences = []
    for location in locations["locations"]:
        reference = str(location["reference_ia"])
        point = location.get("point_wgs84")
        lambert = location.get("point_lambert93")
        if not point or not lambert:
            errors.append(f"{reference} : site non localisé, contexte non calculé")
            continue
        transformed = transformer.transform(*lambert)
        crs_difference = geometry_distance(
            point, {"type": "Point", "coordinates": transformed}
        )
        crs_differences.append(crs_difference)
        nearest = {}
        for layer in ("hydrographie", "forets", "rail"):
            path = tiled_index[(reference, layer)]
            if path not in geojson_cache:
                geojson_cache[path] = load_json(path)
                feature_index_cache[path] = _feature_index(geojson_cache[path])
            nearest[layer] = _nearest_indexed(point, feature_index_cache[path])
        hydro_feature, hydro_distance = nearest["hydrographie"]
        forest_feature, forest_distance = nearest["forets"]
        rail_feature, rail_distance = nearest["rail"]

        lithology_candidates = [
            feature
            for feature in brgm_features["lithologie"]
            if feature.get("geometry")
            and geometry_distance(point, feature["geometry"]) == 0
        ]
        lithology = lithology_candidates[0] if lithology_candidates else None
        if lithology is None:
            errors.append(f"{reference} : lithologie non déterminée")
        mineral_candidates = [
            (geometry_distance(point, feature["geometry"]), layer, feature)
            for layer in ("mines", "gites")
            for feature in brgm_features[layer]
            if feature.get("geometry")
        ]
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
                "precision_geographique_code": location[
                    "precision_geographique_code"
                ],
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
                        (
                            "cleabs",
                            "nature",
                            "etat_de_l_objet",
                            "origine",
                            "cpx_toponyme_de_cours_d_eau",
                        ),
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
                    "objet": _selected_properties(
                        forest_feature,
                        ("id", "code_tfv", "tfv", "tfv_g11", "essence"),
                    ),
                    "source": "BD Forêt v2 2006-2019",
                    "relation_historique": "non_etablie_par_la_seule_proximite",
                },
                "geologie": {
                    "lithologie": _selected_properties(
                        lithology, ("CODE_GEOL", "DESCR", "TYPE")
                    ),
                    "source": "BRGM LITHO_1M_SIMPLIFIEE",
                    "echelle": "1:1 000 000",
                    "usage": "contexte_general_non_preuve_d_approvisionnement",
                },
                "ressource_minerale": {
                    "distance_m": mineral_distance,
                    "classe_proximite": proximity_class(
                        mineral_distance,
                        (
                            (1000, "moins_1_km"),
                            (5000, "moins_5_km"),
                            (10000, "moins_10_km"),
                        ),
                    ),
                    "type_source": mineral_layer,
                    "objet": _selected_properties(
                        mineral_feature,
                        (
                            "id_unique",
                            "identifiant",
                            "nom_site",
                            "nom_gite",
                            "substance",
                            "c_substance",
                        ),
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
                        (
                            "cleabs",
                            "nature",
                            "etat_de_l_objet",
                            "date_d_apparition",
                            "usage",
                        ),
                    ),
                    "source": "BD TOPO V3 2026-06-15",
                    "couverture_historique": "non_exhaustive",
                    "relation_historique": "non_etablie_par_la_seule_proximite",
                },
            }
        )

    def class_counts(key: str) -> dict[str, int]:
        return dict(
            sorted(Counter(item[key]["classe_proximite"] for item in results).items())
        )

    report = {
        "schema_version": "1.0",
        "date_controle": date.today().isoformat(),
        "checks_passed": not errors and len(results) == 318,
        "errors": errors,
        "counts": {
            "sites": len(results),
            "lithologies_renseignees": sum(
                bool(item["geologie"]["lithologie"]) for item in results
            ),
            "sites_avec_indice_mineral_dans_10_km": sum(
                item["ressource_minerale"]["classe_proximite"]
                != "hors_rayon_de_recherche"
                for item in results
            ),
            "systemes_coordonnees_coherents": sum(
                item["systemes_coordonnees"]["statut"] == "coherent"
                for item in results
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
        "interpretation": (
            "Les proximités sont des indices spatiaux, jamais des causes historiques "
            "prouvées."
        ),
    }
    output = {
        "schema_version": "1.0",
        "date_controle": date.today().isoformat(),
        "sources": {
            "hydrographie": "BD TOPO V3 2026-06-15",
            "forets": "BD Forêt v2 2006-2019",
            "rail": "BD TOPO V3 2026-06-15",
            "geologie_minerais": "BRGM",
        },
        "seuils": {
            "cours_eau_m": [25, 100, 500, 2500],
            "foret_m": [0, 100, 500, 2500],
            "ressource_minerale_m": [1000, 5000, 10000],
            "rail_m": [100, 500, 2000, 5000],
        },
        "sites": results,
    }
    return output, report


def write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def attach_context(
    corpus: dict[str, Any], context: Mapping[str, Any], report: Mapping[str, Any]
) -> dict[str, Any]:
    by_site = {str(row["site_id"]): row for row in context["sites"]}
    if set(by_site) != {str(site["site_id"]) for site in corpus["sites"]}:
        raise ValueError("le contexte territorial ne couvre pas exactement le corpus")
    for site in corpus["sites"]:
        site["contexte_territorial"] = by_site[str(site["site_id"])]
    corpus["status"] = "enrichissement_et_contexte_territorial_phase8"
    corpus["counts"]["contextes_territoriaux_calcules"] = len(by_site)
    corpus["counts"]["sites_avec_indice_mineral_dans_10_km"] = report["counts"][
        "sites_avec_indice_mineral_dans_10_km"
    ]
    return corpus


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locations", type=Path, default=DEFAULT_LOCATIONS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    args = parser.parse_args()
    output, report = build_full_context(
        load_json(args.locations), load_json(args.manifest)
    )
    write_json(args.output, output)
    write_json(args.report, report)
    write_json(args.corpus, attach_context(load_json(args.corpus), output, report))
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    if not report["checks_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
