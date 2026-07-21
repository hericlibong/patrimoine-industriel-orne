-- Jeu de donnees strictement synthetique : aucune ligne ne decrit un site reel.

INSERT INTO sources (
    source_id, titre, producteur, role_code, methode_acces_code,
    statut_audit_code, date_dernier_audit, notes, cree_par
) VALUES
    (
        'test_inventaire', 'Source patrimoniale fictive', 'Projet - test',
        'principal', 'fichier_test', 'test', DATE '2026-07-20',
        'Donnees synthetiques reservees aux tests.', 'fixture'
    ),
    (
        'test_terrain', 'Observation de terrain fictive', 'Projet - test',
        'verification', 'observation_test', 'test', DATE '2026-07-20',
        'Donnees synthetiques reservees aux tests.', 'fixture'
    );

INSERT INTO sites (
    site_id, nom_principal, niveau_structurel_code,
    commune_actuelle_code_insee, commune_actuelle_nom, lieu_dit_principal,
    statut_corpus_code, decision_inclusion_code, motif_decision,
    fiabilite_code, notes_internes, cree_par
) VALUES
    (
        '10000000-0000-4000-8000-000000000001', 'Forge du Test', 'site_principal',
        '61001', 'Commune Test A', 'La Riviere', 'cartographiable', 'inclus',
        'Activite industrielle anterieure a 1950 attestee par la source de test.',
        'forte', 'Site fictif.', 'fixture'
    ),
    (
        '10000000-0000-4000-8000-000000000002', 'Usine Nouvelle du Test',
        'site_principal', '61002', 'Commune Test B', 'La Gare',
        'cartographiable', 'inclus',
        'Nouvelle emprise liee par transfert au premier site.',
        'forte', 'Site fictif.', 'fixture'
    ),
    (
        '10000000-0000-4000-8000-000000000003', 'Tuilerie Disparue du Test',
        'site_principal', '61003', 'Commune Test C', 'Les Terres',
        'rapproche', 'inclus',
        'Activite attestee, localisation encore insuffisante.',
        'moyenne', 'Site fictif sans geometrie.', 'fixture'
    );

INSERT INTO noms_sites (
    nom_site_id, site_id, nom, type_nom_code, debut_min, debut_max,
    debut_precision_code, debut_texte_source, fiabilite_code, cree_par
) VALUES (
    '11000000-0000-4000-8000-000000000001',
    '10000000-0000-4000-8000-000000000001',
    'Moulin du Test', 'historique', DATE '1880-01-01', DATE '1880-12-31',
    'annee', '1880', 'forte', 'fixture'
);

INSERT INTO activites (
    activite_id, site_id, secteur_code, activite_code,
    activite_libelle_source, type_installation_code,
    debut_min, debut_max, debut_precision_code, debut_texte_source,
    fin_min, fin_max, fin_precision_code, fin_texte_source,
    principale, fiabilite_code, cree_par
) VALUES
    (
        '20000000-0000-4000-8000-000000000001',
        '10000000-0000-4000-8000-000000000001',
        'metal', 'forge', 'Forge hydraulique', 'forge',
        DATE '1800-01-01', DATE '1800-12-31', 'annee', '1800',
        DATE '1879-01-01', DATE '1879-12-31', 'annee', '1879',
        true, 'forte', 'fixture'
    ),
    (
        '20000000-0000-4000-8000-000000000002',
        '10000000-0000-4000-8000-000000000001',
        'agroalimentaire', 'moulin_farines', 'Moulin a farine', 'moulin',
        DATE '1880-01-01', DATE '1880-12-31', 'annee', '1880',
        DATE '1930-01-01', DATE '1930-12-31', 'annee', '1930',
        true, 'forte', 'fixture'
    ),
    (
        '20000000-0000-4000-8000-000000000003',
        '10000000-0000-4000-8000-000000000002',
        'metal', 'petite_metallurgie', 'Atelier de petite metallurgie', 'usine',
        DATE '1920-01-01', DATE '1920-12-31', 'annee', '1920',
        NULL, NULL, 'apres', 'apres 1920',
        true, 'forte', 'fixture'
    ),
    (
        '20000000-0000-4000-8000-000000000004',
        '10000000-0000-4000-8000-000000000003',
        'materiaux', 'tuilerie', 'Tuilerie', 'tuilerie',
        DATE '1870-01-01', DATE '1879-12-31', 'decennie', 'annees 1870',
        DATE '1910-01-01', DATE '1919-12-31', 'decennie', 'annees 1910',
        true, 'moyenne', 'fixture'
    );

