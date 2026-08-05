"""Réunit les 30 pilotes et les 50 dossiers du lot 1 dans un format commun."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import unicodedata
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from patrimoine_orne.classify.sectors import (
    classify_denomination,
    classify_non_activity_term,
    load_classifications,
    load_pop_manifest_sample,
)
from patrimoine_orne.enrich.pilot import source_periods
from patrimoine_orne.extract.corpus import load_lot_records


DEFAULT_PILOT_CORPUS = Path("data/processed/corpus_pilote_socle_v1.json")
DEFAULT_PILOT_MANIFEST = Path("reports/audits/phase5_pop_manifest.json")
DEFAULT_LOT_MANIFEST = Path("reports/audits/phase8_lot1_pop_manifest.json")
DEFAULT_LOT_CONFIG = Path("config/phase8_lot1.yml")
DEFAULT_CORRECTIONS = Path("data/manual/corrections_textes_sources.yml")
DEFAULT_OUTPUT = Path("data/interim/phase8_corpus_80.json")
DEFAULT_SUMMARY = Path("reports/quality/phase8_corpus_80_resume.json")
DEFAULT_CSV = Path("reports/quality/phase8_corpus_80.csv")
DEFAULT_MATCHES = Path("reports/quality/phase8_corpus_80_rapprochements.csv")


def corrections_historiques(
    chemin: Path = DEFAULT_CORRECTIONS,
) -> dict[str, str]:
    """Textes sources repris à la main, avec leur provenance documentée.

    Le parseur HTML de la phase 5 a renvoyé « $26 » à la place de deux
    historiques. Les archives JSON de la même campagne contiennent le texte
    complet : on le reprend, on ne l'écrit pas.
    """
    if not chemin.exists():
        return {}
    donnees = yaml.safe_load(chemin.read_text(encoding="utf-8")) or {}
    return {
        reference: entree["texte"]
        for reference, entree in (donnees.get("historiques") or {}).items()
    }


def _as_list(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [str(item) for item in value if item not in (None, "")]
    return [str(value)]


def _normalise(value: Any) -> str:
    decomposed = unicodedata.normalize("NFKD", str(value or "").casefold())
    plain = "".join(char for char in decomposed if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", " ", plain).strip()


def _first(values: Sequence[str]) -> str | None:
    return values[0] if values else None


def _source_point(notice: Mapping[str, Any]) -> tuple[float, float] | None:
    point = notice.get("POP_COORDONNEES")
    if not isinstance(point, Mapping):
        return None
    try:
        lon, lat = float(point.get("lon")), float(point.get("lat"))
    except (TypeError, ValueError):
        return None
    if lon == 0 or lat == 0 or not (-2 <= lon <= 2 and 47 <= lat <= 50):
        return None
    return lon, lat


def _pilot_point(site: Mapping[str, Any], notice: Mapping[str, Any]) -> tuple[float, float] | None:
    reference = site.get("localisation", {}).get("geometrie_reference", {})
    point = reference.get("point_wgs84")
    if isinstance(point, Sequence) and len(point) == 2:
        return float(point[0]), float(point[1])
    return _source_point(notice)


def _common_activity(
    *,
    order: int,
    source_label: str,
    activity_code: str,
    sector_code: str,
    installation_code: str,
    reference: str,
    source_centuries: Sequence[str],
    source_period_codes: Sequence[str],
) -> dict[str, Any]:
    return {
        "ordre": order,
        "libelle_source": source_label,
        "activite_code": activity_code,
        "secteur_code": sector_code,
        "installation_code": installation_code,
        "debut_min": None,
        "debut_max": None,
        "debut_precision_code": None,
        "debut_texte_source": None,
        "fin_min": None,
        "fin_max": None,
        "fin_precision_code": None,
        "fin_texte_source": None,
        "periodes_codes": [],
        "periodes_libelles": [],
        "periode_methode_code": None,
        "siecles_source_site": list(source_centuries),
        "periodes_source_site_codes": list(source_period_codes),
        "fiabilite_code": "moyenne",
        "source_id": "pop_merimee",
        "reference_source": reference,
        "note": "Chronologie détaillée non encore structurée pour ce dossier.",
    }


def _default_current_state() -> dict[str, Any]:
    return {
        "accessibilite_code": "inconnu",
        "conservation_code": "inconnu",
        "date_verification": None,
        "fiabilite_code": "faible",
        "methode_verification_code": "non_verifie_phase8",
        "note": "Situation actuelle non encore documentée pour ce dossier.",
        "source_id": None,
        "usages": ["inconnu"],
    }


def project_pilot(
    site: Mapping[str, Any],
    notice: Mapping[str, Any],
    *,
    raw_path: str,
    objects: Sequence[Mapping[str, Any]],
    classifications_version: str,
) -> dict[str, Any]:
    reference = str(site["reference_ia"])
    point = _pilot_point(site, notice)
    activities = []
    for activity in site.get("activites", []):
        common = dict(activity)
        common.setdefault("periodes_libelles", [])
        common.setdefault(
            "periodes_source_site_codes", list(site.get("periodes_source_codes", []))
        )
        activities.append(common)
    return {
        "dossier_id": reference,
        "dossier_reference": reference,
        "origine": "pilote_30",
        "statut_traitement": "enrichi_socle_v1",
        "statut_site": "site_pilote_valide",
        "site_id": site.get("site_id"),
        "nombre_sites_provisoire": 1,
        "titre_source": notice.get("TICO") or site.get("nom_principal"),
        "nom_principal": site.get("nom_principal"),
        "communes_source": _as_list(notice.get("COM")),
        "insee_source": _as_list(notice.get("INSEE")),
        "adresses_source": _as_list(notice.get("ADRS")),
        "lieux_dits_source": _as_list(notice.get("LIEU")),
        "denominations_source": _as_list(notice.get("DENO")),
        "siecles_source": _as_list(notice.get("SCLE")),
        "historique_source": corrections_historiques().get(
            reference, notice.get("HIST") or site.get("historique_source")
        ),
        "description_source": notice.get("DESC"),
        "dossier_url": notice.get("DOSURL"),
        "classifications_version": classifications_version,
        "activites": activities,
        "secteurs_codes": sorted({activity["secteur_code"] for activity in activities}),
        "installations_codes": sorted(
            {activity["installation_code"] for activity in activities}
        ),
        "periodes_activite_codes": list(site.get("periodes_activite_codes", [])),
        "periodes_source_codes": list(site.get("periodes_source_codes", [])),
        "situation_actuelle": site.get("situation_actuelle") or _default_current_state(),
        "localisation_statut_code": site.get("localisation", {}).get(
            "statut_localisation_code"
        ),
        "precision_geographique_code": site.get("localisation", {})
        .get("geometrie_reference", {})
        .get("precision_geographique_code"),
        "longitude_source": point[0] if point else None,
        "latitude_source": point[1] if point else None,
        "localisation_detail": site.get("localisation"),
        "contexte_territorial": site.get("contexte_territorial"),
        "protection_mh_reference": site.get("protection_mh_reference"),
        "objets_techniques": [dict(item) for item in objects],
        "composants_non_productifs_source": [],
        "sources": list(site.get("sources", [])),
        "notice_brute": raw_path,
        "decision_inclusion_code": site.get("decision_inclusion_code"),
        "decision_rapprochement": "aucun_rapprochement_requis_a_ce_stade",
    }


def project_lot1(
    notice: Mapping[str, Any],
    *,
    raw_path: str,
    classifications: Mapping[str, Any],
    origin: str = "phase8_lot1_50",
    treatment_status: str = "structure_classee_a_enrichir",
    site_status: str = "site_provisoire_lot1_valide",
) -> dict[str, Any]:
    reference = str(notice["REF"])
    source_centuries = _as_list(notice.get("SCLE"))
    _, source_period_codes = source_periods(source_centuries, classifications)
    activities = []
    non_productive_components = []
    for order, source_label in enumerate(_as_list(notice.get("DENO")), start=1):
        classified = classify_denomination(source_label, classifications)
        if classified is None:
            outside = classify_non_activity_term(source_label, classifications)
            if outside is None:
                raise ValueError(
                    f"dénomination non classée pour {reference}: {source_label!r}"
                )
            non_productive_components.append(
                {"libelle_source": source_label, "nature": outside["nature"]}
            )
            continue
        activities.append(
            _common_activity(
                order=order,
                source_label=source_label,
                activity_code=classified["activite_code"],
                sector_code=classified["secteur_code"],
                installation_code=classified["installation_code"],
                reference=reference,
                source_centuries=source_centuries,
                source_period_codes=source_period_codes,
            )
        )
    point = _source_point(notice)
    return {
        "dossier_id": reference,
        "dossier_reference": reference,
        "origine": origin,
        "statut_traitement": treatment_status,
        "statut_site": site_status,
        "site_id": None,
        "nombre_sites_provisoire": 1,
        "titre_source": notice.get("TICO"),
        "nom_principal": notice.get("TICO"),
        "communes_source": _as_list(notice.get("COM")),
        "insee_source": _as_list(notice.get("INSEE")),
        "adresses_source": _as_list(notice.get("ADRS")),
        "lieux_dits_source": _as_list(notice.get("LIEU")),
        "denominations_source": _as_list(notice.get("DENO")),
        "siecles_source": source_centuries,
        "historique_source": notice.get("HIST"),
        "description_source": notice.get("DESC"),
        "dossier_url": notice.get("DOSURL"),
        "classifications_version": str(classifications["version"]),
        "activites": activities,
        "secteurs_codes": sorted({activity["secteur_code"] for activity in activities}),
        "installations_codes": sorted(
            {activity["installation_code"] for activity in activities}
        ),
        "periodes_activite_codes": [],
        "periodes_source_codes": source_period_codes,
        "situation_actuelle": _default_current_state(),
        "localisation_statut_code": "source_non_controlee" if point else "non_localise",
        "precision_geographique_code": None,
        "longitude_source": point[0] if point else None,
        "latitude_source": point[1] if point else None,
        "localisation_detail": None,
        "contexte_territorial": None,
        "protection_mh_reference": None,
        "objets_techniques": [],
        "composants_non_productifs_source": non_productive_components,
        "sources": [
            {
                "fiabilite_code": "forte",
                "reference": reference,
                "role": "notice_principale",
                "source_id": "pop_merimee",
                "url": f"https://pop.culture.gouv.fr/notice/merimee/{reference}",
            }
        ],
        "notice_brute": raw_path,
        "decision_inclusion_code": "inclus_provisoirement",
        "decision_rapprochement": "aucun_rapprochement_requis_a_ce_stade",
    }


def _distance_m(first: tuple[float, float], second: tuple[float, float]) -> float:
    mean_latitude = math.radians((first[1] + second[1]) / 2)
    dx = (first[0] - second[0]) * 111_320 * math.cos(mean_latitude)
    dy = (first[1] - second[1]) * 110_540
    return math.hypot(dx, dy)


def find_match_candidates(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Signale des indices de même emprise sans prendre de décision."""
    candidates: dict[tuple[str, str], dict[str, Any]] = {}
    for index, first in enumerate(records):
        for second in records[index + 1 :]:
            reasons = []
            first_insee = set(first["insee_source"])
            second_insee = set(second["insee_source"])
            same_insee = bool(first_insee & second_insee)
            first_address = _normalise(_first(first["adresses_source"]))
            second_address = _normalise(_first(second["adresses_source"]))
            first_place = _normalise(_first(first["lieux_dits_source"]))
            second_place = _normalise(_first(second["lieux_dits_source"]))
            if first.get("dossier_url") and first.get("dossier_url") == second.get("dossier_url"):
                reasons.append("meme_url_dossier")
            if same_insee and first_address and first_address == second_address:
                reasons.append("meme_adresse_normalisee")
            if same_insee and first_place and first_place == second_place:
                reasons.append("meme_lieu_dit_normalise")
            first_point = (
                (first["longitude_source"], first["latitude_source"])
                if first.get("longitude_source") is not None
                and first.get("latitude_source") is not None
                else None
            )
            second_point = (
                (second["longitude_source"], second["latitude_source"])
                if second.get("longitude_source") is not None
                and second.get("latitude_source") is not None
                else None
            )
            distance = None
            if first_point and second_point:
                distance = _distance_m(first_point, second_point)
                if distance <= 50:
                    reasons.append("points_sources_a_moins_de_50_m")
            if reasons:
                key = tuple(sorted((first["dossier_reference"], second["dossier_reference"])))
                candidates[key] = {
                    "reference_1": key[0],
                    "reference_2": key[1],
                    "origines": " | ".join(sorted({first["origine"], second["origine"]})),
                    "motifs": " | ".join(reasons),
                    "distance_m": round(distance, 1) if distance is not None else None,
                    "decision": "a_verifier",
                }
    return [candidates[key] for key in sorted(candidates)]


