"""Extractions tests des cinq sources principales de la phase 2."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlencode

from .http import RetrievalResult, RetrievalSpec, retrieve

EXTRACTOR_VERSION = "0.1.0"
INVENTAIRE_REFERENCES = (
    "IA00060965",  # forge de Varenne : affinerie et moulin à blé
    "IA00061095",  # briqueterie des Chauffetières
    "IA00060938",  # centrale hydroélectrique de Rabodanges
    "IA00061190",  # filature liée à la Martinique
    "IA00061038",  # filature devenue minoterie
    "IA00061008",  # mine de Halouze
    "IA00061113",  # laminoir et usine de quincaillerie
    "IA00061091",  # moulin à farine non géolocalisé
    "IA00061082",  # moulin à farine et à huile non géolocalisé
    "IA00061147",  # cartonnerie
)
PALISSY_REFERENCES = ("PM61000916", "PM61000814")

POP_BASE = "https://pop.culture.gouv.fr/notice/merimee"
INVENTAIRE_STATIC_BASE = "http://www2.culture.gouv.fr/documentation/memoire/HTML/IVR25"
PALISSY_API = (
    "https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/"
    "liste-des-objets-mobiliers-propriete-publique-classes-au-titre-des-monuments/records"
)
MH_API = (
    "https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/"
    "liste-des-immeubles-proteges-au-titre-des-monuments-historiques/records"
)
CASIAS_WFS = (
    "https://ogc.geo-ide.developpement-durable.gouv.fr/wxs?"
    "map=/opt/data/stack/mapfiles/1.4/org_4930752/"
    "47dbcca9-c749-4082-9a87-69e869981ffa.internet.map"
)


def _read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def validate_inventaire_index(reference: str) -> Callable[[Path], dict[str, Any]]:
    def validator(path: Path) -> dict[str, Any]:
        payload = _read_bytes(path)
        if reference.encode("ascii") not in payload:
            raise ValueError(f"référence {reference} absente de l'index Inventaire")
        if b"THUMBNAILFRAME.HTM" not in payload:
            raise ValueError("index Inventaire sans sommaire de pages")
        challenge_text = "Vérification de la connexion".encode()
        if b"haphash" in payload or challenge_text in payload:
            raise ValueError("réponse remplacée par le contrôle anti-robot")
        return {"reference": reference, "kind": "index"}

    return validator


def validate_inventaire_thumbnails(reference: str) -> Callable[[Path], dict[str, Any]]:
    def validator(path: Path) -> dict[str, Any]:
        payload = _read_bytes(path)
        if reference.encode("ascii") not in payload:
            raise ValueError(f"référence {reference} absente du sommaire Inventaire")
        page_pattern = rb"PAGES/" + reference.encode("ascii") + rb"_\d+\.HTM"
        pages = sorted(set(match.decode("ascii") for match in re.findall(page_pattern, payload)))
        if not pages:
            raise ValueError("sommaire Inventaire sans page numérisée")
        return {"reference": reference, "kind": "thumbnails", "page_count": len(pages)}

    return validator


def validate_pop_notice(reference: str) -> Callable[[Path], dict[str, Any]]:
    def validator(path: Path) -> dict[str, Any]:
        payload = _read_bytes(path)
        if reference.encode("ascii") not in payload:
            raise ValueError(f"référence {reference} absente de la notice POP")
        if b"haphash" in payload:
            raise ValueError("réponse POP remplacée par un contrôle anti-robot")
        return {
            "reference": reference,
            "has_inventaire_link": b"inventaire-patrimoine.normandie.fr" in payload,
            "has_static_dossier_link": b"www2.culture.gouv.fr" in payload,
        }

    return validator


def validate_palissy_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    results = payload.get("results", [])
    references = sorted(record.get("reference") for record in results)
    if references != sorted(PALISSY_REFERENCES):
        raise ValueError("l'échantillon Palissy ne contient pas les références attendues")
    return {
        "total_count": payload.get("total_count"),
        "result_count": len(results),
        "references": references,
        "field_count": len(results[0]) if results else 0,
        "with_merimee_reference": sum(
            bool(record.get("reference_a_une_notice_merimee_mh")) for record in results
        ),
    }


def validate_mh_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    results = payload.get("results", [])
    departments = [record.get("departement_en_lettres") for record in results]
    outside_orne = [
        value
        for value in departments
        if "Orne" not in (value if isinstance(value, list) else [value])
    ]
    if not results or outside_orne:
        raise ValueError("l'échantillon Monuments historiques n'est pas limité à l'Orne")
    return {
        "total_count": payload.get("total_count"),
        "result_count": len(results),
        "field_count": len(results[0]),
        "with_coordinates": sum(
            bool(record.get("coordonnees_au_format_wgs84")) for record in results
        ),
        "references": sorted(record.get("reference") for record in results),
    }


def validate_casias_xml(expected_localized: bool) -> Callable[[Path], dict[str, Any]]:
    def validator(path: Path) -> dict[str, Any]:
        root = ET.parse(path).getroot()
        features = [node for node in root.iter() if node.tag.endswith("drealnorm_casias_s_r28")]
        if not features:
            raise ValueError("l'échantillon CASIAS ne contient aucune entité")

        records: list[dict[str, str]] = []
        for feature in features:
            record = {child.tag.rsplit("}", 1)[-1]: child.text or "" for child in feature}
            records.append(record)
        if any(record.get("code_depar") != "61" for record in records):
            raise ValueError("l'échantillon CASIAS contient un autre département")

        with_coordinates = sum(bool(record.get("x_wgs84")) for record in records)
        if expected_localized and with_coordinates != len(records):
            raise ValueError("le lot CASIAS localisé contient une ligne sans coordonnées")
        if not expected_localized and with_coordinates:
            raise ValueError("le lot CASIAS non localisé contient des coordonnées")
        return {
            "result_count": len(records),
            "with_coordinates": with_coordinates,
            "without_establishment_name": sum(not record.get("nom_etabli") for record in records),
            "inventory_codes": sorted(record.get("code_inven", "") for record in records),
        }

    return validator


def _wfs_filter(*conditions: tuple[str, str, str]) -> str:
    fragments = []
    for operator, field, value in conditions:
        fragments.append(
            f"<fes:{operator}><fes:ValueReference>{field}</fes:ValueReference>"
            f"<fes:Literal>{value}</fes:Literal></fes:{operator}>"
        )
    body = "".join(fragments)
    if len(fragments) > 1:
        body = f"<fes:And>{body}</fes:And>"
    return f'<fes:Filter xmlns:fes="http://www.opengis.net/fes/2.0">{body}</fes:Filter>'


def build_specs() -> list[RetrievalSpec]:
    specs: list[RetrievalSpec] = []
    inventaire_page = (
        "https://www.data.gouv.fr/datasets/inventaire-du-patrimoine-architectural-normand"
    )
    for reference in INVENTAIRE_REFERENCES:
        base = f"{INVENTAIRE_STATIC_BASE}/{reference}"
        common_notes = (
            "Le portail régional renvoie un contrôle JavaScript aux requêtes directes.",
            "Le dossier statique est lié depuis la notice POP et se compose de pages numérisées.",
        )
        specs.extend(
            [
                RetrievalSpec(
                    source_id="inventaire_normandie_orne",
                    resource_id=f"{reference}_index",
                    scope="orne",
                    source_page_url=inventaire_page,
                    request_url=f"{base}/INDEX.HTM",
                    format="html",
                    license="Non précisée sur le jeu data.gouv.fr ; © Région Normandie",
                    notes=common_notes,
                    validator=validate_inventaire_index(reference),
                ),
                RetrievalSpec(
                    source_id="inventaire_normandie_orne",
                    resource_id=f"{reference}_thumbnails",
                    scope="orne",
                    source_page_url=inventaire_page,
                    request_url=f"{base}/THUMBNAILFRAME.HTM",
                    format="html",
                    license="Non précisée sur le jeu data.gouv.fr ; © Région Normandie",
                    notes=common_notes,
                    validator=validate_inventaire_thumbnails(reference),
                ),
            ]
        )

        specs.append(
            RetrievalSpec(
                source_id="pop_merimee",
                resource_id=reference,
                scope="orne",
                source_page_url="https://pop.culture.gouv.fr/donnees-ouvertes",
                request_url=f"{POP_BASE}/{reference}",
                format="html",
                license="Licence Ouverte 2.0 sauf mention contraire ; © Région Normandie",
                notes=("Notice de l'Inventaire général diffusée dans la base Mérimée de POP.",),
                validator=validate_pop_notice(reference),
            )
        )

    palissy_where = "reference in (" + ",".join(f'\"{ref}\"' for ref in PALISSY_REFERENCES) + ")"
    palissy_query = {"where": palissy_where, "limit": 10}
    specs.append(
        RetrievalSpec(
            source_id="pop_palissy",
            resource_id="objets_techniques_cibles",
            scope="orne",
            source_page_url=(
                "https://data.culture.gouv.fr/explore/dataset/"
                "liste-des-objets-mobiliers-propriete-publique-classes-au-titre-des-monuments/"
            ),
            request_url=f"{PALISSY_API}?{urlencode(palissy_query)}",
            format="json",
            license="Licence Ouverte 2.0 ; médias selon leurs droits propres",
            query=palissy_query,
            validator=validate_palissy_json,
        )
    )

    mh_terms = (
        "usine",
        "filature",
        "forge",
        "briqueterie",
        "tuilerie",
        "minoterie",
        "moulin",
        "scierie",
    )
    mh_where = 'departement_en_lettres="Orne" and (' + " or ".join(
        f'search("{term}")' for term in mh_terms
    ) + ")"
    mh_query = {"where": mh_where, "order_by": "reference", "limit": 100}
    specs.append(
        RetrievalSpec(
            source_id="monuments_historiques_data_culture",
            resource_id="candidats_industriels",
            scope="orne",
            source_page_url=(
                "https://data.culture.gouv.fr/explore/dataset/"
                "liste-des-immeubles-proteges-au-titre-des-monuments-historiques/"
            ),
            request_url=f"{MH_API}?{urlencode(mh_query)}",
            format="json",
            license="Licence Ouverte 2.0",
            query=mh_query,
            notes=("Recherche plein texte volontairement large ; faux positifs attendus.",),
            validator=validate_mh_json,
        )
    )

    casias_common = {
        "SERVICE": "WFS",
        "VERSION": "2.0.0",
        "REQUEST": "GetFeature",
        "TYPENAMES": "ms:drealnorm_casias_s_r28",
        "COUNT": 10,
    }
    localized_filter = _wfs_filter(
        ("PropertyIsEqualTo", "code_depar", "61"),
        ("PropertyIsNotEqualTo", "x_wgs84", ""),
    )
    nonlocalized_filter = _wfs_filter(
        ("PropertyIsEqualTo", "code_depar", "61"),
        ("PropertyIsEqualTo", "nature_loc", "Site non gélocalisé"),
    )
    for resource_id, filter_xml, localized in (
        ("wfs_localises", localized_filter, True),
        ("wfs_non_localises", nonlocalized_filter, False),
    ):
        query = {**casias_common, "FILTER": filter_xml}
        specs.append(
            RetrievalSpec(
                source_id="casias",
                resource_id=resource_id,
                scope="orne",
                source_page_url=(
                    "https://www.data.gouv.fr/datasets/"
                    "carte-des-anciens-sites-industriels-et-activites-de-services-casias-normandie"
                ),
                request_url=f"{CASIAS_WFS}&{urlencode(query)}",
                format="gml",
                license="Licence Ouverte 2.0",
                query=query,
                notes=("La géométrie WFS ne vaut pas localisation précise du site.",),
                validator=validate_casias_xml(localized),
            )
        )
    return specs


def current_git_commit() -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def result_manifest(result: RetrievalResult) -> dict[str, Any]:
    return {
        "data_file": _relative(result.data_file),
        "metadata_file": _relative(result.metadata_file),
        "file_size_bytes": result.metadata["file_size_bytes"],
        "sha256": result.metadata["sha256"],
        "observations": result.observations,
    }


def extract_all_samples(
    *,
    raw_root: Path = Path("data/raw"),
    manifest_path: Path = Path("reports/audits/phase2_extraction_samples_manifest.json"),
) -> dict[str, Any]:
    retrieved_at = datetime.now(timezone.utc).replace(microsecond=0)
    git_commit = current_git_commit()
    grouped: dict[str, list[dict[str, Any]]] = {}

    for spec in build_specs():
        result = retrieve(
            spec,
            retrieved_at=retrieved_at,
            raw_root=raw_root,
            extractor="patrimoine_orne.extract.samples",
            extractor_version=EXTRACTOR_VERSION,
            git_commit=git_commit,
        )
        grouped.setdefault(spec.source_id, []).append(result_manifest(result))

    manifest = {
        "schema_version": "1.0",
        "generated_at": retrieved_at.isoformat().replace("+00:00", "Z"),
        "git_commit": git_commit,
        "sources": grouped,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-root", type=Path, default=Path("data/raw"))
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("reports/audits/phase2_extraction_samples_manifest.json"),
    )
    args = parser.parse_args()
    manifest = extract_all_samples(raw_root=args.raw_root, manifest_path=args.manifest)
    counts = {source: len(files) for source, files in manifest["sources"].items()}
    print(json.dumps(counts, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
