"""Consolide le corpus pilote et produit les livrables du socle V1."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping, Sequence
from uuid import UUID, uuid5

import duckdb
import yaml
from pyproj import Transformer

from patrimoine_orne.model.database import (
    connect_database,
    initialize_database,
)
from patrimoine_orne.model.validation import assert_database_valid


NAMESPACE = UUID("d8422e8e-c614-45d2-9a0d-85f39023c458")

EXPORT_COLUMNS: tuple[tuple[str, str], ...] = (
    ("site_id", "VARCHAR"),
    ("reference_ia", "VARCHAR"),
    ("nom_principal", "VARCHAR"),
    ("commune_actuelle_code_insee", "VARCHAR"),
    ("commune_actuelle_nom", "VARCHAR"),
    ("commune_historique_nom", "VARCHAR"),
    ("lieu_dit", "VARCHAR"),
    ("secteurs_codes", "VARCHAR"),
    ("activites_codes", "VARCHAR"),
    ("activites_libelles", "VARCHAR"),
    ("nombre_activites", "INTEGER"),
    ("siecles_source", "VARCHAR"),
    ("periodes_activite_codes", "VARCHAR"),
    ("periodes_source_codes", "VARCHAR"),
    ("periodes_situation_actuelle_codes", "VARCHAR"),
    ("periodes_codes", "VARCHAR"),
    ("periodes_libelles", "VARCHAR"),
    ("periode_methode_codes", "VARCHAR"),
    ("premiere_annee_documentee", "INTEGER"),
    ("derniere_annee_documentee", "INTEGER"),
    ("historique_source", "VARCHAR"),
    ("conservation_code", "VARCHAR"),
    ("usages_actuels_codes", "VARCHAR"),
    ("accessibilite_code", "VARCHAR"),
    ("situation_verifiee_le", "DATE"),
    ("protection_mh_reference", "VARCHAR"),
    ("longitude", "DOUBLE"),
    ("latitude", "DOUBLE"),
    ("x_lambert93", "DOUBLE"),
    ("y_lambert93", "DOUBLE"),
    ("precision_point_code", "VARCHAR"),
    ("statut_localisation_code", "VARCHAR"),
    ("emprise_documentaire_disponible", "BOOLEAN"),
    ("parcelle_candidate_id", "VARCHAR"),
    ("reference_cadastrale_concordante", "BOOLEAN"),
    ("controle_cartographique_code", "VARCHAR"),
    ("motifs_controle", "VARCHAR"),
    ("distance_cours_eau_m", "DOUBLE"),
    ("proximite_cours_eau_code", "VARCHAR"),
    ("distance_foret_m", "DOUBLE"),
    ("proximite_foret_code", "VARCHAR"),
    ("lithologie", "VARCHAR"),
    ("distance_ressource_minerale_m", "DOUBLE"),
    ("proximite_ressource_minerale_code", "VARCHAR"),
    ("distance_rail_m", "DOUBLE"),
    ("proximite_rail_code", "VARCHAR"),
    ("source_principale_url", "VARCHAR"),
)

ACTIVITY_EXPORT_COLUMNS: tuple[tuple[str, str], ...] = (
    ("activite_id", "VARCHAR"),
    ("site_id", "VARCHAR"),
    ("reference_ia", "VARCHAR"),
    ("nom_site", "VARCHAR"),
    ("commune_actuelle_code_insee", "VARCHAR"),
    ("commune_actuelle_nom", "VARCHAR"),
    ("ordre", "INTEGER"),
    ("secteur_code", "VARCHAR"),
    ("activite_code", "VARCHAR"),
    ("activite_libelle_source", "VARCHAR"),
    ("installation_code", "VARCHAR"),
    ("debut_min", "DATE"),
    ("debut_max", "DATE"),
    ("debut_precision_code", "VARCHAR"),
    ("debut_texte_source", "VARCHAR"),
    ("fin_min", "DATE"),
    ("fin_max", "DATE"),
    ("fin_precision_code", "VARCHAR"),
    ("fin_texte_source", "VARCHAR"),
    ("periodes_codes", "VARCHAR"),
    ("periodes_libelles", "VARCHAR"),
    ("periode_methode_code", "VARCHAR"),
    ("siecles_source_site", "VARCHAR"),
    ("fiabilite_code", "VARCHAR"),
    ("source_reference", "VARCHAR"),
    ("source_url", "VARCHAR"),
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write_json(value: Mapping[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def stable_uuid(kind: str, *parts: object) -> str:
    value = "|".join([kind, *(str(part) for part in parts)])
    return str(uuid5(NAMESPACE, value))


def clean_value(value: Any) -> Any:
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    if isinstance(value, list):
        return [clean_value(item) for item in value]
    if isinstance(value, dict):
        return {key: clean_value(item) for key, item in value.items()}
    return value


def index_by_reference(items: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(item["reference_ia"]): item for item in items}


def consolidate_corpus(
    corpus: Mapping[str, Any],
    locations: Mapping[str, Any],
    context: Mapping[str, Any],
    cartographic_control: Mapping[str, Any],
) -> dict[str, Any]:
    location_index = index_by_reference(locations["locations"])
    context_index = index_by_reference(context["sites"])
    control_index = {
        str(item["reference"]): item for item in cartographic_control["cas_sensibles"]
    }
    references = [str(site["reference_ia"]) for site in corpus["sites"]]
    if len(references) != len(set(references)):
        raise ValueError("le corpus contient plusieurs fois une référence IA")
    if set(references) != set(location_index) or set(references) != set(context_index):
        raise ValueError("les jeux géographiques ne couvrent pas exactement le corpus")

    sites = []
    for original_site in sorted(corpus["sites"], key=lambda item: item["reference_ia"]):
        site = clean_value(deepcopy(original_site))
        reference = str(site["reference_ia"])
        location = clean_value(deepcopy(location_index[reference]))
        spatial_context = clean_value(deepcopy(context_index[reference]))
        control = clean_value(deepcopy(control_index.get(reference)))

        location["geometrie_reference"]["precision_geographique_code"] = (
            "point_approximatif"
        )
        location["controle_humain_cartographique"] = (
            "localisation_a_verifier" if control else "controle_coherent_approximatif"
        )
        site["statut_corpus_code"] = "cartographiable"
        site["localisation"] = location
        site["contexte_territorial"] = spatial_context
        site["controle_cartographique"] = control or {
            "reference": reference,
            "motifs": [],
            "anomalies": [],
            "decision_manuelle": "aucune_alerte_detectee",
            "note_manuelle": None,
        }
        sites.append(site)

    return {
        "schema_version": "1.1",
        "socle_version": "1.1",
        "corpus_version_source": corpus["corpus_version"],
        "classifications_version": corpus["classifications_version"],
        "date_consolidation": "2026-07-22",
        "status": "socle_v1_consolide",
        "validation": {
            **corpus["validation"],
            "phase6_geographie": "validee",
            "precision_points": "point_approximatif",
            "geometries_verifiees": 0,
        },
        "nettoyage": {
            "chaines_vides_converties_en_null": True,
            "sites_tries_par_reference_ia": True,
            "statut_sites": "cartographiable",
            "localisation_contexte_et_controle_integres": True,
            "donnees_sources_non_ecrasees": True,
            "dates_activites_normalisees": True,
            "periodes_historiques_calculees": True,
        },
        "sites": sites,
        "objets_techniques": sorted(
            clean_value(deepcopy(corpus.get("objets_techniques", []))),
            key=lambda item: item["reference_palissy"],
        ),
        "anomalies": clean_value(deepcopy(corpus.get("anomalies", []))),
    }


def flat_rows(corpus: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for site in corpus["sites"]:
        activities = site["activites"]
        state = site["situation_actuelle"]
        location = site["localisation"]
        geometry = location["geometrie_reference"]
        context = site["contexte_territorial"]
        control = site["controle_cartographique"]
        parcel = location["parcelles_actuelles_candidates"][0]
        principal_source = next(
            source for source in site["sources"] if source["role"] == "notice_principale"
        )
        lithology = context["geologie"]["lithologie"] or {}
        rows.append(
            {
                "site_id": site["site_id"],
                "reference_ia": site["reference_ia"],
                "nom_principal": site["nom_principal"],
                "commune_actuelle_code_insee": site["commune_actuelle_code_insee"],
                "commune_actuelle_nom": site["commune_actuelle_nom"],
                "commune_historique_nom": site["commune_historique_nom"],
                "lieu_dit": site["lieu_dit"],
                "secteurs_codes": "|".join(
                    sorted({activity["secteur_code"] for activity in activities})
                ),
                "activites_codes": "|".join(
                    activity["activite_code"] for activity in activities
                ),
                "activites_libelles": "|".join(
                    activity["libelle_source"] for activity in activities
                ),
                "nombre_activites": len(activities),
                "siecles_source": "|".join(site["siecles_source"]),
                "periodes_activite_codes": "|".join(
                    site["periodes_activite_codes"]
                ),
                "periodes_source_codes": "|".join(site["periodes_source_codes"]),
                "periodes_situation_actuelle_codes": "|".join(
                    site["periodes_situation_actuelle_codes"]
                ),
                "periodes_codes": "|".join(site["periodes_codes"]),
                "periodes_libelles": "|".join(site["periodes_libelles"]),
                "periode_methode_codes": "|".join(
                    site["periode_methode_codes"]
                ),
                "premiere_annee_documentee": site["premiere_annee_documentee"],
                "derniere_annee_documentee": site["derniere_annee_documentee"],
                "historique_source": site["historique_source"],
                "conservation_code": state["conservation_code"],
                "usages_actuels_codes": "|".join(state["usages"]),
                "accessibilite_code": state["accessibilite_code"],
                "situation_verifiee_le": state["date_verification"],
                "protection_mh_reference": site["protection_mh_reference"],
                "longitude": geometry["point_wgs84"][0],
                "latitude": geometry["point_wgs84"][1],
                "x_lambert93": geometry["point_lambert93"][0],
                "y_lambert93": geometry["point_lambert93"][1],
                "precision_point_code": "point_approximatif",
                "statut_localisation_code": location["statut_localisation_code"],
                "emprise_documentaire_disponible": bool(location["emprise_source"]),
                "parcelle_candidate_id": parcel["idu"],
                "reference_cadastrale_concordante": parcel[
                    "reference_source_concordante"
                ],
                "controle_cartographique_code": (
                    "a_verifier" if control["motifs"] else "coherent_approximatif"
                ),
                "motifs_controle": "|".join(control["motifs"]),
                "distance_cours_eau_m": context["cours_eau"]["distance_m"],
                "proximite_cours_eau_code": context["cours_eau"]["classe_proximite"],
                "distance_foret_m": context["foret"]["distance_m"],
                "proximite_foret_code": context["foret"]["classe_proximite"],
                "lithologie": lithology.get("DESCR"),
                "distance_ressource_minerale_m": context["ressource_minerale"][
                    "distance_m"
                ],
                "proximite_ressource_minerale_code": context[
                    "ressource_minerale"
                ]["classe_proximite"],
                "distance_rail_m": context["rail"]["distance_m"],
                "proximite_rail_code": context["rail"]["classe_proximite"],
                "source_principale_url": principal_source["url"],
            }
        )
    return rows


def flat_activity_rows(corpus: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for site in corpus["sites"]:
        principal_source = next(
            source for source in site["sources"] if source["role"] == "notice_principale"
        )
        for activity in site["activites"]:
            activity_id = stable_uuid(
                "activite",
                site["site_id"],
                activity["ordre"],
                activity["activite_code"],
            )
            rows.append(
                {
                    "activite_id": activity_id,
                    "site_id": site["site_id"],
                    "reference_ia": site["reference_ia"],
                    "nom_site": site["nom_principal"],
                    "commune_actuelle_code_insee": site[
                        "commune_actuelle_code_insee"
                    ],
                    "commune_actuelle_nom": site["commune_actuelle_nom"],
                    "ordre": activity["ordre"],
                    "secteur_code": activity["secteur_code"],
                    "activite_code": activity["activite_code"],
                    "activite_libelle_source": activity["libelle_source"],
                    "installation_code": activity["installation_code"],
                    "debut_min": activity["debut_min"],
                    "debut_max": activity["debut_max"],
                    "debut_precision_code": activity["debut_precision_code"],
                    "debut_texte_source": activity["debut_texte_source"],
                    "fin_min": activity["fin_min"],
                    "fin_max": activity["fin_max"],
                    "fin_precision_code": activity["fin_precision_code"],
                    "fin_texte_source": activity["fin_texte_source"],
                    "periodes_codes": "|".join(activity["periodes_codes"]),
                    "periodes_libelles": "|".join(activity["periodes_libelles"]),
                    "periode_methode_code": activity["periode_methode_code"],
                    "siecles_source_site": "|".join(
                        activity["siecles_source_site"]
                    ),
                    "fiabilite_code": activity["fiabilite_code"],
                    "source_reference": activity["reference_source"],
                    "source_url": principal_source["url"],
                }
            )
    return rows


def _insert_sources(connection: duckdb.DuckDBPyConnection, registry: Mapping[str, Any]) -> None:
    for source in registry["sources"]:
        connection.execute(
            """
            INSERT INTO sources (
                source_id, titre, producteur, role_code, url_reference,
                methode_acces_code, statut_audit_code, date_dernier_audit, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                source["id"],
                source["name"],
                source["producer"],
                source["role"],
                source.get("url"),
                "|".join(source.get("access", [])) or None,
                source.get("audit_status", "a_auditer"),
                str(registry["updated_at"]),
                json.dumps(source.get("limits", []), ensure_ascii=False),
            ],
        )


