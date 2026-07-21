"""Classifications de chronologie, conservation, usages, accès et protections."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence

from patrimoine_orne.classify.sectors import (
    load_classifications,
    load_pop_manifest_sample,
    normalize_term,
)


DEFAULT_MH_SAMPLE = Path(
    "data/raw/monuments_historiques_data_culture/2026/2026-07-20/"
    "monuments_historiques_data_culture__candidats_industriels__orne__"
    "20260720T072951Z.json"
)


def validate_current_state_classifications(config: Mapping[str, Any]) -> list[str]:
    """Contrôle la cohérence interne des vocabulaires du bloc 2."""
    errors: list[str] = []
    periods = list(config.get("periodes_historiques", {}).items())
    previous_end: int | None = None
    for index, (code, period) in enumerate(periods):
        start, end = period.get("debut_annee"), period.get("fin_annee")
        if index and start != previous_end + 1:
            errors.append(f"période {code}: début non contigu à la période précédente")
        if start is not None and end is not None and start > end:
            errors.append(f"période {code}: bornes inversées")
        previous_end = end
    if periods and periods[0][1].get("debut_annee") is not None:
        errors.append("la première période doit être ouverte vers le passé")
    if periods and periods[-1][1].get("fin_annee") is not None:
        errors.append("la dernière période doit être ouverte vers le présent")

    conservation = config.get("conservation", {})
    for row in config.get("correspondances_conservation_sources", []):
        if row.get("conservation_code") not in conservation:
            errors.append(f"conservation inconnue pour {row.get('terme')!r}")
    forbidden_terms = {
        normalize_term(str(row.get("terme", "")))
        for row in config.get("termes_hors_conservation", [])
    }
    if "desaffecte" not in forbidden_terms:
        errors.append("le terme 'désaffecté' doit être exclu de la conservation")

    usages = config.get("usages_actuels", {})
    if "usage_mixte" in usages:
        errors.append("usage_mixte ne doit pas être une catégorie")
    if not config.get("regles_chronologie_situation_actuelle", {}).get("usages", {}).get(
        "multiplicite_autorisee"
    ):
        errors.append("plusieurs usages actuels doivent pouvoir coexister")

    required_sections = (
        "conservation",
        "usages_actuels",
        "accessibilite",
        "types_protection",
        "portees_protection",
        "statuts_protection",
    )
    for section in required_sections:
        if not config.get(section):
            errors.append(f"vocabulaire vide : {section}")
    return errors


def period_codes_for_interval(
    start_year: int | None,
    end_year: int | None,
    config: Mapping[str, Any],
) -> list[str]:
    """Retourne toutes les périodes que chevauche un intervalle historique."""
    if start_year is None and end_year is None:
        return []
    if start_year is not None and end_year is not None and start_year > end_year:
        raise ValueError("l'année de début doit précéder l'année de fin")
    result: list[str] = []
    for code, period in config["periodes_historiques"].items():
        period_start = period.get("debut_annee")
        period_end = period.get("fin_annee")
        starts_before_end = end_year is None or period_start is None or period_start <= end_year
        ends_after_start = start_year is None or period_end is None or period_end >= start_year
        if starts_before_end and ends_after_start:
            result.append(code)
    return result


def classify_conservation_term(
    value: str, config: Mapping[str, Any]
) -> dict[str, str] | None:
    """Classe un terme exact, ou signale qu'il décrit autre chose que la conservation."""
    normalized = normalize_term(value)
    for row in config.get("termes_hors_conservation", []):
        if normalize_term(str(row["terme"])) == normalized:
            return {"hors_conservation": str(row["nature"])}
    for row in config.get("correspondances_conservation_sources", []):
        if normalize_term(str(row["terme"])) == normalized:
            return {"conservation_code": str(row["conservation_code"])}
    return None


def parse_protection_label(value: str, config: Mapping[str, Any]) -> list[dict[str, str]]:
    """Extrait les mesures MH sans confondre type et portée de protection."""
    normalized = normalize_term(value)
    if "protection totale" in normalized:
        scope = "totale"
    elif "partiellement" in normalized or "protection partielle" in normalized:
        scope = "partielle"
    else:
        scope = "inconnue"

    measures: list[dict[str, str]] = []
    for row in config.get("correspondances_protections_sources", []):
        pattern = normalize_term(str(row["motif"]))
        if re.search(rf"\b{re.escape(pattern)}\b", normalized):
            measure = {
                "type_protection_code": str(row["type_protection_code"]),
                "portee_code": scope,
            }
            if measure not in measures:
                measures.append(measure)
    return measures


