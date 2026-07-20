"""Évaluation reproductible de la qualité des échantillons de la phase 2."""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

from patrimoine_orne.extract.metadata import sha256_file

CHARSET_RE = re.compile(
    rb"charset\s*=\s*[\"']?\s*([A-Za-z0-9._-]+)",
    re.IGNORECASE,
)
XML_ENCODING_RE = re.compile(
    rb"<\?xml[^>]+encoding=[\"']([^\"']+)[\"']",
    re.IGNORECASE,
)
SCRIPT_RE = re.compile(r"<script(?:\s[^>]*)?>(.*?)</script>", re.DOTALL | re.IGNORECASE)
PUSH_PREFIX = "self.__next_f.push("

POP_PRIORITY_FIELDS = (
    "REF",
    "TICO",
    "DENO",
    "COM",
    "INSEE",
    "LIEU",
    "ADRS",
    "HIST",
    "DESC",
    "HYDR",
    "ENER",
    "SCLE",
    "ETAT",
    "POP_COORDONNEES",
    "COOR",
    "DOSURL",
)
PALISSY_PRIORITY_FIELDS = (
    "reference",
    "titre_editorial",
    "denomination",
    "commune_forme_editoriale",
    "cog_insee",
    "nom_de_l_edifice",
    "historique",
    "description",
    "date_et_typologie_de_la_protection",
    "reference_a_une_notice_merimee_mh",
    "geo_point_2d",
)
MH_PRIORITY_FIELDS = (
    "reference",
    "titre_editorial_de_la_notice",
    "denomination_de_l_edifice",
    "commune_forme_editoriale",
    "cog_insee_lors_de_la_protection",
    "historique",
    "description_de_l_edifice",
    "date_et_typologie_de_la_protection",
    "coordonnees_au_format_wgs84",
    "destination_actuelle_de_l_edifice",
    "etat_de_conservation",
    "nom_du_cours_d_eau_traversant_ou_bordant_l_edifice",
    "source_de_l_energie_utilisee_par_l_edifice",
    "lien_vers_la_base_palissy",
)
CASIAS_PRIORITY_FIELDS = (
    "code_metie",
    "code_inven",
    "nom_etabli",
    "adresse",
    "code_posta",
    "code_insee",
    "nom_commun",
    "etat_activ",
    "activite_p",
    "nature_loc",
    "x_wgs84",
    "y_wgs84",
    "url_fiche",
)


def is_filled(value: Any) -> bool:
    """Indique si une valeur contient une information exploitable."""
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, Mapping):
        return any(is_filled(item) for item in value.values())
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return any(is_filled(item) for item in value)
    return True


def _declared_charset(payload: bytes, content_type: str) -> str | None:
    match = re.search(r"charset\s*=\s*[\"']?\s*([A-Za-z0-9._-]+)", content_type, re.I)
    if match:
        return match.group(1)
    for pattern in (XML_ENCODING_RE, CHARSET_RE):
        match_bytes = pattern.search(payload[:8192])
        if match_bytes:
            return match_bytes.group(1).decode("ascii")
    return None


def inspect_encoding(payload: bytes, content_type: str) -> dict[str, Any]:
    """Teste le décodage strict en privilégiant l'encodage déclaré."""
    declared = _declared_charset(payload, content_type)
    candidates = [declared, "utf-8", "cp1252"]
    tried: list[str] = []
    for candidate in candidates:
        if not candidate:
            continue
        normalised = candidate.lower()
        if normalised in tried:
            continue
        tried.append(normalised)
        try:
            payload.decode(candidate, errors="strict")
        except (LookupError, UnicodeDecodeError):
            continue
        return {
            "declared": declared,
            "decoded_as": normalised,
            "strict_decode": True,
        }
    return {"declared": declared, "decoded_as": None, "strict_decode": False}


