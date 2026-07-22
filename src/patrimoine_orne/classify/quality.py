"""Règles de précision géographique, fiabilité et reproductibilité."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from patrimoine_orne.classify.current_state import (
    audit_current_state_samples,
    load_mh_sample,
    validate_current_state_classifications,
)
from patrimoine_orne.classify.sectors import (
    classify_pop_records,
    load_classifications,
    load_pop_manifest_sample,
    validate_classifications,
)


PRECISION_BY_EVIDENCE = {
    ("emprise_site", True): "emprise_site_verifiee",
    ("parcelle", True): "parcelle_verifiee",
    ("batiment", True): "batiment_verifie",
    ("point_site", True): "point_site_verifie",
    ("adresse", False): "point_adresse",
    ("point_approximatif", False): "point_approximatif",
    ("zone_documentaire", False): "zone_documentaire",
}

PUBLISHED_VOCABULARIES = (
    "secteurs",
    "activites_detaillees",
    "types_installations",
    "energies",
    "roles_energies",
    "periodes_historiques",
    "methodes_periodes",
    "conservation",
    "usages_actuels",
    "accessibilite",
    "types_protection",
    "portees_protection",
    "statuts_protection",
    "statuts_protection_site_calcules",
    "precision_geographique",
    "statuts_localisation",
    "methodes_localisation",
    "fiabilite",
)


def validate_quality_classifications(config: Mapping[str, Any]) -> list[str]:
    """Contrôle les vocabulaires et règles du troisième bloc de la phase 4."""
    errors: list[str] = []
    precision = config.get("precision_geographique", {})
    reliability = config.get("fiabilite", {})
    location_statuses = config.get("statuts_localisation", {})
    methods = config.get("methodes_localisation", {})
    rules = config.get("regles_qualite", {})

    required_precision = set(PRECISION_BY_EVIDENCE.values())
    missing_precision = required_precision - set(precision)
    if missing_precision:
        errors.append(f"précisions absentes : {sorted(missing_precision)}")
    for forbidden in ("centre_commune", "non_localise"):
        if forbidden in precision:
            errors.append(f"{forbidden} est un statut, pas une précision géographique")
    orders = [item.get("ordre") for item in precision.values()]
    if any(order is None for order in orders) or len(orders) != len(set(orders)):
        errors.append("les niveaux de précision doivent avoir un ordre unique")

    for status_code, status in location_statuses.items():
        for precision_code in status.get("precisions", []):
            if precision_code not in precision:
                errors.append(
                    f"statut {status_code}: précision inconnue {precision_code!r}"
                )
    if location_statuses.get("commune_seule", {}).get("geometrie_site_autorisee") is not False:
        errors.append("commune_seule ne doit pas autoriser une géométrie de site")
    if "autre_methode" not in methods:
        errors.append("la méthode autre doit être explicite et documentable")

    if set(reliability) != {"forte", "moyenne", "faible"}:
        errors.append("les niveaux de fiabilité doivent être forte, moyenne et faible")
    if "a_verifier" in reliability:
        errors.append("a_verifier est un statut de travail, pas une fiabilité")
    reliability_orders = [item.get("ordre") for item in reliability.values()]
    if len(reliability_orders) != len(set(reliability_orders)):
        errors.append("les niveaux de fiabilité doivent avoir un ordre unique")

    generic_other = rules.get("autre", {})
    if generic_other.get("emploi") != "valeur_positivement_documentee_absente_du_vocabulaire":
        errors.append("la règle d'emploi de 'autre' est absente ou incorrecte")
    if not {"libelle_source_conserve", "justification_documentee", "validation_humaine"}.issubset(
        set(generic_other.get("conditions_obligatoires", []))
    ):
        errors.append("'autre' doit conserver la source, la justification et la validation")

    generic_unknown = rules.get("inconnu", {})
    if generic_unknown.get("emploi") != "question_applicable_examinee_sans_reponse":
        errors.append("la règle d'emploi de 'inconnu' est absente ou incorrecte")
    if not {"verification_effectuee", "absence_de_reponse_documentee"}.issubset(
        set(generic_unknown.get("conditions_obligatoires", []))
    ):
        errors.append("'inconnu' doit résulter d'une vérification documentée")

    reproducibility = rules.get("reproductibilite", {})
    for key in (
        "meme_entree_meme_configuration_meme_sortie",
        "ordre_des_enregistrements_sans_effet",
        "sortie_canonique_triee",
        "empreinte_sha256",
    ):
        if reproducibility.get(key) != "obligatoire":
            errors.append(f"règle de reproductibilité manquante : {key}")
    return errors


def validate_published_classifications(config: Mapping[str, Any]) -> list[str]:
    """Contrôle le registre complet publié."""
    errors = [
        *(f"secteurs: {error}" for error in validate_classifications(config)),
        *(
            f"situation actuelle: {error}"
            for error in validate_current_state_classifications(config)
        ),
        *(f"qualité: {error}" for error in validate_quality_classifications(config)),
    ]
    if str(config.get("version")) not in {"1.0", "1.1", "1.2", "1.3"}:
        errors.append("la version publiée doit être comprise entre 1.0 et 1.3")
    if config.get("status") not in {
        "phase4_validee",
        "phase5_enrichissement",
        "socle_v1",
        "phase8_corpus",
    }:
        errors.append("statut de publication des classifications invalide")

    for section in PUBLISHED_VOCABULARIES:
        vocabulary = config.get(section)
        if not isinstance(vocabulary, Mapping) or not vocabulary:
            errors.append(f"vocabulaire publié absent ou vide : {section}")
            continue
        for code, item in vocabulary.items():
            if not isinstance(item, Mapping) or not item.get("libelle"):
                errors.append(f"{section}.{code}: libellé obligatoire")

    for section in (
        "secteurs",
        "conservation",
        "usages_actuels",
        "accessibilite",
        "precision_geographique",
        "fiabilite",
    ):
        for code, item in config.get(section, {}).items():
            if not item.get("definition"):
                errors.append(f"{section}.{code}: définition obligatoire")
    return errors


def classify_geographic_precision(
    reference_level: str,
    *,
    verified: bool,
    config: Mapping[str, Any],
) -> str:
    """Classe une géométrie à partir du niveau réellement établi."""
    key = (reference_level, verified)
    if key not in PRECISION_BY_EVIDENCE:
        raise ValueError(
            "combinaison de preuve géographique non classable automatiquement : "
            f"{reference_level!r}, verified={verified}"
        )
    code = PRECISION_BY_EVIDENCE[key]
    if code not in config["precision_geographique"]:
        raise ValueError(f"code de précision absent du registre : {code}")
    return code


def classify_reliability(
    *,
    direct_evidence: bool,
    independent_concordant_sources: int,
    target_unambiguous: bool,
    unresolved_contradiction: bool,
    interpretation_required: bool,
) -> str:
    """Applique la grille minimale de fiabilité à une information précise."""
    if not target_unambiguous or unresolved_contradiction:
        return "faible"
    if direct_evidence and not interpretation_required:
        return "forte"
    if direct_evidence or independent_concordant_sources >= 2:
        return "moyenne"
    return "faible"


def decide_generic_value(
    *,
    applicable: bool,
    checked: bool,
    documented_unrepresented_value: bool,
    source_label: str | None = None,
    justification: str | None = None,
    human_validated: bool = False,
) -> dict[str, str | None]:
    """Décide entre `autre`, `inconnu` et une absence normalisée."""
    if not applicable:
        return {"code": None, "statut_valeur_code": "non_applicable"}
    if documented_unrepresented_value:
        if not source_label or not justification or not human_validated:
            raise ValueError(
                "'autre' exige le libellé source, une justification et une validation humaine"
            )
        return {"code": "autre", "statut_valeur_code": "renseignee"}
    if checked:
        return {"code": "inconnu", "statut_valeur_code": "inconnue"}
    return {"code": None, "statut_valeur_code": "non_renseignee_source"}


def canonical_fingerprint(value: Any) -> str:
    """Calcule l'empreinte d'une sortie JSON canonique et triée."""
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=lambda item: item.isoformat(),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _quality_decision_cases(config: Mapping[str, Any]) -> dict[str, Any]:
    precision_cases = {
        "adresse": classify_geographic_precision("adresse", verified=False, config=config),
        "batiment": classify_geographic_precision("batiment", verified=True, config=config),
        "emprise": classify_geographic_precision("emprise_site", verified=True, config=config),
        "parcelle": classify_geographic_precision("parcelle", verified=True, config=config),
        "point_approximatif": classify_geographic_precision(
            "point_approximatif", verified=False, config=config
        ),
        "point_site": classify_geographic_precision("point_site", verified=True, config=config),
        "zone_documentaire": classify_geographic_precision(
            "zone_documentaire", verified=False, config=config
        ),
    }
    reliability_cases = {
        "preuve_directe": classify_reliability(
            direct_evidence=True,
            independent_concordant_sources=1,
            target_unambiguous=True,
            unresolved_contradiction=False,
            interpretation_required=False,
        ),
        "recoupement_indirect": classify_reliability(
            direct_evidence=False,
            independent_concordant_sources=2,
            target_unambiguous=True,
            unresolved_contradiction=False,
            interpretation_required=True,
        ),
        "cible_ambigue": classify_reliability(
            direct_evidence=True,
            independent_concordant_sources=2,
            target_unambiguous=False,
            unresolved_contradiction=False,
            interpretation_required=False,
        ),
    }
    generic_cases = {
        "autre": decide_generic_value(
            applicable=True,
            checked=True,
            documented_unrepresented_value=True,
            source_label="production spéciale",
            justification="aucun code existant ne convient",
            human_validated=True,
        ),
        "inconnu": decide_generic_value(
            applicable=True,
            checked=True,
            documented_unrepresented_value=False,
        ),
        "non_applicable": decide_generic_value(
            applicable=False,
            checked=True,
            documented_unrepresented_value=False,
        ),
        "non_renseignee_source": decide_generic_value(
            applicable=True,
            checked=False,
            documented_unrepresented_value=False,
        ),
    }
    return {
        "precision_geographique": precision_cases,
        "fiabilite": reliability_cases,
        "valeurs_generiques": generic_cases,
    }


def audit_sample_geographic_information(
    pop_records: Sequence[Mapping[str, Any]], manifest: Mapping[str, Any]
) -> dict[str, Any]:
    """Mesure la présence de géométries sans leur attribuer une fausse précision."""
    pop_points = sum(bool(record.get("COOR")) for record in pop_records)
    pop_footprint_candidates = sum(
        bool(record.get("COORM"))
        and "/" in str(record.get("COORM"))
        and ";" in str(record.get("COORM"))
        for record in pop_records
    )
    casias_items = manifest["sources"]["casias"]
    casias_records = sum(item["observations"]["result_count"] for item in casias_items)
    casias_with_coordinates = sum(
        item["observations"]["with_coordinates"] for item in casias_items
    )
    return {
        "pop_merimee": {
            "record_count": len(pop_records),
            "with_source_point": pop_points,
            "with_footprint_candidate": pop_footprint_candidates,
            "automatically_verified_precision": 0,
        },
        "casias": {
            "sample_record_count": casias_records,
            "with_coordinates": casias_with_coordinates,
            "without_coordinates": casias_records - casias_with_coordinates,
            "automatically_verified_precision": 0,
        },
    }


def build_reproducibility_report(
    pop_records: Sequence[Mapping[str, Any]],
    mh_records: Sequence[Mapping[str, Any]],
    manifest: Mapping[str, Any],
    config: Mapping[str, Any],
) -> dict[str, Any]:
    """Rejoue les classements dans un ordre inverse et compare les sorties."""
    sector_a = classify_pop_records(pop_records, config)
    sector_b = classify_pop_records(list(reversed(pop_records)), config)
    current_a = audit_current_state_samples(pop_records, mh_records, config)
    current_b = audit_current_state_samples(
        list(reversed(pop_records)), list(reversed(mh_records)), config
    )
    quality_a = _quality_decision_cases(config)
    quality_b = _quality_decision_cases(config)

    checks = {
        "secteurs_ordre_inverse_identique": sector_a == sector_b,
        "situation_actuelle_ordre_inverse_identique": current_a == current_b,
        "grille_qualite_reexecution_identique": quality_a == quality_b,
    }
    fingerprints = {
        "secteurs": canonical_fingerprint(sector_a),
        "situation_actuelle": canonical_fingerprint(current_a),
        "grille_qualite": canonical_fingerprint(quality_a),
        "registre_classifications": canonical_fingerprint(config),
    }
    return {
        "configuration_version": config["version"],
        "validation_errors": {
            "secteurs": validate_classifications(config),
            "situation_actuelle": validate_current_state_classifications(config),
            "qualite": validate_quality_classifications(config),
        },
        "geographic_sample": audit_sample_geographic_information(pop_records, manifest),
        "decision_cases": quality_a,
        "reproducibility_checks": checks,
        "fingerprints_sha256": fingerprints,
        "all_reproducible": all(checks.values()),
    }


def build_final_validation_report(
    pop_records: Sequence[Mapping[str, Any]],
    mh_records: Sequence[Mapping[str, Any]],
    manifest: Mapping[str, Any],
    config: Mapping[str, Any],
) -> dict[str, Any]:
    """Produit le bilan de publication du registre de classifications V1."""
    reproducibility = build_reproducibility_report(
        pop_records, mh_records, manifest, config
    )
    errors = validate_published_classifications(config)
    counts = {
        section: len(config.get(section, {})) for section in PUBLISHED_VOCABULARIES
    }
    definition_sections = (
        "secteurs",
        "conservation",
        "usages_actuels",
        "accessibilite",
        "precision_geographique",
        "fiabilite",
    )
    definition_count = sum(
        bool(item.get("definition"))
        for section in definition_sections
        for item in config.get(section, {}).values()
    )
    expected_definition_count = sum(
        len(config.get(section, {})) for section in definition_sections
    )
    return {
        "published_version": str(config.get("version")),
        "status": config.get("status"),
        "vocabulary_counts": counts,
        "published_code_count": sum(counts.values()),
        "core_definitions": {
            "defined": definition_count,
            "expected": expected_definition_count,
            "complete": definition_count == expected_definition_count,
        },
        "validation_errors": errors,
        "reproducibility_checks": reproducibility["reproducibility_checks"],
        "fingerprints_sha256": reproducibility["fingerprints_sha256"],
        "all_valid": not errors and reproducibility["all_reproducible"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Auditer la qualité des classifications")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("reports/audits/phase2_extraction_samples_manifest.json"),
    )
    parser.add_argument(
        "--mh-sample",
        type=Path,
        default=Path(
            "data/raw/monuments_historiques_data_culture/2026/2026-07-20/"
            "monuments_historiques_data_culture__candidats_industriels__orne__"
            "20260720T072951Z.json"
        ),
    )
    parser.add_argument("--config", type=Path, default=Path("config/classifications.yml"))
    parser.add_argument(
        "--final",
        action="store_true",
        help="produire le bilan de publication de la phase 4",
    )
    arguments = parser.parse_args()
    config = load_classifications(arguments.config)
    manifest = json.loads(arguments.manifest.read_text(encoding="utf-8"))
    pop_records = load_pop_manifest_sample(arguments.manifest)
    mh_records = load_mh_sample(arguments.mh_sample)
    if arguments.final:
        report = build_final_validation_report(
            pop_records, mh_records, manifest, config
        )
        success = report["all_valid"]
    else:
        report = build_reproducibility_report(
            pop_records, mh_records, manifest, config
        )
        success = report["all_reproducible"]
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
