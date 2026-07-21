"""Contrôle reproductible de la composition de l'échantillon pilote."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


IA_PATTERN = re.compile(r"^IA\d{8}$")
PROTECTION_SIGNALS = {"protege_mh_identifie", "sans_protection_mh_identifiee"}
LOCALISATION_DIFFICULTIES = {"facile", "intermediaire", "difficile"}


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _list_counter(sites: list[dict[str, Any]], field: str) -> Counter[str]:
    return Counter(value for site in sites for value in site[field])


def build_composition_report(
    sample: dict[str, Any], classifications: dict[str, Any]
) -> dict[str, Any]:
    sites = sample["sites"]
    method = sample["methode"]
    quotas = method["quotas"]
    references = [site["ia_reference"] for site in sites]
    zones = Counter(site["zone_controle"] for site in sites)
    sectors = _list_counter(sites, "secteurs_preselection")
    periods = _list_counter(sites, "periodes_preselection")
    conservation = Counter(site["conservation_source_signal"] for site in sites)
    protection = Counter(site["protection_signal"] for site in sites)
    localisation = Counter(site["localisation_difficulte"] for site in sites)

    errors: list[str] = []
    if len(sites) != method["taille_cible"]:
        errors.append("taille différente de la cible")
    if len(references) != len(set(references)):
        errors.append("références IA dupliquées")
    if any(not IA_PATTERN.fullmatch(reference) for reference in references):
        errors.append("référence IA mal formée")

    unknown_sectors = set(sectors) - set(classifications["secteurs"])
    unknown_periods = set(periods) - set(classifications["periodes_historiques"])
    unknown_conservation = set(conservation) - set(classifications["conservation"])
    if unknown_sectors:
        errors.append(f"secteurs inconnus : {sorted(unknown_sectors)}")
    if unknown_periods:
        errors.append(f"périodes inconnues : {sorted(unknown_periods)}")
    if unknown_conservation:
        errors.append(f"conservations inconnues : {sorted(unknown_conservation)}")
    if set(protection) - PROTECTION_SIGNALS:
        errors.append("signal de protection inconnu")
    if set(localisation) - LOCALISATION_DIFFICULTIES:
        errors.append("difficulté de localisation inconnue")

    zone_quota = quotas["zones_controle"]
    if len(zones) < zone_quota["minimum_distinct"]:
        errors.append("nombre de zones insuffisant")
    if min(zones.values(), default=0) < zone_quota["minimum_par_zone"]:
        errors.append("une zone est sous le quota minimal")
    if len(sectors) < quotas["secteurs"]["minimum_distinct"]:
        errors.append("diversité sectorielle insuffisante")
    if len(periods) < quotas["periodes"]["minimum_distinct"]:
        errors.append("diversité chronologique insuffisante")
    conservation_quota = quotas["conservation_source"]
    if len(conservation) < conservation_quota["minimum_distinct"]:
        errors.append("diversité des états de conservation insuffisante")
    if not set(conservation_quota["valeurs_requises"]).issubset(conservation):
        errors.append("un état de conservation requis manque")
    protection_quota = quotas["protection"]
    if protection["protege_mh_identifie"] < protection_quota["minimum_proteges_mh_identifies"]:
        errors.append("nombre de sites protégés insuffisant")
    if (
        protection["sans_protection_mh_identifiee"]
        < protection_quota["minimum_sans_protection_mh_identifiee"]
    ):
        errors.append("nombre de sites sans protection identifiée insuffisant")
    localisation_quota = quotas["difficulte_localisation"]
    if localisation["difficile"] < localisation_quota["minimum_difficiles"]:
        errors.append("nombre de localisations difficiles insuffisant")
    easy_or_medium = localisation["facile"] + localisation["intermediaire"]
    if easy_or_medium < localisation_quota["minimum_faciles_ou_intermediaires"]:
        errors.append("nombre de localisations faciles ou intermédiaires insuffisant")

    protected_without_reference = [
        site["ia_reference"]
        for site in sites
        if site["protection_signal"] == "protege_mh_identifie"
        and not site.get("protection_reference")
    ]
    if protected_without_reference:
        errors.append(f"protections sans référence PA : {protected_without_reference}")

    return {
        "sample_version": str(sample["version"]),
        "sample_status": sample["status"],
        "universe_announced_count": sample["univers"]["nombre_dossiers_annonce"],
        "selected_count": len(sites),
        "unique_references": len(set(references)),
        "counts": {
            "zones": dict(sorted(zones.items())),
            "sectors": dict(sorted(sectors.items())),
            "periods": dict(sorted(periods.items())),
            "conservation_source_signals": dict(sorted(conservation.items())),
            "protection_signals": dict(sorted(protection.items())),
            "localisation_difficulty": dict(sorted(localisation.items())),
        },
        "multi_sector_sites": sum(len(site["secteurs_preselection"]) > 1 for site in sites),
        "checks_passed": not errors,
        "errors": errors,
    }


def write_report(report: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", type=Path, default=Path("config/echantillon_pilote.yml"))
    parser.add_argument(
        "--classifications", type=Path, default=Path("config/classifications.yml")
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/quality/phase5_composition_echantillon.json"),
    )
    args = parser.parse_args()
    report = build_composition_report(load_yaml(args.sample), load_yaml(args.classifications))
    write_report(report, args.output)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    if not report["checks_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