def _manifest_paths(manifest: Mapping[str, Any]) -> dict[str, str]:
    return {
        str(row["observations"]["reference"]): str(row["data_file"])
        for row in manifest["sources"]["pop_merimee"]
    }


def build_common_corpus(
    pilot_corpus: Mapping[str, Any],
    pilot_notices: Sequence[Mapping[str, Any]],
    lot_records: Sequence[Mapping[str, Any]],
    *,
    pilot_raw_paths: Mapping[str, str],
    lot_raw_paths: Mapping[str, str],
    lot_references: Sequence[str],
    classifications: Mapping[str, Any],
) -> dict[str, Any]:
    pilot_sites = {str(site["reference_ia"]): site for site in pilot_corpus["sites"]}
    pilot_notice_map = {str(notice["REF"]): notice for notice in pilot_notices}
    lot_map = {str(notice["REF"]): notice for notice in lot_records}
    if set(pilot_sites) != set(pilot_notice_map) or set(pilot_sites) != set(pilot_raw_paths):
        raise ValueError("les références du pilote ne concordent pas")
    if set(lot_map) != set(lot_references) or set(lot_map) != set(lot_raw_paths):
        raise ValueError("les références du lot 1 ne concordent pas")
    if set(pilot_sites) & set(lot_map):
        raise ValueError("une référence IA appartient aux deux ensembles")

    objects_by_reference: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for item in pilot_corpus.get("objets_techniques", []):
        objects_by_reference[str(item["site_candidat_reference"])].append(item)

    records = [
        project_pilot(
            pilot_sites[reference],
            pilot_notice_map[reference],
            raw_path=pilot_raw_paths[reference],
            objects=objects_by_reference.get(reference, []),
            classifications_version=str(classifications["version"]),
        )
        for reference in sorted(pilot_sites)
    ]
    records.extend(
        project_lot1(
            lot_map[reference],
            raw_path=lot_raw_paths[reference],
            classifications=classifications,
        )
        for reference in sorted(lot_map)
    )
    matches = find_match_candidates(records)
    matched_references = {
        reference
        for match in matches
        for reference in (match["reference_1"], match["reference_2"])
    }
    for record in records:
        if record["dossier_reference"] in matched_references:
            record["decision_rapprochement"] = "candidat_a_verifier"

    references = [record["dossier_reference"] for record in records]
    urls = [record["dossier_url"] for record in records if record.get("dossier_url")]
    if len(references) != 80 or len(set(references)) != 80:
        raise ValueError("le corpus commun doit contenir 80 références IA uniques")
    if len(urls) != len(set(urls)):
        raise ValueError("deux dossiers partagent la même URL source")
    return {
        "schema_version": "1.0",
        "corpus_version": "phase8_80_dossiers_v1",
        "generated_at": date.today().isoformat(),
        "status": "intermediaire_non_canonique",
        "classifications_version": str(classifications["version"]),
        "counts": {
            "pilot": len(pilot_sites),
            "lot1": len(lot_map),
            "dossiers": len(records),
            "references_uniques": len(set(references)),
            "sites_ids_attribues": sum(record["site_id"] is not None for record in records),
            "sites_provisoires": sum(record["nombre_sites_provisoire"] for record in records),
            "activites": sum(len(record["activites"]) for record in records),
            "rapprochements_a_verifier": len(matches),
        },
        "canonical_site_count": None,
        "canonical_count_status": "inconnu_avant_traitement_des_319_dossiers",
        "rapprochements_candidats": matches,
        "anomalies_pilote_conservees": list(pilot_corpus.get("anomalies", [])),
        "dossiers": records,
    }