def audit_current_state_samples(
    pop_records: Sequence[Mapping[str, Any]],
    mh_records: Sequence[Mapping[str, Any]],
    config: Mapping[str, Any],
) -> dict[str, Any]:
    """Mesure ce que les échantillons peuvent réellement alimenter."""
    pop_states: Counter[str] = Counter()
    pop_classified: Counter[str] = Counter()
    pop_outside: Counter[str] = Counter()
    pop_unknown: Counter[str] = Counter()
    pop_period_filled = 0
    for record in pop_records:
        if record.get("SCLE"):
            pop_period_filled += 1
        values = record.get("ETAT") or []
        if isinstance(values, str):
            values = [values]
        for value in values:
            pop_states[str(value)] += 1
            result = classify_conservation_term(str(value), config)
            if result is None:
                pop_unknown[str(value)] += 1
            elif "conservation_code" in result:
                pop_classified[result["conservation_code"]] += 1
            else:
                pop_outside[result["hors_conservation"]] += 1

    mh_state_terms: Counter[str] = Counter()
    mh_classified: Counter[str] = Counter()
    mh_outside: Counter[str] = Counter()
    mh_unknown: Counter[str] = Counter()
    protection_types: Counter[str] = Counter()
    protection_scopes: Counter[str] = Counter()
    records_with_protection = 0
    records_without_parsed_protection = 0
    destination_filled = 0
    for record in mh_records:
        if record.get("destination_actuelle_de_l_edifice"):
            destination_filled += 1
        values = record.get("etat_de_conservation") or []
        if isinstance(values, str):
            values = [values]
        for value in values:
            mh_state_terms[str(value)] += 1
            result = classify_conservation_term(str(value), config)
            if result is None:
                mh_unknown[str(value)] += 1
            elif "conservation_code" in result:
                mh_classified[result["conservation_code"]] += 1
            else:
                mh_outside[result["hors_conservation"]] += 1

        protection_label = str(
            record.get("date_et_typologie_de_la_protection")
            or record.get("typologie_de_la_protection")
            or ""
        )
        measures = parse_protection_label(protection_label, config)
        if protection_label:
            records_with_protection += 1
        if protection_label and not measures:
            records_without_parsed_protection += 1
        for measure in measures:
            protection_types[measure["type_protection_code"]] += 1
            protection_scopes[measure["portee_code"]] += 1

    return {
        "pop_merimee": {
            "record_count": len(pop_records),
            "period_field_filled": pop_period_filled,
            "state_terms": dict(sorted(pop_states.items())),
            "conservation_codes": dict(sorted(pop_classified.items())),
            "outside_conservation": dict(sorted(pop_outside.items())),
            "unknown_state_terms": dict(sorted(pop_unknown.items())),
        },
        "monuments_historiques": {
            "record_count": len(mh_records),
            "current_destination_filled": destination_filled,
            "state_terms": dict(sorted(mh_state_terms.items())),
            "conservation_codes": dict(sorted(mh_classified.items())),
            "outside_conservation": dict(sorted(mh_outside.items())),
            "unknown_state_terms": dict(sorted(mh_unknown.items())),
            "records_with_protection_label": records_with_protection,
            "records_without_parsed_protection": records_without_parsed_protection,
            "protection_type_counts": dict(sorted(protection_types.items())),
            "protection_scope_counts": dict(sorted(protection_scopes.items())),
        },
    }


def load_mh_sample(path: str | Path = DEFAULT_MH_SAMPLE) -> list[dict[str, Any]]:
    """Charge l'échantillon brut de notices Monuments historiques."""
    content = json.loads(Path(path).read_text(encoding="utf-8"))
    return list(content["results"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Auditer chronologie et situation actuelle")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("reports/audits/phase2_extraction_samples_manifest.json"),
    )
    parser.add_argument("--mh-sample", type=Path, default=DEFAULT_MH_SAMPLE)
    parser.add_argument("--config", type=Path, default=Path("config/classifications.yml"))
    arguments = parser.parse_args()
    config = load_classifications(arguments.config)
    errors = validate_current_state_classifications(config)
    if errors:
        raise ValueError("\n".join(errors))
    report = audit_current_state_samples(
        load_pop_manifest_sample(arguments.manifest),
        load_mh_sample(arguments.mh_sample),
        config,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
