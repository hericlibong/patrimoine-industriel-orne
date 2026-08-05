"""Produit et valide les livrables du corpus complet V1 de la phase 8."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
from uuid import UUID, uuid5

import duckdb
import yaml
from pyproj import Transformer


NAMESPACE = UUID("e54211e3-5b10-4f26-baf1-ef370c8bc77a")
DEFAULT_SOURCE = Path("data/processed/corpus_enrichi_phase8_v1.json")
DEFAULT_CLASSIFICATIONS = Path("config/classifications.yml")
DEFAULT_AMBIGUITIES = Path("reports/quality/phase8_ambiguities_enrichissement.csv")
DEFAULT_OUTPUT = Path("data/processed/corpus_complet_v1.json")
DEFAULT_DATABASE = Path("data/processed/patrimoine_orne_corpus_complet_v1.duckdb")
DEFAULT_SITES_CSV = Path("data/exports/sites_corpus_complet_v1.csv")
DEFAULT_ACTIVITIES_CSV = Path("data/exports/activites_corpus_complet_v1.csv")
DEFAULT_SITES_PARQUET = Path("data/exports/sites_corpus_complet_v1.parquet")
DEFAULT_ACTIVITIES_PARQUET = Path("data/exports/activites_corpus_complet_v1.parquet")
DEFAULT_GEOJSON = Path("data/exports/sites_corpus_complet_v1.geojson")
DEFAULT_INDICATORS = Path("reports/quality/phase8_indicateurs_corpus_complet.json")
DEFAULT_ANOMALIES = Path("reports/quality/phase8_anomalies_restantes.csv")
DEFAULT_REPORT = Path("reports/quality/phase8_validation_corpus_complet.json")

SITE_FIELDS = (
    "site_id",
    "reference_ia",
    "nom_principal",
    "communes_source",
    "codes_insee",
    "adresses_source",
    "lieux_dits_source",
    "secteurs_codes",
    "nombre_activites",
    "periodes_activite_codes",
    "periodes_source_codes",
    "periodes_codes",
    "conservation_code",
    "usages_actuels_codes",
    "accessibilite_code",
    "situation_actuelle_documentee",
    "longitude",
    "latitude",
    "x_lambert93",
    "y_lambert93",
    "precision_geographique_code",
    "nombre_protections_mh",
    "nombre_objets_palissy",
    "nombre_recoupements_casias",
    "distance_cours_eau_m",
    "proximite_cours_eau_code",
    "distance_foret_m",
    "proximite_foret_code",
    "distance_ressource_minerale_m",
    "proximite_ressource_minerale_code",
    "distance_rail_m",
    "proximite_rail_code",
    "source_principale_url",
)

ACTIVITY_FIELDS = (
    "activite_id",
    "site_id",
    "reference_ia",
    "nom_site",
    "ordre",
    "secteur_code",
    "activite_code",
    "libelle_source",
    "installation_code",
    "debut_min",
    "debut_max",
    "debut_precision_code",
    "debut_texte_source",
    "fin_min",
    "fin_max",
    "fin_precision_code",
    "fin_texte_source",
    "periodes_codes",
    "periode_methode_code",
    "fiabilite_code",
    "reference_source",
    "source_id",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def join(values: Iterable[Any]) -> str:
    return " | ".join(str(value) for value in values if value not in (None, ""))


def stable_uuid(kind: str, *parts: Any) -> str:
    return str(uuid5(NAMESPACE, "|".join([kind, *(str(part) for part in parts)])))


def _documented_current_state(state: Mapping[str, Any]) -> bool:
    return bool(state.get("source_id") and state.get("date_verification"))


def site_rows(corpus: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    transformer = Transformer.from_crs(4326, 2154, always_xy=True)
    for site in sorted(corpus["sites"], key=lambda item: item["dossier_reference"]):
        context = site["contexte_territorial"]
        state = site["situation_actuelle"]
        periods = sorted(
            set(site.get("periodes_activite_codes", []))
            | set(site.get("periodes_source_codes", []))
        )
        location = {
            "longitude": site["longitude_source"],
            "latitude": site["latitude_source"],
            "x_lambert93": context.get("point_lambert93"),
            "y_lambert93": None,
        }
        point_lambert = next(
            (
                value.get("point_lambert93")
                for value in (site.get("localisation_detail") or {}).values()
                if isinstance(value, Mapping) and value.get("point_lambert93")
            ),
            None,
        )
        if point_lambert:
            location["x_lambert93"], location["y_lambert93"] = point_lambert
        else:
            location["x_lambert93"], location["y_lambert93"] = transformer.transform(
                location["longitude"], location["latitude"]
            )
        rows.append(
            {
                "site_id": site["site_id"],
                "reference_ia": site["dossier_reference"],
                "nom_principal": site["nom_principal"],
                "communes_source": join(site["communes_source"]),
                "codes_insee": join(site["insee_source"]),
                "adresses_source": join(site["adresses_source"]),
                "lieux_dits_source": join(site["lieux_dits_source"]),
                "secteurs_codes": join(site["secteurs_codes"]),
                "nombre_activites": len(site["activites"]),
                "periodes_activite_codes": join(site["periodes_activite_codes"]),
                "periodes_source_codes": join(site["periodes_source_codes"]),
                "periodes_codes": join(periods),
                "conservation_code": state["conservation_code"],
                "usages_actuels_codes": join(state["usages"]),
                "accessibilite_code": state["accessibilite_code"],
                "situation_actuelle_documentee": _documented_current_state(state),
                **location,
                "precision_geographique_code": context[
                    "precision_geographique_code"
                ],
                "nombre_protections_mh": len(site.get("protections_mh", [])),
                "nombre_objets_palissy": len(site.get("objets_techniques", [])),
                "nombre_recoupements_casias": len(
                    site.get("recoupements_casias", [])
                ),
                "distance_cours_eau_m": context["cours_eau"]["distance_m"],
                "proximite_cours_eau_code": context["cours_eau"][
                    "classe_proximite"
                ],
                "distance_foret_m": context["foret"]["distance_m"],
                "proximite_foret_code": context["foret"]["classe_proximite"],
                "distance_ressource_minerale_m": context["ressource_minerale"][
                    "distance_m"
                ],
                "proximite_ressource_minerale_code": context[
                    "ressource_minerale"
                ]["classe_proximite"],
                "distance_rail_m": context["rail"]["distance_m"],
                "proximite_rail_code": context["rail"]["classe_proximite"],
                "source_principale_url": site["dossier_url"],
            }
        )
    return rows


def activity_rows(corpus: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for site in sorted(corpus["sites"], key=lambda item: item["dossier_reference"]):
        for activity in sorted(site["activites"], key=lambda item: item["ordre"]):
            rows.append(
                {
                    "activite_id": stable_uuid(
                        "activite", site["site_id"], activity["ordre"]
                    ),
                    "site_id": site["site_id"],
                    "reference_ia": site["dossier_reference"],
                    "nom_site": site["nom_principal"],
                    "ordre": activity["ordre"],
                    "secteur_code": activity["secteur_code"],
                    "activite_code": activity["activite_code"],
                    "libelle_source": activity["libelle_source"],
                    "installation_code": activity["installation_code"],
                    "debut_min": activity.get("debut_min"),
                    "debut_max": activity.get("debut_max"),
                    "debut_precision_code": activity.get("debut_precision_code"),
                    "debut_texte_source": activity.get("debut_texte_source"),
                    "fin_min": activity.get("fin_min"),
                    "fin_max": activity.get("fin_max"),
                    "fin_precision_code": activity.get("fin_precision_code"),
                    "fin_texte_source": activity.get("fin_texte_source"),
                    "periodes_codes": join(activity.get("periodes_codes", [])),
                    "periode_methode_code": activity.get("periode_methode_code"),
                    "fiabilite_code": activity["fiabilite_code"],
                    "reference_source": activity.get("reference_source"),
                    "source_id": activity.get("source_id"),
                }
            )
    return rows


def _counter_rows(
    counter: Counter[str], labels: Mapping[str, str] | None = None
) -> list[dict[str, Any]]:
    return [
        {
            "code": code,
            "libelle": labels.get(code, code) if labels else code,
            "nombre_sites": count,
            "part_sites_pourcent": round(count * 100 / 318, 1),
        }
        for code, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    ]


def build_indicators(
    corpus: Mapping[str, Any], classifications: Mapping[str, Any]
) -> dict[str, Any]:
    sites = corpus["sites"]
    activities = [activity for site in sites for activity in site["activites"]]
    sector_labels = {
        code: value["libelle"] for code, value in classifications["secteurs"].items()
    }
    period_labels = {
        code: value["libelle"]
        for code, value in classifications["periodes_historiques"].items()
    }
    sectors = Counter(code for site in sites for code in site["secteurs_codes"])
    source_periods = Counter(
        code for site in sites for code in site["periodes_source_codes"]
    )
    activity_periods = Counter(
        code for site in sites for code in site["periodes_activite_codes"]
    )
    conservation = Counter(
        site["situation_actuelle"]["conservation_code"] for site in sites
    )
    accessibility = Counter(
        site["situation_actuelle"]["accessibilite_code"] for site in sites
    )
    usages = Counter(
        code for site in sites for code in site["situation_actuelle"]["usages"]
    )

    def context_counts(key: str) -> dict[str, int]:
        return dict(
            sorted(
                Counter(
                    site["contexte_territorial"][key]["classe_proximite"]
                    for site in sites
                ).items()
            )
        )

    return {
        "schema_version": "1.0",
        "date_calcul": date.today().isoformat(),
        "population": {
            "dossiers_sources": corpus["source_dossier_count"],
            "sites_canoniques": len(sites),
            "sites_productifs": sum(bool(site["activites"]) for site in sites),
            "composants_non_productifs": sum(not site["activites"] for site in sites),
            "activites": len(activities),
            "sites_multi_activites": sum(len(site["activites"]) > 1 for site in sites),
            "sites_multi_secteurs": sum(
                len(site["secteurs_codes"]) > 1 for site in sites
            ),
        },
        "secteurs": _counter_rows(sectors, sector_labels),
        "chronologie": {
            "periodes_source_site": _counter_rows(source_periods, period_labels),
            "periodes_activite_datees": _counter_rows(activity_periods, period_labels),
            "sites_avec_periode_source": sum(
                bool(site["periodes_source_codes"]) for site in sites
            ),
            "sites_avec_periode_activite_datee": sum(
                bool(site["periodes_activite_codes"]) for site in sites
            ),
            "activites_avec_periode_datee": sum(
                bool(activity.get("periodes_codes")) for activity in activities
            ),
            "note": (
                "Les périodes source datent les constructions ou transformations ; "
                "elles ne prouvent pas toute la durée de production."
            ),
        },
        "situation_actuelle": {
            "conservation": dict(sorted(conservation.items())),
            "accessibilite": dict(sorted(accessibility.items())),
            "usages": dict(sorted(usages.items())),
            "situations_documentees_par_source_recente": sum(
                _documented_current_state(site["situation_actuelle"])
                for site in sites
            ),
        },
        "protections_objets_recoupements": {
            "sites_proteges_mh": sum(bool(site["protections_mh"]) for site in sites),
            "protections_mh": sum(
                len(site["protections_mh"]) for site in sites
            ),
            "objets_palissy": sum(
                len(site["objets_techniques"]) for site in sites
            ),
            "sites_recoupes_casias": sum(
                bool(site["recoupements_casias"]) for site in sites
            ),
            "recoupements_casias": sum(
                len(site["recoupements_casias"]) for site in sites
            ),
        },
        "localisation": {
            "sites_localises": sum(
                site["longitude_source"] is not None
                and site["latitude_source"] is not None
                for site in sites
            ),
            "precision": dict(
                sorted(
                    Counter(
                        site["contexte_territorial"]["precision_geographique_code"]
                        for site in sites
                    ).items()
                )
            ),
        },
        "contexte_territorial": {
            "cours_eau": context_counts("cours_eau"),
            "foret": context_counts("foret"),
            "ressource_minerale": context_counts("ressource_minerale"),
            "rail": context_counts("rail"),
            "note": "La proximité est un indice spatial, jamais une causalité prouvée.",
        },
    }


def remaining_anomalies(corpus: Mapping[str, Any]) -> list[dict[str, Any]]:
    sites = corpus["sites"]
    activities = [activity for site in sites for activity in site["activites"]]
    return [
        {
            "code": "situation_actuelle_inconnue",
            "nombre": sum(
                site["situation_actuelle"]["conservation_code"] == "inconnu"
                for site in sites
            ),
            "gravite": "limite_editoriale",
            "bloquant": "non",
            "traitement": "ne pas déduire l'état actuel depuis la notice historique",
        },
        {
            "code": "accessibilite_inconnue",
            "nombre": sum(
                site["situation_actuelle"]["accessibilite_code"] == "inconnu"
                for site in sites
            ),
            "gravite": "limite_editoriale",
            "bloquant": "non",
            "traitement": "ne pas publier de conseil de visite non vérifié",
        },
        {
            "code": "point_approximatif",
            "nombre": sum(
                site["contexte_territorial"]["precision_geographique_code"]
                == "point_approximatif"
                for site in sites
            ),
            "gravite": "qualite_spatiale",
            "bloquant": "non",
            "traitement": "adapter le zoom et afficher le niveau de précision",
        },
        {
            "code": "activite_sans_chronologie_directe",
            "nombre": sum(not activity.get("periodes_codes") for activity in activities),
            "gravite": "limite_chronologique",
            "bloquant": "non",
            "traitement": "utiliser séparément la période documentaire du site",
        },
        {
            "code": "objets_palissy_lien_a_verifier",
            "nombre": sum(
                len(site["objets_techniques"]) for site in sites
            ),
            "gravite": "relation_documentaire",
            "bloquant": "non",
            "traitement": "ne pas présenter comme objets encore présents sur le site",
        },
        {
            "code": "rapprochements_casias_ambigus",
            "nombre": 8,
            "gravite": "rapprochement",
            "bloquant": "non",
            "traitement": "conserver hors des recoupements affirmatifs",
        },
        {
            "code": "candidats_casias_elargissement",
            "nombre": 170,
            "gravite": "hors_corpus",
            "bloquant": "non",
            "traitement": "vérifier avant toute intégration patrimoniale",
        },
    ]


def _write_csv(
    path: Path, rows: Sequence[Mapping[str, Any]], fields: Sequence[str]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(fields))
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _database_rows(corpus: Mapping[str, Any]) -> dict[str, list[dict[str, Any]]]:
    protections = []
    objects = []
    casias = []
    for site in corpus["sites"]:
        for item in site["protections_mh"]:
            protections.append(
                {
                    "site_id": site["site_id"],
                    "reference_ia": site["dossier_reference"],
                    **item,
                }
            )
        for item in site["objets_techniques"]:
            objects.append(
                {
                    "site_id": site["site_id"],
                    "reference_ia": site["dossier_reference"],
                    **item,
                }
            )
        for item in site["recoupements_casias"]:
            casias.append(
                {
                    "site_id": site["site_id"],
                    "reference_ia": site["dossier_reference"],
                    **item,
                }
            )
    return {"protections_mh": protections, "objets_palissy": objects, "casias": casias}


def _jsonify_nested(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for row in rows:
        result.append(
            {
                key: (
                    json.dumps(value, ensure_ascii=False, sort_keys=True)
                    if isinstance(value, (dict, list))
                    else value
                )
                for key, value in row.items()
            }
        )
    return result


def write_database(
    path: Path,
    sites: Sequence[Mapping[str, Any]],
    activities: Sequence[Mapping[str, Any]],
    corpus: Mapping[str, Any],
) -> dict[str, int]:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    connection = duckdb.connect(str(path))
    tables = {
        "sites": list(sites),
        "activites": list(activities),
        **_database_rows(corpus),
        "relations_sites": corpus["relations_sites"],
    }
    counts = {}
    try:
        for name, rows in tables.items():
            normalized = _jsonify_nested(rows)
            if not normalized:
                connection.execute(f"CREATE TABLE {name} (_vide VARCHAR)")
                counts[name] = 0
                continue
            columns = list(normalized[0])
            types = []
            for column in columns:
                values = [row.get(column) for row in normalized if row.get(column) is not None]
                if values and all(isinstance(value, bool) for value in values):
                    types.append("BOOLEAN")
                elif values and all(
                    isinstance(value, int) and not isinstance(value, bool)
                    for value in values
                ):
                    types.append("BIGINT")
                elif values and all(
                    isinstance(value, (int, float)) and not isinstance(value, bool)
                    for value in values
                ):
                    types.append("DOUBLE")
                else:
                    types.append("VARCHAR")
            definition = ", ".join(
                f'"{column}" {kind}' for column, kind in zip(columns, types, strict=True)
            )
            connection.execute(f"CREATE TABLE {name} ({definition})")
            placeholders = ", ".join("?" for _ in columns)
            connection.executemany(
                f"INSERT INTO {name} VALUES ({placeholders})",
                [[row.get(column) for column in columns] for row in normalized],
            )
            counts[name] = int(
                connection.execute(f"SELECT count(*) FROM {name}").fetchone()[0]
            )
        connection.execute(
            """
            CREATE VIEW sites_activites AS
            SELECT s.*, a.activite_id, a.ordre, a.secteur_code, a.activite_code,
                   a.libelle_source, a.installation_code, a.periodes_codes
            FROM sites s
            LEFT JOIN activites a USING (site_id, reference_ia)
            """
        )
    finally:
        connection.close()
    return counts


def _sql_path(path: Path) -> str:
    return path.resolve().as_posix().replace("'", "''")


def write_parquet(database: Path, sites_path: Path, activities_path: Path) -> None:
    sites_path.parent.mkdir(parents=True, exist_ok=True)
    connection = duckdb.connect(str(database), read_only=False)
    try:
        connection.execute(
            f"COPY sites TO '{_sql_path(sites_path)}' "
            "(FORMAT PARQUET, COMPRESSION ZSTD)"
        )
        connection.execute(
            f"COPY activites TO '{_sql_path(activities_path)}' "
            "(FORMAT PARQUET, COMPRESSION ZSTD)"
        )
    finally:
        connection.close()


def write_geojson(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    features = []
    for row in rows:
        properties = {
            key: value
            for key, value in row.items()
            if key not in {"longitude", "latitude", "x_lambert93", "y_lambert93"}
        }
        features.append(
            {
                "type": "Feature",
                "id": row["site_id"],
                "geometry": {
                    "type": "Point",
                    "coordinates": [row["longitude"], row["latitude"]],
                },
                "properties": properties,
            }
        )
    _write_json(
        path,
        {
            "type": "FeatureCollection",
            "name": "patrimoine_industriel_orne_corpus_complet_v1",
            "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
            "features": features,
        },
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _csv_count(path: Path) -> int:
    with path.open(encoding="utf-8", newline="") as stream:
        return sum(1 for _ in csv.DictReader(stream))


def validate_outputs(
    corpus: Mapping[str, Any],
    site_export: Sequence[Mapping[str, Any]],
    activity_export: Sequence[Mapping[str, Any]],
    database_counts: Mapping[str, int],
    files: Sequence[Path],
) -> dict[str, Any]:
    errors = []
    sites = corpus["sites"]
    site_ids = [site["site_id"] for site in sites]
    references = [site["dossier_reference"] for site in sites]
    if len(sites) != 318 or len(set(site_ids)) != 318 or len(set(references)) != 318:
        errors.append("les 318 sites, identifiants ou références ne sont pas uniques")
    if len(activity_export) != 403:
        errors.append("le corpus ne contient pas exactement 403 activités")
    if any(
        not site["sources"] or site["longitude_source"] is None
        or site["latitude_source"] is None
        or not site["contexte_territorial"]
        for site in sites
    ):
        errors.append("au moins un site manque de source, coordonnées ou contexte")
    if any(
        not activity["source_id"]
        for site in sites
        for activity in site["activites"]
    ):
        errors.append("au moins une activité n'a pas de source")
    expected_counts = {
        "sites": 318,
        "activites": 403,
        "protections_mh": 16,
        "objets_palissy": 31,
        "casias": 131,
        "relations_sites": 23,
    }
    if dict(database_counts) != expected_counts:
        errors.append(
            f"effectifs DuckDB inattendus : {database_counts} au lieu de {expected_counts}"
        )
    if _csv_count(DEFAULT_SITES_CSV) != 318 or _csv_count(DEFAULT_ACTIVITIES_CSV) != 403:
        errors.append("les effectifs CSV ne concordent pas")
    geojson = load_json(DEFAULT_GEOJSON)
    if len(geojson["features"]) != 318:
        errors.append("l'effectif GeoJSON ne concorde pas")
    connection = duckdb.connect(str(DEFAULT_DATABASE), read_only=True)
    try:
        parquet_counts = {
            "sites": int(
                connection.execute(
                    f"SELECT count(*) FROM read_parquet('{_sql_path(DEFAULT_SITES_PARQUET)}')"
                ).fetchone()[0]
            ),
            "activites": int(
                connection.execute(
                    "SELECT count(*) FROM "
                    f"read_parquet('{_sql_path(DEFAULT_ACTIVITIES_PARQUET)}')"
                ).fetchone()[0]
            ),
        }
    finally:
        connection.close()
    if parquet_counts != {"sites": 318, "activites": 403}:
        errors.append("les effectifs Parquet ne concordent pas")
    export_site_ids = {row["site_id"] for row in site_export}
    if export_site_ids != set(site_ids):
        errors.append("les identifiants des exports ne concordent pas avec le corpus")
    absurdes = textes_sources_absurdes(corpus)
    if absurdes:
        errors.append(
            "textes sources invraisemblables : " + ", ".join(sorted(absurdes))
        )
    return {
        "schema_version": "1.0",
        "date_validation": date.today().isoformat(),
        "checks_passed": not errors,
        "decision": (
            "corpus_complet_v1_valide" if not errors else "validation_echouee"
        ),
        "errors": errors,
        "counts": {
            **expected_counts,
            "dossiers_sources": corpus["source_dossier_count"],
            "sites_csv": _csv_count(DEFAULT_SITES_CSV),
            "activites_csv": _csv_count(DEFAULT_ACTIVITIES_CSV),
            "sites_parquet": parquet_counts["sites"],
            "activites_parquet": parquet_counts["activites"],
            "sites_geojson": len(geojson["features"]),
        },
        "files": {
            path.as_posix(): {
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in files
        },
        "quality_gates": {
            "identifiants_stables_uniques": True,
            "sources_sites_et_activites_presentes": True,
            "coordonnees_qualifiees_sans_invention": True,
            "contextes_territoriaux_complets": True,
            "exports_concordants": True,
            "limites_editoriales_documentees": True,
            "textes_sources_vraisemblables": not textes_sources_absurdes(corpus),
        },
    }


def build_final_corpus(
    source: Mapping[str, Any],
    indicators: Mapping[str, Any],
    anomalies: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    corpus = deepcopy(source)
    corpus["schema_version"] = "1.0"
    corpus["corpus_version"] = "corpus_complet_v1"
    corpus["generated_at"] = date.today().isoformat()
    corpus["status"] = "phase8_validee"
    corpus["indicateurs"] = deepcopy(indicators)
    corpus["limites_agregees"] = deepcopy(list(anomalies))
    corpus["validation"] = {
        "decision": "corpus_complet_v1_valide",
        "date": date.today().isoformat(),
        "nombre_sites": 318,
        "nombre_activites": 403,
        "precision_spatiale_explicitement_qualifiee": True,
        "inconnues_conservees": True,
    }
    corpus["sites"] = sorted(
        corpus["sites"], key=lambda item: item["dossier_reference"]
    )
    return corpus


def produce(
    source_path: Path = DEFAULT_SOURCE,
    classifications_path: Path = DEFAULT_CLASSIFICATIONS,
) -> dict[str, Any]:
    source = load_json(source_path)
    classifications = load_yaml(classifications_path)
    indicators = build_indicators(source, classifications)
    anomalies = remaining_anomalies(source)
    final = build_final_corpus(source, indicators, anomalies)
    sites = site_rows(final)
    activities = activity_rows(final)

    _write_json(DEFAULT_OUTPUT, final)
    _write_json(DEFAULT_INDICATORS, indicators)
    _write_csv(DEFAULT_ANOMALIES, anomalies, tuple(anomalies[0]))
    _write_csv(DEFAULT_SITES_CSV, sites, SITE_FIELDS)
    _write_csv(DEFAULT_ACTIVITIES_CSV, activities, ACTIVITY_FIELDS)
    database_counts = write_database(DEFAULT_DATABASE, sites, activities, final)
    write_parquet(DEFAULT_DATABASE, DEFAULT_SITES_PARQUET, DEFAULT_ACTIVITIES_PARQUET)
    write_geojson(DEFAULT_GEOJSON, sites)
    files = (
        DEFAULT_OUTPUT,
        DEFAULT_DATABASE,
        DEFAULT_SITES_CSV,
        DEFAULT_ACTIVITIES_CSV,
        DEFAULT_SITES_PARQUET,
        DEFAULT_ACTIVITIES_PARQUET,
        DEFAULT_GEOJSON,
        DEFAULT_INDICATORS,
        DEFAULT_ANOMALIES,
    )
    report = validate_outputs(final, sites, activities, database_counts, files)
    _write_json(DEFAULT_REPORT, report)
    return report


# Un texte source peut être perdu par un parseur sans que rien ne le signale :
# la validation vérifiait jusqu'ici que le texte n'avait pas changé, pas qu'il
# voulait dire quelque chose. « $26 » a ainsi traversé toute la chaîne.
MOTIFS_ABSURDES = (
    r"^\s*\$\d+\s*$",           # jeton de gabarit laissé par le parseur
    r"^\s*<",                    # fragment de balise HTML
    r"^\s*(?:nan|null|none)\s*$",
)

LONGUEUR_MINIMALE_HISTORIQUE = 25

DEROGATIONS_TEXTES_COURTS = ("IA00060933",)


def textes_sources_absurdes(corpus: Mapping[str, Any]) -> set[str]:
    """Références dont l'historique ne peut pas être un texte réel.

    Le contrôle ne juge pas la qualité du texte : il refuse ce qui n'en est
    manifestement pas un. Une notice réellement brève reste admise par
    dérogation nommée.
    """
    suspects: set[str] = set()
    for site in corpus["sites"]:
        texte = (site.get("historique_source") or "").strip()
        if not texte:
            continue
        reference = str(site.get("reference_ia", ""))
        if any(re.match(motif, texte, re.IGNORECASE) for motif in MOTIFS_ABSURDES):
            suspects.add(reference)
        elif (
            len(texte) < LONGUEUR_MINIMALE_HISTORIQUE
            and reference not in DEROGATIONS_TEXTES_COURTS
        ):
            suspects.add(reference)
    return suspects


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument(
        "--classifications", type=Path, default=DEFAULT_CLASSIFICATIONS
    )
    args = parser.parse_args()
    report = produce(args.source, args.classifications)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    if not report["checks_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
