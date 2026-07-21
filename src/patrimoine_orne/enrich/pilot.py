"""Construit le corpus enrichi des 30 sites pilotes et son rapport de contrôle."""

from __future__ import annotations

import argparse
import json
import uuid
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from patrimoine_orne.classify.sectors import (
    classify_denomination,
    load_classifications,
    load_pop_manifest_sample,
)


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [str(item) for item in value if item not in (None, "")]
    return [str(value)] if str(value).strip() else []


def first(value: Any) -> str | None:
    values = as_list(value)
    return values[0] if values else None


def validate_site_ids(sample: Mapping[str, Any], enrichment: Mapping[str, Any]) -> list[str]:
    references = [str(site["ia_reference"]) for site in sample["sites"]]
    identifiers = enrichment["site_ids"]
    errors: list[str] = []
    if set(references) != set(identifiers):
        errors.append("le registre d'identifiants ne couvre pas exactement les 30 références")
    parsed: list[uuid.UUID] = []
    for reference, value in identifiers.items():
        try:
            identifier = uuid.UUID(str(value))
        except ValueError:
            errors.append(f"UUID invalide pour {reference}")
            continue
        parsed.append(identifier)
        if identifier.version != 4:
            errors.append(f"l'identifiant de {reference} n'est pas un UUID v4")
    if len(parsed) != len(set(parsed)):
        errors.append("des identifiants internes sont dupliqués")
    return errors


def build_activities(
    reference: str,
    record: Mapping[str, Any],
    enrichment: Mapping[str, Any],
    classifications: Mapping[str, Any],
) -> tuple[str, list[dict[str, Any]], list[str]]:
    chronology = enrichment.get("chronologies", {}).get(reference)
    if chronology:
        mode = str(chronology["mode"])
        phases = chronology["phases"]
    else:
        mode = "phase_unique" if len(as_list(record.get("DENO"))) == 1 else "ordre_a_verifier"
        phases = [{"libelle_source": label} for label in as_list(record.get("DENO"))]

    activities: list[dict[str, Any]] = []
    unknown: list[str] = []
    for order, phase in enumerate(phases, start=1):
        label = str(phase["libelle_source"])
        classified = classify_denomination(label, classifications)
        if classified is None:
            unknown.append(label)
            classified = {
                "activite_code": None,
                "secteur_code": None,
                "installation_code": None,
            }
        activities.append(
            {
                "ordre": order,
                "libelle_source": label,
                **classified,
                "debut_texte_source": phase.get("debut"),
                "fin_texte_source": phase.get("fin"),
                "note": phase.get("note"),
                "fiabilite_code": "forte" if phase.get("debut") or phase.get("fin") else "moyenne",
                "source_id": "pop_merimee",
                "reference_source": reference,
            }
        )
    return mode, activities, unknown


def load_palissy_records(manifest_path: Path) -> list[dict[str, Any]]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    data_path = Path(manifest["sources"]["pop_palissy"][0]["data_file"])
    return json.loads(data_path.read_text(encoding="utf-8"))["results"]


def load_mh_records(manifest_path: Path) -> list[dict[str, Any]]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    item = manifest["sources"]["monuments_historiques_data_culture"][0]
    return json.loads(Path(item["data_file"]).read_text(encoding="utf-8"))["results"]


def validate_mh_links(
    confirmed: Mapping[str, str], records: Sequence[Mapping[str, Any]]
) -> list[str]:
    by_reference = {str(record["reference"]): record for record in records}
    errors: list[str] = []
    field = "renvoi_vers_une_notice_de_la_base_merimee_ou_palissy"
    for ia_reference, pa_reference in confirmed.items():
        record = by_reference.get(str(pa_reference))
        if record is None:
            errors.append(f"protection {pa_reference} absente de l'extraction MH")
        elif ia_reference not in as_list(record.get(field)):
            errors.append(f"{pa_reference} ne renvoie pas à {ia_reference}")
    return errors