def _insert_mention(
    connection: duckdb.DuckDBPyConnection,
    *,
    source_id: str,
    reference: str | None,
    url: str | None,
    entity_type: str,
    entity_id: str,
    field: str | None,
    original_value: Any,
    reliability: str,
) -> None:
    mention_id = stable_uuid("mention", source_id, reference, entity_type, entity_id, field)
    connection.execute(
        """
        INSERT INTO mentions_sources (
            mention_id, source_id, reference_source, url_precise,
            date_consultation, entite_type_code, entite_id, champ_cible,
            valeur_originale, valeur_normalisee, statut_valeur_code,
            nature_information_code, fiabilite_code, extracteur, version_extracteur
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?::JSON, ?::JSON, ?, ?, ?, ?, ?)
        """,
        [
            mention_id,
            source_id,
            reference,
            url,
            "2026-07-22T00:00:00+02:00",
            entity_type,
            entity_id,
            field,
            json.dumps(original_value, ensure_ascii=False),
            json.dumps(original_value, ensure_ascii=False),
            "renseignee" if original_value is not None else "non_renseignee_source",
            "sourcee",
            reliability,
            "patrimoine_orne.export.socle_v1",
            "1.0",
        ],
    )


def _format_number(value: float) -> str:
    return f"{value:.8f}".rstrip("0").rstrip(".")


