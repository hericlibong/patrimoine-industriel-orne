"""Produit la carte QGIS et le contrôle cartographique du pilote."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml
from pyproj import Transformer

from patrimoine_orne.geocode.pilot import ORNE_ENVELOPE, haversine_metres, valid_wgs84
from patrimoine_orne.geocode.territorial_context import geometry_distance, point_in_ring


MIN_DOCUMENTARY_AREA_M2 = 100
MAX_DOCUMENTARY_AREA_M2 = 100_000
OUTSIDE_EMPRISE_TOLERANCE_M = 5
NEAR_DUPLICATE_TOLERANCE_M = 50


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write_json(value: Mapping[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def feature_collection(features: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {"type": "FeatureCollection", "features": list(features)}


def polygon_area_m2(
    ring: Sequence[Sequence[float]], transformer: Transformer
) -> float:
    projected = [transformer.transform(*point[:2]) for point in ring]
    value = sum(
        x1 * y2 - x2 * y1
        for (x1, y1), (x2, y2) in zip(projected, projected[1:])
    )
    return abs(value) / 2


def ring_is_closed(ring: Sequence[Sequence[float]]) -> bool:
    return len(ring) >= 4 and list(ring[0][:2]) == list(ring[-1][:2])


def _orientation(
    left: Sequence[float], middle: Sequence[float], right: Sequence[float]
) -> float:
    return (middle[1] - left[1]) * (right[0] - middle[0]) - (
        middle[0] - left[0]
    ) * (right[1] - middle[1])


def _segments_cross(
    a: Sequence[float], b: Sequence[float], c: Sequence[float], d: Sequence[float]
) -> bool:
    return _orientation(a, b, c) * _orientation(a, b, d) < 0 and _orientation(
        c, d, a
    ) * _orientation(c, d, b) < 0


def ring_self_intersects(ring: Sequence[Sequence[float]]) -> bool:
    segments = list(zip(ring, ring[1:]))
    last_index = len(segments) - 1
    for left_index, (a, b) in enumerate(segments):
        for right_index, (c, d) in enumerate(segments[left_index + 1 :], left_index + 1):
            if right_index == left_index + 1:
                continue
            if left_index == 0 and right_index == last_index:
                continue
            if _segments_cross(a, b, c, d):
                return True
    return False


def polygon_distance_m(point: Sequence[float], ring: Sequence[Sequence[float]]) -> float:
    return geometry_distance(point, {"type": "Polygon", "coordinates": [ring]})


def _manual_index(config: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(item["reference"]): item for item in config["cas_controles"]}


def _ban_candidates(manifest: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    candidates = {}
    for item in manifest["sources"]["ban"]:
        reference = str(item["observations"]["reference"])
        payload = load_json(Path(item["data_file"]))
        if payload.get("features"):
            candidates[reference] = payload["features"][0]
    return candidates


def _nearest_neighbours(locations: Sequence[Mapping[str, Any]]) -> dict[str, float]:
    result: dict[str, float] = {}
    for location in locations:
        reference = str(location["reference_ia"])
        point = location["geometrie_reference"]["point_wgs84"]
        distances = [
            haversine_metres(point, other["geometrie_reference"]["point_wgs84"])
            for other in locations
            if other["reference_ia"] != reference
        ]
        result[reference] = min(distances)
    return result


def build_cartographic_control(
    locations_payload: Mapping[str, Any],
    corpus_payload: Mapping[str, Any],
    localisation_manifest: Mapping[str, Any],
    manual_config: Mapping[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    locations = locations_payload["locations"]
    sites = {str(item["reference_ia"]): item for item in corpus_payload["sites"]}
    manual = _manual_index(manual_config)
    ban_candidates = _ban_candidates(localisation_manifest)
    nearest = _nearest_neighbours(locations)
    to_lambert = Transformer.from_crs(4326, 2154, always_xy=True)
    to_wgs84 = Transformer.from_crs(2154, 4326, always_xy=True)

    point_features = []
    sensitive_point_features = []
    emprise_features = []
    parcel_features = []
    ban_features = []
    sensitive_cases = []
    gross_anomalies = []
    errors = []

    for location in locations:
        reference = str(location["reference_ia"])
        site = sites[reference]
        point = location["geometrie_reference"]["point_wgs84"]
        lambert_point = location["geometrie_reference"]["point_lambert93"]
        transformed_point = to_wgs84.transform(*lambert_point)
        crs_difference = geometry_distance(
            point, {"type": "Point", "coordinates": transformed_point}
        )
        reasons = []
        anomalies = []
        emprise = location.get("emprise_source")
        area = None
        point_in_emprise = None
        distance_to_emprise = None

        if emprise:
            ring = emprise["polygon_wgs84"]
            area = polygon_area_m2(ring, to_lambert)
            point_in_emprise = point_in_ring(point, ring)
            distance_to_emprise = polygon_distance_m(point, ring)
            if not ring_is_closed(ring) or ring_self_intersects(ring):
                anomalies.append("emprise_invalide")
            if not point_in_emprise and distance_to_emprise > OUTSIDE_EMPRISE_TOLERANCE_M:
                reasons.append("point_hors_emprise")
            if area < MIN_DOCUMENTARY_AREA_M2:
                reasons.append("emprise_tres_petite")
            if area > MAX_DOCUMENTARY_AREA_M2:
                reasons.append("emprise_tres_grande")
            emprise_features.append(
                {
                    "type": "Feature",
                    "properties": {
                        "reference": reference,
                        "nom": site["nom_principal"],
                        "surface_m2": round(area, 1),
                        "point_dedans": point_in_emprise,
                        "distance_point_m": round(distance_to_emprise, 1),
                        "precision": "zone_documentaire",
                    },
                    "geometry": {"type": "Polygon", "coordinates": [ring]},
                }
            )
        else:
            reasons.append("emprise_absente")

        parcel = location["parcelles_actuelles_candidates"][0]
        parcel_distance = geometry_distance(point, parcel["geometrie_wgs84"])
        commune_matches = parcel["code_insee"] == site["commune_actuelle_code_insee"]
        if parcel_distance > 1:
            anomalies.append("point_hors_parcelle_candidate")
        if not commune_matches:
            anomalies.append("commune_parcelle_incoherente")
        parcel_features.append(
            {
                "type": "Feature",
                "properties": {
                    "reference": reference,
                    "idu": parcel["idu"],
                    "commune": parcel["code_insee"],
                    "cadastre_concordant": parcel["reference_source_concordante"],
                    "statut": "candidate_non_verifiee",
                },
                "geometry": parcel["geometrie_wgs84"],
            }
        )

        geocoding = location.get("adresse_geocodee")
        if geocoding and geocoding["statut"] == "adresse_unique_geocodee_non_concordante":
            reasons.append("adresse_ban_non_concordante")
        elif location.get("adresse_source") and not geocoding:
            reasons.append("adresse_non_unique")

        if not valid_wgs84(point):
            anomalies.append("point_hors_enveloppe_orne")
        if crs_difference > 1:
            anomalies.append("transformation_crs_incoherente")
        if nearest[reference] < NEAR_DUPLICATE_TOLERANCE_M:
            anomalies.append("point_quasi_duplique")

        manual_review = manual.get(reference)
        if reasons and manual_review is None:
            errors.append(f"{reference} : cas sensible sans décision manuelle")
        if manual_review and not reasons:
            errors.append(f"{reference} : décision manuelle sans motif automatique")
        if manual_review and set(manual_review.get("motifs", [])) != set(reasons):
            errors.append(f"{reference} : motifs manuels différents des motifs détectés")

        status = "coherent"
        if reasons:
            status = "sensible_controle"
        if anomalies:
            status = "anomalie_a_verifier"
            gross_anomalies.append(
                {"reference": reference, "anomalies": anomalies, "point_wgs84": point}
            )

        properties = {
            "reference": reference,
            "site_id": location["site_id"],
            "nom": site["nom_principal"],
            "commune": site["commune_actuelle_nom"],
            "secteurs": ", ".join(
                sorted({item["secteur_code"] for item in site["activites"]})
            ),
            "statut": status,
            "motifs": ", ".join(reasons),
            "anomalies": ", ".join(anomalies),
            "precision": location["precision_reference_code"],
            "emprise_m2": round(area, 1) if area is not None else None,
            "point_dans_emprise": point_in_emprise,
            "distance_emprise_m": (
                round(distance_to_emprise, 1) if distance_to_emprise is not None else None
            ),
            "parcelle": parcel["idu"],
            "cadastre_concordant": parcel["reference_source_concordante"],
            "plus_proche_site_m": round(nearest[reference], 1),
            "decision_manuelle": manual_review.get("decision") if manual_review else None,
            "note_manuelle": manual_review.get("note") if manual_review else None,
        }
        feature = {
            "type": "Feature",
            "properties": properties,
            "geometry": {"type": "Point", "coordinates": point},
        }
        point_features.append(feature)
        if reasons or anomalies:
            sensitive_point_features.append(feature)
            sensitive_cases.append(
                {
                    "reference": reference,
                    "motifs": reasons,
                    "anomalies": anomalies,
                    "decision_manuelle": (
                        manual_review.get("decision") if manual_review else None
                    ),
                    "note_manuelle": manual_review.get("note") if manual_review else None,
                }
            )

    for reference, candidate in ban_candidates.items():
        geocoding = next(
            item.get("adresse_geocodee")
            for item in locations
            if item["reference_ia"] == reference
        )
        ban_features.append(
            {
                "type": "Feature",
                "properties": {
                    "reference": reference,
                    "label": candidate.get("properties", {}).get("label"),
                    "score": candidate.get("properties", {}).get("score"),
                    "statut": geocoding["statut"] if geocoding else "non_qualifie",
                },
                "geometry": candidate.get("geometry"),
            }
        )

    reason_counts = Counter(
        reason for item in sensitive_cases for reason in item["motifs"]
    )
    report = {
        "schema_version": "1.0",
        "date_controle": "2026-07-22",
        "checks_passed": not errors and not gross_anomalies,
        "errors": errors,
        "enveloppe_testee": ORNE_ENVELOPE,
        "seuils": {
            "surface_documentaire_min_m2": MIN_DOCUMENTARY_AREA_M2,
            "surface_documentaire_max_m2": MAX_DOCUMENTARY_AREA_M2,
            "point_hors_emprise_tolerance_m": OUTSIDE_EMPRISE_TOLERANCE_M,
            "quasi_doublon_m": NEAR_DUPLICATE_TOLERANCE_M,
        },
        "counts": {
            "sites": len(point_features),
            "emprises_documentaires": len(emprise_features),
            "parcelles_candidates": len(parcel_features),
            "points_ban": len(ban_features),
            "points_aberrants_grossiers": len(gross_anomalies),
            "cas_sensibles_controles": len(sensitive_cases),
            "cas_sans_decision_manuelle": sum(
                item["decision_manuelle"] is None for item in sensitive_cases
            ),
        },
        "motifs_sensibilite": dict(sorted(reason_counts.items())),
        "points_aberrants": gross_anomalies,
        "cas_sensibles": sensitive_cases,
        "decision": (
            "Aucun point grossièrement aberrant. Toutes les géométries restent "
            "approximatives ; les cas sensibles conservent une décision explicite."
        ),
    }
    layers = {
        "sites_pilote": feature_collection(point_features),
        "sites_sensibles": feature_collection(sensitive_point_features),
        "emprises_documentaires": feature_collection(emprise_features),
        "parcelles_candidates": feature_collection(parcel_features),
        "adresses_ban": feature_collection(ban_features),
    }
    return layers, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--locations", type=Path, default=Path("data/pilot/localisations_pilote_phase6.json")
    )
    parser.add_argument(
        "--corpus", type=Path, default=Path("data/pilot/corpus_pilote_v1.json")
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("reports/audits/phase6_localisation_manifest.json"),
    )
    parser.add_argument(
        "--manual",
        type=Path,
        default=Path("config/controle_cartographique_pilote.yml"),
    )
    parser.add_argument("--qgis-data", type=Path, default=Path("qgis/data"))
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/quality/phase6_controle_cartographique.json"),
    )
    args = parser.parse_args()
    layers, report = build_cartographic_control(
        load_json(args.locations),
        load_json(args.corpus),
        load_json(args.manifest),
        load_yaml(args.manual),
    )
    for name, payload in layers.items():
        write_json(payload, args.qgis_data / f"{name}.geojson")
    write_json(report, args.report)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    if not report["checks_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
