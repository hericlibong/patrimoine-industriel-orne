"""Archive les couches territoriales par tuiles pour les 318 sites."""

from __future__ import annotations

import argparse
import json
import math
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping
from urllib.parse import urlencode

from patrimoine_orne.extract.http import RetrievalResult, RetrievalSpec, retrieve
from patrimoine_orne.extract.pilot import current_git_commit
from patrimoine_orne.extract.territorial_context import (
    BRGM_LAYERS,
    BRGM_WFS,
    IGN_LAYERS,
    IGN_WFS,
)


EXTRACTOR_VERSION = "0.1.0"
DEFAULT_LOCATIONS = Path("data/processed/localisations_corpus_phase8_v1.json")
DEFAULT_MANIFEST = Path("reports/audits/phase8_contexte_territorial_manifest.json")
TILE_SIZE = 0.15


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _tile(point: list[float]) -> tuple[int, int]:
    return math.floor(point[0] / TILE_SIZE), math.floor(point[1] / TILE_SIZE)


def _bbox_text(values: tuple[float, float, float, float], *, crs: bool) -> str:
    parts = [f"{value:.7f}" for value in values]
    if crs:
        parts.append("EPSG:4326")
    return ",".join(parts)


def _padded_tile_bbox(
    key: tuple[int, int], radius_m: float
) -> tuple[float, float, float, float]:
    lon_min, lat_min = key[0] * TILE_SIZE, key[1] * TILE_SIZE
    lon_max, lat_max = lon_min + TILE_SIZE, lat_min + TILE_SIZE
    mid_lat = (lat_min + lat_max) / 2
    lat_pad = radius_m / 111_320
    lon_pad = radius_m / (111_320 * math.cos(math.radians(mid_lat)))
    return lon_min - lon_pad, lat_min - lat_pad, lon_max + lon_pad, lat_max + lat_pad


def validate_ign_tile(
    tile_id: str, layer: str, references: list[str]
) -> Callable[[Path], dict[str, Any]]:
    def validator(path: Path) -> dict[str, Any]:
        payload = load_json(path)
        features = payload.get("features")
        if payload.get("type") != "FeatureCollection" or not isinstance(features, list):
            raise ValueError("réponse WFS IGN invalide")
        matched = payload.get("numberMatched")
        if matched not in (None, "unknown"):
            try:
                matched_count = int(matched)
            except (TypeError, ValueError) as exc:
                raise ValueError("nombre de résultats IGN illisible") from exc
            if matched_count > len(features):
                raise ValueError(f"tuile IGN tronquée : {len(features)} sur {matched_count}")
        return {
            "tile": tile_id,
            "layer": layer,
            "references": references,
            "feature_count": len(features),
            "number_matched": matched,
        }

    return validator


def validate_brgm_full(layer: str) -> Callable[[Path], dict[str, Any]]:
    def validator(path: Path) -> dict[str, Any]:
        root = ET.parse(path).getroot()
        if root.tag.rsplit("}", 1)[-1] == "ServiceExceptionReport":
            message = " ".join(text.strip() for text in root.itertext() if text.strip())
            raise ValueError(f"erreur WFS BRGM : {message}")
        members = [
            item
            for item in root.iter()
            if item.tag.rsplit("}", 1)[-1] == "featureMember"
        ]
        return {"layer": layer, "feature_count": len(members)}

    return validator


