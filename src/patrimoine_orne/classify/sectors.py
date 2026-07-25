"""Application et contrôle des secteurs, activités, installations et énergies."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml

from patrimoine_orne.validate.sample_quality import extract_pop_notice, is_filled


DEFAULT_CLASSIFICATIONS_PATH = Path("config/classifications.yml")


def normalize_term(value: str) -> str:
    """Normalise un libellé de source sans modifier la valeur conservée."""
    decomposed = unicodedata.normalize("NFKD", value)
    without_accents = "".join(char for char in decomposed if not unicodedata.combining(char))
    lowered = without_accents.casefold().replace("’", "'")
    return re.sub(r"\s+", " ", lowered).strip(" ,.;:")


def load_classifications(path: str | Path = DEFAULT_CLASSIFICATIONS_PATH) -> dict[str, Any]:
    """Charge le registre YAML des classifications."""
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _index_by_term(rows: Iterable[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {normalize_term(str(row["terme"])): row for row in rows}


def validate_classifications(config: Mapping[str, Any]) -> list[str]:
    """Retourne les incohérences structurelles du registre de classifications."""
    errors: list[str] = []
    sectors = config.get("secteurs", {})
    activities = config.get("activites_detaillees", {})
    installations = config.get("types_installations", {})
    energies = config.get("energies", {})
    energy_roles = config.get("roles_energies", {})

    if "activite_mixte" in sectors:
        errors.append("activite_mixte ne doit pas être un secteur")

    for activity_code, activity in activities.items():
        if activity.get("secteur_code") not in sectors:
            errors.append(
                f"activité {activity_code}: secteur inconnu {activity.get('secteur_code')!r}"
            )

    seen_terms: set[str] = set()
    for row in config.get("correspondances_sources", []):
        term = normalize_term(str(row.get("terme", "")))
        if not term:
            errors.append("correspondance de source sans terme")
        elif term in seen_terms:
            errors.append(f"terme source dupliqué : {row['terme']!r}")
        seen_terms.add(term)
        if row.get("activite_code") not in activities:
            errors.append(f"{row.get('terme')!r}: activité inconnue")
        if row.get("installation_code") not in installations:
            errors.append(f"{row.get('terme')!r}: installation inconnue")

    for row in config.get("termes_hors_activite", []):
        term = normalize_term(str(row.get("terme", "")))
        if not term:
            errors.append("terme hors activité sans libellé")
        elif term in seen_terms:
            errors.append(f"terme présent comme activité et hors activité : {row['terme']!r}")
        seen_terms.add(term)
        if not row.get("nature"):
            errors.append(f"{row.get('terme')!r}: nature hors activité absente")

    for row in config.get("correspondances_energies_sources", []):
        energy_code = row.get("energie_code")
        role_code = row.get("role_energie_code")
        if bool(energy_code) == bool(role_code):
            errors.append(f"{row.get('terme')!r}: énergie ou rôle attendu, exclusivement")
        if energy_code and energy_code not in energies:
            errors.append(f"{row.get('terme')!r}: énergie inconnue")
        if role_code and role_code not in energy_roles:
            errors.append(f"{row.get('terme')!r}: rôle énergétique inconnu")

    rules = config.get("regles_affectation_secteurs", {})
    if rules.get("unite_classee") != "activite":
        errors.append("l'unité classée doit être l'activité")
    if not rules.get("activite_mixte_interdite"):
        errors.append("le secteur activite_mixte doit être interdit")
    return errors


def classify_denomination(
    value: str, config: Mapping[str, Any]
) -> dict[str, str] | None:
    """Classe une dénomination exacte, sans inférence par mot-clé silencieuse."""
    row = _index_by_term(config.get("correspondances_sources", [])).get(
        normalize_term(value)
    )
    if row is None:
        return None
    activity_code = str(row["activite_code"])
    return {
        "activite_code": activity_code,
        "secteur_code": str(config["activites_detaillees"][activity_code]["secteur_code"]),
        "installation_code": str(row["installation_code"]),
    }


def classify_non_activity_term(
    value: str, config: Mapping[str, Any]
) -> dict[str, str] | None:
    """Reconnaît une dénomination patrimoniale qui ne décrit pas une production."""
    row = _index_by_term(config.get("termes_hors_activite", [])).get(
        normalize_term(value)
    )
    if row is None:
        return None
    return {"nature": str(row["nature"])}


def classify_energy_terms(
    values: Iterable[str], config: Mapping[str, Any]
) -> dict[str, list[str]]:
    """Sépare énergies, rôles, équipements et termes encore inconnus."""
    energy_index = _index_by_term(config.get("correspondances_energies_sources", []))
    excluded_index = _index_by_term(config.get("termes_hors_energie", []))
    result: dict[str, list[str]] = {
        "energies": [],
        "roles": [],
        "hors_energie": [],
        "inconnus": [],
    }
    for value in values:
        normalized = normalize_term(value)
        row = energy_index.get(normalized)
        if row and row.get("energie_code"):
            result["energies"].append(str(row["energie_code"]))
        elif row and row.get("role_energie_code"):
            result["roles"].append(str(row["role_energie_code"]))
        elif normalized in excluded_index:
            result["hors_energie"].append(str(excluded_index[normalized]["nature"]))
        else:
            result["inconnus"].append(value)
    return result


def _as_strings(value: Any) -> list[str]:
    if not is_filled(value):
        return []
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [str(item) for item in value if is_filled(item)]
    return [str(value)]


def classify_pop_records(
    records: Sequence[Mapping[str, Any]], config: Mapping[str, Any]
) -> dict[str, Any]:
    """Mesure la couverture des vocabulaires sur des notices POP structurées."""
    denomination_count = 0
    classified_count = 0
    outside_activity_count = 0
    unknown_terms: Counter[str] = Counter()
    outside_activity_terms: Counter[str] = Counter()
    activity_counts: Counter[str] = Counter()
    sector_counts: Counter[str] = Counter()
    installation_counts: Counter[str] = Counter()
    multi_activity_references: list[str] = []
    multi_sector_references: list[str] = []
    energy_counts: Counter[str] = Counter()
    energy_role_counts: Counter[str] = Counter()
    outside_energy_counts: Counter[str] = Counter()
    unknown_energy_terms: Counter[str] = Counter()

    for record in records:
        reference = str(record.get("REF", ""))
        classifications = []
        denominations = _as_strings(record.get("DENO"))
        denomination_count += len(denominations)
        for denomination in denominations:
            classification = classify_denomination(denomination, config)
            if classification is None:
                outside = classify_non_activity_term(denomination, config)
                if outside is None:
                    unknown_terms[denomination] += 1
                else:
                    outside_activity_count += 1
                    outside_activity_terms[denomination] += 1
                continue
            classified_count += 1
            classifications.append(classification)
            activity_counts[classification["activite_code"]] += 1
            sector_counts[classification["secteur_code"]] += 1
            installation_counts[classification["installation_code"]] += 1
        if len(classifications) > 1:
            multi_activity_references.append(reference)
        if len({item["secteur_code"] for item in classifications}) > 1:
            multi_sector_references.append(reference)

        energy_result = classify_energy_terms(_as_strings(record.get("ENER")), config)
        energy_counts.update(energy_result["energies"])
        energy_role_counts.update(energy_result["roles"])
        outside_energy_counts.update(energy_result["hors_energie"])
        unknown_energy_terms.update(energy_result["inconnus"])

    coverage = round(classified_count * 100 / denomination_count, 1) if denomination_count else 0.0
    resolved = classified_count + outside_activity_count
    resolved_coverage = round(resolved * 100 / denomination_count, 1) if denomination_count else 0.0
    return {
        "record_count": len(records),
        "denominations": {
            "total": denomination_count,
            "classified": classified_count,
            "coverage_percent": coverage,
            "outside_activity": outside_activity_count,
            "outside_activity_terms": dict(sorted(outside_activity_terms.items())),
            "resolved": resolved,
            "resolved_percent": resolved_coverage,
            "unknown_terms": dict(sorted(unknown_terms.items())),
        },
        "activity_counts": dict(sorted(activity_counts.items())),
        "sector_counts": dict(sorted(sector_counts.items())),
        "installation_counts": dict(sorted(installation_counts.items())),
        "multi_activity_references": sorted(multi_activity_references),
        "multi_sector_references": sorted(multi_sector_references),
        "energies": {
            "energy_counts": dict(sorted(energy_counts.items())),
            "role_counts": dict(sorted(energy_role_counts.items())),
            "outside_energy_counts": dict(sorted(outside_energy_counts.items())),
            "unknown_terms": dict(sorted(unknown_energy_terms.items())),
        },
    }


def load_pop_manifest_sample(manifest_path: str | Path) -> list[dict[str, Any]]:
    """Recharge les notices POP référencées par le manifeste validé de phase 2."""
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    records = []
    for item in manifest["sources"]["pop_merimee"]:
        path = Path(item["data_file"])
        reference = item["observations"]["reference"]
        records.append(extract_pop_notice(path.read_text(encoding="utf-8"), reference))
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description="Tester les secteurs sur l'échantillon POP")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("reports/audits/phase2_extraction_samples_manifest.json"),
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CLASSIFICATIONS_PATH)
    arguments = parser.parse_args()
    config = load_classifications(arguments.config)
    errors = validate_classifications(config)
    if errors:
        raise ValueError("\n".join(errors))
    report = classify_pop_records(load_pop_manifest_sample(arguments.manifest), config)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