INSERT INTO energies_activites (
    energie_activite_id, activite_id, energie_code, role_energie_code,
    debut_min, debut_max, debut_precision_code, debut_texte_source,
    fiabilite_code, cree_par
) VALUES (
    '21000000-0000-4000-8000-000000000001',
    '20000000-0000-4000-8000-000000000001',
    'eau', 'force_motrice', DATE '1800-01-01', DATE '1800-12-31',
    'annee', '1800', 'forte', 'fixture'
);

INSERT INTO etats_actuels (
    etat_actuel_id, site_id, conservation_code,
    accessibilite_code, date_verification, methode_verification_code,
    fiabilite_code, version_numero, remplace_etat_actuel_id,
    motif_version_code, notes, cree_par
) VALUES
    (
        '30000000-0000-4000-8000-000000000001',
        '10000000-0000-4000-8000-000000000001',
        'partiellement_conserve', 'visible_espace_public', DATE '2025-07-20',
        'terrain_test', 'forte', 1, NULL, 'nouvelle_observation',
        'Premiere observation fictive.', 'fixture'
    );

INSERT INTO etats_actuels (
    etat_actuel_id, site_id, conservation_code,
    accessibilite_code, date_verification, methode_verification_code,
    fiabilite_code, version_numero, remplace_etat_actuel_id,
    motif_version_code, notes, cree_par
) VALUES
    (
        '30000000-0000-4000-8000-000000000002',
        '10000000-0000-4000-8000-000000000001',
        NULL, 'prive_non_visible', DATE '2026-07-20',
        'terrain_test', 'forte', 2,
        '30000000-0000-4000-8000-000000000001', 'nouvelle_observation',
        'Seule l accessibilite a ete reverifiee.', 'fixture'
    ),
    (
        '30000000-0000-4000-8000-000000000003',
        '10000000-0000-4000-8000-000000000002',
        'conserve', 'inconnu', DATE '2026-07-20',
        'source_test', 'moyenne', 1, NULL, 'nouvelle_observation',
        'Observation fictive.', 'fixture'
    ),
    (
        '30000000-0000-4000-8000-000000000004',
        '10000000-0000-4000-8000-000000000003',
        'disparu', 'inaccessible', DATE '2026-07-20',
        'source_test', 'moyenne', 1, NULL, 'nouvelle_observation',
        'Observation fictive.', 'fixture'
    );

INSERT INTO usages_actuels (
    usage_actuel_id, etat_actuel_id, usage_code, principal, cree_par
) VALUES
    (
        '31000000-0000-4000-8000-000000000001',
        '30000000-0000-4000-8000-000000000001', 'logement', true, 'fixture'
    ),
    (
        '31000000-0000-4000-8000-000000000002',
        '30000000-0000-4000-8000-000000000003',
        'activite_industrielle', true, 'fixture'
    ),
    (
        '31000000-0000-4000-8000-000000000003',
        '30000000-0000-4000-8000-000000000004', 'sans_usage', true, 'fixture'
    );

INSERT INTO exploitants (
    exploitant_id, nom_principal, type_exploitant_code, notes, cree_par
) VALUES
    (
        '40000000-0000-4000-8000-000000000001', 'Societe Ancienne Test',
        'entreprise', 'Exploitant fictif.', 'fixture'
    ),
    (
        '40000000-0000-4000-8000-000000000002', 'Societe Nouvelle Test',
        'entreprise', 'Exploitant fictif.', 'fixture'
    );

INSERT INTO noms_exploitants (
    nom_exploitant_id, exploitant_id, nom, debut_min, debut_max,
    debut_precision_code, debut_texte_source, fiabilite_code, cree_par
) VALUES (
    '40100000-0000-4000-8000-000000000001',
    '40000000-0000-4000-8000-000000000001', 'Etablissements Test et Cie',
    DATE '1880-01-01', DATE '1880-12-31', 'annee', '1880', 'forte', 'fixture'
);