def build_specs(locations: Mapping[str, Any]) -> list[RetrievalSpec]:
    by_tile: dict[tuple[int, int], list[Mapping[str, Any]]] = {}
    points = []
    for item in locations["locations"]:
        point = item.get("point_wgs84")
        if not point:
            continue
        points.append(point)
        by_tile.setdefault(_tile(point), []).append(item)
    specs = []
    for key, items in sorted(by_tile.items()):
        tile_id = f"t{key[0]:+04d}_{key[1]:+04d}".replace("+", "p").replace("-", "m")
        references = sorted(str(item["reference_ia"]) for item in items)
        for layer, settings in IGN_LAYERS.items():
            parameters = {
                "SERVICE": "WFS",
                "VERSION": "2.0.0",
                "REQUEST": "GetFeature",
                "TYPENAMES": settings["typename"],
                "SRSNAME": "EPSG:4326",
                "BBOX": _bbox_text(
                    _padded_tile_bbox(key, settings["radius_m"]), crs=True
                ),
                "COUNT": 10000,
                "OUTPUTFORMAT": "application/json",
            }
            specs.append(
                RetrievalSpec(
                    source_id=str(settings["source_id"]),
                    resource_id=f"{tile_id}_{layer}",
                    scope="orne_phase8_contexte_complet",
                    source_page_url="https://documentation.geoservices.ign.fr/?BDTopo=",
                    request_url=f"{IGN_WFS}?{urlencode(parameters)}",
                    format="geojson",
                    license="Licence Ouverte 2.0",
                    query=parameters,
                    notes=(
                        f"Tuile de {TILE_SIZE} degré avec marge de "
                        f"{settings['radius_m']} mètres.",
                        "La proximité calculée ne prouve pas une relation historique.",
                    ),
                    validator=validate_ign_tile(tile_id, layer, references),
                )
            )

    lon_values = [point[0] for point in points]
    lat_values = [point[1] for point in points]
    for layer, settings in BRGM_LAYERS.items():
        radius = settings["radius_m"]
        mid_lat = sum(lat_values) / len(lat_values)
        lat_pad = radius / 111_320
        lon_pad = radius / (111_320 * math.cos(math.radians(mid_lat)))
        bbox = (
            min(lon_values) - lon_pad,
            min(lat_values) - lat_pad,
            max(lon_values) + lon_pad,
            max(lat_values) + lat_pad,
        )
        parameters = {
            "SERVICE": "WFS",
            "VERSION": "1.0.0",
            "REQUEST": "GetFeature",
            "TYPENAME": settings["typename"],
            "SRSNAME": "EPSG:4326",
            "BBOX": _bbox_text(bbox, crs=False),
            "MAXFEATURES": 10000,
        }
        specs.append(
            RetrievalSpec(
                source_id="brgm",
                resource_id=f"orne_complete_{layer}",
                scope="orne_phase8_contexte_complet",
                source_page_url="https://infoterre.brgm.fr/page/geoservices-ogc",
                request_url=f"{BRGM_WFS}?{urlencode(parameters)}",
                format="gml",
                license="Conditions de réutilisation des données du BRGM",
                query=parameters,
                notes=(
                    f"Couche {settings['typename']} sur l'enveloppe du corpus.",
                    "La proximité calculée ne prouve pas une relation historique.",
                ),
                validator=validate_brgm_full(layer),
            )
        )
    return specs


def _relative(path: Path) -> str:
    return path.resolve().relative_to(Path.cwd().resolve()).as_posix()


def _manifest_item(spec: RetrievalSpec, result: RetrievalResult) -> dict[str, Any]:
    return {
        "source_id": spec.source_id,
        "data_file": _relative(result.data_file),
        "metadata_file": _relative(result.metadata_file),
        "sha256": result.metadata["sha256"],
        "observations": result.observations,
    }


def extract_full_context(
    *,
    locations_path: Path = DEFAULT_LOCATIONS,
    raw_root: Path = Path("data/raw"),
    manifest_path: Path = DEFAULT_MANIFEST,
) -> dict[str, Any]:
    timestamp = datetime.now(timezone.utc).replace(microsecond=0)
    specs = build_specs(load_json(locations_path))
    results = [
        retrieve(
            spec,
            retrieved_at=timestamp,
            raw_root=raw_root,
            extractor="patrimoine_orne.extract.full_territorial_context",
            extractor_version=EXTRACTOR_VERSION,
            git_commit=current_git_commit(),
            max_bytes=100 * 1024 * 1024,
        )
        for spec in specs
    ]
    manifest = {
        "schema_version": "1.0",
        "generated_at": timestamp.isoformat().replace("+00:00", "Z"),
        "locations_file": locations_path.as_posix(),
        "status": "complete",
        "tile_size_degrees": TILE_SIZE,
        "request_count": len(results),
        "items": [
            _manifest_item(spec, result)
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
    parser.add_argument("--locations", type=Path, default=DEFAULT_LOCATIONS)
    parser.add_argument("--raw-root", type=Path, default=Path("data/raw"))
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    manifest = extract_full_context(
        locations_path=args.locations,
        raw_root=args.raw_root,
        manifest_path=args.manifest,
    )
    print(json.dumps({"requests": manifest["request_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
