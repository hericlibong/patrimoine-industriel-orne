"""Enrichit prudemment les 318 sites canoniques avec MH, Palissy et CASIAS."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import unicodedata
from collections import defaultdict
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Sequence

from pyproj import Transformer
import yaml

from patrimoine_orne.extract.full_enrichment import load_culture_records
from patrimoine_orne.validate.sample_quality import parse_casias


DEFAULT_CORPUS = Path("data/processed/corpus_canonique_phase8_v1.json")
DEFAULT_MANIFEST = Path("reports/audits/phase8_enrichissement_sources_manifest.json")
DEFAULT_OUTPUT = Path("data/processed/corpus_enrichi_phase8_v1.json")
DEFAULT_LOCATIONS = Path("data/processed/localisations_corpus_phase8_v1.json")
DEFAULT_SUMMARY = Path("reports/quality/phase8_enrichissement_resume.json")
DEFAULT_MH = Path("reports/quality/phase8_protections_mh.csv")
DEFAULT_PALISSY = Path("reports/quality/phase8_objets_palissy.csv")
DEFAULT_CASIAS = Path("reports/quality/phase8_recoupements_casias.csv")
DEFAULT_EXPANSION = Path("reports/quality/phase8_casias_elargissement.csv")
DEFAULT_AMBIGUITIES = Path("reports/quality/phase8_ambiguities_enrichissement.csv")
DEFAULT_DECISIONS = Path("config/phase8_decisions_enrichissement.yml")

REFERENCE_IA_RE = re.compile(r"\bIA\d{8}\b")
REFERENCE_PA_RE = re.compile(r"\bPA\d{8}\b")
INDUSTRIAL_TERMS = (
    "abattoir",
    "briqueterie",
    "carriere",
    "cartonnerie",
    "centrale",
    "ceramique",
    "distillerie",
    "filature",
    "fonderie",
    "forge",
    "imprimerie",
    "laiterie",
    "manufacture",
    "metallurgie",
    "mine",
    "minoterie",
    "moulin",
    "papeterie",
    "scierie",
    "textile",
    "tissage",
    "tuilerie",
    "usine",
    "verrerie",
)
EXCLUDED_EXPANSION_TERMS = (
    "carrosserie",
    "decharge",
    "dechetterie",
    "garage",
    "pressing",
    "station service",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(value: Any) -> str:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        value = " ".join(str(item) for item in value)
    text = unicodedata.normalize("NFKD", str(value or "").casefold())
    text = "".join(char for char in text if not unicodedata.combining(char))
    return " ".join(re.findall(r"[a-z0-9]+", text))


def token_set_ratio(first: str, second: str) -> int:
    """Mesure simple et déterministe du recouvrement des mots."""
    first_tokens, second_tokens = set(first.split()), set(second.split())
    if not first_tokens or not second_tokens:
        return 0
    common = first_tokens & second_tokens
    return round(200 * len(common) / (len(first_tokens) + len(second_tokens)))


def _values(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [str(item) for item in value if item not in (None, "")]
    return [str(value)] if value != "" else []


def _references(record: Mapping[str, Any], pattern: re.Pattern[str]) -> set[str]:
    return set(pattern.findall(json.dumps(record, ensure_ascii=False)))


def _point(record: Mapping[str, Any]) -> list[float] | None:
    point = record.get("POP_COORDONNEES") or {}
    try:
        lon, lat = float(point["lon"]), float(point["lat"])
    except (KeyError, TypeError, ValueError):
        return None
    if lon == 0 and lat == 0:
        return None
    return [lon, lat]


def haversine_metres(first: Sequence[float], second: Sequence[float]) -> float:
    lon1, lat1 = map(math.radians, first[:2])
    lon2, lat2 = map(math.radians, second[:2])
    delta_lon, delta_lat = lon2 - lon1, lat2 - lat1
    value = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
    )
    return 2 * 6_371_008.8 * math.asin(math.sqrt(value))


def _site_text(site: Mapping[str, Any]) -> str:
    return normalize(
        [
            site.get("nom_principal"),
            site.get("titre_source"),
            *site.get("adresses_source", []),
            *site.get("lieux_dits_source", []),
        ]
    )


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(fields))
        writer.writeheader()
        writer.writerows(rows)


def reconcile_mh(
    sites: Sequence[dict[str, Any]], merimee: Sequence[Mapping[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    site_by_ia = {str(site["dossier_reference"]): site for site in sites}
    pa_records = {
        str(record["REF"]): record
        for record in merimee
        if str(record.get("REF", "")).startswith("PA")
    }
    pa_to_ia: dict[str, str] = {}
    rows = []
    for pa_reference, record in pa_records.items():
        candidates = sorted(_references(record, REFERENCE_IA_RE) & set(site_by_ia))
        if len(candidates) != 1:
            continue
        ia_reference = candidates[0]
        pa_to_ia[pa_reference] = ia_reference
        site = site_by_ia[ia_reference]
        mh_point = _point(record)
        site_point = [site["longitude_source"], site["latitude_source"]]
        mh_distance = haversine_metres(mh_point, site_point) if mh_point else None
        protection = {
            "reference_mh": pa_reference,
            "titre": record.get("TICO"),
            "protection": record.get("PROT"),
            "date_protection": record.get("DPRO"),
            "precision_protection": record.get("PPRO"),
            "source_url": f"https://pop.culture.gouv.fr/notice/merimee/{pa_reference}",
            "methode_rapprochement": "reference_IA_explicite_dans_notice_PA",
            "fiabilite_code": "forte",
            "distance_coordonnees_m": (
                round(mh_distance, 1) if mh_distance is not None else None
            ),
        }
        site.setdefault("protections_mh", []).append(protection)
        rows.append(
            {
                "site_id": site["site_id"],
                "reference_ia": ia_reference,
                "reference_mh": pa_reference,
                "titre_mh": record.get("TICO"),
                "protection": " | ".join(_values(record.get("PROT"))),
                "date_protection": " | ".join(_values(record.get("DPRO"))),
                "distance_coordonnees_m": (
                    round(mh_distance, 1) if mh_distance is not None else ""
                ),
                "methode": protection["methode_rapprochement"],
                "fiabilite": "forte",
            }
        )
    return rows, pa_to_ia


def reconcile_palissy(
    sites: Sequence[dict[str, Any]],
    palissy: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    pm_by_reference = {
        str(record["REF"]): record
        for record in palissy
        if str(record.get("REF", "")).startswith("PM")
    }
    rows: list[dict[str, Any]] = []
    ambiguities: list[dict[str, Any]] = []
    existing_references = set()
    for site in sites:
        for item in site.get("objets_techniques", []):
            reference = str(item["reference_palissy"])
            existing_references.add(reference)
            record = pm_by_reference.get(reference, {})
            rows.append(
                {
                    "site_id": site["site_id"],
                    "reference_ia": site["dossier_reference"],
                    "reference_palissy": reference,
                    "titre_objet": record.get("TICO") or item.get("nom_principal"),
                    "edifice": record.get("EDIF"),
                    "statut_rapprochement": "a_verifier",
                    "methode": "rapprochement_documentaire_pilote_conserve",
                    "fiabilite": item.get("fiabilite_code", "faible"),
                }
            )

    sites_by_insee: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for site in sites:
        for code in site.get("insee_source", []):
            sites_by_insee[str(code)].append(site)
    for reference, record in pm_by_reference.items():
        if reference in existing_references:
            continue
        candidates = []
        record_text = normalize([record.get("EDIF"), record.get("EMPL"), record.get("TICO")])
        for insee in _values(record.get("INSEE")):
            for site in sites_by_insee.get(insee, []):
                score = token_set_ratio(record_text, _site_text(site))
                if score >= 82:
                    candidates.append((score, site))
        if not candidates:
            continue
        candidates.sort(key=lambda item: (-item[0], item[1]["dossier_reference"]))
        best_score, best_site = candidates[0]
        if len(candidates) > 1 and candidates[1][0] == best_score:
            continue
        ambiguities.append(
            {
                "type": "palissy",
                "reference_source": reference,
                "site_candidat_reference": best_site["dossier_reference"],
                "score_texte": best_score,
                "distance_m": "",
                "motif": "meme_commune_et_similarite_edifice_site",
                "decision": "non_rattache_a_verifier",
            }
        )
    return rows, ambiguities


def _casias_point(record: Mapping[str, Any]) -> list[float] | None:
    try:
        point = [float(record["x_wgs84"]), float(record["y_wgs84"])]
    except (KeyError, TypeError, ValueError):
        return None
    return point if -1.0 <= point[0] <= 1.0 and 48.2 <= point[1] <= 49.1 else None


def reconcile_casias(
    sites: Sequence[dict[str, Any]], records: Sequence[Mapping[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    sites_by_insee: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for site in sites:
        for code in site.get("insee_source", []):
            sites_by_insee[str(code)].append(site)
    confirmed: list[dict[str, Any]] = []
    ambiguities: list[dict[str, Any]] = []
    matched_casias: set[str] = set()
    overlap_candidates: set[str] = set()
    for record in records:
        reference = str(record.get("code_inven") or record.get("code_metie"))
        point = _casias_point(record)
        record_text = normalize([record.get("nom_etabli"), record.get("adresse")])
        candidates = []
        for site in sites_by_insee.get(str(record.get("code_insee")), []):
            site_point = [site["longitude_source"], site["latitude_source"]]
            distance = haversine_metres(point, site_point) if point else None
            score = token_set_ratio(record_text, _site_text(site)) if record_text else 0
            if (distance is not None and distance <= 500) or score >= 72:
                candidates.append((distance, score, site))
        if not candidates:
            continue
        overlap_candidates.add(reference)
        candidates.sort(
            key=lambda item: (
                -(item[1]),
                item[0] if item[0] is not None else float("inf"),
                item[2]["dossier_reference"],
            )
        )
        distance, score, site = candidates[0]
        unique = not (
            len(candidates) > 1
            and candidates[1][1] == score
            and candidates[1][0] == distance
        )
        accepted = unique and (
            (distance is not None and distance <= 100 and score >= 55)
            or (distance is not None and distance <= 50 and score >= 15)
            or score >= 90
        )
        row = {
            "site_id": site["site_id"],
            "reference_ia": site["dossier_reference"],
            "reference_casias": reference,
            "nom_casias": record.get("nom_etabli"),
            "adresse_casias": record.get("adresse"),
            "distance_m": round(distance, 1) if distance is not None else "",
            "score_texte": score,
            "statut": "recoupement_confirme" if accepted else "candidat_a_verifier",
            "usage": "recoupement_uniquement",
        }
        if accepted:
            confirmed.append(row)
            matched_casias.add(reference)
            site.setdefault("recoupements_casias", []).append(
                {
                    "reference_casias": reference,
                    "nom": record.get("nom_etabli"),
                    "source_url": record.get("url_fiche"),
                    "distance_m": row["distance_m"],
                    "methode": "meme_commune_et_concordance_spatiale_ou_textuelle",
                    "fiabilite_code": "moyenne",
                }
            )
        else:
            ambiguities.append(
                {
                    "type": "casias",
                    "reference_source": reference,
                    "site_candidat_reference": site["dossier_reference"],
                    "score_texte": score,
                    "distance_m": row["distance_m"],
                    "motif": "candidat_insuffisant_pour_rattachement_automatique",
                    "decision": "non_rattache_a_verifier",
                }
            )

    expansion = []
    for record in records:
        reference = str(record.get("code_inven") or record.get("code_metie"))
        text = normalize([record.get("nom_etabli"), record.get("adresse")])
        if reference in matched_casias or reference in overlap_candidates:
            continue
        if not any(term in text for term in INDUSTRIAL_TERMS):
            continue
        if any(term in text for term in EXCLUDED_EXPANSION_TERMS):
            continue
        expansion.append(
            {
                "reference_casias": reference,
                "nom": record.get("nom_etabli"),
                "adresse": record.get("adresse"),
                "code_insee": record.get("code_insee"),
                "commune": record.get("nom_commun"),
                "avec_coordonnees": "oui" if _casias_point(record) else "non",
                "statut": "candidat_elargissement_non_integre",
                "motif": "mot_cle_industriel_conservateur",
                "source_url": record.get("url_fiche"),
            }
        )
    return confirmed, ambiguities, expansion


def apply_casias_review(
    sites: Sequence[dict[str, Any]],
    records: Sequence[Mapping[str, Any]],
    confirmed: list[dict[str, Any]],
    ambiguities: list[dict[str, Any]],
    decisions: Mapping[str, Any],
) -> dict[str, int]:
    """Applique la lecture humaine consignée des candidats CASIAS."""
    sets = {
        "confirme_apres_revue": {str(value) for value in decisions["confirmer"]},
        "rejete_apres_revue": {str(value) for value in decisions["rejeter"]},
        "maintenu_ambigu_apres_revue": {
            str(value) for value in decisions["maintenir_ambigu"]
        },
    }
    covered = set().union(*sets.values())
    expected = {str(row["reference_source"]) for row in ambiguities}
    if covered != expected or sum(map(len, sets.values())) != len(covered):
        raise ValueError("les décisions CASIAS ne couvrent pas exactement les ambiguïtés")
    record_by_reference = {
        str(row.get("code_inven") or row.get("code_metie")): row for row in records
    }
    site_by_reference = {str(site["dossier_reference"]): site for site in sites}
    for row in ambiguities:
        reference = str(row["reference_source"])
        decision = next(label for label, values in sets.items() if reference in values)
        row["decision"] = decision
        if decision != "confirme_apres_revue":
            continue
        site = site_by_reference[str(row["site_candidat_reference"])]
        source = record_by_reference[reference]
        confirmed_row = {
            "site_id": site["site_id"],
            "reference_ia": site["dossier_reference"],
            "reference_casias": reference,
            "nom_casias": source.get("nom_etabli"),
            "adresse_casias": source.get("adresse"),
            "distance_m": row["distance_m"],
            "score_texte": row["score_texte"],
            "statut": "recoupement_confirme_apres_revue",
            "usage": "recoupement_uniquement",
        }
        confirmed.append(confirmed_row)
        site.setdefault("recoupements_casias", []).append(
            {
                "reference_casias": reference,
                "nom": source.get("nom_etabli"),
                "source_url": source.get("url_fiche"),
                "distance_m": row["distance_m"],
                "methode": "revue_manuelle_nom_lieu_adresse_activite",
                "fiabilite_code": "moyenne",
            }
        )
    return {label: len(values) for label, values in sets.items()}


def build_locations(sites: Sequence[Mapping[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    transformer = Transformer.from_crs(4326, 2154, always_xy=True)
    locations = []
    errors = []
    duplicate_points: dict[tuple[float, float], list[str]] = defaultdict(list)
    for site in sites:
        try:
            point = [float(site["longitude_source"]), float(site["latitude_source"])]
        except (TypeError, ValueError):
            point = None
        if point is None or not (-1.0 <= point[0] <= 1.0 and 48.2 <= point[1] <= 49.1):
            errors.append(f"{site['dossier_reference']}: coordonnées absentes ou hors Orne")
            location = {
                "site_id": site["site_id"],
                "reference_ia": site["dossier_reference"],
                "statut_localisation_code": "non_localise",
                "precision_geographique_code": None,
                "point_wgs84": None,
                "point_lambert93": None,
                "methode_localisation_code": None,
                "fiabilite_code": "inconnue",
            }
        else:
            x, y = transformer.transform(*point)
            duplicate_points[(round(point[0], 7), round(point[1], 7))].append(
                site["dossier_reference"]
            )
            existing = site.get("localisation_detail") or {}
            precision = (
                existing.get("precision_reference_code")
                if existing.get("geometrie_reference")
                else "point_approximatif"
            )
            location = {
                "site_id": site["site_id"],
                "reference_ia": site["dossier_reference"],
                "statut_localisation_code": "geometrie_approximative",
                "precision_geographique_code": precision or "point_approximatif",
                "point_wgs84": point,
                "point_lambert93": [round(x, 3), round(y, 3)],
                "methode_localisation_code": "coordonnees_source",
                "fiabilite_code": "moyenne",
                "emprise_documentaire_presente": bool(
                    existing.get("emprise_source") if existing else False
                ),
            }
        locations.append(location)
    duplicates = [
        " | ".join(references)
        for references in duplicate_points.values()
        if len(references) > 1
    ]
    return {
        "schema_version": "1.0",
        "generated_at": date.today().isoformat(),
        "source": DEFAULT_CORPUS.as_posix(),
        "locations": locations,
        "counts": {
            "sites": len(locations),
            "localises": sum(row["point_wgs84"] is not None for row in locations),
            "non_localises": sum(row["point_wgs84"] is None for row in locations),
            "points_approximatifs": sum(
                row["precision_geographique_code"] == "point_approximatif"
                for row in locations
            ),
            "coordonnees_dupliquees": len(duplicates),
        },
    }, duplicates


def build_full_enrichment(
    corpus: Mapping[str, Any],
    manifest: Mapping[str, Any],
    decisions: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, list[dict[str, Any]]]]:
    enriched = deepcopy(corpus)
    sites = enriched["sites"]
    merimee = load_culture_records(manifest, "monuments_historiques")
    palissy = load_culture_records(manifest, "pop_palissy")
    casias_path = Path(manifest["sources"]["casias"][0]["data_file"])
    casias = parse_casias(casias_path)

    for site in sites:
        site["protections_mh"] = []
        site["recoupements_casias"] = []
    mh_rows, _pa_to_ia = reconcile_mh(sites, merimee)
    palissy_rows, palissy_ambiguities = reconcile_palissy(sites, palissy)
    casias_rows, casias_ambiguities, expansion = reconcile_casias(sites, casias)
    review_counts = apply_casias_review(
        sites, casias, casias_rows, casias_ambiguities, decisions
    )
    locations, duplicate_points = build_locations(sites)
    ambiguities = [*palissy_ambiguities, *casias_ambiguities]
    ambiguities.extend(
        {
            "type": "localisation",
            "reference_source": "",
            "site_candidat_reference": references,
            "score_texte": "",
            "distance_m": "",
            "motif": "coordonnees_source_identiques",
            "decision": "a_verifier",
        }
        for references in duplicate_points
    )

    enriched["corpus_version"] = "phase8_enrichi_patrimoine_casias_v1"
    enriched["generated_at"] = date.today().isoformat()
    enriched["status"] = "enrichissement_phase8_bloc2"
    enriched["counts"].update(
        {
            "sites_proteges_mh_confirmes": len({row["site_id"] for row in mh_rows}),
            "protections_mh": len(mh_rows),
            "objets_palissy_conserves": len(palissy_rows),
            "sites_recoupes_casias": len({row["site_id"] for row in casias_rows}),
            "recoupements_casias": len(casias_rows),
        }
    )
    summary = {
        "schema_version": "1.0",
        "generated_at": date.today().isoformat(),
        "status": "rapprochements_conservateurs_termines",
        "sources_extraites": manifest["counts"],
        "corpus": {
            "sites": len(sites),
            "sites_localises": locations["counts"]["localises"],
            "sites_non_localises": locations["counts"]["non_localises"],
        },
        "monuments_historiques": {
            "notices_PA_dans_extraction": sum(
                str(row.get("REF", "")).startswith("PA") for row in merimee
            ),
            "protections_confirmees": len(mh_rows),
            "sites_proteges": len({row["site_id"] for row in mh_rows}),
            "protections_avec_points_concordants_a_250_m": sum(
                row["distance_coordonnees_m"] != ""
                and float(row["distance_coordonnees_m"]) <= 250
                for row in mh_rows
            ),
            "regle": "référence IA explicite dans la notice PA",
        },
        "palissy": {
            "notices_PM_dans_extraction": sum(
                str(row.get("REF", "")).startswith("PM") for row in palissy
            ),
            "objets_documentaires_conserves": len(palissy_rows),
            "candidats_supplementaires_non_rattaches": len(palissy_ambiguities),
        },
        "casias": {
            "entrees_examinees": len(casias),
            "recoupements_confirmes": len(casias_rows),
            "sites_recoupes": len({row["site_id"] for row in casias_rows}),
            "candidats_soumis_a_revue": len(casias_ambiguities),
            "ambiguities_restantes": review_counts[
                "maintenu_ambigu_apres_revue"
            ],
            "candidats_elargissement_non_integres": len(expansion),
            "revue_manuelle": review_counts,
        },
        "localisation": locations["counts"],
        "ambiguities_a_verifier": (
            len(palissy_ambiguities)
            + review_counts["maintenu_ambigu_apres_revue"]
            + len(duplicate_points)
        ),
        "principes": [
            "aucun rapprochement seulement communal n'est confirmé",
            "aucune coordonnée CASIAS ne remplace la coordonnée patrimoniale",
            "aucun candidat CASIAS d'élargissement n'est ajouté aux 318 sites",
            "les coordonnées POP restent qualifiées d'approximatives",
        ],
    }
    return enriched, locations, {
        "mh": mh_rows,
        "palissy": palissy_rows,
        "casias": casias_rows,
        "expansion": expansion,
        "ambiguities": ambiguities,
        "summary": [summary],
    }


def write_outputs(
    enriched: Mapping[str, Any],
    locations: Mapping[str, Any],
    outputs: Mapping[str, list[dict[str, Any]]],
    *,
    output_path: Path = DEFAULT_OUTPUT,
    locations_path: Path = DEFAULT_LOCATIONS,
    summary_path: Path = DEFAULT_SUMMARY,
) -> None:
    for path, payload in ((output_path, enriched), (locations_path, locations)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(outputs["summary"][0], ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    _write_csv(
        DEFAULT_MH,
        outputs["mh"],
        (
            "site_id",
            "reference_ia",
            "reference_mh",
            "titre_mh",
            "protection",
            "date_protection",
            "distance_coordonnees_m",
            "methode",
            "fiabilite",
        ),
    )
    _write_csv(
        DEFAULT_PALISSY,
        outputs["palissy"],
        (
            "site_id",
            "reference_ia",
            "reference_palissy",
            "titre_objet",
            "edifice",
            "statut_rapprochement",
            "methode",
            "fiabilite",
        ),
    )
    _write_csv(
        DEFAULT_CASIAS,
        outputs["casias"],
        (
            "site_id",
            "reference_ia",
            "reference_casias",
            "nom_casias",
            "adresse_casias",
            "distance_m",
            "score_texte",
            "statut",
            "usage",
        ),
    )
    _write_csv(
        DEFAULT_EXPANSION,
        outputs["expansion"],
        (
            "reference_casias",
            "nom",
            "adresse",
            "code_insee",
            "commune",
            "avec_coordonnees",
            "statut",
            "motif",
            "source_url",
        ),
    )
    _write_csv(
        DEFAULT_AMBIGUITIES,
        outputs["ambiguities"],
        (
            "type",
            "reference_source",
            "site_candidat_reference",
            "score_texte",
            "distance_m",
            "motif",
            "decision",
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--locations", type=Path, default=DEFAULT_LOCATIONS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--decisions", type=Path, default=DEFAULT_DECISIONS)
    args = parser.parse_args()
    enriched, locations, outputs = build_full_enrichment(
        load_json(args.corpus),
        load_json(args.manifest),
        yaml.safe_load(args.decisions.read_text(encoding="utf-8")),
    )
    write_outputs(
        enriched,
        locations,
        outputs,
        output_path=args.output,
        locations_path=args.locations,
        summary_path=args.summary,
    )
    print(json.dumps(outputs["summary"][0], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
