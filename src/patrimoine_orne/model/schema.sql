CREATE TABLE IF NOT EXISTS schema_metadata (
    schema_version VARCHAR PRIMARY KEY,
    installed_at TIMESTAMPTZ NOT NULL DEFAULT current_timestamp
);

DELETE FROM schema_metadata;
INSERT INTO schema_metadata (schema_version) VALUES ('1.0.0');

CREATE TABLE IF NOT EXISTS sources (
    source_id VARCHAR PRIMARY KEY,
    titre VARCHAR NOT NULL,
    producteur VARCHAR NOT NULL,
    role_code VARCHAR NOT NULL,
    url_reference VARCHAR,
    methode_acces_code VARCHAR,
    licence_donnees VARCHAR,
    droits_medias VARCHAR,
    statut_audit_code VARCHAR NOT NULL,
    date_dernier_audit DATE,
    notes VARCHAR,
    statut_enregistrement_code VARCHAR NOT NULL DEFAULT 'actif',
    cree_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    cree_par VARCHAR NOT NULL DEFAULT 'systeme',
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    CHECK (regexp_full_match(source_id, '[a-z][a-z0-9_]*')),
    CHECK (statut_enregistrement_code IN ('actif', 'archive', 'annule'))
);

CREATE TABLE IF NOT EXISTS sites (
    site_id UUID PRIMARY KEY DEFAULT uuid(),
    site_id_canonique UUID,
    nom_principal VARCHAR,
    niveau_structurel_code VARCHAR,
    commune_actuelle_code_insee VARCHAR,
    commune_actuelle_nom VARCHAR,
    commune_historique_nom VARCHAR,
    lieu_dit_principal VARCHAR,
    statut_corpus_code VARCHAR NOT NULL,
    decision_inclusion_code VARCHAR NOT NULL,
    motif_decision VARCHAR,
    fiabilite_code VARCHAR NOT NULL,
    notes_internes VARCHAR,
    statut_enregistrement_code VARCHAR NOT NULL DEFAULT 'actif',
    cree_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    cree_par VARCHAR NOT NULL DEFAULT 'systeme',
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    FOREIGN KEY (site_id_canonique) REFERENCES sites(site_id),
    CHECK (site_id_canonique IS NULL OR site_id_canonique <> site_id),
    CHECK (commune_actuelle_code_insee IS NULL OR regexp_full_match(commune_actuelle_code_insee, '[0-9]{5}')),
    CHECK (statut_corpus_code IN ('candidat', 'rapproche', 'cartographiable', 'publie', 'exclu')),
    CHECK (decision_inclusion_code IN ('inclus', 'exclu', 'a_verifier')),
    CHECK (statut_enregistrement_code IN ('actif', 'fusionne', 'annule')),
    CHECK (
        (statut_enregistrement_code = 'fusionne' AND site_id_canonique IS NOT NULL)
        OR (statut_enregistrement_code <> 'fusionne' AND site_id_canonique IS NULL)
    )
);

CREATE TABLE IF NOT EXISTS noms_sites (
    nom_site_id UUID PRIMARY KEY DEFAULT uuid(),
    site_id UUID NOT NULL REFERENCES sites(site_id),
    nom VARCHAR NOT NULL,
    type_nom_code VARCHAR NOT NULL,
    debut_min DATE,
    debut_max DATE,
    debut_precision_code VARCHAR,
    debut_texte_source VARCHAR,
    fin_min DATE,
    fin_max DATE,
    fin_precision_code VARCHAR,
    fin_texte_source VARCHAR,
    fiabilite_code VARCHAR NOT NULL,
    statut_enregistrement_code VARCHAR NOT NULL DEFAULT 'actif',
    cree_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    cree_par VARCHAR NOT NULL DEFAULT 'systeme',
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    CHECK (debut_min IS NULL OR debut_max IS NULL OR debut_min <= debut_max),
    CHECK (fin_min IS NULL OR fin_max IS NULL OR fin_min <= fin_max)
);

