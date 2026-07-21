"""Archive les contrôles BAN et cadastraux du pilote de phase 6."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import urlencode

from patrimoine_orne.classify.sectors import load_pop_manifest_sample

from .http import RetrievalResult, RetrievalSpec, retrieve
from .pilot import current_git_commit


EXTRACTOR_VERSION = "0.1.0"
GEOCODING_BASE = "https://data.geopf.fr/geocodage/search"
CADASTRE_BASE = "https://apicarto.ign.fr/api/cadastre/parcelle"
ADDRESS_PATTERN = re.compile(r"^(.+?)\s+\(([^)]+)\)\s+(\d+[A-Za-z]?)$")


def sufficient_address_query(record: Mapping[str, Any]) -> str | None:
    """Convertit une adresse POP unique en requête ; refuse rues et plages de numéros."""
    address = str(record.get("ADRS") or "").strip()
    match = ADDRESS_PATTERN.fullmatch(address)
    if not match:
        return None
    street_name, street_type, number = match.groups()
    commune = record.get("COM") or []
    city = commune[0] if isinstance(commune, list) and commune else str(commune)
    return f"{number} {street_type} {street_name} {city}".strip()


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_geocoding(reference: str, expected_citycode: str):
    def validator(path: Path) -> dict[str, Any]:
        payload = _read_json(path)
        features = payload.get("features", [])
        top = features[0].get("properties", {}) if features else {}
        return {
            "reference": reference,
            "candidate_count": len(features),
            "top_citycode": top.get("citycode"),
            "top_type": top.get("type"),
            "top_score": top.get("score"),
            "citycode_matches": top.get("citycode") == expected_citycode,
        }

    return validator


def validate_cadastre(reference: str):
    def validator(path: Path) -> dict[str, Any]:
        payload = _read_json(path)
        features = payload.get("features", [])
        return {
            "reference": reference,
            "parcel_count": len(features),
            "parcel_ids": [item.get("properties", {}).get("idu") for item in features],
        }

    return validator


def build_specs(records: Sequence[Mapping[str, Any]]) -> tuple[list[RetrievalSpec], list[str]]:
    specs: list[RetrievalSpec] = []
    rejected_addresses: list[str] = []
    for record in records:
        reference = str(record["REF"])
        citycode_values = record.get("INSEE") or []
        citycode = str(citycode_values[0] if isinstance(citycode_values, list) else citycode_values)
        query = sufficient_address_query(record)
        if record.get("ADRS") and query is None:
            rejected_addresses.append(reference)
        if query:
            parameters = {
                "q": query,
                "index": "address",
                "type": "housenumber",
                "citycode": citycode,
                "limit": 5,
            }
            specs.append(
                RetrievalSpec(
                    source_id="ban",
                    resource_id=f"{reference}_adresse",
                    scope="orne_pilote_phase6",
                    source_page_url=(
                        "https://cartes.gouv.fr/aide/fr/guides-utilisateur/"
                        "utiliser-les-services-de-la-geoplateforme/geocodage/"
                    ),
                    request_url=f"{GEOCODING_BASE}?{urlencode(parameters)}",
                    format="json",
                    license="Licence Ouverte 2.0",
                    query=parameters,
                    notes=(
                        "Adresse POP reformattée sans modifier le nom de voie.",
                        "Le résultat BAN contrôle un point d'adresse, pas le bâtiment industriel.",
                    ),
                    validator=validate_geocoding(reference, citycode),
                )
            )

        point = record.get("POP_COORDONNEES")
        if not isinstance(point, Mapping) or point.get("lon") is None or point.get("lat") is None:
            continue
        geometry = json.dumps(
            {"type": "Point", "coordinates": [point["lon"], point["lat"]]},
            ensure_ascii=False,
            separators=(",", ":"),
        )
        parameters = {"geom": geometry}
        specs.append(
            RetrievalSpec(
                source_id="cadastre",
                resource_id=f"{reference}_parcelle_point_pop",
                scope="orne_pilote_phase6",
                source_page_url=(
                    "https://cartes.gouv.fr/aide/fr/partenaires/ign/"
                    "outils-cartographiques/api-carto/"
                ),
                request_url=f"{CADASTRE_BASE}?{urlencode(parameters)}",
                format="geojson",
                license="Licence Ouverte 2.0",
                query=parameters,
                notes=(
                    "Intersection du point POP avec le Parcellaire Express courant.",
                    "Une parcelle trouvée reste candidate tant que l'emprise n'est pas contrôlée.",
                ),
                validator=validate_cadastre(reference),
            )
        )
    return specs, rejected_addresses


def _relative(path: Path) -> str:
    return path.resolve().relative_to(Path.cwd().resolve()).as_posix()


def result_manifest(result: RetrievalResult) -> dict[str, Any]:
    return {
        "data_file": _relative(result.data_file),
        "metadata_file": _relative(result.metadata_file),
        "sha256": result.metadata["sha256"],
        "observations": result.observations,
    }


def extract_pilot_geography(
    *,
    pop_manifest_path: Path = Path("reports/audits/phase5_pop_manifest.json"),
    raw_root: Path = Path("data/raw"),
    manifest_path: Path = Path("reports/audits/phase6_localisation_manifest.json"),
    retrieved_at: datetime | None = None,
) -> dict[str, Any]:
    timestamp = retrieved_at or datetime.now(timezone.utc).replace(microsecond=0)
    records = load_pop_manifest_sample(pop_manifest_path)
    specs, rejected_addresses = build_specs(records)
    results = [
        retrieve(
            spec,
            retrieved_at=timestamp,
            raw_root=raw_root,
            extractor="patrimoine_orne.extract.pilot_geography",
            extractor_version=EXTRACTOR_VERSION,
            git_commit=current_git_commit(),
        )
        for spec in specs
    ]
    sources: dict[str, list[dict[str, Any]]] = {"ban": [], "cadastre": []}
    for spec, result in zip(specs, results, strict=True):
        sources[spec.source_id].append(result_manifest(result))
    manifest = {
        "schema_version": "1.0",
        "generated_at": timestamp.isoformat().replace("+00:00", "Z"),
        "pop_manifest": pop_manifest_path.as_posix(),
        "rejected_non_unique_addresses": rejected_addresses,
        "sources": sources,
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
        "--pop-manifest",
        type=Path,
        default=Path("reports/audits/phase5_pop_manifest.json"),
    )
    parser.add_argument("--raw-root", type=Path, default=Path("data/raw"))
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("reports/audits/phase6_localisation_manifest.json"),
    )
    args = parser.parse_args()
    manifest = extract_pilot_geography(
        pop_manifest_path=args.pop_manifest,
        raw_root=args.raw_root,
        manifest_path=args.manifest,
    )
    print(
        json.dumps(
            {source: len(items) for source, items in manifest["sources"].items()},
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