def _ring_wkt(ring: Sequence[Sequence[float]]) -> str:
    return ", ".join(f"{_format_number(x)} {_format_number(y)}" for x, y in ring)


def geometry_to_lambert_wkt(
    geometry: Mapping[str, Any], transformer: Transformer
) -> str:
    kind = geometry["type"]
    coordinates = geometry["coordinates"]

    def project_ring(ring: Sequence[Sequence[float]]) -> list[list[float]]:
        return [list(transformer.transform(*point[:2])) for point in ring]

    if kind == "Point":
        x, y = transformer.transform(*coordinates[:2])
        return f"POINT ({_format_number(x)} {_format_number(y)})"
    if kind == "Polygon":
        rings = ", ".join(f"({_ring_wkt(project_ring(ring))})" for ring in coordinates)
        return f"POLYGON ({rings})"
    if kind == "MultiPolygon":
        polygons = []
        for polygon in coordinates:
            rings = ", ".join(
                f"({_ring_wkt(project_ring(ring))})" for ring in polygon
            )
            polygons.append(f"({rings})")
        return f"MULTIPOLYGON ({', '.join(polygons)})"
    raise ValueError(f"géométrie GeoJSON non prise en charge : {kind}")


def _insert_core_data(
    connection: duckdb.DuckDBPyConnection,
    corpus: Mapping[str, Any],
) -> None:
    to_lambert = Transformer.from_crs(4326, 2154, always_xy=True)
    sites_by_reference = {site["reference_ia"]: site for site in corpus["sites"]}

    for site in corpus["sites"]:
        site_id = site["site_id"]
        connection.execute(
            """
            INSERT INTO sites (
                site_id, nom_principal, niveau_structurel_code,
                commune_actuelle_code_insee, commune_actuelle_nom,
                commune_historique_nom, lieu_dit_principal, statut_corpus_code,
                decision_inclusion_code, fiabilite_code
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                site_id,
                site["nom_principal"],
                "site_principal",
                site["commune_actuelle_code_insee"],
                site["commune_actuelle_nom"],
                site["commune_historique_nom"],
                site["lieu_dit"],
                "cartographiable",
                site["decision_inclusion_code"],
                site["fiabilite_code"],
            ],
        )
        principal_source = next(
            source for source in site["sources"] if source["role"] == "notice_principale"
        )
        _insert_mention(
            connection,
            source_id=principal_source["source_id"],
            reference=principal_source["reference"],
            url=principal_source["url"],
            entity_type="sites",
            entity_id=site_id,
            field="nom_principal",
            original_value=site["nom_principal"],
            reliability=principal_source["fiabilite_code"],
        )
        connection.execute(
            """
            INSERT INTO identifiants_externes (
                identifiant_externe_id, source_id, type_identifiant_code, valeur,
                entite_type_code, entite_id, principal_pour_source,
                date_verification, fiabilite_code
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                stable_uuid("identifiant", "pop_merimee", site["reference_ia"]),
                "pop_merimee",
                "reference_ia",
                site["reference_ia"],
                "sites",
                site_id,
                True,
                "2026-07-22",
                "forte",
            ],
        )

        for activity in site["activites"]:
            activity_id = stable_uuid(
                "activite", site_id, activity["ordre"], activity["activite_code"]
            )
            connection.execute(
                """
                INSERT INTO activites (
                    activite_id, site_id, secteur_code, activite_code,
                    activite_libelle_source, type_installation_code,
                    debut_min, debut_max, debut_precision_code,
                    debut_texte_source, fin_min, fin_max, fin_precision_code,
                    fin_texte_source, principale, fiabilite_code, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    activity_id,
                    site_id,
                    activity["secteur_code"],
                    activity["activite_code"],
                    activity["libelle_source"],
                    activity["installation_code"],
                    activity["debut_min"],
                    activity["debut_max"],
                    activity["debut_precision_code"],
                    activity["debut_texte_source"],
                    activity["fin_min"],
                    activity["fin_max"],
                    activity["fin_precision_code"],
                    activity["fin_texte_source"],
                    activity["ordre"] == 1,
                    activity["fiabilite_code"],
                    activity["note"],
                ],
            )
            _insert_mention(
                connection,
                source_id=activity["source_id"],
                reference=activity["reference_source"],
                url=principal_source["url"],
                entity_type="activites",
                entity_id=activity_id,
                field="activite_libelle_source",
                original_value=activity["libelle_source"],
                reliability=activity["fiabilite_code"],
            )

        state = site["situation_actuelle"]
        state_id = stable_uuid("etat_actuel", site_id, state["date_verification"], 1)
        connection.execute(
            """
            INSERT INTO etats_actuels (
                etat_actuel_id, site_id, conservation_code, accessibilite_code,
                date_verification, methode_verification_code, fiabilite_code,
                version_numero, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                state_id,
                site_id,
                state["conservation_code"],
                state["accessibilite_code"],
                state["date_verification"],
                state["methode_verification_code"],
                state["fiabilite_code"],
                1,
                state["note"],
            ],
        )
        for index, usage in enumerate(state["usages"]):
            connection.execute(
                """
                INSERT INTO usages_actuels (
                    usage_actuel_id, etat_actuel_id, usage_code, principal
                ) VALUES (?, ?, ?, ?)
                """,
                [stable_uuid("usage", state_id, usage), state_id, usage, index == 0],
            )
        if state.get("source_id"):
            _insert_mention(
                connection,
                source_id=state["source_id"],
                reference=None,
                url=state.get("source_url"),
                entity_type="etats_actuels",
                entity_id=state_id,
                field="conservation_code",
                original_value=state["conservation_code"],
                reliability=state["fiabilite_code"],
            )

        if site.get("protection_mh_reference"):
            protection_id = stable_uuid(
                "protection", site_id, site["protection_mh_reference"]
            )
            protection_source = next(
                source
                for source in site["sources"]
                if source["role"] == "protection_confirmee"
            )
            connection.execute(
                """
                INSERT INTO protections (
                    protection_id, site_id, type_protection_code,
                    reference_protection, portee_code, statut_actuel_code,
                    date_verification
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    protection_id,
                    site_id,
                    "monument_historique",
                    site["protection_mh_reference"],
                    "inconnu",
                    "actif",
                    "2026-07-21",
                ],
            )
            _insert_mention(
                connection,
                source_id=protection_source["source_id"],
                reference=protection_source["reference"],
                url=protection_source["url"],
                entity_type="protections",
                entity_id=protection_id,
                field="reference_protection",
                original_value=site["protection_mh_reference"],
                reliability="forte",
            )

        location = site["localisation"]
        reference_geometry = location["geometrie_reference"]
        x, y = reference_geometry["point_lambert93"]
        geometry_id = stable_uuid("geometrie", site_id, "point_reference")
        connection.execute(
            """
            INSERT INTO geometries (
                geometrie_id, site_id, geom, type_geometrie_code,
                precision_geographique_code, methode_localisation_code,
                crs_source, geometrie_reference, usage_code, date_verification,
                fiabilite_code, notes
            ) VALUES (?, ?, ST_GeomFromText(?), ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                geometry_id,
                site_id,
                f"POINT ({_format_number(x)} {_format_number(y)})",
                "point_site",
                "point_approximatif",
                "coordonnees_source",
                "EPSG:2154",
                True,
                "affichage",
                "2026-07-22",
                "moyenne",
                "Point POP contrôlé, cible physique non vérifiée.",
            ],
        )
        _insert_mention(
            connection,
            source_id="pop_merimee",
            reference=site["reference_ia"],
            url=principal_source["url"],
            entity_type="geometries",
            entity_id=geometry_id,
            field="geom",
            original_value=reference_geometry["point_wgs84"],
            reliability="moyenne",
        )

        emprise = location.get("emprise_source")
        if emprise:
            if emprise.get("polygon_lambert93"):
                wkt = f"POLYGON (({_ring_wkt(emprise['polygon_lambert93'])}))"
            else:
                wkt = geometry_to_lambert_wkt(
                    {"type": "Polygon", "coordinates": [emprise["polygon_wgs84"]]},
                    to_lambert,
                )
            connection.execute(
                """
                INSERT INTO geometries (
                    geometrie_id, site_id, geom, type_geometrie_code,
                    precision_geographique_code, methode_localisation_code,
                    crs_source, geometrie_reference, usage_code,
                    date_verification, fiabilite_code, notes
                ) VALUES (?, ?, ST_GeomFromText(?), ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    stable_uuid("geometrie", site_id, "emprise_documentaire"),
                    site_id,
                    wkt,
                    "zone_documentaire",
                    "zone_documentaire",
                    "emprise_source",
                    emprise["crs_source"],
                    False,
                    "emprise_historique",
                    "2026-07-22",
                    "moyenne",
                    "Contour documentaire POP non vérifié sur le terrain actuel.",
                ],
            )

    for item in corpus["objets_techniques"]:
        object_id = stable_uuid("objet", item["reference_palissy"])
        connection.execute(
            """
            INSERT INTO objets_techniques (
                objet_technique_id, nom_principal, denomination_code,
                description, reference_palissy, fiabilite_code, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                object_id,
                item["nom_principal"],
                item["denomination_source"],
                item["description"],
                item["reference_palissy"],
                item["fiabilite_code"],
                f"Rapprochement {item['statut_rapprochement']} ; ensemble "
                f"{item['ensemble_reference']}.",
            ],
        )
        site = sites_by_reference[item["site_candidat_reference"]]
        link_id = stable_uuid("lien_objet_site", object_id, site["site_id"])
        connection.execute(
            """
            INSERT INTO liens_objets_sites (
                lien_objet_site_id, objet_technique_id, site_id,
                type_lien_code, fiabilite_code, notes
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                link_id,
                object_id,
                site["site_id"],
                item["type_lien_code"],
                item["fiabilite_code"],
                "Lien candidat conservé sans rattachement automatique.",
            ],
        )
        _insert_mention(
            connection,
            source_id=item["source_id"],
            reference=item["reference_palissy"],
            url=item["source_url"],
            entity_type="objets_techniques",
            entity_id=object_id,
            field="nom_principal",
            original_value=item["nom_principal"],
            reliability=item["fiabilite_code"],
        )
        connection.execute(
            """
            INSERT INTO identifiants_externes (
                identifiant_externe_id, source_id, type_identifiant_code, valeur,
                entite_type_code, entite_id, principal_pour_source,
                date_verification, fiabilite_code
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                stable_uuid("identifiant", "pop_palissy", item["reference_palissy"]),
                "pop_palissy",
                "reference_palissy",
                item["reference_palissy"],
                "objets_techniques",
                object_id,
                True,
                "2026-07-22",
                "forte",
            ],
        )