CREATE TABLE IF NOT EXISTS activites (
    activite_id UUID PRIMARY KEY DEFAULT uuid(),
    site_id UUID NOT NULL REFERENCES sites(site_id),
    secteur_code VARCHAR,
    activite_code VARCHAR,
    activite_libelle_source VARCHAR,
    type_installation_code VARCHAR,
    debut_min DATE,
    debut_max DATE,
    debut_precision_code VARCHAR,
    debut_texte_source VARCHAR,
    fin_min DATE,
    fin_max DATE,
    fin_precision_code VARCHAR,
    fin_texte_source VARCHAR,
    principale BOOLEAN NOT NULL DEFAULT false,
    fiabilite_code VARCHAR NOT NULL,
    notes VARCHAR,
    statut_enregistrement_code VARCHAR NOT NULL DEFAULT 'actif',
    cree_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    cree_par VARCHAR NOT NULL DEFAULT 'systeme',
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    CHECK (activite_code IS NOT NULL OR nullif(trim(activite_libelle_source), '') IS NOT NULL),
    CHECK (debut_min IS NULL OR debut_max IS NULL OR debut_min <= debut_max),
    CHECK (fin_min IS NULL OR fin_max IS NULL OR fin_min <= fin_max),
    CHECK (debut_min IS NULL OR fin_max IS NULL OR debut_min <= fin_max)
);

CREATE TABLE IF NOT EXISTS energies_activites (
    energie_activite_id UUID PRIMARY KEY DEFAULT uuid(),
    activite_id UUID NOT NULL REFERENCES activites(activite_id),
    energie_code VARCHAR NOT NULL,
    role_energie_code VARCHAR,
    debut_min DATE,
    debut_max DATE,
    debut_precision_code VARCHAR,
    debut_texte_source VARCHAR,
    fin_min DATE,
    fin_max DATE,
    fin_precision_code VARCHAR,
    fin_texte_source VARCHAR,
    fiabilite_code VARCHAR NOT NULL,
    statut_enregistrement_code VARCHAR NOT NULL DEFAULT 'actif',
    cree_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    cree_par VARCHAR NOT NULL DEFAULT 'systeme',
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    CHECK (debut_min IS NULL OR debut_max IS NULL OR debut_min <= debut_max),
    CHECK (fin_min IS NULL OR fin_max IS NULL OR fin_min <= fin_max)
);

CREATE TABLE IF NOT EXISTS etats_actuels (
    etat_actuel_id UUID PRIMARY KEY DEFAULT uuid(),
    site_id UUID NOT NULL REFERENCES sites(site_id),
    conservation_code VARCHAR,
    usage_actuel_code VARCHAR,
    accessibilite_code VARCHAR,
    date_verification DATE NOT NULL,
    methode_verification_code VARCHAR NOT NULL,
    fiabilite_code VARCHAR NOT NULL,
    version_numero INTEGER NOT NULL,
    remplace_etat_actuel_id UUID,
    motif_version_code VARCHAR NOT NULL DEFAULT 'nouvelle_observation',
    enregistre_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    notes VARCHAR,
    statut_enregistrement_code VARCHAR NOT NULL DEFAULT 'actif',
    cree_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    cree_par VARCHAR NOT NULL DEFAULT 'systeme',
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    FOREIGN KEY (remplace_etat_actuel_id) REFERENCES etats_actuels(etat_actuel_id),
    UNIQUE (site_id, version_numero),
    CHECK (version_numero > 0),
    CHECK (motif_version_code IN ('nouvelle_observation', 'correction', 'annulation')),
    CHECK (
        motif_version_code = 'annulation'
        OR conservation_code IS NOT NULL
        OR usage_actuel_code IS NOT NULL
        OR accessibilite_code IS NOT NULL
    ),
    CHECK (
        motif_version_code <> 'annulation'
        OR remplace_etat_actuel_id IS NOT NULL
    )
);