INSERT INTO exploitations (
    exploitation_id, site_id, exploitant_id, activite_id, role_code,
    debut_min, debut_max, debut_precision_code, debut_texte_source,
    fin_min, fin_max, fin_precision_code, fin_texte_source,
    fiabilite_code, cree_par
) VALUES
    (
        '41000000-0000-4000-8000-000000000001',
        '10000000-0000-4000-8000-000000000001',
        '40000000-0000-4000-8000-000000000001',
        '20000000-0000-4000-8000-000000000002', 'exploitant_principal',
        DATE '1880-01-01', DATE '1880-12-31', 'annee', '1880',
        DATE '1930-01-01', DATE '1930-12-31', 'annee', '1930',
        'forte', 'fixture'
    ),
    (
        '41000000-0000-4000-8000-000000000002',
        '10000000-0000-4000-8000-000000000002',
        '40000000-0000-4000-8000-000000000002',
        '20000000-0000-4000-8000-000000000003', 'exploitant_principal',
        DATE '1920-01-01', DATE '1920-12-31', 'annee', '1920',
        NULL, NULL, 'apres', 'apres 1920', 'forte', 'fixture'
    );

INSERT INTO objets_techniques (
    objet_technique_id, nom_principal, denomination_code, description,
    fabricant, date_creation_min, date_creation_max,
    date_creation_precision_code, date_creation_texte_source,
    reference_palissy, etat_conservation_code, date_verification,
    fiabilite_code, notes, cree_par
) VALUES (
    '50000000-0000-4000-8000-000000000001', 'Turbine du Test', 'turbine',
    'Machine fictive deplacee entre deux sites.', 'Constructeur Test',
    DATE '1895-01-01', DATE '1895-12-31', 'annee', '1895',
    'PMTEST0001', 'conserve', DATE '2026-07-20', 'forte',
    'Objet fictif.', 'fixture'
);

INSERT INTO liens_objets_sites (
    lien_objet_site_id, objet_technique_id, site_id, type_lien_code,
    debut_min, debut_max, debut_precision_code, debut_texte_source,
    fin_min, fin_max, fin_precision_code, fin_texte_source,
    fiabilite_code, cree_par
) VALUES
    (
        '51000000-0000-4000-8000-000000000001',
        '50000000-0000-4000-8000-000000000001',
        '10000000-0000-4000-8000-000000000001', 'emplacement_historique',
        DATE '1895-01-01', DATE '1895-12-31', 'annee', '1895',
        DATE '1950-01-01', DATE '1950-12-31', 'annee', '1950',
        'forte', 'fixture'
    ),
    (
        '51000000-0000-4000-8000-000000000002',
        '50000000-0000-4000-8000-000000000001',
        '10000000-0000-4000-8000-000000000002', 'emplacement_actuel',
        DATE '1951-01-01', DATE '1951-12-31', 'annee', '1951',
        NULL, NULL, NULL, NULL, 'forte', 'fixture'
    );

INSERT INTO protections (
    protection_id, objet_technique_id, type_protection_code,
    reference_protection, date_protection_min, date_protection_max,
    date_protection_precision_code, date_protection_texte_source,
    element_protege, statut_actuel_code, date_verification, cree_par
) VALUES (
    '52000000-0000-4000-8000-000000000001',
    '50000000-0000-4000-8000-000000000001', 'inscrit_mh', 'PMTEST0001',
    DATE '2000-01-01', DATE '2000-12-31', 'annee', '2000',
    'Turbine fictive', 'actif', DATE '2026-07-20', 'fixture'
);

INSERT INTO geometries (
    geometrie_id, site_id, geom, type_geometrie_code,
    precision_geographique_code, methode_localisation_code,
    crs_source, geometrie_reference, usage_code, date_verification,
    fiabilite_code, notes, cree_par
) VALUES
    (
        '60000000-0000-4000-8000-000000000001',
        '10000000-0000-4000-8000-000000000001', ST_Point(450000, 6850000),
        'point_site', 'parcelle_verifiee', 'coordonnees_source', 'EPSG:2154', true,
        'affichage', DATE '2026-07-20', 'forte', 'Coordonnees fictives.', 'fixture'
    ),
    (
        '60000000-0000-4000-8000-000000000002',
        '10000000-0000-4000-8000-000000000002', ST_Point(460000, 6860000),
        'point_site', 'point_adresse', 'geocodage_adresse', 'EPSG:2154', true,
        'affichage', DATE '2026-07-20', 'moyenne', 'Coordonnees fictives.', 'fixture'
    );