def _create_flat_table(
    connection: duckdb.DuckDBPyConnection,
    table_name: str,
    columns: Sequence[tuple[str, str]],
    rows: Sequence[Mapping[str, Any]],
) -> None:
    definitions = ", ".join(f"{name} {kind}" for name, kind in columns)
    connection.execute(f"CREATE TABLE {table_name} ({definitions})")
    names = [name for name, _ in columns]
    placeholders = ", ".join("?" for _ in names)
    connection.executemany(
        f"INSERT INTO {table_name} VALUES ({placeholders})",
        [[row[name] for name in names] for row in rows],
    )


def _create_activity_period_table(
    connection: duckdb.DuckDBPyConnection,
    activity_rows: Sequence[Mapping[str, Any]],
) -> None:
    connection.execute(
        """
        CREATE TABLE activites_periodes_v1 (
            activite_id VARCHAR NOT NULL,
            site_id VARCHAR NOT NULL,
            periode_code VARCHAR NOT NULL,
            periode_libelle VARCHAR NOT NULL,
            periode_methode_code VARCHAR NOT NULL,
            PRIMARY KEY (activite_id, periode_code)
        )
        """
    )
    values = []
    for row in activity_rows:
        codes = str(row["periodes_codes"]).split("|")
        labels = str(row["periodes_libelles"]).split("|")
        values.extend(
            (
                row["activite_id"],
                row["site_id"],
                code,
                label,
                row["periode_methode_code"],
            )
            for code, label in zip(codes, labels, strict=True)
        )
    connection.executemany(
        "INSERT INTO activites_periodes_v1 VALUES (?, ?, ?, ?, ?)", values
    )