def inspect_artifact(data_file: Path, metadata_file: Path) -> dict[str, Any]:
    """Contrôle l'encodage et la conformité du format déclaré d'un fichier."""
    metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
    payload = data_file.read_bytes()
    encoding = inspect_encoding(payload, metadata["content_type"])
    format_name = metadata["format"]
    valid_format = True
    try:
        if format_name == "json":
            json.loads(payload.decode(encoding["decoded_as"] or "utf-8"))
        elif format_name == "gml":
            ET.fromstring(payload)
        elif format_name == "html":
            text = payload.decode(encoding["decoded_as"] or "utf-8")
            valid_format = "<html" in text.lower() or "<!doctype html" in text.lower()
        else:
            valid_format = False
    except (UnicodeDecodeError, json.JSONDecodeError, ET.ParseError):
        valid_format = False
    return {
        "data_file": data_file.as_posix(),
        "format": format_name,
        "content_type": metadata["content_type"],
        "encoding": encoding,
        "valid_format": valid_format,
    }


def extract_pop_notice(text: str, expected_reference: str | None = None) -> dict[str, Any]:
    """Extrait l'objet notice du flux Next.js incorporé dans une page POP."""
    decoder = json.JSONDecoder()
    candidates: list[dict[str, Any]] = []
    for script in SCRIPT_RE.findall(text):
        script = script.strip()
        if not script.startswith(PUSH_PREFIX) or not script.endswith(")"):
            continue
        try:
            pushed = json.loads(script[len(PUSH_PREFIX) : -1])
        except json.JSONDecodeError:
            continue
        if len(pushed) < 2 or not isinstance(pushed[1], str):
            continue
        chunk = pushed[1]
        marker = '"notice":'
        start = chunk.find(marker)
        while start >= 0:
            try:
                notice, _ = decoder.raw_decode(chunk[start + len(marker) :])
            except json.JSONDecodeError:
                break
            if isinstance(notice, dict) and is_filled(notice.get("REF")):
                candidates.append(notice)
            start = chunk.find(marker, start + len(marker))

    if expected_reference:
        for notice in candidates:
            if notice.get("REF") == expected_reference:
                return notice
        raise ValueError(f"notice POP {expected_reference} introuvable dans le HTML")
    if len(candidates) != 1:
        raise ValueError(f"nombre inattendu de notices POP structurées : {len(candidates)}")
    return candidates[0]


def parse_casias(path: Path) -> list[dict[str, str]]:
    """Lit les attributs métier des entités CASIAS d'un fichier GML."""
    root = ET.parse(path).getroot()
    features = [node for node in root.iter() if node.tag.endswith("drealnorm_casias_s_r28")]
    records = []
    for feature in features:
        record = {
            child.tag.rsplit("}", 1)[-1]: child.text or ""
            for child in feature
            if child.tag.rsplit("}", 1)[-1] not in {"boundedBy", "geometry"}
        }
        records.append(record)
    return records


def completeness_profile(
    records: Sequence[Mapping[str, Any]],
    priority_fields: Iterable[str],
) -> dict[str, Any]:
    """Mesure la complétude de tous les champs et d'une sélection prioritaire."""
    record_count = len(records)
    field_names = sorted({field for record in records for field in record})

    def measure(field: str) -> dict[str, Any]:
        filled = sum(is_filled(record.get(field)) for record in records)
        return {
            "filled": filled,
            "missing": record_count - filled,
            "filled_percent": round(filled * 100 / record_count, 1) if record_count else 0.0,
        }

    all_fields = {field: measure(field) for field in field_names}
    return {
        "record_count": record_count,
        "field_count": len(field_names),
        "priority_fields": {field: measure(field) for field in priority_fields},
        "all_fields": all_fields,
    }


def identifier_profile(
    records: Sequence[Mapping[str, Any]],
    identifier_fields: Iterable[str],
) -> dict[str, Any]:
    """Mesure présence, unicité et doublons des identifiants candidats."""
    result = {}
    for field in identifier_fields:
        populated = [record.get(field) for record in records if is_filled(record.get(field))]
        values: list[str] = []
        for value in populated:
            if isinstance(value, Sequence) and not isinstance(
                value, (str, bytes, bytearray)
            ):
                values.extend(str(item).strip() for item in value if is_filled(item))
            else:
                values.append(str(value).strip())
        counts = Counter(values)
        duplicates = sorted(value for value, count in counts.items() if count > 1)
        result[field] = {
            "filled": len(populated),
            "value_count": len(values),
            "unique": len(counts),
            "duplicate_values": duplicates,
        }
    return result