INSERT INTO relations_sites (
    relation_site_id, site_source_id, site_cible_id, type_relation_code,
    debut_min, debut_max, debut_precision_code, debut_texte_source,
    statut_validation_code, fiabilite_code, notes, cree_par
) VALUES (
    '70000000-0000-4000-8000-000000000001',
    '10000000-0000-4000-8000-000000000001',
    '10000000-0000-4000-8000-000000000002', 'transfert_vers',
    DATE '1920-01-01', DATE '1920-12-31', 'annee', '1920',
    'confirmee', 'forte', 'Relation fictive.', 'fixture'
);

INSERT INTO mentions_sources (
    mention_id, source_id, reference_source, date_consultation,
    entite_type_code, entite_id, champ_cible, valeur_originale,
    valeur_normalisee, statut_valeur_code, nature_information_code,
    fiabilite_code, extracteur, version_extracteur, cree_par
) VALUES
    (
        '80000000-0000-4000-8000-000000000001', 'test_inventaire', 'IATEST0001',
        TIMESTAMPTZ '2026-07-20 12:00:00+02', 'sites',
        '10000000-0000-4000-8000-000000000001', 'nom_principal',
        json_object('texte', 'Forge du Test'), json_object('texte', 'Forge du Test'),
        'renseignee', 'sourcee', 'forte', 'fixture_sql', '1.0', 'fixture'
    ),
    (
        '80000000-0000-4000-8000-000000000002', 'test_inventaire', 'IATEST0002',
        TIMESTAMPTZ '2026-07-20 12:00:00+02', 'sites',
        '10000000-0000-4000-8000-000000000002', 'nom_principal',
        json_object('texte', 'Usine Nouvelle du Test'),
        json_object('texte', 'Usine Nouvelle du Test'),
        'renseignee', 'sourcee', 'forte', 'fixture_sql', '1.0', 'fixture'
    ),
    (
        '80000000-0000-4000-8000-000000000003', 'test_inventaire', 'IATEST0003',
        TIMESTAMPTZ '2026-07-20 12:00:00+02', 'sites',
        '10000000-0000-4000-8000-000000000003', 'nom_principal',
        json_object('texte', 'Tuilerie Disparue du Test'),
        json_object('texte', 'Tuilerie Disparue du Test'),
        'renseignee', 'sourcee', 'moyenne', 'fixture_sql', '1.0', 'fixture'
    ),
    (
        '80000000-0000-4000-8000-000000000004', 'test_terrain', 'OBS-TEST-001',
        TIMESTAMPTZ '2026-07-20 15:00:00+02', 'etats_actuels',
        '30000000-0000-4000-8000-000000000002', 'accessibilite_code',
        json_object('texte', 'propriete privee'),
        json_object('code', 'prive_non_visitable'),
        'renseignee', 'sourcee', 'forte', 'fixture_sql', '1.0', 'fixture'
    );

INSERT INTO identifiants_externes (
    identifiant_externe_id, source_id, type_identifiant_code, valeur,
    entite_type_code, entite_id, principal_pour_source,
    date_verification, fiabilite_code, cree_par
) VALUES
    (
        '90000000-0000-4000-8000-000000000001', 'test_inventaire', 'IA',
        'IATEST0001', 'sites', '10000000-0000-4000-8000-000000000001',
        true, DATE '2026-07-20', 'forte', 'fixture'
    ),
    (
        '90000000-0000-4000-8000-000000000002', 'test_inventaire', 'IA',
        'IATEST0002', 'sites', '10000000-0000-4000-8000-000000000002',
        true, DATE '2026-07-20', 'forte', 'fixture'
    ),
    (
        '90000000-0000-4000-8000-000000000003', 'test_inventaire', 'IA',
        'IATEST0003', 'sites', '10000000-0000-4000-8000-000000000003',
        true, DATE '2026-07-20', 'moyenne', 'fixture'
    );