def build_database(
    path: Path,
    corpus: Mapping[str, Any],
    site_rows: Sequence[Mapping[str, Any]],
    activity_rows: Sequence[Mapping[str, Any]],
    source_registry: Mapping[str, Any],
) -> dict[str, int]:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.unlink(missing_ok=True)
    connection = connect_database(path)
    try:
        initialize_database(connection)
        _insert_sources(connection, source_registry)
        _insert_core_data(connection, corpus)
        _create_flat_table(
            connection, "sites_export_v1", EXPORT_COLUMNS, site_rows
        )
        _create_flat_table(
            connection,
            "activites_export_v1",
            ACTIVITY_EXPORT_COLUMNS,
            activity_rows,
        )
        _create_activity_period_table(connection, activity_rows)
        assert_database_valid(connection)
        tables = (
            "sources",
            "sites",
            "activites",
            "etats_actuels",
            "usages_actuels",
            "protections",
            "objets_techniques",
            "liens_objets_sites",
            "geometries",
            "mentions_sources",
            "identifiants_externes",
            "sites_export_v1",
            "activites_export_v1",
            "activites_periodes_v1",
        )
        return {
            table: connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
            for table in tables
        }
    finally:
        connection.close()


def _sql_path(path: Path) -> str:
    return str(path.resolve()).replace("\\", "/").replace("'", "''")


