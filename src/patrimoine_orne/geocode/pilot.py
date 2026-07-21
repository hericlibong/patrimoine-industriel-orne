"""Qualifie les localisations POP, BAN et cadastrales du corpus pilote."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence

from patrimoine_orne.classify.sectors import load_pop_manifest_sample


ORNE_ENVELOPE = {"lon_min": -1.0, "lon_max": 1.0, "lat_min": 48.2, "lat_max": 49.1}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_lambert_point(value: Any) -> list[float] | None:
    if not value:
        return None
    try:
        x, y = (float(part) for part in str(value).split(";"))
    except (TypeError, ValueError):
        return None
    return [x, y]


def parse_lambert_polygon(value: Any) -> list[list[float]] | None:
    if not value:
        return None
    coordinates = [parse_lambert_point(part) for part in str(value).split("/")]
    if any(point is None for point in coordinates) or len(coordinates) < 4:
        return None
    return [point for point in coordinates if point is not None]


def parse_pop_wgs_polygon(value: Any) -> list[list[float]] | None:
    if not isinstance(value, Mapping):
        return None
    coordinates = value.get("coordinates")
    if not isinstance(coordinates, list) or len(coordinates) < 4:
        return None
    # POP fournit ici [latitude, longitude], contrairement à l'ordre GeoJSON.
    return [[float(item[1]), float(item[0])] for item in coordinates]


def valid_wgs84(point: Sequence[float] | None) -> bool:
    if point is None or len(point) != 2:
        return False
    lon, lat = point
    return (
        ORNE_ENVELOPE["lon_min"] <= lon <= ORNE_ENVELOPE["lon_max"]
        and ORNE_ENVELOPE["lat_min"] <= lat <= ORNE_ENVELOPE["lat_max"]
    )


def haversine_metres(left: Sequence[float], right: Sequence[float]) -> float:
    lon1, lat1, lon2, lat2 = map(math.radians, [left[0], left[1], right[0], right[1]])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    value = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * 6_371_008.8 * math.asin(math.sqrt(value))


def cadastral_reference_matches(
    section: Any, number: Any, source_references: Sequence[str]
) -> bool:
    """Teste une concordance simple section/numéro, y compris les plages « A »."""
    current_section = str(section or "").lstrip("0")
    try:
        current_number = int(str(number))
    except ValueError:
        return False
    for reference in source_references:
        match = re.match(r"^\d{4}\s+([A-Z0-9]+)\s+(.+)$", str(reference))
        if not match or match.group(1).lstrip("0") != current_section:
            continue
        expression = match.group(2)
        if re.search(rf"(?<!\d){current_number}(?!\d)", expression):
            return True
        for start, end in re.findall(r"(\d+)\s+A\s+(\d+)", expression):
            if int(start) <= current_number <= int(end):
                return True
    return False


def _manifest_payloads(manifest: Mapping[str, Any], source_id: str) -> dict[str, dict[str, Any]]:
    result = {}
    for item in manifest["sources"][source_id]:
        reference = str(item["observations"]["reference"])
        result[reference] = load_json(Path(item["data_file"]))
    return result


def build_location_audit(
    corpus: Mapping[str, Any],
    pop_records: Sequence[Mapping[str, Any]],
    extraction_manifest: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    pop_by_reference = {str(record["REF"]): record for record in pop_records}
    ban_by_reference = _manifest_payloads(extraction_manifest, "ban")
    cadastre_by_reference = _manifest_payloads(extraction_manifest, "cadastre")
    errors: list[str] = []
    locations: list[dict[str, Any]] = []

    for site in corpus["sites"]:
        reference = str(site["reference_ia"])
        record = pop_by_reference[reference]
        lambert_point = parse_lambert_point(record.get("COOR"))
        lambert_polygon = parse_lambert_polygon(record.get("COORM"))
        pop_point = record.get("POP_COORDONNEES") or {}
        wgs_point = (
            [float(pop_point["lon"]), float(pop_point["lat"])]
            if pop_point.get("lon") is not None and pop_point.get("lat") is not None
            else None
        )
        wgs_polygon = parse_pop_wgs_polygon(record.get("POP_COORDINATES_POLYGON"))
        if lambert_point is None or not valid_wgs84(wgs_point):
            errors.append(f"{reference} : coordonnées POP absentes ou invalides")
        if record.get("COORM") and not lambert_polygon and not wgs_polygon:
            errors.append(f"{reference} : emprise POP présente mais illisible")

        geocoding = None
        ban_payload = ban_by_reference.get(reference)
        if ban_payload:
            features = ban_payload.get("features", [])
            candidate = features[0] if features else None
            properties = candidate.get("properties", {}) if candidate else {}
            candidate_point = candidate.get("geometry", {}).get("coordinates") if candidate else None
            candidate_distance = (
                haversine_metres(wgs_point, candidate_point)
                if candidate_point and valid_wgs84(candidate_point) and wgs_point
                else None
            )
            accepted = bool(
                candidate
                and properties.get("type") == "housenumber"
                and properties.get("citycode") == site["commune_historique_code_insee"]
                and valid_wgs84(candidate_point)
                and float(properties.get("score") or 0) >= 0.65
                and candidate_distance is not None
                and candidate_distance <= 250
            )
            geocoding = {
                "statut": (
                    "adresse_unique_geocodee_concordante"
                    if accepted
                    else "adresse_unique_geocodee_non_concordante"
                ),
                "requete_source": site["adresse"],
                "label_ban": properties.get("label"),
                "id_ban": properties.get("banId"),
                "score": properties.get("score"),
                "point_wgs84": candidate_point if accepted else None,
                "distance_au_point_pop_m": (
                    round(candidate_distance, 1) if candidate_distance is not None else None
                ),
                "precision_geographique_code": "point_adresse" if accepted else None,
                "methode_localisation_code": "geocodage_adresse" if accepted else None,
            }

        parcel_payload = cadastre_by_reference.get(reference, {})
        parcels = []
        source_cadastral_references = record.get("CADA") or []
        for feature in parcel_payload.get("features", []):
            properties = feature.get("properties", {})
            parcels.append(
                {
                    "idu": properties.get("idu"),
                    "section": properties.get("section"),
                    "numero": properties.get("numero"),
                    "code_insee": properties.get("code_insee"),
                    "contenance_m2": properties.get("contenance"),
                    "reference_source_concordante": cadastral_reference_matches(
                        properties.get("section"),
                        properties.get("numero"),
                        source_cadastral_references,
                    ),
                    "geometrie_wgs84": feature.get("geometry"),
                    "statut": "candidate_intersection_point_pop",
                    "precision_geographique_code": None,
                    "note": "Intersection automatique ; parcelle non qualifiée de vérifiée.",
                }
            )

        has_geometry = lambert_point is not None and valid_wgs84(wgs_point)
        locations.append(
            {
                "site_id": site["site_id"],
                "reference_ia": reference,
                "statut_localisation_code": (
                    "geometrie_approximative" if has_geometry else "non_localise"
                ),
                "precision_reference_code": (
                    "zone_documentaire"
                    if lambert_polygon or wgs_polygon
                    else "point_approximatif" if has_geometry else None
                ),
                "geometrie_reference": (
                    {
                        "type_geometrie_code": "point_site",
                        "point_lambert93": lambert_point,
                        "point_wgs84": wgs_point,
                        "crs_source": "EPSG:2154",
                        "methode_localisation_code": "coordonnees_source",
                        "fiabilite_code": "moyenne",
                    }
                    if has_geometry
                    else None
                ),
                "emprise_source": (
                    {
                        "type_geometrie_code": "zone_documentaire",
                        "polygon_lambert93": lambert_polygon,
                        "polygon_wgs84": wgs_polygon,
                        "crs_source": "EPSG:2154" if lambert_polygon else "EPSG:4326",
                        "precision_geographique_code": "zone_documentaire",
                        "methode_localisation_code": "emprise_source",
                        "fiabilite_code": "moyenne",
                    }
                    if lambert_polygon or wgs_polygon
                    else None
                ),
                "adresse_source": site.get("adresse"),
                "adresse_geocodee": geocoding,
                "references_cadastrales_source": source_cadastral_references,
                "parcelles_actuelles_candidates": parcels,
                "controle_humain_cartographique": "a_realiser_phase6_bloc_controle",
            }
        )

    counts = {
        "sites": len(locations),
        "points_pop_valides": sum(item["geometrie_reference"] is not None for item in locations),
        "emprises_pop_disponibles": sum(item["emprise_source"] is not None for item in locations),
        "adresses_pop_renseignees": sum(bool(item["adresse_source"]) for item in locations),
        "adresses_uniques_soumises_au_geocodeur": sum(
            bool(item["adresse_geocodee"]) for item in locations
        ),
        "adresses_uniques_geocodees_concordantes": sum(
            bool(item["adresse_geocodee"])
            and item["adresse_geocodee"]["statut"]
            == "adresse_unique_geocodee_concordante"
            for item in locations
        ),
        "adresses_uniques_non_concordantes": sum(
            bool(item["adresse_geocodee"])
            and item["adresse_geocodee"]["statut"]
            == "adresse_unique_geocodee_non_concordante"
            for item in locations
        ),
        "adresses_non_uniques_non_geocodees": len(
            extraction_manifest["rejected_non_unique_addresses"]
        ),
        "sites_avec_parcelle_actuelle_candidate": sum(
            bool(item["parcelles_actuelles_candidates"]) for item in locations
        ),
        "parcelles_actuelles_candidates": sum(
            len(item["parcelles_actuelles_candidates"]) for item in locations
        ),
        "sites_avec_reference_cadastrale_source_encore_concordante": sum(
            any(
                parcel["reference_source_concordante"]
                for parcel in item["parcelles_actuelles_candidates"]
            )
            for item in locations
        ),
        "geometries_verifiees": 0,
        "localisations_approximatives": sum(
            item["statut_localisation_code"] == "geometrie_approximative"
            for item in locations
        ),
        "sites_non_localises": sum(
            item["statut_localisation_code"] == "non_localise" for item in locations
        ),
        "coordonnees_inventees": 0,
    }
    distances = [
        item["adresse_geocodee"]["distance_au_point_pop_m"]
        for item in locations
        if item["adresse_geocodee"]
        and item["adresse_geocodee"]["statut"] == "adresse_unique_geocodee_concordante"
        and item["adresse_geocodee"]["distance_au_point_pop_m"] is not None
    ]
    audit = {
        "schema_version": "1.0",
        "date_controle": "2026-07-22",
        "crs_travail": "EPSG:2154",
        "crs_export_web": "EPSG:4326",
        "locations": locations,
    }
    report = {
        "schema_version": "1.0",
        "date_controle": "2026-07-22",
        "checks_passed": not errors,
        "errors": errors,
        "counts": counts,
        "distance_ban_pop_m": {
            "minimum": min(distances) if distances else None,
            "maximum": max(distances) if distances else None,
            "moyenne": round(sum(distances) / len(distances), 1) if distances else None,
        },
        "parcelles_par_site": dict(
            sorted(
                Counter(
                    len(item["parcelles_actuelles_candidates"]) for item in locations
                ).items()
            )
        ),
        "decision": (
            "Localisations utilisables comme données de travail, toutes approximatives "
            "jusqu'au contrôle cartographique."
        ),
    }
    return audit, report


def write_json(value: Mapping[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=Path("data/pilot/corpus_pilote_v1.json"))
    parser.add_argument(
        "--pop-manifest",
        type=Path,
        default=Path("reports/audits/phase5_pop_manifest.json"),
    )
    parser.add_argument(
        "--extraction-manifest",
        type=Path,
        default=Path("reports/audits/phase6_localisation_manifest.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/pilot/localisations_pilote_phase6.json"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/quality/phase6_localisation.json"),
    )
    args = parser.parse_args()
    audit, report = build_location_audit(
        load_json(args.corpus),
        load_pop_manifest_sample(args.pop_manifest),
        load_json(args.extraction_manifest),
    )
    write_json(audit, args.output)
    write_json(report, args.report)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    if not report["checks_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