def coordinate_profile(
    records: Sequence[Mapping[str, Any]],
    coordinate_getter: Callable[[Mapping[str, Any]], tuple[Any, Any] | None],
) -> dict[str, Any]:
    """Contrôle présence, validité WGS84 et enveloppe large de l'Orne."""
    present = valid_wgs84 = within_orne_envelope = 0
    invalid_rows: list[int] = []
    for index, record in enumerate(records):
        coordinates = coordinate_getter(record)
        if not coordinates or not all(is_filled(value) for value in coordinates):
            continue
        present += 1
        try:
            lon, lat = (float(value) for value in coordinates)
        except (TypeError, ValueError):
            invalid_rows.append(index)
            continue
        if not (-180 <= lon <= 180 and -90 <= lat <= 90):
            invalid_rows.append(index)
            continue
        valid_wgs84 += 1
        if -1.25 <= lon <= 1.25 and 48.0 <= lat <= 49.1:
            within_orne_envelope += 1
    return {
        "record_count": len(records),
        "present": present,
        "missing": len(records) - present,
        "valid_wgs84": valid_wgs84,
        "within_broad_orne_envelope": within_orne_envelope,
        "invalid_row_indexes": invalid_rows,
        "warning": (
            "L'enveloppe géographique est un contrôle d'anomalie grossière, "
            "pas une validation de l'emplacement du site."
        ),
    }


def _pop_coordinates(record: Mapping[str, Any]) -> tuple[Any, Any] | None:
    point = record.get("POP_COORDONNEES")
    if not isinstance(point, Mapping):
        return None
    return point.get("lon"), point.get("lat")


def _mh_coordinates(record: Mapping[str, Any]) -> tuple[Any, Any] | None:
    point = record.get("coordonnees_au_format_wgs84")
    if not isinstance(point, Mapping):
        return None
    return point.get("lon"), point.get("lat")


def _palissy_coordinates(record: Mapping[str, Any]) -> tuple[Any, Any] | None:
    point = record.get("geo_point_2d")
    if isinstance(point, Mapping):
        return point.get("lon"), point.get("lat")
    return None


def _casias_coordinates(record: Mapping[str, Any]) -> tuple[Any, Any] | None:
    return record.get("x_wgs84"), record.get("y_wgs84")


def _manifest_rows(manifest: Mapping[str, Any], source: str) -> list[Mapping[str, Any]]:
    return list(manifest["sources"][source])