def export_flat_files(
    database: Path,
    csv_path: Path,
    parquet_path: Path,
    geojson_path: Path,
    activities_csv_path: Path,
    activities_parquet_path: Path,
) -> None:
    for path in (
        csv_path,
        parquet_path,
        geojson_path,
        activities_csv_path,
        activities_parquet_path,
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.unlink(missing_ok=True)
    connection = duckdb.connect(str(database), read_only=True)
    try:
        connection.execute(
            f"COPY sites_export_v1 TO '{_sql_path(csv_path)}' "
            "(FORMAT CSV, HEADER true, DELIMITER ',')"
        )
        connection.execute(
            f"COPY sites_export_v1 TO '{_sql_path(parquet_path)}' "
            "(FORMAT PARQUET, COMPRESSION ZSTD)"
        )
        connection.execute(
            f"COPY activites_export_v1 TO '{_sql_path(activities_csv_path)}' "
            "(FORMAT CSV, HEADER true, DELIMITER ',')"
        )
        connection.execute(
            f"COPY activites_export_v1 TO '{_sql_path(activities_parquet_path)}' "
            "(FORMAT PARQUET, COMPRESSION ZSTD)"
        )
        names = [name for name, _ in EXPORT_COLUMNS]
        rows = [dict(zip(names, row)) for row in connection.execute(
            "SELECT * FROM sites_export_v1 ORDER BY reference_ia"
        ).fetchall()]
    finally:
        connection.close()

    features = []
    for row in rows:
        properties = dict(row)
        longitude = properties.pop("longitude")
        latitude = properties.pop("latitude")
        if properties.get("situation_verifiee_le") is not None:
            properties["situation_verifiee_le"] = str(
                properties["situation_verifiee_le"]
            )
        features.append(
            {
                "type": "Feature",
                "id": row["site_id"],
                "properties": properties,
                "geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude],
                },
            }
        )
    write_json({"type": "FeatureCollection", "features": features}, geojson_path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_outputs(
    database: Path,
    csv_path: Path,
    parquet_path: Path,
    geojson_path: Path,
    activities_csv_path: Path,
    activities_parquet_path: Path,
    consolidated_path: Path,
    table_counts: Mapping[str, int],
) -> dict[str, Any]:
    with csv_path.open(encoding="utf-8-sig", newline="") as stream:
        csv_rows = list(csv.DictReader(stream))
    with activities_csv_path.open(encoding="utf-8-sig", newline="") as stream:
        activity_csv_rows = list(csv.DictReader(stream))
    connection = duckdb.connect(str(database), read_only=True)
    try:
        parquet_ids = {
            str(row[0])
            for row in connection.execute(
                f"SELECT site_id FROM read_parquet('{_sql_path(parquet_path)}')"
            ).fetchall()
        }
        activity_parquet_ids = {
            str(row[0])
            for row in connection.execute(
                "SELECT activite_id FROM "
                f"read_parquet('{_sql_path(activities_parquet_path)}')"
            ).fetchall()
        }
        database_activities_with_dates = connection.execute(
            """
            SELECT count(*)
            FROM activites
            WHERE debut_min IS NOT NULL
               OR debut_max IS NOT NULL
               OR fin_min IS NOT NULL
               OR fin_max IS NOT NULL
            """
        ).fetchone()[0]
    finally:
        connection.close()
    geojson = load_json(geojson_path)
    consolidated = load_json(consolidated_path)
    csv_ids = {row["site_id"] for row in csv_rows}
    geojson_ids = {str(feature["id"]) for feature in geojson["features"]}
    corpus_ids = {str(site["site_id"]) for site in consolidated["sites"]}
    errors = []
    if not (len(csv_rows) == len(geojson["features"]) == len(corpus_ids) == 30):
        errors.append("les exports ne contiennent pas exactement 30 sites")
    if not (csv_ids == parquet_ids == geojson_ids == corpus_ids):
        errors.append("les identifiants diffèrent entre les formats")
    if table_counts["sites"] != 30 or table_counts["activites"] != 47:
        errors.append("les effectifs du modèle relationnel sont incohérents")
    activity_csv_ids = {row["activite_id"] for row in activity_csv_rows}
    if len(activity_csv_rows) != 47:
        errors.append("l'export des activités ne contient pas exactement 47 phases")
    if activity_csv_ids != activity_parquet_ids:
        errors.append("les identifiants d'activité diffèrent entre CSV et Parquet")
    if any(not row["periodes_codes"] for row in csv_rows):
        errors.append("un site ne possède aucune période filtrable")
    sites_with_contemporary_period = sum(
        "periode_contemporaine" in row["periodes_codes"].split("|")
        for row in csv_rows
    )
    if sites_with_contemporary_period != 4:
        errors.append("les quatre situations actuelles sourcées ne sont pas datées")
    if any(not row["periodes_codes"] for row in activity_csv_rows):
        errors.append("une activité ne possède aucune période filtrable")
    if table_counts["activites_periodes_v1"] < 47:
        errors.append("la relation activité-période est incomplète")
    if database_activities_with_dates != 30:
        errors.append("DuckDB ne contient pas les 30 chronologies normalisées attendues")
    paths = (
        database,
        csv_path,
        parquet_path,
        geojson_path,
        activities_csv_path,
        activities_parquet_path,
        consolidated_path,
    )
    return {
        "schema_version": "1.1",
        "date_validation": "2026-07-22",
        "checks_passed": not errors,
        "errors": errors,
        "table_counts": dict(table_counts),
        "export_counts": {
            "csv": len(csv_rows),
            "parquet": len(parquet_ids),
            "geojson": len(geojson["features"]),
            "corpus_consolide": len(corpus_ids),
            "activites_csv": len(activity_csv_rows),
            "activites_parquet": len(activity_parquet_ids),
        },
        "identifiants_concordants": not errors,
        "chronologie": {
            "sites_avec_periodes_filtrables": sum(
                bool(row["periodes_codes"]) for row in csv_rows
            ),
            "sites_avec_periode_contemporaine_sourcee": (
                sites_with_contemporary_period
            ),
            "activites_avec_periodes_filtrables": sum(
                bool(row["periodes_codes"]) for row in activity_csv_rows
            ),
            "activites_avec_dates_normalisees": database_activities_with_dates,
            "activites_par_chronologie_phase": sum(
                row["periode_methode_code"] == "chronologie_phase"
                for row in activity_csv_rows
            ),
            "activites_par_siecles_source": sum(
                row["periode_methode_code"] == "siecles_source_site"
                for row in activity_csv_rows
            ),
        },
        "files": {
            str(path).replace("\\", "/"): {
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in paths
        },
        "decision": "bloc_consolidation_phase7_valide" if not errors else "invalide",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=Path("data/pilot/corpus_pilote_v1.json"))
    parser.add_argument(
        "--locations", type=Path, default=Path("data/pilot/localisations_pilote_phase6.json")
    )
    parser.add_argument(
        "--context", type=Path, default=Path("data/pilot/contexte_territorial_phase6.json")
    )
    parser.add_argument(
        "--cartographic-control",
        type=Path,
        default=Path("reports/quality/phase6_controle_cartographique.json"),
    )
    parser.add_argument("--sources", type=Path, default=Path("config/sources.yml"))
    parser.add_argument(
        "--consolidated",
        type=Path,
        default=Path("data/processed/corpus_pilote_socle_v1.json"),
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=Path("data/processed/patrimoine_orne_socle_v1.duckdb"),
    )
    parser.add_argument("--csv", type=Path, default=Path("data/exports/sites_pilote_v1.csv"))
    parser.add_argument(
        "--parquet", type=Path, default=Path("data/exports/sites_pilote_v1.parquet")
    )
    parser.add_argument(
        "--geojson", type=Path, default=Path("data/exports/sites_pilote_v1.geojson")
    )
    parser.add_argument(
        "--activities-csv",
        type=Path,
        default=Path("data/exports/activites_pilote_v1.csv"),
    )
    parser.add_argument(
        "--activities-parquet",
        type=Path,
        default=Path("data/exports/activites_pilote_v1.parquet"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/quality/phase7_consolidation.json"),
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    consolidated = consolidate_corpus(
        load_json(args.corpus),
        load_json(args.locations),
        load_json(args.context),
        load_json(args.cartographic_control),
    )
    write_json(consolidated, args.consolidated)
    site_rows = flat_rows(consolidated)
    activity_rows = flat_activity_rows(consolidated)
    table_counts = build_database(
        args.database,
        consolidated,
        site_rows,
        activity_rows,
        load_yaml(args.sources),
    )
    export_flat_files(
        args.database,
        args.csv,
        args.parquet,
        args.geojson,
        args.activities_csv,
        args.activities_parquet,
    )
    report = validate_outputs(
        args.database,
        args.csv,
        args.parquet,
        args.geojson,
        args.activities_csv,
        args.activities_parquet,
        args.consolidated,
        table_counts,
    )
    write_json(report, args.report)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    if not report["checks_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
