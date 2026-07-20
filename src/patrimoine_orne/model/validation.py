"""Validations transversales impossibles a exprimer par de simples CHECK SQL."""

from __future__ import annotations

from dataclasses import dataclass

import duckdb


@dataclass(frozen=True)
class ValidationIssue:
    """Anomalie structurelle detectee dans une base du projet."""

    code: str
    table: str
    record_id: str
    message: str


class DatabaseValidationError(ValueError):
    """Erreur levee lorsqu'une base ne respecte pas le modele."""


TARGETS = {
    "activites": ("activites", "activite_id"),
    "energies_activites": ("energies_activites", "energie_activite_id"),
    "etats_actuels": ("etats_actuels", "etat_actuel_id"),
    "exploitants": ("exploitants", "exploitant_id"),
    "exploitations": ("exploitations", "exploitation_id"),
    "geometries": ("geometries", "geometrie_id"),
    "liens_objets_sites": ("liens_objets_sites", "lien_objet_site_id"),
    "noms_exploitants": ("noms_exploitants", "nom_exploitant_id"),
    "noms_sites": ("noms_sites", "nom_site_id"),
    "objets_techniques": ("objets_techniques", "objet_technique_id"),
    "protections": ("protections", "protection_id"),
    "propositions_rapprochement": (
        "propositions_rapprochement",
        "proposition_rapprochement_id",
    ),
    "relations_sites": ("relations_sites", "relation_site_id"),
    "sites": ("sites", "site_id"),
}


def _rows(connection: duckdb.DuckDBPyConnection, query: str) -> list[tuple]:
    return connection.execute(query).fetchall()


def _validate_generic_targets(
    connection: duckdb.DuckDBPyConnection,
    issues: list[ValidationIssue],
    association_table: str,
    id_column: str,
    *,
    require_active: bool,
) -> None:
    rows = _rows(
        connection,
        f"SELECT {id_column}, entite_type_code, entite_id "
        f"FROM {association_table} WHERE statut_enregistrement_code = 'actif'",
    )
    for association_id, entity_type, entity_id in rows:
        if entity_type not in TARGETS:
            issues.append(
                ValidationIssue(
                    "TYPE_CIBLE_INCONNU",
                    association_table,
                    str(association_id),
                    f"Type de cible non autorise : {entity_type!r}.",
                )
            )
            continue
        target_table, target_id = TARGETS[entity_type]
        active_clause = " AND statut_enregistrement_code = 'actif'" if require_active else ""
        exists = connection.execute(
            f"SELECT 1 FROM {target_table} "
            f"WHERE {target_id} = ?{active_clause} LIMIT 1",
            [entity_id],
        ).fetchone()
        if not exists:
            issues.append(
                ValidationIssue(
                    "CIBLE_ABSENTE",
                    association_table,
                    str(association_id),
                    f"La cible attendue {entity_type}/{entity_id} n'existe pas.",
                )
            )


def _validate_mention_fields(
    connection: duckdb.DuckDBPyConnection, issues: list[ValidationIssue]
) -> None:
    columns_by_table = {
        entity_type: {
            row[0]
            for row in connection.execute(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_schema = 'main' AND table_name = ?",
                [table_name],
            ).fetchall()
        }
        for entity_type, (table_name, _) in TARGETS.items()
    }
    for mention_id, entity_type, field_name in _rows(
        connection,
        """
        SELECT mention_id, entite_type_code, champ_cible
        FROM mentions_sources
        WHERE statut_enregistrement_code = 'actif' AND champ_cible IS NOT NULL
        """,
    ):
        if entity_type in columns_by_table and field_name not in columns_by_table[entity_type]:
            issues.append(
                ValidationIssue(
                    "CHAMP_CIBLE_INCONNU",
                    "mentions_sources",
                    str(mention_id),
                    f"Le champ {entity_type}.{field_name} n'existe pas.",
                )
            )