def build_objects(records: Sequence[Mapping[str, Any]], association: Mapping[str, Any]) -> list[dict[str, Any]]:
    result = []
    for record in sorted(records, key=lambda item: str(item["reference"])):
        ensemble = first(record.get("reference_a_un_ensemble"))
        if ensemble and "/" in ensemble:
            ensemble = ensemble.rsplit("/", 1)[-1]
        result.append(
            {
                "reference_palissy": record["reference"],
                "nom_principal": record.get("titre_editorial") or record.get("denomination"),
                "denomination_source": record.get("denomination"),
                "description": record.get("description") or record.get("historique"),
                "ensemble_reference": ensemble
                or (record["reference"] if record["reference"] == association["ensemble_reference"] else None),
                "site_candidat_reference": association["site_candidat"],
                "type_lien_code": association["type_lien_code"],
                "statut_rapprochement": association["statut"],
                "fiabilite_code": association["fiabilite_code"],
                "source_id": "pop_palissy",
                "source_url": f"https://pop.culture.gouv.fr/notice/palissy/{record['reference']}",
            }
        )
    return result


def build_current_state(reference: str, enrichment: Mapping[str, Any]) -> dict[str, Any]:
    settings = enrichment["situation_actuelle"]
    state = deepcopy(settings["defaut"])
    state.update(settings.get("exceptions", {}).get(reference, {}))
    state["date_verification"] = str(enrichment["date_verification"])
    state["source_id"] = "tourisme_local" if state.get("source_url") else None
    return state