def evaluate_samples(manifest_path: Path) -> dict[str, Any]:
    """Évalue toutes les sources référencées dans un manifeste d'extraction."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    artifact_quality: dict[str, list[dict[str, Any]]] = {}
    for source, rows in manifest["sources"].items():
        artifact_quality[source] = [
            inspect_artifact(Path(row["data_file"]), Path(row["metadata_file"]))
            for row in rows
        ]

    pop_records = []
    for row in _manifest_rows(manifest, "pop_merimee"):
        expected = row["observations"]["reference"]
        text = Path(row["data_file"]).read_text(encoding="utf-8")
        pop_records.append(extract_pop_notice(text, expected))

    palissy_path = Path(_manifest_rows(manifest, "pop_palissy")[0]["data_file"])
    palissy_records = json.loads(palissy_path.read_text(encoding="utf-8"))["results"]
    mh_path = Path(
        _manifest_rows(manifest, "monuments_historiques_data_culture")[0]["data_file"]
    )
    mh_records = json.loads(mh_path.read_text(encoding="utf-8"))["results"]
    casias_records = [
        record
        for row in _manifest_rows(manifest, "casias")
        for record in parse_casias(Path(row["data_file"]))
    ]
    inventory_references = sorted(
        {
            row["observations"]["reference"]
            for row in _manifest_rows(manifest, "inventaire_normandie_orne")
        }
    )

    return {
        "schema_version": "1.0",
        "evaluated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
            "+00:00", "Z"
        ),
        "sample_manifest": manifest_path.as_posix(),
        "sample_manifest_sha256": sha256_file(manifest_path),
        "artifact_quality": artifact_quality,
        "sources": {
            "inventaire_normandie_orne": {
                "record_count": len(inventory_references),
                "artifact_count": len(_manifest_rows(manifest, "inventaire_normandie_orne")),
                "identifiers": {
                    "REF_IA": {
                        "filled": len(inventory_references),
                        "value_count": len(inventory_references),
                        "unique": len(set(inventory_references)),
                        "duplicate_values": [],
                    }
                },
                "coordinates": {
                    "record_count": len(inventory_references),
                    "present": 0,
                    "missing": len(inventory_references),
                    "note": "Les fichiers d'index ne portent pas de coordonnées structurées.",
                },
                "automation": "moyenne",
                "manual_tasks": [
                    "télécharger et OCRiser seulement les scans nécessaires",
                    "contrôler les résultats OCR et les informations absentes de POP",
                ],
            },
            "pop_merimee": {
                "completeness": completeness_profile(pop_records, POP_PRIORITY_FIELDS),
                "identifiers": identifier_profile(pop_records, ("REF", "LBASE2", "INSEE")),
                "coordinates": coordinate_profile(pop_records, _pop_coordinates),
                "automation": "élevée pour l'extraction, moyenne pour la publication",
                "manual_tasks": [
                    "interpréter les activités successives et les états historiques",
                    "vérifier les localisations absentes ou insuffisamment précises",
                ],
            },
            "pop_palissy": {
                "completeness": completeness_profile(
                    palissy_records, PALISSY_PRIORITY_FIELDS
                ),
                "identifiers": identifier_profile(
                    palissy_records,
                    ("reference", "identifiant_agregee", "cog_insee"),
                ),
                "coordinates": coordinate_profile(palissy_records, _palissy_coordinates),
                "automation": "élevée pour l'extraction, moyenne pour le rattachement",
                "manual_tasks": [
                    "rattacher les objets sans référence Mérimée à un site contrôlé",
                    "déterminer si l'objet est encore présent et publiable",
                ],
            },
            "monuments_historiques_data_culture": {
                "completeness": completeness_profile(mh_records, MH_PRIORITY_FIELDS),
                "identifiers": identifier_profile(
                    mh_records,
                    ("reference", "identifiant_agregee", "cog_insee_lors_de_la_protection"),
                ),
                "coordinates": coordinate_profile(mh_records, _mh_coordinates),
                "automation": "élevée pour l'extraction, moyenne pour la sélection",
                "manual_tasks": [
                    "écarter les faux positifs de la recherche plein texte",
                    "vérifier si la protection concerne bien les éléments industriels",
                ],
            },
            "casias": {
                "completeness": completeness_profile(casias_records, CASIAS_PRIORITY_FIELDS),
                "identifiers": identifier_profile(
                    casias_records,
                    ("code_metie", "code_inven", "id", "code_insee"),
                ),
                "coordinates": coordinate_profile(casias_records, _casias_coordinates),
                "automation": "élevée pour l'extraction, faible pour l'inclusion directe",
                "manual_tasks": [
                    "retrouver l'activité absente de la couche WFS",
                    "localiser les fiches explicitement non géolocalisées",
                    "qualifier l'intérêt patrimonial et dédoublonner avec les autres sources",
                ],
                "geometry_policy": (
                    "Ignorer la géométrie WFS lorsque x_wgs84 et y_wgs84 sont absents."
                ),
            },
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("reports/audits/phase2_extraction_samples_manifest.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/quality/phase2_evaluation_samples.json"),
    )
    args = parser.parse_args()
    result = evaluate_samples(args.manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    summary = {
        source: data.get("record_count")
        or data.get("completeness", {}).get("record_count")
        for source, data in result["sources"].items()
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
