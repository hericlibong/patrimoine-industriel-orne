"""Archive les couches territoriales autour des sites du pilote."""

from __future__ import annotations

import argparse
import json
import math
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping
from urllib.parse import urlencode

from .http import RetrievalResult, RetrievalSpec, retrieve
from .pilot import current_git_commit


EXTRACTOR_VERSION = "0.1.0"
IGN_WFS = "https://data.geopf.fr/wfs/ows"
BRGM_WFS = "https://geoservices.brgm.fr/geologie"

IGN_LAYERS = {
    "hydrographie": {
        "typename": "BDTOPO_V3:troncon_hydrographique",
        "radius_m": 2_500,
        "source_id": "hydrographie",
        "edition": "BD TOPO V3 2026-06-15",
    },
    "forets": {
        "typename": "LANDCOVER.FORESTINVENTORY.V2:formation_vegetale",
        "radius_m": 2_500,
        "source_id": "forets",
        "edition": "BD Forêt v2 2006-2019",
    },
    "rail": {
        "typename": "BDTOPO_V3:troncon_de_voie_ferree",
        "radius_m": 5_000,
        "source_id": "rail",
        "edition": "BD TOPO V3 2026-06-15",
    },
}

BRGM_LAYERS = {
    "lithologie": {
        "typename": "LITHO_1M_SIMPLIFIEE",
        "radius_m": 100,
        "max_features": 10,
    },
    "mines": {"typename": "MINES_PT", "radius_m": 10_000, "max_features": 500},
    "gites": {"typename": "GITES_PT", "radius_m": 10_000, "max_features": 500},
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def bbox_around(point: list[float], radius_m: float) -> tuple[float, float, float, float]:
    lon, lat = point
    lat_delta = radius_m / 111_320
    lon_delta = radius_m / (111_320 * math.cos(math.radians(lat)))
    return lon - lon_delta, lat - lat_delta, lon + lon_delta, lat + lat_delta


def bbox_text(point: list[float], radius_m: float, *, include_crs: bool) -> str:
    values = [f"{value:.7f}" for value in bbox_around(point, radius_m)]
    if include_crs:
        values.append("EPSG:4326")
    return ",".join(values)


def validate_ign(reference: str, layer: str) -> Callable[[Path], dict[str, Any]]:
    def validator(path: Path) -> dict[str, Any]:
        payload = load_json(path)
        if payload.get("type") != "FeatureCollection" or not isinstance(
            payload.get("features"), list
        ):
            raise ValueError("réponse WFS IGN invalide")
        crs_block = payload.get("crs") or {}
        crs_name = crs_block.get("properties", {}).get("name")
        return {
            "reference": reference,
            "layer": layer,
            "feature_count": len(payload["features"]),
            "number_matched": payload.get("numberMatched"),
            "crs": crs_name,
        }

    return validator


def validate_brgm(reference: str, layer: str) -> Callable[[Path], dict[str, Any]]:
    def validator(path: Path) -> dict[str, Any]:
        root = ET.parse(path).getroot()
        if root.tag.rsplit("}", 1)[-1] == "ServiceExceptionReport":
            message = " ".join(text.strip() for text in root.itertext() if text.strip())
            raise ValueError(f"erreur WFS BRGM : {message}")
        members = [item for item in root.iter() if item.tag.rsplit("}", 1)[-1] == "featureMember"]
        srs_names = sorted(
            {
                str(item.attrib["srsName"])
                for item in root.iter()
                if item.attrib.get("srsName")
            }
        )
        return {
            "reference": reference,
            "layer": layer,
            "feature_count": len(members),
            "crs": srs_names,
        }

    return validator


def build_specs(locations: Mapping[str, Any]) -> list[RetrievalSpec]:
    specs: list[RetrievalSpec] = []
    for item in locations["locations"]:
        reference = str(item["reference_ia"])
        point = item["geometrie_reference"]["point_wgs84"]
        for layer, settings in IGN_LAYERS.items():
            parameters = {
                "SERVICE": "WFS",
                "VERSION": "2.0.0",
                "REQUEST": "GetFeature",
                "TYPENAMES": settings["typename"],
                "SRSNAME": "EPSG:4326",
                "BBOX": bbox_text(point, settings["radius_m"], include_crs=True),
                "COUNT": 2000,
                "OUTPUTFORMAT": "application/json",
            }
            specs.append(
                RetrievalSpec(
                    source_id=str(settings["source_id"]),
                    resource_id=f"{reference}_{layer}",
                    scope="orne_pilote_phase6_contexte",
                    source_page_url="https://documentation.geoservices.ign.fr/?BDTopo=",
                    request_url=f"{IGN_WFS}?{urlencode(parameters)}",
                    format="geojson",
                    license="Licence Ouverte 2.0",
                    query=parameters,
                    notes=(
                        f"Couche {settings['typename']} ; {settings['edition']}.",
                        f"Recherche dans un rayon maximal de {settings['radius_m']} mètres.",
                        "La proximité calculée ne prouve pas une relation historique.",
                    ),
                    validator=validate_ign(reference, layer),
                )
            )
        for layer, settings in BRGM_LAYERS.items():
            parameters = {
                "SERVICE": "WFS",
                "VERSION": "1.0.0",
                "REQUEST": "GetFeature",
                "TYPENAME": settings["typename"],
                "SRSNAME": "EPSG:4326",
                "BBOX": bbox_text(point, settings["radius_m"], include_crs=False),
                "MAXFEATURES": settings["max_features"],
            }
            specs.append(
                RetrievalSpec(
                    source_id="brgm",
                    resource_id=f"{reference}_{layer}",
                    scope="orne_pilote_phase6_contexte",
                    source_page_url="https://infoterre.brgm.fr/page/geoservices-ogc",
                    request_url=f"{BRGM_WFS}?{urlencode(parameters)}",
                    format="gml",
                    license="Conditions de réutilisation des données du BRGM",
                    query=parameters,
                    notes=(
                        f"Couche {settings['typename']}.",
                        f"Recherche dans un rayon maximal de {settings['radius_m']} mètres.",
                        "La proximité calculée ne prouve pas une relation historique.",
                    ),
                    validator=validate_brgm(reference, layer),
                )
            )
    return specs


def _relative(path: Path) -> str:
    return path.resolve().relative_to(Path.cwd().resolve()).as_posix()


def result_manifest(spec: RetrievalSpec, result: RetrievalResult) -> dict[str, Any]:
    return {
        "source_id": spec.source_id,
        "data_file": _relative(result.data_file),
        "metadata_file": _relative(result.metadata_file),
        "sha256": result.metadata["sha256"],
        "observations": result.observations,
    }


def extract_territorial_context(
    *,
    locations_path: Path = Path("data/pilot/localisations_pilote_phase6.json"),
    raw_root: Path = Path("data/raw"),
    manifest_path: Path = Path("reports/audits/phase6_contexte_manifest.json"),
    retrieved_at: datetime | None = None,
) -> dict[str, Any]:
    timestamp = retrieved_at or datetime.now(timezone.utc).replace(microsecond=0)
    specs = build_specs(load_json(locations_path))
    results = [
        retrieve(
            spec,
            retrieved_at=timestamp,
            raw_root=raw_root,
            extractor="patrimoine_orne.extract.territorial_context",
            extractor_version=EXTRACTOR_VERSION,
            git_commit=current_git_commit(),
            max_bytes=50 * 1024 * 1024,
        )
        for spec in specs
    ]
    manifest = {
        "schema_version": "1.0",
        "generated_at": timestamp.isoformat().replace("+00:00", "Z"),
        "locations_file": locations_path.as_posix(),
        "request_count": len(results),
        "layers": {
            "hydrographie": "BDTOPO_V3:troncon_hydrographique — 2026-06-15",
            "forets": "LANDCOVER.FORESTINVENTORY.V2:formation_vegetale — 2006-2019",
            "rail": "BDTOPO_V3:troncon_de_voie_ferree — 2026-06-15",
            "lithologie": "BRGM LITHO_1M_SIMPLIFIEE",
            "mines": "BRGM MINES_PT",
            "gites": "BRGM GITES_PT",
        },
        "items": [
            result_manifest(spec, result)
            for spec, result in zip(specs, results, strict=True)
        ],
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--locations",
        type=Path,
        default=Path("data/pilot/localisations_pilote_phase6.json"),
    )
    parser.add_argument("--raw-root", type=Path, default=Path("data/raw"))
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("reports/audits/phase6_contexte_manifest.json"),
    )
    args = parser.parse_args()
    manifest = extract_territorial_context(
        locations_path=args.locations,
        raw_root=args.raw_root,
        manifest_path=args.manifest,
    )
    print(json.dumps({"requests": manifest["request_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