def build_enriched_corpus(
    sample: Mapping[str, Any],
    enrichment: Mapping[str, Any],
    classifications: Mapping[str, Any],
    pop_records: Sequence[Mapping[str, Any]],
    palissy_records: Sequence[Mapping[str, Any]],
    mh_records: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    errors = validate_site_ids(sample, enrichment)
    pop_by_reference = {str(record["REF"]): record for record in pop_records}
    sample_references = [str(site["ia_reference"]) for site in sample["sites"]]
    if set(pop_by_reference) != set(sample_references):
        errors.append("les notices POP archivées ne couvrent pas exactement l'échantillon")

    sites = []
    unknown_activities: list[str] = []
    protection_links = enrichment["rapprochements_mh_confirmes"]
    errors.extend(validate_mh_links(protection_links, mh_records))
    for selected in sample["sites"]:
        reference = str(selected["ia_reference"])
        record = pop_by_reference[reference]
        mode, activities, unknown = build_activities(
            reference, record, enrichment, classifications
        )
        unknown_activities.extend(unknown)
        current_commune = enrichment.get("communes_actuelles", {}).get(reference, {})
        historical_status = {
            "conservation_source": as_list(record.get("ETAT")),
            "destination_source": as_list(record.get("ACTU")),
            "date_enquete_source": first(record.get("DATO")),
            "avertissement": "Observation historique conservée séparément de la situation actuelle.",
        }
        sources = [
            {
                "source_id": "pop_merimee",
                "reference": reference,
                "url": f"https://pop.culture.gouv.fr/notice/merimee/{reference}",
                "role": "notice_principale",
                "fiabilite_code": "forte",
            }
        ]
        current_code = current_commune.get("code_insee") or first(record.get("INSEE"))
        sources.append(
            {
                "source_id": "api_geo",
                "reference": current_code,
                "url": f"https://geo.api.gouv.fr/communes/{current_code}",
                "role": "commune_actuelle",
                "fiabilite_code": "forte",
            }
        )
        if reference in protection_links:
            pa_reference = protection_links[reference]
            sources.append(
                {
                    "source_id": "monuments_historiques_data_culture",
                    "reference": pa_reference,
                    "url": f"https://pop.culture.gouv.fr/notice/merimee/{pa_reference}",
                    "role": "protection_confirmee",
                    "fiabilite_code": "forte",
                }
            )
        current_state = build_current_state(reference, enrichment)
        if current_state.get("source_url"):
            sources.append(
                {
                    "source_id": current_state["source_id"],
                    "reference": None,
                    "url": current_state["source_url"],
                    "role": "situation_actuelle",
                    "fiabilite_code": current_state["fiabilite_code"],
                }
            )
        history = record.get("HIST")
        if history == "$26":
            history = None
        sites.append(
            {
                "site_id": str(enrichment["site_ids"][reference]),
                "reference_ia": reference,
                "nom_principal": first(record.get("TICO")) or selected["titre"],
                "commune_historique_nom": first(record.get("COM")) or selected["commune"],
                "commune_historique_code_insee": first(record.get("INSEE")),
                "commune_actuelle_nom": current_commune.get("nom")
                or first(record.get("COM")),
                "commune_actuelle_code_insee": current_code,
                "lieu_dit": first(record.get("LIEU")),
                "adresse": first(record.get("ADRS")),
                "statut_corpus_code": "rapproche",
                "decision_inclusion_code": "inclus",
                "fiabilite_code": "forte",
                "historique_source": history,
                "mode_chronologique": mode,
                "activites": activities,
                "situation_inventaire_historique": historical_status,
                "situation_actuelle": current_state,
                "protection_mh_reference": protection_links.get(reference),
                "sources": sources,
            }
        )

    if unknown_activities:
        errors.append(f"activités sans classification : {sorted(set(unknown_activities))}")
    objects = build_objects(palissy_records, enrichment["objets_palissy"])
    if len(objects) != 31:
        errors.append("la collection Palissy doit contenir 31 notices")
    recent_current = sum(bool(site["situation_actuelle"].get("source_url")) for site in sites)
    activity_count = sum(len(site["activites"]) for site in sites)
    source_mention_count = sum(len(site["sources"]) for site in sites) + len(objects)
    anomalies = list(enrichment["anomalies_connues"])
    corpus = {
        "schema_version": "0.1",
        "date_verification": str(enrichment["date_verification"]),
        "classifications_version": str(classifications["version"]),
        "sites": sites,
        "objets_techniques": objects,
        "anomalies": anomalies,
    }
    report = {
        "schema_version": "1.0",
        "date_verification": str(enrichment["date_verification"]),
        "checks_passed": not errors,
        "errors": errors,
        "counts": {
            "sites": len(sites),
            "site_ids_unique": len({site["site_id"] for site in sites}),
            "activites_structurees": activity_count,
            "sites_avec_source_recente_situation_actuelle": recent_current,
            "sites_situation_actuelle_inconnue": len(sites) - recent_current,
            "protections_mh_confirmees": len(protection_links),
            "rapprochements_mh_rejetes": 1,
            "objets_palissy_recenses": len(objects),
            "mentions_sources": source_mention_count,
            "anomalies_documentees": len(anomalies),
        },
        "chronology_modes": dict(
            sorted(Counter(site["mode_chronologique"] for site in sites).items())
        ),
        "current_state_reliability": dict(
            sorted(Counter(site["situation_actuelle"]["fiabilite_code"] for site in sites).items())
        ),
    }
    return corpus, report


def write_json(value: Mapping[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", type=Path, default=Path("config/echantillon_pilote.yml"))
    parser.add_argument(
        "--enrichment", type=Path, default=Path("config/enrichissement_pilote.yml")
    )
    parser.add_argument(
        "--classifications", type=Path, default=Path("config/classifications.yml")
    )
    parser.add_argument(
        "--pop-manifest",
        type=Path,
        default=Path("reports/audits/phase5_pop_manifest.json"),
    )
    parser.add_argument(
        "--palissy-manifest",
        type=Path,
        default=Path("reports/audits/phase5_palissy_manifest.json"),
    )
    parser.add_argument(
        "--mh-manifest",
        type=Path,
        default=Path("reports/audits/phase2_extraction_samples_manifest.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/interim/phase5_pilot_enriched.json"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/quality/phase5_enrichissement_pilote.json"),
    )
    args = parser.parse_args()
    corpus, report = build_enriched_corpus(
        load_yaml(args.sample),
        load_yaml(args.enrichment),
        load_classifications(args.classifications),
        load_pop_manifest_sample(args.pop_manifest),
        load_palissy_records(args.palissy_manifest),
        load_mh_records(args.mh_manifest),
    )
    write_json(corpus, args.output)
    write_json(report, args.report)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    if not report["checks_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