def flat_rows(corpus: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for record in corpus["dossiers"]:
        rows.append(
            {
                "dossier_reference": record["dossier_reference"],
                "origine": record["origine"],
                "statut_traitement": record["statut_traitement"],
                "statut_site": record["statut_site"],
                "site_id": record["site_id"],
                "titre_source": record["titre_source"],
                "communes_source": " | ".join(record["communes_source"]),
                "insee_source": " | ".join(record["insee_source"]),
                "adresses_source": " | ".join(record["adresses_source"]),
                "lieux_dits_source": " | ".join(record["lieux_dits_source"]),
                "denominations_source": " | ".join(record["denominations_source"]),
                "activites_codes": " | ".join(
                    activity["activite_code"] for activity in record["activites"]
                ),
                "secteurs_codes": " | ".join(record["secteurs_codes"]),
                "installations_codes": " | ".join(record["installations_codes"]),
                "periodes_activite_codes": " | ".join(
                    record["periodes_activite_codes"]
                ),
                "periodes_source_codes": " | ".join(record["periodes_source_codes"]),
                "localisation_statut_code": record["localisation_statut_code"],
                "longitude_source": record["longitude_source"],
                "latitude_source": record["latitude_source"],
                "decision_rapprochement": record["decision_rapprochement"],
                "dossier_url": record["dossier_url"],
            }
        )
    return rows


def build_summary(corpus: Mapping[str, Any]) -> dict[str, Any]:
    records = corpus["dossiers"]
    record_shapes = {tuple(sorted(row)) for row in records}
    activity_shapes = {
        tuple(sorted(activity)) for row in records for activity in row["activites"]
    }
    return {
        "schema_version": "1.0",
        "generated_at": corpus["generated_at"],
        "corpus_version": corpus["corpus_version"],
        "counts": corpus["counts"],
        "checks": {
            "expected_80_dossiers": len(records) == 80,
            "unique_references": len({row["dossier_reference"] for row in records}) == 80,
            "pilot_30": sum(row["origine"] == "pilote_30" for row in records) == 30,
            "lot1_50": sum(row["origine"] == "phase8_lot1_50" for row in records) == 50,
            "all_have_source": all(row["sources"] for row in records),
            "all_have_activities": all(row["activites"] for row in records),
            "all_classified": all(
                activity.get("activite_code") and activity.get("secteur_code")
                for row in records
                for activity in row["activites"]
            ),
            "uniform_record_structure": len(record_shapes) == 1,
            "uniform_activity_structure": len(activity_shapes) == 1,
            "no_duplicate_dossier_url": len(
                {row["dossier_url"] for row in records if row.get("dossier_url")}
            )
            == sum(bool(row.get("dossier_url")) for row in records),
        },
        "differences_assumees": {
            "pilot": "données enrichies, localisées et dotées d'un site_id",
            "lot1": "données structurées et classées, enrichissement encore à faire",
            "site_id_null_count": sum(row["site_id"] is None for row in records),
        },
        "canonical_site_count": None,
        "next_step": "traiter_les_239_dossiers_restants",
    }


def write_outputs(
    corpus: Mapping[str, Any],
    *,
    output_path: Path,
    summary_path: Path,
    csv_path: Path,
    matches_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(corpus, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    summary = build_summary(corpus)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    rows = flat_rows(corpus)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    matches_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "reference_1",
        "reference_2",
        "origines",
        "motifs",
        "distance_m",
        "decision",
    ]
    with matches_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(corpus["rapprochements_candidats"])


def load_and_build(args: argparse.Namespace) -> dict[str, Any]:
    pilot_corpus = json.loads(args.pilot_corpus.read_text(encoding="utf-8"))
    pilot_manifest = json.loads(args.pilot_manifest.read_text(encoding="utf-8"))
    lot_manifest = json.loads(args.lot_manifest.read_text(encoding="utf-8"))
    lot_config = yaml.safe_load(args.lot_config.read_text(encoding="utf-8"))
    classifications = load_classifications(args.classifications)
    corpus = build_common_corpus(
        pilot_corpus,
        load_pop_manifest_sample(args.pilot_manifest),
        load_lot_records(lot_manifest),
        pilot_raw_paths=_manifest_paths(pilot_manifest),
        lot_raw_paths=_manifest_paths(lot_manifest),
        lot_references=lot_config["references"],
        classifications=classifications,
    )
    write_outputs(
        corpus,
        output_path=args.output,
        summary_path=args.summary,
        csv_path=args.csv,
        matches_path=args.matches,
    )
    return build_summary(corpus)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot-corpus", type=Path, default=DEFAULT_PILOT_CORPUS)
    parser.add_argument("--pilot-manifest", type=Path, default=DEFAULT_PILOT_MANIFEST)
    parser.add_argument("--lot-manifest", type=Path, default=DEFAULT_LOT_MANIFEST)
    parser.add_argument("--lot-config", type=Path, default=DEFAULT_LOT_CONFIG)
    parser.add_argument("--classifications", type=Path, default=Path("config/classifications.yml"))
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--matches", type=Path, default=DEFAULT_MATCHES)
    args = parser.parse_args()
    print(json.dumps(load_and_build(args), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