CREATE TABLE IF NOT EXISTS exploitants (
    exploitant_id UUID PRIMARY KEY DEFAULT uuid(),
    nom_principal VARCHAR NOT NULL,
    type_exploitant_code VARCHAR NOT NULL,
    identifiant_externe VARCHAR,
    notes VARCHAR,
    statut_enregistrement_code VARCHAR NOT NULL DEFAULT 'actif',
    cree_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    cree_par VARCHAR NOT NULL DEFAULT 'systeme',
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS noms_exploitants (
    nom_exploitant_id UUID PRIMARY KEY DEFAULT uuid(),
    exploitant_id UUID NOT NULL REFERENCES exploitants(exploitant_id),
    nom VARCHAR NOT NULL,
    debut_min DATE,
    debut_max DATE,
    debut_precision_code VARCHAR,
    debut_texte_source VARCHAR,
    fin_min DATE,
    fin_max DATE,
    fin_precision_code VARCHAR,
    fin_texte_source VARCHAR,
    fiabilite_code VARCHAR NOT NULL,
    statut_enregistrement_code VARCHAR NOT NULL DEFAULT 'actif',
    cree_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    cree_par VARCHAR NOT NULL DEFAULT 'systeme',
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    CHECK (debut_min IS NULL OR debut_max IS NULL OR debut_min <= debut_max),
    CHECK (fin_min IS NULL OR fin_max IS NULL OR fin_min <= fin_max)
);

CREATE TABLE IF NOT EXISTS exploitations (
    exploitation_id UUID PRIMARY KEY DEFAULT uuid(),
    site_id UUID NOT NULL REFERENCES sites(site_id),
    exploitant_id UUID NOT NULL REFERENCES exploitants(exploitant_id),
    activite_id UUID REFERENCES activites(activite_id),
    role_code VARCHAR NOT NULL,
    debut_min DATE,
    debut_max DATE,
    debut_precision_code VARCHAR,
    debut_texte_source VARCHAR,
    fin_min DATE,
    fin_max DATE,
    fin_precision_code VARCHAR,
    fin_texte_source VARCHAR,
    fiabilite_code VARCHAR NOT NULL,
    notes VARCHAR,
    statut_enregistrement_code VARCHAR NOT NULL DEFAULT 'actif',
    cree_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    cree_par VARCHAR NOT NULL DEFAULT 'systeme',
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    CHECK (debut_min IS NULL OR debut_max IS NULL OR debut_min <= debut_max),
    CHECK (fin_min IS NULL OR fin_max IS NULL OR fin_min <= fin_max)
);

CREATE TABLE IF NOT EXISTS objets_techniques (
    objet_technique_id UUID PRIMARY KEY DEFAULT uuid(),
    nom_principal VARCHAR,
    denomination_code VARCHAR,
    description VARCHAR,
    fabricant VARCHAR,
    date_creation_min DATE,
    date_creation_max DATE,
    date_creation_precision_code VARCHAR,
    date_creation_texte_source VARCHAR,
    reference_palissy VARCHAR,
    etat_conservation_code VARCHAR,
    date_verification DATE,
    fiabilite_code VARCHAR NOT NULL,
    notes VARCHAR,
    statut_enregistrement_code VARCHAR NOT NULL DEFAULT 'actif',
    cree_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    cree_par VARCHAR NOT NULL DEFAULT 'systeme',
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    CHECK (nom_principal IS NOT NULL OR denomination_code IS NOT NULL),
    CHECK (
        date_creation_min IS NULL
        OR date_creation_max IS NULL
        OR date_creation_min <= date_creation_max
    )
);

CREATE TABLE IF NOT EXISTS liens_objets_sites (
    lien_objet_site_id UUID PRIMARY KEY DEFAULT uuid(),
    objet_technique_id UUID NOT NULL REFERENCES objets_techniques(objet_technique_id),
    site_id UUID NOT NULL REFERENCES sites(site_id),
    type_lien_code VARCHAR NOT NULL,
    debut_min DATE,
    debut_max DATE,
    debut_precision_code VARCHAR,
    debut_texte_source VARCHAR,
    fin_min DATE,
    fin_max DATE,
    fin_precision_code VARCHAR,
    fin_texte_source VARCHAR,
    fiabilite_code VARCHAR NOT NULL,
    notes VARCHAR,
    statut_enregistrement_code VARCHAR NOT NULL DEFAULT 'actif',
    cree_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    cree_par VARCHAR NOT NULL DEFAULT 'systeme',
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    CHECK (debut_min IS NULL OR debut_max IS NULL OR debut_min <= debut_max),
    CHECK (fin_min IS NULL OR fin_max IS NULL OR fin_min <= fin_max)
);

CREATE TABLE IF NOT EXISTS protections (
    protection_id UUID PRIMARY KEY DEFAULT uuid(),
    site_id UUID REFERENCES sites(site_id),
    objet_technique_id UUID REFERENCES objets_techniques(objet_technique_id),
    type_protection_code VARCHAR NOT NULL,
    reference_protection VARCHAR NOT NULL,
    date_protection_min DATE,
    date_protection_max DATE,
    date_protection_precision_code VARCHAR,
    date_protection_texte_source VARCHAR,
    element_protege VARCHAR,
    portee VARCHAR,
    statut_actuel_code VARCHAR,
    date_verification DATE NOT NULL,
    statut_enregistrement_code VARCHAR NOT NULL DEFAULT 'actif',
    cree_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    cree_par VARCHAR NOT NULL DEFAULT 'systeme',
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    UNIQUE (reference_protection),
    CHECK (
        (site_id IS NOT NULL AND objet_technique_id IS NULL)
        OR (site_id IS NULL AND objet_technique_id IS NOT NULL)
    ),
    CHECK (
        date_protection_min IS NULL
        OR date_protection_max IS NULL
        OR date_protection_min <= date_protection_max
    )
);

CREATE TABLE IF NOT EXISTS geometries (
    geometrie_id UUID PRIMARY KEY DEFAULT uuid(),
    site_id UUID NOT NULL REFERENCES sites(site_id),
    geom GEOMETRY NOT NULL,
    crs_normalise INTEGER NOT NULL DEFAULT 2154,
    type_geometrie_code VARCHAR NOT NULL,
    precision_geographique_code VARCHAR NOT NULL,
    methode_localisation_code VARCHAR NOT NULL,
    crs_source VARCHAR,
    geometrie_reference BOOLEAN NOT NULL DEFAULT false,
    usage_code VARCHAR NOT NULL DEFAULT 'affichage',
    date_geometrie_min DATE,
    date_geometrie_max DATE,
    date_geometrie_precision_code VARCHAR,
    date_geometrie_texte_source VARCHAR,
    date_verification DATE,
    fiabilite_code VARCHAR NOT NULL,
    notes VARCHAR,
    statut_enregistrement_code VARCHAR NOT NULL DEFAULT 'actif',
    cree_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    cree_par VARCHAR NOT NULL DEFAULT 'systeme',
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    CHECK (crs_normalise = 2154),
    CHECK (
        date_geometrie_min IS NULL
        OR date_geometrie_max IS NULL
        OR date_geometrie_min <= date_geometrie_max
    )
);

CREATE TABLE IF NOT EXISTS relations_sites (
    relation_site_id UUID PRIMARY KEY DEFAULT uuid(),
    site_source_id UUID NOT NULL REFERENCES sites(site_id),
    site_cible_id UUID NOT NULL REFERENCES sites(site_id),
    type_relation_code VARCHAR NOT NULL,
    debut_min DATE,
    debut_max DATE,
    debut_precision_code VARCHAR,
    debut_texte_source VARCHAR,
    fin_min DATE,
    fin_max DATE,
    fin_precision_code VARCHAR,
    fin_texte_source VARCHAR,
    statut_validation_code VARCHAR NOT NULL,
    fiabilite_code VARCHAR NOT NULL,
    notes VARCHAR,
    statut_enregistrement_code VARCHAR NOT NULL DEFAULT 'actif',
    cree_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    cree_par VARCHAR NOT NULL DEFAULT 'systeme',
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    CHECK (site_source_id <> site_cible_id),
    CHECK (
        type_relation_code IN (
            'composant_de',
            'transfert_vers',
            'successeur_de',
            'depend_de',
            'partage_infrastructure_avec'
        )
    ),
    CHECK (debut_min IS NULL OR debut_max IS NULL OR debut_min <= debut_max),
    CHECK (fin_min IS NULL OR fin_max IS NULL OR fin_min <= fin_max)
);

CREATE TABLE IF NOT EXISTS propositions_rapprochement (
    proposition_rapprochement_id UUID PRIMARY KEY DEFAULT uuid(),
    site_a_id UUID NOT NULL REFERENCES sites(site_id),
    site_b_id UUID NOT NULL REFERENCES sites(site_id),
    methode_code VARCHAR NOT NULL,
    score_similarite DECIMAL(5, 4),
    criteres JSON,
    statut_decision_code VARCHAR NOT NULL DEFAULT 'a_verifier',
    site_canonique_id UUID REFERENCES sites(site_id),
    date_decision DATE,
    fiabilite_code VARCHAR NOT NULL,
    notes VARCHAR,
    statut_enregistrement_code VARCHAR NOT NULL DEFAULT 'actif',
    cree_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    cree_par VARCHAR NOT NULL DEFAULT 'systeme',
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    UNIQUE (site_a_id, site_b_id),
    CHECK (site_a_id <> site_b_id),
    CHECK (score_similarite IS NULL OR score_similarite BETWEEN 0 AND 1),
    CHECK (
        statut_decision_code IN (
            'a_verifier',
            'confirme_meme_site',
            'rejete_sites_distincts'
        )
    ),
    CHECK (
        site_canonique_id IS NULL
        OR site_canonique_id = site_a_id
        OR site_canonique_id = site_b_id
    ),
    CHECK (
        (
            statut_decision_code = 'a_verifier'
            AND site_canonique_id IS NULL
            AND date_decision IS NULL
        )
        OR (
            statut_decision_code = 'confirme_meme_site'
            AND site_canonique_id IS NOT NULL
            AND date_decision IS NOT NULL
        )
        OR (
            statut_decision_code = 'rejete_sites_distincts'
            AND site_canonique_id IS NULL
            AND date_decision IS NOT NULL
        )
    )
);

CREATE TABLE IF NOT EXISTS mentions_sources (
    mention_id UUID PRIMARY KEY DEFAULT uuid(),
    source_id VARCHAR NOT NULL REFERENCES sources(source_id),
    reference_source VARCHAR,
    url_precise VARCHAR,
    date_consultation TIMESTAMPTZ NOT NULL,
    localisateur VARCHAR,
    entite_type_code VARCHAR NOT NULL,
    entite_id UUID NOT NULL,
    champ_cible VARCHAR,
    valeur_originale JSON,
    valeur_normalisee JSON,
    statut_valeur_code VARCHAR NOT NULL,
    nature_information_code VARCHAR NOT NULL,
    fiabilite_code VARCHAR NOT NULL,
    extracteur VARCHAR,
    version_extracteur VARCHAR,
    notes VARCHAR,
    statut_enregistrement_code VARCHAR NOT NULL DEFAULT 'actif',
    cree_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    cree_par VARCHAR NOT NULL DEFAULT 'systeme',
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    CHECK (
        statut_valeur_code IN (
            'renseignee',
            'inconnue',
            'non_renseignee_source',
            'non_applicable',
            'contradictoire',
            'a_verifier'
        )
    ),
    CHECK (nature_information_code IN ('sourcee', 'calculee', 'interpretee'))
);

CREATE TABLE IF NOT EXISTS identifiants_externes (
    identifiant_externe_id UUID PRIMARY KEY DEFAULT uuid(),
    source_id VARCHAR NOT NULL REFERENCES sources(source_id),
    type_identifiant_code VARCHAR NOT NULL,
    valeur VARCHAR NOT NULL,
    entite_type_code VARCHAR NOT NULL,
    entite_id UUID NOT NULL,
    principal_pour_source BOOLEAN NOT NULL DEFAULT false,
    date_verification DATE NOT NULL,
    fiabilite_code VARCHAR NOT NULL,
    statut_enregistrement_code VARCHAR NOT NULL DEFAULT 'actif',
    cree_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    cree_par VARCHAR NOT NULL DEFAULT 'systeme',
    modifie_le TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    UNIQUE (source_id, type_identifiant_code, valeur),
    CHECK (nullif(trim(valeur), '') IS NOT NULL)
);

CREATE OR REPLACE VIEW sites_actifs AS
SELECT *
FROM sites
WHERE statut_enregistrement_code = 'actif';

CREATE OR REPLACE VIEW geometries_reference AS
SELECT *
FROM geometries
WHERE statut_enregistrement_code = 'actif'
  AND geometrie_reference;

CREATE OR REPLACE VIEW etats_actuels_courants AS
WITH observations_valides AS (
    SELECT observation.*
    FROM etats_actuels AS observation
    WHERE observation.statut_enregistrement_code = 'actif'
      AND observation.motif_version_code <> 'annulation'
      AND NOT EXISTS (
          SELECT 1
          FROM etats_actuels AS annulation
          WHERE annulation.motif_version_code = 'annulation'
            AND annulation.remplace_etat_actuel_id = observation.etat_actuel_id
      )
),
conservation AS (
    SELECT *, row_number() OVER (
        PARTITION BY site_id
        ORDER BY date_verification DESC, version_numero DESC, enregistre_le DESC
    ) AS rang
    FROM observations_valides
    WHERE conservation_code IS NOT NULL
),
usage_actuel AS (
    SELECT *, row_number() OVER (
        PARTITION BY site_id
        ORDER BY date_verification DESC, version_numero DESC, enregistre_le DESC
    ) AS rang
    FROM observations_valides
    WHERE usage_actuel_code IS NOT NULL
),
accessibilite AS (
    SELECT *, row_number() OVER (
        PARTITION BY site_id
        ORDER BY date_verification DESC, version_numero DESC, enregistre_le DESC
    ) AS rang
    FROM observations_valides
    WHERE accessibilite_code IS NOT NULL
)
SELECT
    site.site_id,
    conservation.conservation_code,
    conservation.date_verification AS conservation_verifiee_le,
    conservation.date_verification + INTERVAL 12 MONTH AS conservation_valide_jusqu_au,
    usage_actuel.usage_actuel_code,
    usage_actuel.date_verification AS usage_verifie_le,
    usage_actuel.date_verification + INTERVAL 12 MONTH AS usage_valide_jusqu_au,
    accessibilite.accessibilite_code,
    accessibilite.date_verification AS accessibilite_verifiee_le,
    accessibilite.date_verification + INTERVAL 3 MONTH AS accessibilite_valide_jusqu_au
FROM sites_actifs AS site
LEFT JOIN conservation
    ON conservation.site_id = site.site_id AND conservation.rang = 1
LEFT JOIN usage_actuel
    ON usage_actuel.site_id = site.site_id AND usage_actuel.rang = 1
LEFT JOIN accessibilite
    ON accessibilite.site_id = site.site_id AND accessibilite.rang = 1;