def validate_database(connection: duckdb.DuckDBPyConnection) -> list[ValidationIssue]:
    """Retourne toutes les incoherences transversales detectees."""
    issues: list[ValidationIssue] = []

    _validate_generic_targets(
        connection,
        issues,
        "mentions_sources",
        "mention_id",
        require_active=False,
    )
    _validate_generic_targets(
        connection,
        issues,
        "identifiants_externes",
        "identifiant_externe_id",
        require_active=True,
    )
    _validate_mention_fields(connection, issues)

    for site_id, commune_code, commune_name in _rows(
        connection,
        """
        SELECT site_id, commune_actuelle_code_insee, commune_actuelle_nom
        FROM sites
        WHERE statut_enregistrement_code = 'actif'
          AND decision_inclusion_code = 'inclus'
        """,
    ):
        if not commune_code or not commune_name:
            issues.append(
                ValidationIssue(
                    "SITE_INCLUS_SANS_COMMUNE",
                    "sites",
                    str(site_id),
                    "Un site inclus doit avoir un code INSEE et un nom de commune.",
                )
            )
        activity = connection.execute(
            "SELECT 1 FROM activites WHERE site_id = ? "
            "AND statut_enregistrement_code = 'actif' LIMIT 1",
            [site_id],
        ).fetchone()
        if not activity:
            issues.append(
                ValidationIssue(
                    "SITE_INCLUS_SANS_ACTIVITE",
                    "sites",
                    str(site_id),
                    "Un site inclus doit avoir au moins une activite active.",
                )
            )
        mention = connection.execute(
            "SELECT 1 FROM mentions_sources WHERE entite_type_code = 'sites' "
            "AND entite_id = ? AND statut_enregistrement_code = 'actif' LIMIT 1",
            [site_id],
        ).fetchone()
        if not mention:
            issues.append(
                ValidationIssue(
                    "SITE_INCLUS_SANS_SOURCE",
                    "sites",
                    str(site_id),
                    "Un site inclus doit avoir au moins une mention de source active.",
                )
            )

    for (site_id,) in _rows(
        connection,
        """
        SELECT site_id
        FROM sites
        WHERE statut_enregistrement_code = 'actif'
          AND statut_corpus_code IN ('cartographiable', 'publie')
          AND NOT EXISTS (
              SELECT 1 FROM geometries
              WHERE geometries.site_id = sites.site_id
                AND geometries.geometrie_reference
                AND geometries.statut_enregistrement_code = 'actif'
          )
        """,
    ):
        issues.append(
            ValidationIssue(
                "SITE_CARTOGRAPHIABLE_SANS_GEOMETRIE",
                "sites",
                str(site_id),
                "Un site cartographiable ou publie doit avoir une geometrie de reference.",
            )
        )

    for (site_id,) in _rows(
        connection,
        """
        SELECT site_id
        FROM sites
        WHERE statut_enregistrement_code = 'actif'
          AND statut_corpus_code = 'publie'
          AND nullif(trim(nom_principal), '') IS NULL
        """,
    ):
        issues.append(
            ValidationIssue(
                "SITE_PUBLIE_SANS_NOM",
                "sites",
                str(site_id),
                "Un site publie doit avoir un nom principal.",
            )
        )

    for site_id, usage_code, count in _rows(
        connection,
        """
        SELECT site_id, usage_code, count(*)
        FROM geometries
        WHERE statut_enregistrement_code = 'actif' AND geometrie_reference
        GROUP BY site_id, usage_code
        HAVING count(*) > 1
        """,
    ):
        issues.append(
            ValidationIssue(
                "PLUSIEURS_GEOMETRIES_REFERENCE",
                "geometries",
                str(site_id),
                f"{count} geometries de reference actives pour l'usage {usage_code!r}.",
            )
        )

    for geometry_id in _rows(
        connection,
        """
        SELECT geometrie_id
        FROM geometries
        WHERE statut_enregistrement_code = 'actif'
          AND (ST_IsEmpty(geom) OR NOT ST_IsValid(geom))
        """,
    ):
        issues.append(
            ValidationIssue(
                "GEOMETRIE_INVALIDE",
                "geometries",
                str(geometry_id[0]),
                "La geometrie est vide ou invalide.",
            )
        )

    for exploitation_id in _rows(
        connection,
        """
        SELECT exploitation.exploitation_id
        FROM exploitations AS exploitation
        JOIN activites AS activite ON activite.activite_id = exploitation.activite_id
        WHERE exploitation.statut_enregistrement_code = 'actif'
          AND exploitation.site_id <> activite.site_id
        """,
    ):
        issues.append(
            ValidationIssue(
                "ACTIVITE_HORS_SITE_EXPLOITATION",
                "exploitations",
                str(exploitation_id[0]),
                "L'activite rattachee a l'exploitation appartient a un autre site.",
            )
        )

    for state_id in _rows(
        connection,
        """
        SELECT nouveau.etat_actuel_id
        FROM etats_actuels AS nouveau
        JOIN etats_actuels AS ancien
          ON ancien.etat_actuel_id = nouveau.remplace_etat_actuel_id
        WHERE nouveau.site_id <> ancien.site_id
           OR nouveau.version_numero <= ancien.version_numero
        """,
    ):
        issues.append(
            ValidationIssue(
                "REMPLACEMENT_ETAT_INCOHERENT",
                "etats_actuels",
                str(state_id[0]),
                "L'etat remplace doit appartenir au meme site et avoir une version anterieure.",
            )
        )

    symmetric_type = "partage_infrastructure_avec"
    for relation_id in _rows(
        connection,
        """
        SELECT relation_site_id
        FROM relations_sites
        WHERE statut_enregistrement_code = 'actif'
          AND type_relation_code = 'partage_infrastructure_avec'
          AND CAST(site_source_id AS VARCHAR) > CAST(site_cible_id AS VARCHAR)
        """,
    ):
        issues.append(
            ValidationIssue(
                "RELATION_SYMETRIQUE_NON_CANONIQUE",
                "relations_sites",
                str(relation_id[0]),
                f"Les UUID de la relation {symmetric_type!r} doivent etre tries.",
            )
        )

    for proposition_id in _rows(
        connection,
        """
        SELECT proposition_rapprochement_id
        FROM propositions_rapprochement
        WHERE statut_enregistrement_code = 'actif'
          AND CAST(site_a_id AS VARCHAR) > CAST(site_b_id AS VARCHAR)
        """,
    ):
        issues.append(
            ValidationIssue(
                "RAPPROCHEMENT_NON_CANONIQUE",
                "propositions_rapprochement",
                str(proposition_id[0]),
                "Les deux UUID d'une proposition doivent etre tries.",
            )
        )

    for proposition_id in _rows(
        connection,
        """
        SELECT proposition.proposition_rapprochement_id
        FROM propositions_rapprochement AS proposition
        JOIN sites AS site_a ON site_a.site_id = proposition.site_a_id
        JOIN sites AS site_b ON site_b.site_id = proposition.site_b_id
        WHERE proposition.statut_enregistrement_code = 'actif'
          AND proposition.statut_decision_code = 'a_verifier'
          AND (
              site_a.statut_enregistrement_code = 'fusionne'
              OR site_b.statut_enregistrement_code = 'fusionne'
          )
        """,
    ):
        issues.append(
            ValidationIssue(
                "RAPPROCHEMENT_OUVERT_SUR_SITE_FUSIONNE",
                "propositions_rapprochement",
                str(proposition_id[0]),
                "Une proposition ouverte ne peut pas viser un site deja fusionne.",
            )
        )

    for proposition_id in _rows(
        connection,
        """
        SELECT proposition.proposition_rapprochement_id
        FROM propositions_rapprochement AS proposition
        JOIN sites AS site_a ON site_a.site_id = proposition.site_a_id
        JOIN sites AS site_b ON site_b.site_id = proposition.site_b_id
        WHERE proposition.statut_enregistrement_code = 'actif'
          AND proposition.statut_decision_code = 'confirme_meme_site'
          AND NOT (
              (
                  proposition.site_canonique_id = site_a.site_id
                  AND site_a.statut_enregistrement_code = 'actif'
                  AND site_b.statut_enregistrement_code = 'fusionne'
                  AND site_b.site_id_canonique = site_a.site_id
              )
              OR (
                  proposition.site_canonique_id = site_b.site_id
                  AND site_b.statut_enregistrement_code = 'actif'
                  AND site_a.statut_enregistrement_code = 'fusionne'
                  AND site_a.site_id_canonique = site_b.site_id
              )
          )
        """,
    ):
        issues.append(
            ValidationIssue(
                "RAPPROCHEMENT_CONFIRME_SANS_FUSION",
                "propositions_rapprochement",
                str(proposition_id[0]),
                "La confirmation doit fusionner l'autre site vers le site canonique.",
            )
        )

    return issues


def assert_database_valid(connection: duckdb.DuckDBPyConnection) -> None:
    """Leve une erreur lisible si la base contient au moins une anomalie."""
    issues = validate_database(connection)
    if not issues:
        return
    details = "\n".join(
        f"- [{issue.code}] {issue.table}/{issue.record_id}: {issue.message}"
        for issue in issues
    )
    raise DatabaseValidationError(
        f"La base contient {len(issues)} anomalie(s) de validation :\n{details}"
    )
